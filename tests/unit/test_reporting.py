from __future__ import annotations

import json
from pathlib import Path

import pytest

from devquitect_quality.auth_policy import AuthSelection
from devquitect_quality.cli import _auth_evidence
from devquitect_quality.reporting import (
    authentication_metadata,
    build_calibration_report,
    build_evaluation_report,
    build_policy_failure_report,
    build_validation_report,
    calibration_comparability,
    normalize_relative_path,
    render_text,
    serialize_json,
    validation_record,
    write_report_atomic,
)


def test_calibration_report_preserves_configuration_and_unknown_comparisons() -> None:
    report = build_calibration_report(
        run_id="run-1",
        skill_snapshot_id="sha256:snapshot",
        skill_version="abc123",
        model="gpt-5.4-mini",
        runtime={"codex_cli": "0.153.4"},
        suite_id="critical",
        suite_digest="suite-digest",
        repetitions=2,
        dimensions={"outcomes": {"pass": 2}},
        evidence_references=[{"run_id": "run-1"}],
        generated_at="2026-09-10T08:00:00+00:00",
    )

    assert report["report_type"] == "behavior-calibration"
    assert "summary_score" not in report
    assert calibration_comparability(report, report) == "comparable"
    assert calibration_comparability(report, None) == "unknown"
    assert calibration_comparability({}, {}) == "unknown"
    assert calibration_comparability(report, {**report, "model": "other"}) == "not-comparable"


def test_json_and_text_present_the_same_verdict() -> None:
    report = build_validation_report(
        source={"kind": "working-tree", "selector": "working-tree"},
        records=[validation_record("frontmatter.invalid", "skills/bad/SKILL.md", "broken")],
        generated_at="2026-08-30T08:00:00+00:00",
    )

    serialized = json.loads(serialize_json(report))
    text = render_text(report)

    assert serialized["result"] == "fail"
    assert "validation: fail" in text
    assert "frontmatter.invalid" in text
    assert serialized["records"][0]["message"] in text


def test_authentication_metadata_is_non_secret_and_legacy_reports_are_unknown() -> None:
    metadata = authentication_metadata(
        {
            "mode": "api-key",
            "execution_context": "unattended-behavioral",
            "policy": "allowed",
            "credential_state": "injected",
            "cleanup": "not_applicable",
            "token": "must-not-survive",
        }
    )

    assert metadata["mode"] == "api-key"
    assert "must-not-survive" not in json.dumps(metadata)
    assert authentication_metadata(None)["policy"] == "unknown"


def test_policy_failure_report_is_non_passing_and_contains_no_raw_error() -> None:
    report = build_policy_failure_report(
        report_type="check",
        inputs={"source": "working-tree"},
        authentication={
            "mode": "chatgpt-cache-local",
            "execution_context": "unattended-behavioral",
            "policy": "refused",
            "credential_state": "not-needed",
            "cleanup": "not_applicable",
        },
    )

    serialized = json.dumps(report)
    assert report["result"] == "fail"
    assert report["authentication"]["policy"] == "refused"
    assert "auth.json" not in serialized
    assert "token" not in serialized


def test_evaluation_report_collapses_auth_errors_without_retaining_paths_or_tokens() -> None:
    report = build_evaluation_report(
        source={"kind": "working-tree", "selector": "working-tree"},
        records=[
            {
                "case_id": "case-1",
                "repetition": 1,
                "classification": "inconclusive",
                "runtime_errors": [
                    "authentication failed with token=supersecret at /private/operator/auth.json"
                ],
                "redactions": [],
            }
        ],
        authentication={
            "mode": "api-key",
            "execution_context": "interactive-behavioral",
            "policy": "allowed",
            "credential_state": "injected",
            "cleanup": "not_applicable",
        },
    )

    serialized = json.dumps(report)
    assert "supersecret" not in serialized
    assert "/private/operator/auth.json" not in serialized
    assert report["records"][0]["runtime_errors"] == ["authentication runtime failure"]
    assert "authentication-error" in report["redactions"]


def test_cleanup_failure_is_recorded_as_non_passing_auth_evidence() -> None:
    report = build_evaluation_report(
        source={"kind": "working-tree", "selector": "working-tree"},
        records=[
            {
                "case_id": "case-1",
                "repetition": 1,
                "classification": "inconclusive",
                "runtime_errors": ["credential cleanup failed"],
                "redactions": [],
            }
        ],
        authentication=_auth_evidence(
            AuthSelection("chatgpt-cache-local", "interactive-behavioral"),
            execution_context="interactive-behavioral",
            cleanup_failed=True,
        ),
    )

    assert report["result"] == "inconclusive"
    assert report["authentication"]["credential_state"] == "cleanup-failed"
    assert report["authentication"]["cleanup"] == "failed"


def test_atomic_report_replaces_target_and_leaves_no_temporary_file(tmp_path: Path) -> None:
    target = tmp_path / "nested/report.json"
    target.parent.mkdir()
    target.write_text("old", encoding="utf-8")
    report = build_validation_report(
        source={"kind": "git-ref", "selector": "HEAD"},
        records=[],
        generated_at="2026-08-30T08:00:00+00:00",
    )

    write_report_atomic(target, report)

    assert json.loads(target.read_text(encoding="utf-8"))["result"] == "pass"
    assert list(target.parent.glob(".report.json.*.tmp")) == []


@pytest.mark.parametrize("path", ["/absolute/file", "../escape", "safe/../escape", ""])
def test_report_paths_must_be_safe_and_relative(path: str) -> None:
    with pytest.raises(ValueError):
        normalize_relative_path(path)
