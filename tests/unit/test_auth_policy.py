from __future__ import annotations

from pathlib import Path

import pytest

from devquitect_quality.auth_policy import resolve_auth


def test_behavioral_auth_must_be_explicit() -> None:
    with pytest.raises(ValueError, match="authentication is explicit"):
        resolve_auth(None, execution_context="interactive-behavioral")


def test_api_key_requires_only_the_supported_environment_boundary() -> None:
    selection = resolve_auth(
        "api-key",
        execution_context="interactive-behavioral",
        environment={"OPENAI_API_KEY": "secret"},
    )

    assert selection.environment == {"OPENAI_API_KEY": "secret"}
    assert selection.auth_cache is None


def test_local_cache_requires_an_explicit_source() -> None:
    with pytest.raises(ValueError, match="--auth-cache PATH"):
        resolve_auth("chatgpt-cache-local", execution_context="interactive-behavioral")


def test_local_cache_requires_supervised_acknowledgement() -> None:
    with pytest.raises(ValueError, match="--allow-subscription-auth"):
        resolve_auth(
            "chatgpt-cache-local",
            execution_context="interactive-behavioral",
            auth_cache=Path(__file__),
        )


def test_local_cache_is_refused_for_unattended_behavior() -> None:
    with pytest.raises(ValueError, match="supervised-only"):
        resolve_auth(
            "chatgpt-cache-local",
            execution_context="unattended-behavioral",
            auth_cache=Path(__file__),
            allow_subscription_auth=True,
        )


def test_structural_mode_defaults_to_credential_free_and_rejects_auth_options(tmp_path) -> None:
    assert resolve_auth(None, execution_context="structural").mode == "credential-free"
    with pytest.raises(ValueError, match="structural check"):
        resolve_auth("api-key", execution_context="structural")
    with pytest.raises(ValueError, match="credential-free"):
        resolve_auth(
            "credential-free",
            execution_context="structural",
            auth_cache=tmp_path / "auth.json",
        )
