from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPOSITORY = Path(__file__).parents[2]


def test_check_runs_fast_composed_definition_of_done_and_writes_atomic_report(
    tmp_path: Path,
) -> None:
    report = tmp_path / "check.json"
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "devquitect_quality.cli",
            "check",
            "--source",
            "working-tree",
            "--report",
            str(report),
        ],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0, process.stderr
    payload = json.loads(process.stdout)
    assert payload == json.loads(report.read_text(encoding="utf-8"))
    assert payload["report_type"] == "check"
    assert payload["result"] == "pass"
    assert {record["code"] for record in payload["records"]} == {
        "check.validation",
        "check.tests",
    }


def test_check_invalid_source_returns_two_and_still_writes_report(tmp_path: Path) -> None:
    report = tmp_path / "invalid.json"
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "devquitect_quality.cli",
            "check",
            "--source",
            "missing-ref",
            "--report",
            str(report),
        ],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 2
    assert json.loads(report.read_text(encoding="utf-8"))["result"] == "fail"
