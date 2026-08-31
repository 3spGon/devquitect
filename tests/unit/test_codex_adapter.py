from __future__ import annotations

from types import SimpleNamespace

from devquitect_quality.codex_adapter import (
    DEFAULT_TEST_MODEL,
    DEFAULT_TEST_REASONING_EFFORT,
    build_command,
)


def test_behavioral_command_uses_lightweight_defaults(tmp_path) -> None:
    attempt = SimpleNamespace(workspace=tmp_path)

    command = build_command(attempt, ["inspect"])

    assert command[command.index("--model") + 1] == DEFAULT_TEST_MODEL == "gpt-5.4-mini"
    assert f'model_reasoning_effort="{DEFAULT_TEST_REASONING_EFFORT}"' in command
    assert DEFAULT_TEST_REASONING_EFFORT == "low"


def test_behavioral_command_allows_explicit_calibration_override(tmp_path) -> None:
    attempt = SimpleNamespace(workspace=tmp_path)

    command = build_command(
        attempt,
        ["inspect"],
        model="gpt-5.6-terra",
        reasoning_effort="medium",
    )

    assert command[command.index("--model") + 1] == "gpt-5.6-terra"
    assert 'model_reasoning_effort="medium"' in command
