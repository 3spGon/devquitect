"""Behavioral case orchestration over immutable skill snapshots."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .assertions import evaluate_assertions
from .cases import EvalCase
from .codex_adapter import DEFAULT_TEST_MODEL, DEFAULT_TEST_REASONING_EFFORT, run_codex
from .fixtures import materialize_attempt
from .grading import Verdict, grade_observation
from .models import SkillSnapshot

Runner = Callable[..., Any]


def run_case(
    case: EvalCase,
    snapshot: SkillSnapshot,
    repository: Path,
    *,
    model: str | None = None,
    reasoning_effort: str | None = None,
    auth_cache: Path | None = None,
    runner: Runner = run_codex,
) -> list[dict[str, Any]]:
    selected_model = model or DEFAULT_TEST_MODEL
    selected_effort = reasoning_effort or DEFAULT_TEST_REASONING_EFFORT
    fixture = repository / "evals" / "fixtures" / str(case.data["fixture"])
    records: list[dict[str, Any]] = []
    for repetition in range(1, case.repetitions + 1):
        with materialize_attempt(snapshot, fixture) as attempt:
            observation = runner(
                attempt,
                tuple(case.data["turns"]),
                sandbox=str(case.data["sandbox"]),
                model=selected_model,
                reasoning_effort=selected_effort,
                auth_cache=auth_cache,
            )
            checks = evaluate_assertions(tuple(case.data["assertions"]), observation)
            verdict: Verdict = grade_observation(
                observation,
                checks,
                release_eligible_source=snapshot.release_eligible_source,
            )
            records.append(
                {
                    "run_id": str(uuid.uuid4()),
                    "case_id": case.id,
                    "case_digest": case.digest,
                    "repetition": repetition,
                    "snapshot_id": snapshot.snapshot_id,
                    "fixture": str(case.data["fixture"]),
                    "model": selected_model,
                    "reasoning_effort": selected_effort,
                    "classification": verdict.classification,
                    "eligibility": verdict.eligibility,
                    "deterministic_checks": [check.as_dict() for check in checks],
                    "critical_failures": list(verdict.critical_failures),
                    "runtime_errors": list(observation.runtime_status.errors),
                    "redactions": list(observation.redactions),
                }
            )
    return records
