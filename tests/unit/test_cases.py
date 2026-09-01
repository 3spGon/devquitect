from __future__ import annotations

from pathlib import Path

import pytest

from devquitect_quality.cases import CaseError, load_cases, select_cases

ROOT = Path(__file__).parents[2]


def test_cases_are_schema_valid_unique_and_cover_each_skill_routing() -> None:
    cases = load_cases(ROOT / "evals/cases", ROOT / "schemas/eval-case.schema.json")
    routing = {(case.data["target_skill"], case.data["activation"]) for case in cases}
    identifiers = {case.id for case in cases}

    for skill in ("software-idea-to-project", "project-plan-execution", "targeted-refactoring"):
        assert (skill, "implicit-negative") in routing
        assert any(pair[0] == skill and pair[1] != "implicit-negative" for pair in routing)
    assert select_cases(cases, suite="critical")
    assert {
        "change-profile-expedited",
        "change-profile-elevation",
        "change-profile-stale-context",
        "change-profile-legacy-session",
        "change-profile-refactor-routing",
    } <= identifiers
    assert {case.id for case in select_cases(cases, suite="change-profile")} == {
        "change-profile-expedited",
        "change-profile-elevation",
        "change-profile-stale-context",
        "change-profile-legacy-session",
        "change-profile-refactor-routing",
    }


def test_empty_selection_and_conflicting_selectors_fail() -> None:
    cases = load_cases(ROOT / "evals/cases", ROOT / "schemas/eval-case.schema.json")
    with pytest.raises(CaseError):
        select_cases(cases, suite="missing")
    with pytest.raises(CaseError):
        select_cases(cases, suite="critical", case_id=cases[0].id)
