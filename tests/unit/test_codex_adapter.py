from __future__ import annotations

import os
from types import SimpleNamespace

from devquitect_quality.codex_adapter import (
    DEFAULT_TEST_MODEL,
    DEFAULT_TEST_REASONING_EFFORT,
    build_command,
    preflight_codex,
)


def test_preflight_accepts_newer_cli_with_required_capabilities(tmp_path) -> None:
    executable = tmp_path / "codex"
    executable.write_text(
        "#!/bin/sh\n"
        "if [ \"$1\" = \"--version\" ]; then echo 'codex-cli 9.9.9'; else "
        "echo '--ephemeral --json --cd --sandbox --ignore-user-config --ignore-rules'; fi\n",
        encoding="utf-8",
    )
    executable.chmod(os.stat(executable).st_mode | 0o111)

    preflight = preflight_codex(str(executable))

    assert preflight.valid, preflight.errors
    assert preflight.version == "9.9.9"


def test_behavioral_command_uses_configurable_defaults(tmp_path) -> None:
    attempt = SimpleNamespace(workspace=tmp_path)

    command = build_command(attempt, ["inspect"])

    assert command[command.index("--model") + 1] == DEFAULT_TEST_MODEL == "gpt-5.6-luna"
    assert f'model_reasoning_effort="{DEFAULT_TEST_REASONING_EFFORT}"' in command
    assert DEFAULT_TEST_REASONING_EFFORT == "high"


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
