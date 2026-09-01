"""Deterministic-first behavioral verdicts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from .assertions import AssertionResult
from .observations import Observation

Classification = Literal["pass", "fail", "inconclusive"]


@dataclass(frozen=True, slots=True)
class Verdict:
    classification: Classification
    deterministic_checks: tuple[AssertionResult, ...]
    critical_failures: tuple[str, ...]
    semantic_grades: Mapping[str, Any]
    eligibility: str


def grade_observation(
    observation: Observation,
    checks: Sequence[AssertionResult],
    semantic_grades: Mapping[str, Any] | None = None,
    *,
    release_eligible_source: bool = False,
) -> Verdict:
    grades = dict(semantic_grades or {})
    failures = tuple(
        check.assertion_id for check in checks if check.critical and check.status == "fail"
    )
    missing = any(check.critical and check.status == "not-evaluated" for check in checks)
    if observation.runtime_status.classification == "infrastructure-error" or missing:
        classification: Classification = "inconclusive"
    elif failures:
        classification = "fail"
    else:
        classification = "pass"
    eligibility = (
        "release-eligible"
        if classification == "pass" and release_eligible_source
        else ("diagnostic-only" if classification == "pass" else "not-eligible")
    )
    return Verdict(classification, tuple(checks), failures, grades, eligibility)
