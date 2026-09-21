#!/usr/bin/env python3
"""Emit bounded recovery context after a Codex compactation."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

MAX_STDOUT_BYTES = 4096
KNOWN_FIELDS = {"skill", "session", "delivery_status"}
DELIVERY_STATUSES = {
    "active",
    "awaiting-input",
    "awaiting-authorization",
    "blocked",
    "complete",
}
TERMINAL_STATUSES = {"complete"}
ROOT_MARKERS = (".git", ".codex-plugin", "pyproject.toml", "AGENTS.md")


class HookError(ValueError):
    """An invalid hook input or repository layout."""


def _scalar(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    if value in {"null", "~"}:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    if value.startswith("[") or value.startswith("{"):
        return None
    return value


def _frontmatter(path: Path) -> tuple[dict[str, str | None], bool]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return {}, False
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}, False
    fields: dict[str, str | None] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, False
        key, raw = line.split(":", 1)
        key = key.strip()
        if key not in KNOWN_FIELDS:
            continue
        if key in fields:
            return {}, False
        value = _scalar(raw)
        if value is None and raw.strip() not in {"", "null", "~"}:
            return {}, False
        fields[key] = value
    return fields, True


def _repository_root(cwd: str) -> Path:
    path = Path(cwd)
    if not path.is_absolute():
        raise HookError("cwd must be absolute")
    try:
        path = path.resolve(strict=True)
    except OSError as exc:
        raise HookError("cwd is unavailable") from exc
    if not path.is_dir():
        raise HookError("cwd is not a directory")
    for candidate in (path, *path.parents):
        if any((candidate / marker).exists() for marker in ROOT_MARKERS):
            return candidate
    raise HookError("repository root not found")


def _candidate_paths(root: Path) -> tuple[list[Path], list[str]]:
    sessions = root / "docs" / "software-design"
    if not sessions.is_dir() or sessions.is_symlink():
        return [], []
    paths: list[Path] = []
    malformed: list[str] = []
    for session in sorted(sessions.iterdir(), key=lambda item: item.name):
        if session.is_symlink():
            malformed.append((session / "09-delivery-status.md").relative_to(root).as_posix())
            continue
        if not session.is_dir():
            continue
        path = session / "09-delivery-status.md"
        if path.exists() and not path.is_symlink() and path.is_file():
            paths.append(path)
    return paths, malformed


def _classify(root: Path, path: Path) -> tuple[str, str]:
    fields, valid = _frontmatter(path)
    relative = path.relative_to(root).as_posix()
    if not valid:
        return "malformed", relative
    if fields.get("skill") != "project-plan-execution":
        return "ignore", relative
    status = fields.get("delivery_status")
    if fields.get("session") is None or status not in DELIVERY_STATUSES:
        return "malformed", relative
    if status in TERMINAL_STATUSES:
        return "ignore", relative
    return "active", relative


def _context(paths: list[str], *, ambiguous: bool) -> str:
    if ambiguous:
        prefix = (
            "Compaction recovery is ambiguous. Do not resume implementation or select a "
            "checkpoint silently; reconcile the candidates through the project-plan-execution "
            "recovery contract. Candidates: "
        )
    else:
        prefix = (
            "After compactation, enter the project-plan-execution recovery contract before "
            "implementation. Re-read and reconcile the checkpoint with repository evidence; "
            "conversation cannot establish authorization, acceptance, completion, or verification. "
            "Checkpoint: "
        )
    return prefix + ", ".join(paths) + "."


def _bounded_output(paths: list[str], *, ambiguous: bool) -> str:
    omitted = 0
    for count in range(len(paths), -1, -1):
        shown = paths[:count]
        suffix = ""
        omitted = len(paths) - count
        if omitted:
            suffix = f" Omitted {omitted} additional candidate(s)."
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": _context(shown, ambiguous=ambiguous) + suffix,
            }
        }
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(encoded) <= MAX_STDOUT_BYTES:
            return encoded.decode("utf-8")
    raise HookError("recovery output cannot fit the bound")


def _load_event() -> dict[str, Any]:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as exc:
        raise HookError("stdin must contain one JSON object") from exc
    if not isinstance(event, dict):
        raise HookError("stdin must contain one JSON object")
    return event


def main() -> int:
    try:
        event = _load_event()
        if event.get("hook_event_name") != "SessionStart" or event.get("source") != "compact":
            return 0
        cwd = event.get("cwd")
        if not isinstance(cwd, str):
            raise HookError("cwd is required")
        root = _repository_root(cwd)
        active: list[str] = []
        malformed: list[str] = []
        paths, unsafe_candidates = _candidate_paths(root)
        malformed.extend(unsafe_candidates)
        for path in paths:
            kind, relative = _classify(root, path)
            if kind == "active":
                active.append(relative)
            elif kind == "malformed":
                malformed.append(relative)
        if malformed:
            sys.stdout.write(_bounded_output(sorted(active + malformed), ambiguous=True))
        elif len(active) == 1:
            sys.stdout.write(_bounded_output(active, ambiguous=False))
        elif len(active) > 1:
            sys.stdout.write(_bounded_output(active, ambiguous=True))
        return 0
    except (HookError, OSError, ValueError) as exc:
        print(f"compaction recovery unavailable: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
