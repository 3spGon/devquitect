"""Bounded, deterministic secret redaction for retained evaluation evidence."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

_PATTERNS = (
    re.compile(r"(?i)\b(bearer\s+)[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\b(sk-[A-Za-z0-9_-]{12,})\b"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)(\s*[:=]\s*)[^\s,;]+"),
)


@dataclass(frozen=True, slots=True)
class RedactionResult:
    value: Any
    redactions: tuple[str, ...]


def redact_text(text: str, secrets: Sequence[str] = ()) -> RedactionResult:
    """Mask known values and common credential shapes without retaining the secret."""

    redacted = text
    applied: list[str] = []
    for secret in sorted({value for value in secrets if len(value) >= 4}, key=len, reverse=True):
        if secret in redacted:
            redacted = redacted.replace(secret, "[REDACTED]")
            applied.append("explicit-secret")
    for index, pattern in enumerate(_PATTERNS, start=1):
        if pattern.search(redacted):
            if index == 1:
                redacted = pattern.sub(r"\1[REDACTED]", redacted)
            elif index == 3:
                redacted = pattern.sub(r"\1\2[REDACTED]", redacted)
            else:
                redacted = pattern.sub("[REDACTED]", redacted)
            applied.append(f"credential-pattern-{index}")
    return RedactionResult(redacted, tuple(sorted(set(applied))))


def redact_value(value: Any, secrets: Sequence[str] = ()) -> RedactionResult:
    """Recursively redact a JSON-compatible evidence value."""

    labels: set[str] = set()

    def visit(item: Any) -> Any:
        if isinstance(item, str):
            result = redact_text(item, secrets)
            labels.update(result.redactions)
            return result.value
        if isinstance(item, Mapping):
            return {str(key): visit(nested) for key, nested in item.items()}
        if isinstance(item, Sequence) and not isinstance(item, (bytes, bytearray)):
            return [visit(nested) for nested in item]
        return item

    return RedactionResult(visit(value), tuple(sorted(labels)))
