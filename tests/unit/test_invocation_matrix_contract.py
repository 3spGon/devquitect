import hashlib
import json
import re
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from devquitect_quality.assertions import evaluate_assertion
from devquitect_quality.observations import GitState, Observation, RuntimeStatus

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("skill", "implicit"),
    [
        ("project-plan-execution", False),
        ("software-idea-to-project", True),
        ("quick-change", True),
        ("targeted-refactoring", True),
    ],
)
def test_host_invocation_metadata(skill, implicit):
    metadata = yaml.safe_load((ROOT / f"skills/{skill}/agents/openai.yaml").read_text())
    assert metadata["policy"]["allow_implicit_invocation"] is implicit
    assert f"${skill}" in metadata["interface"]["default_prompt"]


def test_explicit_invocation_preserves_scope_and_authority():
    reference = (ROOT / "skills/software-idea-to-project/references/implementation-planning.md")
    text = reference.read_text()
    assert "Explicit user invocation takes precedence over host matching" in text
    assert "does not expand the selected" in text
    assert "grant implementation, behavioral-testing, or external-action authority" in text
    quick = (ROOT / "skills/quick-change/SKILL.md").read_text()
    assert "does not grant implementation authority or suppress escalation" in quick


def test_initial_matrix_rows_are_independent_and_unexecuted():
    text = (ROOT / "docs/skill-change-ledger.md").read_text()
    block = re.search(r"```devquitect-evaluation-matrix\n(.*?)\n```", text, re.S)[1]
    matrix = yaml.safe_load(block)
    assert matrix["prompt_change_group"] == "PC-DN-004-MATRIX"
    cases = matrix["representative_cases"]
    assert len(cases) == len(set(cases))
    suite = "".join(
        f"{case}:{hashlib.sha256((ROOT / f'evals/cases/{case}.yaml').read_bytes()).hexdigest()}\n"
        for case in sorted(cases)
    )
    digest = "sha256:" + hashlib.sha256(suite.encode()).hexdigest()
    rows = matrix["rows"]
    assert [row["model_id"] for row in rows] == [
        "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna", "gpt-6-sol", "gpt-6-luna",
    ]
    for row in rows:
        assert set(row) == {
            "model_id", "host", "runtime", "reasoning_effort", "suite_revision",
            "repetitions", "report_references", "authorization", "verdict",
        }
        assert row["suite_revision"] == digest
        assert row["repetitions"] == 1
        assert row["authorization"] == "not-authorized"
        assert row["host"] is row["runtime"] is row["reasoning_effort"] is None
        assert row["report_references"] == []
        assert row["verdict"] == "not-run"


def test_matrix_rejects_pooled_or_invented_evidence():
    reference = (ROOT / "skills/software-idea-to-project/references/implementation-planning.md")
    text = reference.read_text()
    assert "Behavioral\ncomparisons require separate user authorization" in text
    assert "Keep verdicts independent and never pool scores or\nresults" in text
    assert "do not\nclaim a model-only comparison" in text
    assert "Behavioral success cannot override deterministic failures" in text
    assert "failures as inconclusive; they never pass" in text
    assert "pending row supplies no behavioral or release evidence" in text
    negative = yaml.safe_load((ROOT / "evals/cases/evaluation-matrix-negative.yaml").read_text())
    expected = next(a["contains"] for a in negative["assertions"] if a["type"] == "final-json")
    assert expected == {
        "pooled": False, "model_only_comparison": False,
        "failed_row_verdict": "inconclusive", "release_eligible": False,
    }


@pytest.mark.parametrize("case", ["evaluation-matrix-positive", "evaluation-matrix-negative"])
def test_matrix_case_assertions_accept_safe_output_and_reject_each_violation(case):
    data = yaml.safe_load((ROOT / f"evals/cases/{case}.yaml").read_text())
    assertion = next(a for a in data["assertions"] if a["type"] == "final-json")
    expected = assertion["contains"]
    observation = Observation(
        runtime_status=RuntimeStatus(0, "success"),
        events=(),
        final_response=json.dumps(expected),
        filesystem_before=(),
        filesystem_after=(),
        git_before=GitState((), ""),
        git_after=GitState((), ""),
        persistent_state={},
        redactions=(),
        terminal_event_seen=True,
    )
    assert evaluate_assertion(assertion, observation).status == "pass"
    for field in expected:
        unsafe = replace(observation, final_response=json.dumps({**expected, field: None}))
        result = evaluate_assertion(assertion, unsafe)
        assert result.status == "fail"
        assert result.critical is True
