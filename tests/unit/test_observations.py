from __future__ import annotations

from pathlib import Path

from devquitect_quality.observations import filesystem_manifest, parse_jsonl_events
from devquitect_quality.redaction import redact_text, redact_value

STREAMS = Path(__file__).parents[1] / "fixtures" / "codex-streams"


def test_success_stream_normalizes_commands_final_message_and_terminal_event() -> None:
    events, final, terminal, errors, redactions = parse_jsonl_events(
        (STREAMS / "success.jsonl").read_text(encoding="utf-8")
    )

    assert terminal is True
    assert errors == ()
    assert final == "Completed safely."
    assert [event.category for event in events].count("command") == 1
    assert redactions == ()


def test_truncated_and_invalid_streams_are_infrastructure_errors() -> None:
    _, _, terminal, errors, _ = parse_jsonl_events(
        (STREAMS / "truncated.jsonl").read_text(encoding="utf-8") + "not-json\n"
    )

    assert terminal is False
    assert any("invalid JSONL" in error for error in errors)
    assert any("no terminal event" in error for error in errors)


def test_unknown_optional_event_does_not_invalidate_contract() -> None:
    events, _, terminal, errors, _ = parse_jsonl_events(
        (STREAMS / "optional-event.jsonl").read_text(encoding="utf-8")
    )

    assert terminal is True
    assert errors == ()
    assert any(
        event.type == "future.telemetry" and event.category == "optional" for event in events
    )


def test_filesystem_manifest_records_content_and_does_not_follow_symlinks(tmp_path: Path) -> None:
    (tmp_path / "file.txt").write_text("content", encoding="utf-8")
    (tmp_path / "link").symlink_to("file.txt")

    records = {record.path: record for record in filesystem_manifest(tmp_path)}

    assert records["file.txt"].kind == "file"
    assert records["link"].kind == "symlink"
    assert records["link"].size == len("file.txt")


def test_redaction_masks_explicit_and_pattern_credentials_recursively() -> None:
    explicit = "known-secret-value"
    result = redact_value(
        {
            "message": f"Bearer abcdefghijklmnop and {explicit}",
            "nested": ["api_key=supersecretvalue"],
        },
        (explicit,),
    )

    assert explicit not in str(result.value)
    assert "abcdefghijklmnop" not in str(result.value)
    assert "supersecretvalue" not in str(result.value)
    assert result.redactions
    assert redact_text("ordinary text").value == "ordinary text"
