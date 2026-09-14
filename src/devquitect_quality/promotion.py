"""Release-eligibility policy and proposed promotion records."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .models import SkillSource
from .packaging import SEMVER, PackageArtifact, PackageError, build_package
from .sources import SourceError
from .validate import (
    ValidationConfigurationError,
    ValidationInputs,
    load_validation_inputs,
    validate_report_schema,
)


class PromotionError(ValueError):
    """Evidence or compatibility policy blocks release eligibility."""


def compatibility_impact(previous: str, candidate: str) -> str:
    """Classify a semantic-version transition as patch, minor, or major."""

    if not SEMVER.fullmatch(previous) or not SEMVER.fullmatch(candidate):
        raise PromotionError("compatibility versions must use X.Y.Z")
    old = tuple(map(int, previous.split(".")))
    new = tuple(map(int, candidate.split(".")))
    if new <= old:
        raise PromotionError("candidate version must be greater than the packaged version")
    return "major" if new[0] > old[0] else ("minor" if new[1] > old[1] else "patch")


def validate_compatibility(
    *, impact: str, persistent_schema_changed: bool, migration_refs: list[str]
) -> None:
    if impact not in {"patch", "minor", "major"}:
        raise PromotionError(f"unsupported compatibility impact: {impact}")
    if persistent_schema_changed and not migration_refs:
        raise PromotionError("persistent schema changes require migration or recovery coverage")


def _load_reports(evidence: Path) -> list[dict[str, Any]]:
    if not evidence.is_dir():
        raise PromotionError(f"evidence path is not a directory: {evidence}")
    reports: list[dict[str, Any]] = []
    for path in sorted(evidence.rglob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise PromotionError(f"invalid evidence JSON: {path}") from error
        if isinstance(value, dict) and "report_type" in value:
            reports.append(value)
    return reports


def _deterministic_evidence(
    reports: list[dict[str, Any]], artifact: PackageArtifact, inputs: ValidationInputs
) -> None:
    """Require a passing credential-free check for the packaged snapshot only."""

    has_check = False
    for report in reports:
        report_type = report.get("report_type")
        if report_type in {"evaluation", "comparison", "behavior-calibration"}:
            continue
        if report.get("schema_version") != 1:
            raise PromotionError("evidence uses an unsupported report schema")
        if report.get("result") != "pass":
            raise PromotionError(f"{report.get('report_type')} evidence is not passing")
        if report_type != "check":
            continue
        try:
            validate_report_schema(report, inputs)
        except ValidationConfigurationError as error:
            raise PromotionError(f"check evidence is not canonical: {error.message}") from error
        if report.get("inputs", {}).get("behavioral") is not False:
            raise PromotionError("promotion requires a credential-free check")
        records = {
            record.get("code"): record
            for record in report.get("records", [])
            if isinstance(record, dict)
        }
        complete_check = (
            all(
                records.get(code, {}).get("severity") == "info"
                for code in ("check.validation", "check.tests")
            )
            and any(
                item.get("suite") == "fast" and item.get("exit_code") == 0
                for item in report.get("evidence_manifest", [])
            )
        )
        for item in report.get("evidence_manifest", []):
            source = item.get("source", {})
            if (
                item.get("report_type") == "validation"
                and item.get("result") == "pass"
                and source.get("kind") == "git-ref"
                and source.get("snapshot_id") == artifact.snapshot_id
                and source.get("source_commit") == artifact.source_commit
            ):
                if not complete_check:
                    raise PromotionError("credential-free check is incomplete")
                has_check = True
    if not has_check:
        raise PromotionError("no passing credential-free check matches the source snapshot")


def release_check(
    repository: Path, selector: str, version: str, evidence: Path, output: Path
) -> tuple[PackageArtifact, dict[str, Any]]:
    """Rebuild twice, bind evidence, and emit an unapproved promotion proposal."""

    with tempfile.TemporaryDirectory(prefix="devquitect-release-a-") as first_root:
        first = build_package(repository, selector, version, Path(first_root))
        with tempfile.TemporaryDirectory(prefix="devquitect-release-b-") as second_root:
            second = build_package(repository, selector, version, Path(second_root))
            if first.artifact_digest != second.artifact_digest or first.entries != second.entries:
                raise PromotionError("independent package rebuilds are not identical")
            reports = _load_reports(evidence)
            try:
                inputs = load_validation_inputs(
                    SkillSource.from_selector(first.source_commit, repository)
                )
            except (SourceError, ValidationConfigurationError) as error:
                raise PromotionError(f"cannot load release evidence schema: {error}") from error
            _deterministic_evidence(reports, first, inputs)
            previous_manifest = json.loads(
                subprocess_manifest(repository, f"{first.source_commit}^").decode("utf-8")
            )
            impact = compatibility_impact(str(previous_manifest["version"]), version)
            validate_compatibility(
                impact=impact, persistent_schema_changed=False, migration_refs=[]
            )
            output.mkdir(parents=True, exist_ok=True)
            target = output / first.artifact_path.name
            shutil.copyfile(first.artifact_path, target)
            artifact = PackageArtifact(
                plugin_name=first.plugin_name,
                version=first.version,
                source_commit=first.source_commit,
                snapshot_id=first.snapshot_id,
                artifact_path=target,
                artifact_digest=first.artifact_digest,
                entries=first.entries,
            )
    proposal = {
        "schema_version": 1,
        "version": version,
        "source_commit": artifact.source_commit,
        "snapshot_id": artifact.snapshot_id,
        "package_digest": artifact.artifact_digest,
        "run_ids": [],
        "comparison_ids": [],
        "accepted_deltas": [],
        "compatibility": {"impact": impact, "migration_refs": []},
        "residual_risks": [],
        "approved_by": None,
        "approved_at": None,
    }
    (output / f"devquitect-{version}.promotion.json").write_text(
        json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return artifact, proposal


def subprocess_manifest(repository: Path, commit: str) -> bytes:
    """Read the committed plugin manifest without consulting the working tree."""

    import subprocess

    process = subprocess.run(
        ["git", "-C", str(repository), "show", f"{commit}:.codex-plugin/plugin.json"],
        check=False,
        capture_output=True,
    )
    if process.returncode != 0:
        raise PackageError("source commit has no readable plugin manifest")
    return process.stdout
