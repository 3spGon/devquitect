from __future__ import annotations

from devquitect_quality.assertions import evaluate_assertion, evaluate_assertions
from devquitect_quality.observations import (
    FileRecord,
    GitState,
    NormalizedEvent,
    Observation,
    RuntimeStatus,
)


def observation(
    *, after: tuple[FileRecord, ...] = (), state: dict[str, object] | None = None
) -> Observation:
    return Observation(
        runtime_status=RuntimeStatus(0, "success"),
        events=(
            NormalizedEvent("item.completed", "command", {"command": "git status"}),
            NormalizedEvent("item.completed", "tool", {"tool": "browser/open"}),
        ),
        final_response='{"result":"pass"}',
        filesystem_before=(),
        filesystem_after=after,
        git_before=GitState((), ""),
        git_after=GitState((), ""),
        persistent_state=state or {},
        redactions=(),
        terminal_event_seen=True,
    )


def test_read_only_write_and_allowlist_violation_fail_deterministically() -> None:
    changed = (FileRecord("unexpected.txt", "file", 1, "digest"),)
    result = evaluate_assertion(
        {"id": "workspace-allowlist", "type": "allowed-paths", "paths": ["reports/**"]},
        observation(after=changed),
    )

    assert result.status == "fail"
    assert result.critical is True
    assert result.observed["violations"] == ["unexpected.txt"]


def test_command_tool_artifact_and_final_json_assertions() -> None:
    artifact = FileRecord("reports/result.json", "file", 2, "abc")
    results = evaluate_assertions(
        (
            {"type": "command-occurrence", "pattern": "git *"},
            {"type": "tool-prohibition", "pattern": "email/*"},
            {"type": "artifact-present", "path": "reports/result.json", "sha256": "abc"},
            {"type": "final-json", "contains": {"result": "pass"}},
        ),
        observation(after=(artifact,)),
    )

    assert {result.status for result in results} == {"pass"}


def test_invalid_checkpoint_transition_fails_and_unknown_assertion_is_not_evaluated() -> None:
    observed = observation(state={"before": {"gate": 1}, "after": {"gate": 2}})
    transition = evaluate_assertion(
        {"type": "checkpoint-transition", "before": {"gate": 1}, "after": {"gate": 1}},
        observed,
    )
    unknown = evaluate_assertion({"type": "future-assertion"}, observed)

    assert transition.status == "fail"
    assert unknown.status == "not-evaluated"
