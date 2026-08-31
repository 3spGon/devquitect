"""Canonical report construction and presentation."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

REPORT_SCHEMA_VERSION = 1


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
    for record in records:
        item = dict(record)
        item.update(
            code=f"evaluation.{item['classification']}",
            severity="info" if item["classification"] == "pass" else "error",
            path=f"evals/cases/{item['case_id']}.yaml",
            message=(
                f"case {item['case_id']} repetition {item['repetition']}: {item['classification']}"
            ),
        )
        normalized.append(item)
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "evaluation",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "toolchain": {"package": "devquitect-quality", "version": "0.1.0"},
        "inputs": {"source": dict(source)},
        "result": result,
        "records": normalized,
        "evidence_manifest": [],
        "redactions": sorted(
            {label for record in records for label in record.get("redactions", [])}
        ),
    }


def build_comparison_report(
    *,
    stable: Mapping[str, Any],
    candidate: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
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
        item = dict(record)
        item.update(
            code=f"comparison.{item['classification']}",
            severity="error"
            if item["classification"] in {"regression", "inconclusive"}
            else "info",
            path=f"evals/cases/{item['case_id']}.yaml",
            message=f"case {item['case_id']}: {item['classification']}",
        )
        normalized.append(item)
    return {
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


def build_artifact_report(
    *,
    report_type: str,
    inputs: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    evidence_manifest: Sequence[Mapping[str, Any]],
    result: str = "pass",
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a package or release-check canonical report envelope."""

    if report_type not in {"package", "release-check", "check"}:
        raise ValueError(f"unsupported artifact report type: {report_type}")
    return {
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
