"""Explicit authentication policy for behavioral commands."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

AUTH_MODES = ("credential-free", "api-key", "chatgpt-cache-local")
API_KEY_ENVIRONMENT = "OPENAI_API_KEY"


class AuthPolicyError(ValueError):
    """The requested authentication mode is missing or not allowed."""


@dataclass(frozen=True, slots=True)
class AuthSelection:
    mode: str
    execution_context: str
    auth_cache: Path | None = None
    environment: Mapping[str, str] | None = None


def resolve_auth(
    mode: str | None,
    *,
    execution_context: str,
    auth_cache: Path | None = None,
    allow_subscription_auth: bool = False,
    environment: Mapping[str, str] | None = None,
) -> AuthSelection:
    """Validate explicit auth without reading credential contents."""

    if mode is None:
        if execution_context == "structural":
            mode = "credential-free"
        else:
            raise AuthPolicyError(
                "behavioral authentication is explicit; pass --auth-mode "
                "credential-free, api-key, or chatgpt-cache-local"
            )
    if mode not in AUTH_MODES:
        raise AuthPolicyError(f"unsupported auth mode: {mode}")
    if execution_context == "structural" and mode != "credential-free":
        raise AuthPolicyError("structural check only supports --auth-mode credential-free")
    if mode == "credential-free":
        if auth_cache is not None or allow_subscription_auth:
            raise AuthPolicyError(
                "credential-free cannot be combined with --auth-cache or "
                "--allow-subscription-auth"
            )
        return AuthSelection(mode, execution_context)
    if mode == "api-key":
        if auth_cache is not None or allow_subscription_auth:
            raise AuthPolicyError(
                "api-key cannot be combined with --auth-cache or "
                "--allow-subscription-auth"
            )
        values = environment if environment is not None else os.environ
        if not values.get(API_KEY_ENVIRONMENT):
            raise AuthPolicyError(f"api-key requires {API_KEY_ENVIRONMENT}")
        return AuthSelection(
            mode,
            execution_context,
            environment={API_KEY_ENVIRONMENT: values[API_KEY_ENVIRONMENT]},
        )
    if execution_context == "unattended-behavioral":
        raise AuthPolicyError("chatgpt-cache-local is supervised-only and cannot run unattended")
    if auth_cache is None:
        raise AuthPolicyError("chatgpt-cache-local requires --auth-cache PATH")
    if not allow_subscription_auth:
        raise AuthPolicyError(
            "chatgpt-cache-local requires --allow-subscription-auth for a supervised run"
        )
    if auth_cache.is_symlink() or not auth_cache.is_file():
        raise AuthPolicyError("--auth-cache must name an existing regular file")
    return AuthSelection(mode, execution_context, auth_cache=auth_cache)
