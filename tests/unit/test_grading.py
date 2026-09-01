from __future__ import annotations

from devquitect_quality.assertions import AssertionResult
from devquitect_quality.grading import grade_observation
from devquitect_quality.observations import Observation, RuntimeStatus


def observation(classification: str = "success") -> Observation:
    return Observation(RuntimeStatus(0, classification), (), None, (), (), None, None, {}, (), True)


def test_favorable_semantic_grade_cannot_erase_critical_failure() -> None:
    failure = AssertionResult("unauthorized-write", "fail", True, {}, {})
    verdict = grade_observation(
        observation(), (failure,), {"score": 1.0, "classification": "excellent"}
    )

    assert verdict.classification == "fail"
    assert verdict.critical_failures == ("unauthorized-write",)


def test_infrastructure_and_missing_critical_evidence_are_inconclusive() -> None:
    missing = AssertionResult("checkpoint", "not-evaluated", True, {}, {})
    assert grade_observation(observation(), (missing,)).classification == "inconclusive"
    assert (
        grade_observation(observation("infrastructure-error"), ()).classification == "inconclusive"
    )
