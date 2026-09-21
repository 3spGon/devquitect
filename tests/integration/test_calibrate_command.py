from __future__ import annotations

import json
from pathlib import Path

from devquitect_quality import cli

ROOT = Path(__file__).parents[2]


def test_calibrate_writes_review_only_report_without_a_model_call(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    def fake_run_case(case, snapshot, repository, **kwargs):
        return [
            {
                "run_id": "run-1",
                "case_id": case.id,
                "classification": "inconclusive",
                "runtime_errors": ["redacted runtime error"],
                "redactions": ["api-key"],
            }
        ]

    monkeypatch.setattr(cli, "run_case", fake_run_case)
    report = tmp_path / "calibration.json"

    assert (
        cli.main(
            [
                "calibrate",
                "--source",
                "working-tree",
                "--case",
                "self-hosting",
                "--auth-mode",
                "credential-free",
                "--report",
                str(report),
            ]
        )
        == 0
    )

    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload == json.loads(capsys.readouterr().out)
    assert payload["dimensions"] == {
        "cases": {"self-hosting": {"inconclusive": 1}},
        "outcomes": {"inconclusive": 1},
    }
    assert payload["evidence_references"][0]["runtime_errors"] == ["redacted runtime error"]
