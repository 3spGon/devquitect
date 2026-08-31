from __future__ import annotations

from devquitect_quality.codex_adapter import (
    DISABLED_DISCOVERY_FEATURES,
    REQUIRED_FLAGS,
    SUPPORTED_CODEX_VERSION,
    preflight_codex,
)


def test_local_codex_cli_matches_pinned_runtime_contract() -> None:
    preflight = preflight_codex()

    assert preflight.version == SUPPORTED_CODEX_VERSION
    assert preflight.valid, preflight.errors
    assert REQUIRED_FLAGS
    assert DISABLED_DISCOVERY_FEATURES == ("plugins", "apps", "plugin_sharing")
