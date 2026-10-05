"""Release-eligibility policy and proposed promotion records."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import jsonschema

from .github_evidence import (
    JOBS,
    SHA,
    EvidenceConfigurationError,
    EvidencePolicyError,
    GitHubEvidence,
    digest,
    read_json,
    safe_relative,
    validate_artifact,
    validate_jobs,
    validate_selection,
)
from .models import SkillSource
from .packaging import SEMVER, PackageArtifact, PackageError, build_package
from .reporting import build_artifact_report, write_report_atomic
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
    repository: Path, selector: str, version: str, evidence: Path, output: Path,
    *, ci_repository: str | None = None, ci_run_id: int | None = None,
    ci_run_attempt: int | None = None, previous_release: str | None = None,
    behavioral_evidence: Path | None = None, evidence_manifest: list | None = None,
    report_path: Path | None = None,
) -> tuple[PackageArtifact, dict[str, Any]]:
    """Rebuild twice, bind evidence, and emit an unapproved promotion proposal."""

    selectors = (ci_repository, ci_run_id, ci_run_attempt)
    ci_mode = any(value is not None for value in selectors)
    if ci_mode and not all(value is not None for value in selectors):
        raise EvidenceConfigurationError("all three CI selectors are required together")
    if behavioral_evidence and not ci_mode:
        raise EvidenceConfigurationError("behavioral evidence requires CI mode")
    if ci_mode:
        validate_selection(repository, selector, ci_repository, ci_run_id, ci_run_attempt,
                           previous_release, evidence, output)
        if report_path and any(
            report_path.resolve() == root.resolve()
            or root.resolve() in report_path.resolve().parents
            for root in (evidence, output, behavioral_evidence) if root
        ):
            raise EvidenceConfigurationError("report must be outside evidence and output roots")
    supplementary = []
    if ci_mode and SEMVER.fullmatch(version):
        committed_version = json.loads(subprocess_manifest(repository, selector))["version"]
        if committed_version != version:
            raise PromotionError("requested version differs from the committed candidate")
    with tempfile.TemporaryDirectory(prefix="devquitect-release-a-") as first_root:
        first = build_package(repository, selector, version, Path(first_root))
        with tempfile.TemporaryDirectory(prefix="devquitect-release-b-") as second_root:
            second = build_package(repository, selector, version, Path(second_root))
            if first.artifact_digest != second.artifact_digest or first.entries != second.entries:
                raise PromotionError("independent package rebuilds are not identical")
            observation = None
            if ci_mode:
                observation = GitHubEvidence().collect(
                    ci_repository, selector, ci_run_id, ci_run_attempt, evidence
                )
            reports = _load_reports(evidence / "quality" if ci_mode else evidence)
            try:
                inputs = load_validation_inputs(
                    SkillSource.from_selector(first.source_commit, repository)
                )
            except (SourceError, ValidationConfigurationError) as error:
                raise PromotionError(f"cannot load release evidence schema: {error}") from error
            _deterministic_evidence(reports, first, inputs)
            if observation is not None:
                supplementary.extend(_ci_policy(observation, evidence, first, inputs, repository))
                supplementary.append({
                    "behavioral": _behavioral_policy(behavioral_evidence, first, inputs)
                })
            baseline = previous_release or f"{first.source_commit}^"
            if previous_release:
                if not SHA.fullmatch(previous_release):
                    raise EvidenceConfigurationError("previous release must be a full commit SHA")
                process = subprocess.run(
                    ["git", "-C", str(repository), "merge-base", "--is-ancestor",
                     baseline, first.source_commit],
                    check=False, capture_output=True,
                )
                if process.returncode != 0 or baseline == first.source_commit:
                    raise PromotionError("previous release must be a readable strict ancestor")
            previous_manifest = json.loads(
                subprocess_manifest(repository, baseline).decode("utf-8")
            )
            impact = compatibility_impact(str(previous_manifest["version"]), version)
            validate_compatibility(
                impact=impact, persistent_schema_changed=False, migration_refs=[]
            )
            if previous_release:
                supplementary.append({"previous_release": {
                    "source_commit": baseline, "version": previous_manifest["version"]
                }})
            # CI output remains private until the ZIP, manifest and proposal are complete.
            output.parent.mkdir(parents=True, exist_ok=True)
            stage_context = tempfile.TemporaryDirectory(prefix=".readiness-", dir=output.parent)
            stage = Path(stage_context.name)
            target = stage / first.artifact_path.name
            try:
                shutil.copyfile(first.artifact_path, target)
                if ci_mode:
                    shutil.copyfile(first.artifact_path.with_suffix(".manifest.json"),
                                    target.with_suffix(".manifest.json"))
            except BaseException:
                stage_context.cleanup()
                raise
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
        "run_ids": [str(ci_run_id)] if ci_mode else [],
        "comparison_ids": [],
        "accepted_deltas": [],
        "compatibility": {"impact": impact, "migration_refs": []},
        "residual_risks": [],
        "approved_by": None,
        "approved_at": None,
    }
    try:
        (stage / f"devquitect-{version}.promotion.json").write_text(
            json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if ci_mode:
            if output.exists() or output.is_symlink():
                raise EvidenceConfigurationError("output appeared during verification")
            if report_path:
                # A report-write failure cannot leave an eligible output directory.
                write_report_atomic(report_path, build_artifact_report(
                    report_type="release-check", records=[],
                    inputs={"source": {"kind": "git-ref", "selector": selector,
                                       "source_commit": artifact.source_commit,
                                       "snapshot_id": artifact.snapshot_id}, "version": version,
                            "repository": ci_repository, "ci_run_id": str(ci_run_id),
                            "ci_run_attempt": str(ci_run_attempt),
                            "previous_release": previous_release},
                    evidence_manifest=[artifact.as_dict(), {"promotion": proposal}, *supplementary],
                ))
            stage.rename(output)
        else:
            output.mkdir(parents=True, exist_ok=True)
            for path in stage.iterdir():
                shutil.copyfile(path, output / path.name)
    finally:
        stage_context.cleanup()
    artifact = PackageArtifact(
        plugin_name=artifact.plugin_name, version=artifact.version,
        source_commit=artifact.source_commit, snapshot_id=artifact.snapshot_id,
        artifact_path=output / artifact.artifact_path.name,
        artifact_digest=artifact.artifact_digest, entries=artifact.entries,
    )
    if evidence_manifest is not None:
        evidence_manifest.extend(supplementary)
    return artifact, proposal


def _ci_policy(observation: dict, root: Path, artifact: PackageArtifact,
               inputs: ValidationInputs, repository: Path) -> list[dict]:
    """Recheck actual downloaded files and observed jobs in the shared eligibility policy."""
    source = artifact.source_commit
    run_id, attempt = observation["run_id"], observation["run_attempt"]
    validate_jobs(observation["jobs"], source, run_id, attempt)
    identity_fields = {
        key: observation[key] for key in ("repository", "source_commit", "workflow_path",
                                        "workflow_commit", "run_id", "run_attempt")
    }
    identity_fields.update(event="push", ref="refs/heads/main", pr=None)
    try:
        schema = json.loads(subprocess.check_output(
            ["git", "-C", str(repository), "show", f"{source}:schemas/ci-evidence.schema.json"]
        ))
        identity_schema = {**schema, "required": [
            field for field in schema["required"]
            if field not in {"snapshot_id", "version", "files"}
        ]}
        lock_digest = hashlib.sha256(subprocess.check_output(
            ["git", "-C", str(repository), "show", f"{source}:uv.lock"]
        )).hexdigest()
    except (subprocess.CalledProcessError, ValueError, KeyError) as error:
        raise EvidencePolicyError("candidate CI schema or lock is unavailable") from error
    for row in observation["artifacts"]:
        kind = row["kind"]
        producer = next(job for job in observation["jobs"]
                        if job["name"] == JOBS.get(kind, JOBS["package"]))
        validate_artifact(row, producer, source, run_id)
        if kind == "package":
            continue
        identity = read_json(root / kind / "identity.json")
        result = read_json(root / kind / "result.json")
        try:
            jsonschema.Draft202012Validator(identity_schema).validate(identity)
        except jsonschema.ValidationError as error:
            raise EvidencePolicyError("downloaded identity is not schema-valid") from error
        expected_checks = ({"identity", "check", "ruff", "whitespace"} if kind == "quality"
                           else {"identity", "build-first", "build-second", "index"}
                           if kind == "diagnostics" else {"identity", "smoke"})
        for document in (identity, result):
            if any(document.get(key) != value for key, value in identity_fields.items()):
                raise EvidencePolicyError("downloaded identity differs from API provenance")
        expected_job = "quality" if kind == "quality" else (
            "package" if kind == "diagnostics" else "platform-smoke"
        )
        if (result.get("result") != "pass" or result.get("job") != expected_job
            or result.get("toolchain") != identity["toolchain"]
            or set(result.get("checks", {})) != expected_checks
            or any(check.get("status") != "pass" or check.get("exit_code") != 0
                   for check in result["checks"].values())):
            raise EvidencePolicyError("downloaded mandatory checks are incomplete")
        if (identity["toolchain"]["quality_source_commit"] != source
            or identity["toolchain"]["lock_sha256"] != lock_digest):
            raise EvidencePolicyError("CI quality tool source mismatch")
    package_root = root / "package"
    index = read_json(package_root / "ci-evidence.json")
    try:
        jsonschema.Draft202012Validator(schema).validate(index)
    except (subprocess.CalledProcessError, ValueError, jsonschema.ValidationError) as error:
        raise EvidencePolicyError("CI package index is not schema-valid") from error
    if any(index.get(key) != value for key, value in identity_fields.items()):
        raise EvidencePolicyError("package index provenance mismatch")
    if (index["snapshot_id"] != artifact.snapshot_id or index["version"] != artifact.version
        or index["toolchain"]["quality_source_commit"] != source
        or index["toolchain"]["lock_sha256"] != lock_digest
        or index["toolchain"] != read_json(root / "diagnostics/identity.json")["toolchain"]):
        raise EvidencePolicyError("package snapshot, version or tool identity mismatch")
    file_paths = {}
    for kind, entry in index["files"].items():
        path = package_root / safe_relative(entry["path"])
        if (not path.is_file() or path.is_symlink() or path.stat().st_size != entry["size"]
            or digest(path) != entry["sha256"]):
            raise EvidencePolicyError("downloaded package file digest mismatch")
        file_paths[kind] = path
    if len(set(file_paths.values())) != 3:
        raise EvidencePolicyError("package files must be distinct")
    if set(package_root.iterdir()) != {*file_paths.values(), package_root / "ci-evidence.json"}:
        raise EvidencePolicyError("undeclared package members")
    manifest = read_json(file_paths["manifest"])
    if (manifest != artifact.as_dict()
        or f"sha256:{digest(file_paths['zip'])}" != artifact.artifact_digest):
        raise EvidencePolicyError("downloaded canonical package differs from evaluated rebuild")
    report = read_json(file_paths["report"])
    try:
        validate_report_schema(report, inputs)
    except ValidationConfigurationError as error:
        raise EvidencePolicyError("package report is not canonical") from error
    if (report.get("report_type") != "package" or report.get("result") != "pass"
        or report["inputs"].get("version") != artifact.version
        or report["inputs"].get("source", {}).get("source_commit") != source
        or report["inputs"].get("source", {}).get("snapshot_id") != artifact.snapshot_id):
        raise EvidencePolicyError("package report identity mismatch")
    return [{"ci": observation}, {"package_identity": index}]


def _behavioral_policy(root: Path | None, artifact: PackageArtifact,
                       inputs: ValidationInputs) -> list[dict]:
    if root is None:
        return [{"verdict": "not-run", "host": None, "runtime": None,
                 "reasoning_effort": None, "reports": []}]
    if not root.is_dir() or root.is_symlink() or any(path.is_symlink() for path in root.rglob("*")):
        raise EvidencePolicyError("unsafe behavioral evidence directory")
    rows = read_json(root / "rows.json").get("rows")
    if not isinstance(rows, list) or not rows:
        raise EvidencePolicyError("behavioral rows index must be nonempty")
    declared = {"rows.json"}
    for row in rows:
        required = {"model_id", "host", "runtime", "reasoning_effort", "suite_revision",
                    "repetitions", "authorization", "verdict", "reports"}
        if (not isinstance(row, dict) or not required <= row.keys()
            or row["verdict"] not in {"pass", "fail", "inconclusive", "not-run"}
            or not isinstance(row["reports"], list)
            or type(row["repetitions"]) is not int or row["repetitions"] < 1
            or any(not isinstance(row[key], str) or not row[key]
                   for key in ("model_id", "suite_revision", "authorization"))):
            raise EvidencePolicyError("malformed behavioral dimensions or authorization")
        if not row["reports"]:
            if row["verdict"] not in {"not-run", "inconclusive"} or any(
                row[key] is not None for key in ("host", "runtime", "reasoning_effort")
            ):
                raise EvidencePolicyError("unexecuted rows cannot claim observed runtime")
            continue
        if row["verdict"] == "not-run" or any(not isinstance(row[key], str) or not row[key]
                                              for key in ("host", "runtime")):
            raise EvidencePolicyError("executed rows require observed runtime")
        for reference in row["reports"]:
            if not isinstance(reference, dict):
                raise EvidencePolicyError("malformed behavioral report reference")
            relative = safe_relative(reference.get("path"))
            if relative in declared:
                raise EvidencePolicyError("duplicate behavioral report reference")
            declared.add(relative)
            path = root / relative
            if not path.is_file() or digest(path) != reference.get("sha256"):
                raise EvidencePolicyError("missing or altered behavioral report")
            report = read_json(path)
            try:
                validate_report_schema(report, inputs)
            except ValidationConfigurationError as error:
                raise EvidencePolicyError("behavioral report is not canonical") from error
            source = report.get("inputs", {}).get(
                "candidate" if report["report_type"] == "comparison" else "source", {}
            )
            if (report["report_type"] not in {"evaluation", "comparison"}
                or source.get("source_commit") != artifact.source_commit
                or source.get("snapshot_id") != artifact.snapshot_id):
                raise EvidencePolicyError("behavioral report candidate mismatch")
            if report["result"] != row["verdict"]:
                raise EvidencePolicyError("behavioral row verdict differs from its reports")
            if not report["records"]:
                raise EvidencePolicyError("unexecuted behavioral reports cannot claim runtime")
            for record in report["records"]:
                observed = (record.get("candidate")
                            if report["report_type"] == "comparison" else record)
                if not isinstance(observed, dict):
                    raise EvidencePolicyError("malformed behavioral observation")
                if (
                    observed.get("model") != row["model_id"]
                    or observed.get("reasoning_effort") != row["reasoning_effort"]
                ):
                    raise EvidencePolicyError("behavioral reports combine model/effort rows")
    supplied = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    if supplied != declared:
        raise EvidencePolicyError("undeclared behavioral reports")
    return rows


def subprocess_manifest(repository: Path, commit: str) -> bytes:
    """Read the committed plugin manifest without consulting the working tree."""

    process = subprocess.run(
        ["git", "-C", str(repository), "show", f"{commit}:.codex-plugin/plugin.json"],
        check=False,
        capture_output=True,
    )
    if process.returncode != 0:
        raise PackageError("source commit has no readable plugin manifest")
    return process.stdout
