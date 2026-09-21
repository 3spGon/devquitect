from __future__ import annotations

from devquitect_quality.codex_adapter import (
    DISABLED_DISCOVERY_FEATURES,
    REQUIRED_FLAGS,
    preflight_codex,
)


def test_local_codex_cli_exposes_runtime_contract() -> None:
    preflight = preflight_codex()

    assert preflight.valid, preflight.errors
    assert preflight.version
    assert REQUIRED_FLAGS
    assert DISABLED_DISCOVERY_FEATURES == ("plugins", "apps", "plugin_sharing")
