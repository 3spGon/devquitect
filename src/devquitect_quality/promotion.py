"""Release-eligibility policy and proposed promotion records."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .packaging import SEMVER, PackageArtifact, PackageError, build_package


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


def _evidence_ids(
    reports: list[dict[str, Any]], artifact: PackageArtifact
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    run_ids: set[str] = set()
    comparison_ids: set[str] = set()
    accepted: list[dict[str, Any]] = []
    has_evaluation = False
    has_comparison = False
    for report in reports:
        if report.get("schema_version") != 1:
            raise PromotionError("evidence uses an unsupported report schema")
        if report.get("result") != "pass":
            raise PromotionError(f"{report.get('report_type')} evidence is not passing")
        report_type = report.get("report_type")
        inputs = report.get("inputs", {})
        if report_type == "evaluation":
            source = inputs.get("source", {})
            if source.get("kind") != "git-ref" or source.get("snapshot_id") != artifact.snapshot_id:
                continue
            has_evaluation = True
            for record in report.get("records", []):
                if (
                    record.get("classification") != "pass"
                    or record.get("critical_failures")
                    or record.get("eligibility") != "release-eligible"
                ):
                    raise PromotionError(
                        "critical or unresolved evaluation evidence blocks release"
                    )
                if record.get("run_id"):
                    run_ids.add(record["run_id"])
        elif report_type == "comparison":
            candidate = inputs.get("candidate", {})
            if (
                candidate.get("kind") != "git-ref"
                or candidate.get("snapshot_id") != artifact.snapshot_id
            ):
                continue
            has_comparison = True
            for record in report.get("records", []):
                classification = record.get("classification")
                if classification in {"regression", "inconclusive", "variable"}:
                    raise PromotionError(f"unresolved comparison classification: {classification}")
                if classification not in {"equivalent", "improvement"}:
                    declaration = record.get("declaration_ref")
                    if not declaration:
                        raise PromotionError("behavioral deltas require a reviewed declaration")
                    accepted.append(
                        {
                            "case_id": record.get("case_id"),
                            "classification": classification,
                            "declaration_ref": declaration,
                        }
                    )
                if record.get("comparison_id"):
                    comparison_ids.add(record["comparison_id"])
    if not has_evaluation:
        raise PromotionError("no passing release-eligible evaluation matches the source snapshot")
    if not has_comparison:
        raise PromotionError("no passing clean-candidate comparison matches the source snapshot")
    return sorted(run_ids), sorted(comparison_ids), accepted


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
            run_ids, comparison_ids, accepted = _evidence_ids(reports, first)
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
        "run_ids": run_ids,
        "comparison_ids": comparison_ids,
        "accepted_deltas": accepted,
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
