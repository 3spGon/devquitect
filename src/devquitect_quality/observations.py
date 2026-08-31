"""Normalize process, runtime, filesystem, Git, and checkpoint evidence."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from .redaction import redact_value

RuntimeClass = Literal["success", "quality-failure", "infrastructure-error"]


@dataclass(frozen=True, slots=True)
class RuntimeStatus:
    exit_code: int | None
    classification: RuntimeClass
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class NormalizedEvent:
    type: str
    category: str
    detail: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class FileRecord:
    path: str
    kind: str
    size: int
    sha256: str


@dataclass(frozen=True, slots=True)
class GitState:
    status: tuple[str, ...]
    diff: str


@dataclass(frozen=True, slots=True)
class Observation:
    runtime_status: RuntimeStatus
    events: tuple[NormalizedEvent, ...]
    final_response: str | None
    filesystem_before: tuple[FileRecord, ...]
    filesystem_after: tuple[FileRecord, ...]
    git_before: GitState | None
    git_after: GitState | None
    persistent_state: Mapping[str, Any]
    redactions: tuple[str, ...]
    terminal_event_seen: bool

    @property
    def changed_paths(self) -> tuple[str, ...]:
        before = {record.path: record for record in self.filesystem_before}
        after = {record.path: record for record in self.filesystem_after}
        return tuple(
            sorted(
                path for path in before.keys() | after.keys() if before.get(path) != after.get(path)
            )
        )


def filesystem_manifest(
    root: Path, *, ignored: Iterable[str] = (".git",)
) -> tuple[FileRecord, ...]:
    """Capture a portable, content-addressed manifest without following symlinks."""

    ignored_roots = set(ignored)
    records: list[FileRecord] = []
    if not root.exists():
        return ()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in ignored_roots:
            continue
        normalized = PurePosixPath(*relative.parts).as_posix()
        if path.is_symlink():
            content = os.readlink(path).encode()
            kind = "symlink"
        elif path.is_file():
            content = path.read_bytes()
            kind = "file"
        else:
            continue
        records.append(
            FileRecord(normalized, kind, len(content), hashlib.sha256(content).hexdigest())
        )
    return tuple(records)


def git_state(root: Path) -> GitState | None:
    """Capture status and HEAD diff when the fixture is a Git worktree."""

    probe = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
        check=False,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        return None
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    diff = subprocess.run(
        ["git", "-C", str(root), "diff", "--binary", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return GitState(tuple(status), diff)


def _event_detail(item: Mapping[str, Any]) -> tuple[str, str, dict[str, Any]]:
    event_type = str(item.get("type", "unknown"))
    payload = item.get("item") if isinstance(item.get("item"), Mapping) else item
    assert isinstance(payload, Mapping)
    item_type = str(payload.get("type", event_type))
    if item_type in {"agent_message", "assistant_message", "message"}:
        return event_type, "message", {"text": str(payload.get("text", payload.get("content", "")))}
    if item_type in {"command_execution", "command"}:
        return (
            event_type,
            "command",
            {
                "command": str(payload.get("command", "")),
                "status": payload.get("status"),
                "exit_code": payload.get("exit_code"),
            },
        )
    if item_type in {"mcp_tool_call", "tool_call"}:
        return (
            event_type,
            "tool",
            {
                "tool": str(payload.get("server", ""))
                + "/"
                + str(payload.get("tool", payload.get("name", "")))
            },
        )
    if item_type in {"file_change", "file_changes"}:
        changes = payload.get("changes", payload.get("path", []))
        return event_type, "file", {"changes": changes}
    if item_type in {"web_search", "search"}:
        return event_type, "search", {"query": str(payload.get("query", ""))}
    if event_type in {"error", "turn.failed"}:
        return (
            event_type,
            "runtime-error",
            {"message": str(item.get("message", item.get("error", "runtime error")))},
        )
    return event_type, "optional", {"item_type": item_type}


def parse_jsonl_events(
    lines: str | Iterable[str], *, secrets: Sequence[str] = (), max_events: int = 500
) -> tuple[tuple[NormalizedEvent, ...], str | None, bool, tuple[str, ...], tuple[str, ...]]:
    """Parse untrusted JSONL as data and return bounded normalized evidence."""

    iterable = lines.splitlines() if isinstance(lines, str) else lines
    events: list[NormalizedEvent] = []
    errors: list[str] = []
    labels: set[str] = set()
    final_response: str | None = None
    terminal = False
    for number, line in enumerate(iterable, start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"invalid JSONL at line {number}: {error.msg}")
            continue
        if not isinstance(raw, Mapping):
            errors.append(f"invalid JSONL event at line {number}: object required")
            continue
        event_type, category, detail = _event_detail(raw)
        redacted = redact_value(detail, secrets)
        labels.update(redacted.redactions)
        if len(events) < max_events:
            events.append(NormalizedEvent(event_type, category, redacted.value))
        if category == "message" and redacted.value.get("text"):
            final_response = str(redacted.value["text"])
        if category == "runtime-error":
            errors.append(str(redacted.value["message"]))
        if event_type in {"turn.completed", "turn.failed", "thread.completed"}:
            terminal = True
    if not terminal:
        errors.append("runtime stream has no terminal event")
    return tuple(events), final_response, terminal, tuple(errors), tuple(sorted(labels))
