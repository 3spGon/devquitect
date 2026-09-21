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
    assert {
        "slice-verification-positive",
        "slice-verification-negative",
        "slice-verification-legacy-status",
    } <= identifiers
    assert {
        "compaction-recovery-resume-positive",
        "compaction-recovery-resume-negative",
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


def test_slice_verification_cases_pin_the_supported_flow() -> None:
    cases = load_cases(ROOT / "evals/cases", ROOT / "schemas/eval-case.schema.json")
    selected = {case.id: case.data for case in cases if case.id.startswith("slice-verification-")}
    positive = selected["slice-verification-positive"]["assertions"]
    negative = selected["slice-verification-negative"]["assertions"]
    assert {item["pattern"] for item in positive if item["type"] == "command-occurrence"} == {
        "*verify_slice.py check*",
        "*verify_slice.py close*",
    }
    assert any(
        item["type"] == "checkpoint-transition"
        and item["before"] == {"slice": "SLICE-001", "status": "in-progress"}
        and item["after"] == {"slice": "SLICE-001", "status": "verified"}
        for item in positive
    )
    assert {item["pattern"] for item in negative if item["type"] == "command-prohibition"} == {
        "*verify_slice.py close*"
    }


def test_compaction_recovery_cases_pin_conservative_policy() -> None:
    cases = load_cases(ROOT / "evals/cases", ROOT / "schemas/eval-case.schema.json")
    selected = {case.id: case.data for case in cases if case.id.startswith("compaction-recovery-")}
    positive = selected["compaction-recovery-resume-positive"]
    negative = selected["compaction-recovery-resume-negative"]
    assert positive["fixture"] == negative["fixture"] == "compaction-recovery"
    assert "verification-without-evidence" in positive["forbidden_effects"]
    assert {
        "workspace-write",
        "stale-memory-authority",
        "repeated-completed-work",
    } <= set(negative["forbidden_effects"])
    assert any(
        item.get("id") == "do-not-repeat-completed-slices" for item in positive["assertions"]
    )
    assert any(
        item.get("id") == "reject-stale-memory-repetition" for item in negative["assertions"]
    )
