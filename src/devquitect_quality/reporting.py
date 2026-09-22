"""Canonical report construction and presentation."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from .models import AuthenticationEvidence
from .redaction import redact_value

REPORT_SCHEMA_VERSION = 1
_AUTH_ERROR_MARKERS = ("auth", "credential", "token", "secret", "password", "api_key")


def _sanitize_report_value(value: Any) -> tuple[Any, set[str]]:
    """Redact untrusted report data and collapse authentication errors to a safe class."""

    redacted = redact_value(value)
    labels = set(redacted.redactions)

    def visit(item: Any) -> Any:
        if isinstance(item, Mapping):
            sanitized: dict[str, Any] = {}
            for key, nested in item.items():
                if str(key) == "runtime_errors" and isinstance(nested, Sequence):
                    errors: list[str] = []
                    for error in nested[:10]:
                        text = str(error)
                        if any(marker in text.lower() for marker in _AUTH_ERROR_MARKERS):
                            errors.append("authentication runtime failure")
                            labels.add("authentication-error")
                        else:
                            errors.append(text[:500])
                    sanitized[str(key)] = errors
                else:
                    sanitized[str(key)] = visit(nested)
            return sanitized
        if isinstance(item, Sequence) and not isinstance(item, (str, bytes, bytearray)):
            return [visit(nested) for nested in item]
        return item

    return visit(redacted.value), labels


def authentication_metadata(
    value: Mapping[str, Any] | AuthenticationEvidence | None,
) -> dict[str, str]:
    """Normalize report auth metadata; historical reports resolve to unknown."""

    if isinstance(value, AuthenticationEvidence):
        return value.as_dict()
    return AuthenticationEvidence.from_mapping(value).as_dict()


def build_policy_failure_report(
    *,
    report_type: str,
    inputs: Mapping[str, Any],
    authentication: Mapping[str, Any] | AuthenticationEvidence,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a safe non-passing report for refusal before credential staging."""

    if report_type not in {"evaluation", "comparison", "check"}:
        raise ValueError(f"unsupported policy-failure report type: {report_type}")
    report = build_artifact_report(
        report_type=report_type,
        inputs=inputs,
        records=[
            {
                "code": "authentication.policy",
                "severity": "error",
                "path": "authentication",
                "message": "authentication policy rejected the request before credential staging",
            }
        ],
        evidence_manifest=[],
        authentication=authentication,
        result="fail",
        generated_at=generated_at,
    )
    return report


def normalize_relative_path(path: str | Path) -> str:
    """Return a portable repository-relative path or reject an unsafe one."""

    raw = str(path).replace("\\", "/")
    normalized = PurePosixPath(raw)
    if not raw or "\x00" in raw or normalized.is_absolute() or ".." in normalized.parts:
        raise ValueError(f"report path must be a safe relative path: {raw!r}")
    return normalized.as_posix()


def validation_record(code: str, path: str, message: str) -> dict[str, str]:
    """Create one stable, machine-readable structural-validation record."""

    return {
        "code": code,
        "severity": "error",
        "path": normalize_relative_path(path),
        "message": message,
    }


def build_validation_report(
    *,
    source: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build the approved JSON report envelope for structural validation."""

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "validation",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "toolchain": {"package": "devquitect-quality", "version": "0.1.0"},
        "inputs": {"source": dict(source)},
        "result": "fail" if records else "pass",
        "records": [dict(record) for record in records],
        "evidence_manifest": [],
        "redactions": [],
    }


def build_evaluation_report(
    *,
    source: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    authentication: Mapping[str, Any] | AuthenticationEvidence | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a canonical evaluation report without retaining raw transcripts."""

    classifications = {str(record["classification"]) for record in records}
    result = (
        "fail"
        if "fail" in classifications
        else ("inconclusive" if "inconclusive" in classifications else "pass")
    )
    normalized = []
    report_redactions = {
        label for record in records for label in record.get("redactions", [])
    }
    for record in records:
        item, redactions = _sanitize_report_value(dict(record))
        report_redactions.update(redactions)
        item.update(
            code=f"evaluation.{item['classification']}",
            severity="info" if item["classification"] == "pass" else "error",
            path=f"evals/cases/{item['case_id']}.yaml",
            message=(
                f"case {item['case_id']} repetition {item['repetition']}: {item['classification']}"
            ),
        )
        normalized.append(item)
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "evaluation",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "toolchain": {"package": "devquitect-quality", "version": "0.1.0"},
        "inputs": {"source": dict(source)},
        "result": result,
        "records": normalized,
        "evidence_manifest": [],
        "redactions": sorted(report_redactions),
    }
    if authentication is not None:
        report["authentication"] = authentication_metadata(authentication)
    return report


def build_calibration_report(
    *,
    run_id: str,
    skill_snapshot_id: str,
    skill_version: str,
    model: str,
    runtime: Mapping[str, Any],
    suite_id: str,
    suite_digest: str,
    repetitions: int,
    dimensions: Mapping[str, Any],
    evidence_references: Sequence[Mapping[str, Any]],
    authentication: Mapping[str, Any] | AuthenticationEvidence | None = None,
    summary_score: float | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build bounded, review-only model calibration evidence."""

    if len(evidence_references) > 100:
        raise ValueError("calibration evidence is limited to 100 references")
    safe_references = []
    for reference in evidence_references:
        safe_reference, redactions = _sanitize_report_value(dict(reference))
        safe_reference["redactions"] = sorted(
            set(safe_reference.get("redactions", [])) | redactions
        )
        safe_references.append(safe_reference)
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "behavior-calibration",
        "run_id": run_id,
        "skill_snapshot_id": skill_snapshot_id,
        "skill_version": skill_version,
        "model": model,
        "runtime": dict(runtime),
        "suite_id": suite_id,
        "suite_digest": suite_digest,
        "repetitions": repetitions,
        "dimensions": dict(dimensions),
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "evidence_references": safe_references,
    }
    if summary_score is not None:
        report["summary_score"] = summary_score
    if authentication is not None:
        report["authentication"] = authentication_metadata(authentication)
    return report


def calibration_comparability(
    left: Mapping[str, Any] | None, right: Mapping[str, Any] | None
) -> str:
    """Return whether two optional calibration reports share a configuration."""

    if left is None or right is None:
        return "unknown"
    fields = ("model", "runtime", "suite_digest", "repetitions")
    if any(left.get(field) is None or right.get(field) is None for field in fields):
        return "unknown"
    return (
        "comparable"
        if all(left.get(field) == right.get(field) for field in fields)
        else "not-comparable"
    )


def build_comparison_report(
    *,
    stable: Mapping[str, Any],
    candidate: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    authentication: Mapping[str, Any] | AuthenticationEvidence | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    classifications = {str(record["classification"]) for record in records}
    if "inconclusive" in classifications:
        result = "inconclusive"
    elif "regression" in classifications:
        result = "fail"
    else:
        result = "pass"
    normalized = []
    for record in records:
        item, _ = _sanitize_report_value(dict(record))
        item.update(
            code=f"comparison.{item['classification']}",
            severity="error"
            if item["classification"] in {"regression", "inconclusive"}
            else "info",
            path=f"evals/cases/{item['case_id']}.yaml",
            message=f"case {item['case_id']}: {item['classification']}",
        )
        normalized.append(item)
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "comparison",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "toolchain": {"package": "devquitect-quality", "version": "0.1.0"},
        "inputs": {"stable": dict(stable), "candidate": dict(candidate)},
        "result": result,
        "records": normalized,
        "evidence_manifest": [],
        "redactions": [],
    }
    if authentication is not None:
        report["authentication"] = authentication_metadata(authentication)
    return report


def build_artifact_report(
    *,
    report_type: str,
    inputs: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    evidence_manifest: Sequence[Mapping[str, Any]],
    authentication: Mapping[str, Any] | AuthenticationEvidence | None = None,
    result: str = "pass",
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a package or release-check canonical report envelope."""

    if report_type not in {"evaluation", "comparison", "package", "release-check", "check"}:
        raise ValueError(f"unsupported artifact report type: {report_type}")
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": report_type,
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "toolchain": {"package": "devquitect-quality", "version": "0.1.0"},
        "inputs": dict(inputs),
        "result": result,
        "records": [dict(record) for record in records],
        "evidence_manifest": [dict(item) for item in evidence_manifest],
        "redactions": [],
    }
    if authentication is not None:
        report["authentication"] = authentication_metadata(authentication)
    return report


def serialize_json(report: Mapping[str, Any]) -> str:
    """Serialize a report deterministically while retaining a trailing newline."""

    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def render_text(report: Mapping[str, Any]) -> str:
    """Render the same verdict and records as the canonical JSON report."""

    result = str(report["result"])
    records = report.get("records", [])
    lines = [f"validation: {result} ({len(records)} issue{'s' if len(records) != 1 else ''})"]
    for record in records:
        lines.append(f"- {record['code']} [{record['path']}]: {record['message']}")
    return "\n".join(lines) + "\n"


def write_report_atomic(path: str | Path, report: Mapping[str, Any]) -> None:
    """Atomically replace a report without leaving a partial target."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=target.parent,
        prefix=f".{target.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(serialize_json(report))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
