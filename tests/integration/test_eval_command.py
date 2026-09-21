from __future__ import annotations

from pathlib import Path

from devquitect_quality.assertions import AssertionResult
from devquitect_quality.cases import load_cases, select_cases
from devquitect_quality.evaluation import run_case
from devquitect_quality.fixtures import materialize_attempt
from devquitect_quality.grading import grade_observation
from devquitect_quality.models import SkillSource
from devquitect_quality.observations import NormalizedEvent, Observation, RuntimeStatus
from devquitect_quality.sources import freeze_source
from devquitect_quality.validate import load_validation_inputs

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


def test_run_case_routes_turns_and_scenarios_to_their_separate_runners(tmp_path: Path) -> None:
    cases = load_cases(ROOT / "evals/cases", ROOT / "schemas/eval-case.schema.json")
    old_case = next(case for case in cases if case.id == "compaction-recovery-resume-positive")
    scenario_case = next(case for case in cases if case.id == "compaction-recovery-compact-once")
    source = SkillSource.from_selector("working-tree", ROOT)
    inputs = load_validation_inputs(source)
    snapshot = freeze_source(source, tmp_path / "snapshot")
    calls: list[str] = []

    def observation() -> Observation:
        return Observation(
            RuntimeStatus(0, "success"),
            (
                NormalizedEvent("item/started", "compaction", {"item_id": "cmp"}),
                NormalizedEvent("item/completed", "compaction", {"item_id": "cmp"}),
                NormalizedEvent("turn/completed", "optional", {}),
            ),
            "continued",
            (),
            (),
            None,
            None,
            {"before": {}, "after": {}},
            (),
            True,
        )

    def old_runner(*_args: object, **_kwargs: object) -> Observation:
        calls.append("turns")
        return observation()

    def scenario_runner(*_args: object, **_kwargs: object) -> Observation:
        calls.append("scenario")
        return observation()

    with materialize_attempt(snapshot, ROOT / "evals/fixtures/compaction-recovery"):
        run_case(old_case, snapshot, ROOT, runner=old_runner)
    with materialize_attempt(snapshot, ROOT / "evals/fixtures/compaction-recovery"):
        run_case(
            scenario_case,
            snapshot,
            ROOT,
            validation_inputs=inputs,
            scenario_runner=scenario_runner,
        )

    assert calls == ["turns", "scenario"]
