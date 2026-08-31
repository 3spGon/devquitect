from __future__ import annotations

from pathlib import Path

from devquitect_quality.assertions import AssertionResult
from devquitect_quality.cases import load_cases, select_cases
from devquitect_quality.grading import grade_observation
from devquitect_quality.observations import Observation, RuntimeStatus

ROOT = Path(__file__).parents[2]


def test_critical_suite_has_fixed_repetitions_and_non_overridable_policy() -> None:
    cases = select_cases(
        load_cases(ROOT / "evals/cases", ROOT / "schemas/eval-case.schema.json"),
        suite="critical",
    )
    assert all(case.repetitions == 1 for case in cases)
    assert all(case.data["forbidden_effects"] for case in cases)

    observed = Observation(
        RuntimeStatus(0, "success"), (), "persuasive", (), (), None, None, {}, (), True
    )
    failed = AssertionResult("forbidden-effect", "fail", True, {}, {})
    assert grade_observation(observed, (failed,), {"score": 1.0}).classification == "fail"
