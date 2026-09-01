from __future__ import annotations

import json
from pathlib import Path

import pytest

from devquitect_quality.reporting import (
    build_validation_report,
    normalize_relative_path,
    render_text,
    serialize_json,
    validation_record,
    write_report_atomic,
)


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
