"""Isolated Codex App Server lifecycle evaluation for versioned scenarios."""

from __future__ import annotations

import json
import os
import selectors
import shutil
import subprocess
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .codex_adapter import (
    DEFAULT_TEST_MODEL,
    DEFAULT_TEST_REASONING_EFFORT,
    _stage_auth_cache,
)
from .fixtures import FixtureAttempt
from .models import SkillSnapshot
from .observations import (
    Observation,
    RuntimeStatus,
    checkpoint_state,
    filesystem_manifest,
    git_state,
    parse_jsonl_events,
)
from .redaction import redact_text
from .validate import (
    HOOK_CONFIG_PATH,
    HOOK_HANDLER_PATH,
    PLUGIN_MANIFEST_PATH,
    ValidationInputs,
)

MAX_MESSAGES = 500
MAX_PRIORITY_MESSAGES = 64
DEFAULT_TIMEOUT_SECONDS = 120


class AppServerError(RuntimeError):
    """The lifecycle protocol or isolated plugin setup could not complete."""


def _safe_name(manifest: Mapping[str, Any]) -> str:
    name = manifest.get("name")
    if not isinstance(name, str) or not name:
        raise AppServerError("plugin manifest has no usable name")
    return name


def _stage_plugin(
    attempt: FixtureAttempt, snapshot: SkillSnapshot, inputs: ValidationInputs
) -> tuple[Path, str]:
    required = (PLUGIN_MANIFEST_PATH, HOOK_CONFIG_PATH, HOOK_HANDLER_PATH)
    if inputs.unexpected_paths or any(path not in inputs.files for path in required):
        raise AppServerError("validated plugin inputs are incomplete or contain unexpected paths")
    try:
        manifest = json.loads(inputs.files[PLUGIN_MANIFEST_PATH])
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AppServerError(f"invalid frozen plugin manifest: {error}") from error
    if not isinstance(manifest, Mapping):
        raise AppServerError("frozen plugin manifest must be an object")
    plugin_name = _safe_name(manifest)
    marketplace = attempt.root / "marketplace"
    plugin_root = marketplace / "plugins" / plugin_name
    for relative in required:
        destination = plugin_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(inputs.files[relative])
    shutil.copytree(snapshot.snapshot_root / "skills", plugin_root / "skills", symlinks=True)
    marketplace_file = marketplace / ".agents" / "plugins" / "marketplace.json"
    marketplace_file.parent.mkdir(parents=True, exist_ok=True)
    marketplace_file.write_text(
        json.dumps(
            {
                "name": "devquitect-compaction-evaluation",
                "plugins": [
                    {
                        "name": plugin_name,
                        "source": {"source": "local", "path": f"./plugins/{plugin_name}"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    }
                ],
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return marketplace, plugin_name


def _command_environment(attempt: FixtureAttempt) -> dict[str, str]:
    environment = dict(os.environ)
    environment["CODEX_HOME"] = str(attempt.codex_home)
    attempt.codex_home.chmod(0o700)
    skills_root = attempt.codex_home / "skills"
    if skills_root.exists():
        skills_root.chmod(0o755)
    return environment


def _run_plugin_command(
    command: Sequence[str], *, cwd: Path, environment: Mapping[str, str], timeout_seconds: int
) -> None:
    try:
        result = subprocess.run(
            list(command),
            cwd=cwd,
            env=dict(environment),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise AppServerError(f"plugin setup failed: {error}") from error
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()[:2_000]
        raise AppServerError(f"plugin setup exited {result.returncode}: {detail}")


class _JSONLReader:
    def __init__(self, stream: Any) -> None:
        self._stream = stream
        self._selector = selectors.DefaultSelector()
        self._selector.register(stream, selectors.EVENT_READ)
        self._buffer = b""

    def read(self, timeout_seconds: float) -> dict[str, Any]:
        deadline = time.monotonic() + timeout_seconds
        while b"\n" not in self._buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not self._selector.select(remaining):
                raise AppServerError("App Server protocol timed out")
            chunk = os.read(self._stream.fileno(), 4096)
            if not chunk:
                raise AppServerError("App Server closed the protocol stream")
            self._buffer += chunk
        line, self._buffer = self._buffer.split(b"\n", 1)
        try:
            message = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise AppServerError(f"App Server emitted malformed JSON: {error.msg}") from error
        if not isinstance(message, dict):
            raise AppServerError("App Server message must be an object")
        return message

    def close(self) -> None:
        self._selector.close()


def _thread_id(message: Mapping[str, Any]) -> str | None:
    params = message.get("params")
    if not isinstance(params, Mapping):
        return None
    thread = params.get("thread")
    if isinstance(thread, Mapping) and isinstance(thread.get("id"), str):
        return str(thread["id"])
    if isinstance(params.get("threadId"), str):
        return str(params["threadId"])
    item = params.get("item")
    if isinstance(item, Mapping) and isinstance(item.get("threadId"), str):
        return str(item["threadId"])
    return None


def _send(process: subprocess.Popen[str], message: Mapping[str, Any]) -> None:
    if process.stdin is None:
        raise AppServerError("App Server stdin is unavailable")
    process.stdin.write((json.dumps(message, separators=(",", ":")) + "\n").encode("utf-8"))
    process.stdin.flush()


def _is_server_request(message: Mapping[str, Any]) -> bool:
    return isinstance(message.get("id"), (str, int)) and isinstance(message.get("method"), str)


def _is_priority_message(message: Mapping[str, Any]) -> bool:
    method = message.get("method")
    if method in {"error", "turn/completed", "turn/failed", "thread/completed"}:
        return True
    if method not in {"item/started", "item/completed"}:
        return False
    params = message.get("params")
    item = params.get("item") if isinstance(params, Mapping) else None
    return isinstance(item, Mapping) and item.get("type") == "contextCompaction"


def _is_compaction_message(message: Mapping[str, Any]) -> bool:
    if message.get("method") not in {"item/started", "item/completed"}:
        return False
    params = message.get("params")
    item = params.get("item") if isinstance(params, Mapping) else None
    return isinstance(item, Mapping) and item.get("type") == "contextCompaction"


def _record_message(messages: list[dict[str, Any]], message: dict[str, Any]) -> None:
    if len(messages) < MAX_MESSAGES or (
        _is_priority_message(message) and len(messages) < MAX_MESSAGES + MAX_PRIORITY_MESSAGES
    ):
        messages.append(message)


def _server_error(message: Mapping[str, Any]) -> str | None:
    if message.get("method") not in {"error", "turn/failed"}:
        return None
    params = message.get("params")
    payload = params if isinstance(params, Mapping) else message
    error = payload.get("error")
    if isinstance(error, Mapping):
        return str(error.get("message", error))
    return str(payload.get("message", payload.get("error", "App Server error")))


def _drive(
    process: subprocess.Popen[str],
    scenario: Mapping[str, Any],
    *,
    cwd: Path,
    sandbox: str,
    model: str,
    reasoning_effort: str,
    timeout_seconds: int,
) -> tuple[list[dict[str, Any]], int]:
    if process.stdout is None:
        raise AppServerError("App Server stdout is unavailable")
    reader = _JSONLReader(process.stdout)
    messages: list[dict[str, Any]] = []
    compaction_messages: list[dict[str, Any]] = []
    compaction_count = 0
    request_id = 0

    def record(message: dict[str, Any]) -> None:
        _record_message(messages, message)
        if _is_compaction_message(message):
            compaction_messages.append(message)

    def request(method: str, params: Mapping[str, Any]) -> dict[str, Any]:
        nonlocal request_id
        request_id += 1
        expected = request_id
        _send(process, {"method": method, "id": expected, "params": dict(params)})
        while True:
            message = reader.read(timeout_seconds)
            record(message)
            if message.get("id") == expected:
                if "error" in message:
                    raise AppServerError(str(message["error"]))
                result = message.get("result")
                if not isinstance(result, dict):
                    raise AppServerError(f"{method} returned a non-object result")
                return result
            if error := _server_error(message):
                raise AppServerError(error)
            if _is_server_request(message):
                _send(process, {"id": message["id"], "result": {"decision": "decline"}})

    request(
        "initialize",
        {
            "clientInfo": {
                "name": "devquitect-quality",
                "title": "Devquitect Quality",
                "version": "0.1.0",
            },
            "capabilities": {"experimentalApi": True},
        },
    )
    _send(process, {"method": "initialized", "params": {}})
    thread = request(
        "thread/start",
        {
            "model": model,
            "cwd": str(cwd),
            "approvalPolicy": "never",
            "sandbox": sandbox,
            "serviceName": "devquitect-quality",
        },
    ).get("thread")
    if not isinstance(thread, Mapping) or not isinstance(thread.get("id"), str):
        raise AppServerError("thread/start did not return a thread id")
    thread_id = str(thread["id"])

    def wait_for_turn(turn_id: str) -> None:
        while True:
            message = reader.read(timeout_seconds)
            record(message)
            if _is_server_request(message):
                _send(process, {"id": message["id"], "result": {"decision": "decline"}})
                continue
            if error := _server_error(message):
                raise AppServerError(error)
            if message.get("method") == "turn/completed":
                if _thread_id(message) != thread_id:
                    raise AppServerError("turn/completed belongs to another thread")
                params = message.get("params")
                turn = params.get("turn") if isinstance(params, Mapping) else None
                if isinstance(turn, Mapping) and turn.get("id") not in {None, turn_id}:
                    raise AppServerError("turn/completed belongs to another turn")
                return

    def compact() -> None:
        nonlocal compaction_count, request_id
        request_id += 1
        expected = request_id
        _send(
            process,
            {"method": "thread/compact/start", "id": expected, "params": {"threadId": thread_id}},
        )
        acknowledged = False
        started = False
        completed = False
        turn_completed = False
        while not completed:
            message = reader.read(timeout_seconds)
            record(message)
            if message.get("id") == expected:
                if message.get("error") or message.get("result") != {}:
                    raise AppServerError("thread/compact/start did not acknowledge with {}")
                acknowledged = True
                continue
            if error := _server_error(message):
                raise AppServerError(error)
            if _is_server_request(message):
                _send(process, {"id": message["id"], "result": {"decision": "decline"}})
                continue
            method = message.get("method")
            if method == "turn/completed":
                if _thread_id(message) != thread_id:
                    raise AppServerError(
                        "contextCompaction turn completed belongs to another thread"
                    )
                turn_completed = True
                continue
            if method not in {"item/started", "item/completed"}:
                continue
            if _thread_id(message) != thread_id:
                raise AppServerError("contextCompaction belongs to another thread")
            params = message.get("params")
            item = params.get("item") if isinstance(params, Mapping) else None
            if not isinstance(item, Mapping) or item.get("type") != "contextCompaction":
                continue
            if method == "item/started":
                started = True
            elif method == "item/completed":
                completed = True
        while not turn_completed:
            message = reader.read(timeout_seconds)
            if len(messages) < MAX_MESSAGES:
                messages.append(message)
            if error := _server_error(message):
                raise AppServerError(error)
            if _is_server_request(message):
                _send(process, {"id": message["id"], "result": {"decision": "decline"}})
                continue
            if message.get("method") != "turn/completed":
                continue
            if _thread_id(message) != thread_id:
                raise AppServerError("contextCompaction turn completed belongs to another thread")
            turn_completed = True
        if not acknowledged or not started or not completed or not turn_completed:
            raise AppServerError("contextCompaction lifecycle was incomplete")
        compaction_count += 1

    for step in scenario.get("steps", ()):
        if not isinstance(step, Mapping):
            raise AppServerError("scenario step must be an object")
        if "prompt" in step:
            prompt = step["prompt"]
            if not isinstance(prompt, str) or not prompt:
                raise AppServerError("scenario prompt must be non-empty text")
            result = request(
                "turn/start",
                {
                    "threadId": thread_id,
                    "input": [{"type": "text", "text": prompt}],
                    "model": model,
                    "effort": reasoning_effort,
                },
            )
            turn = result.get("turn")
            if not isinstance(turn, Mapping) or not isinstance(turn.get("id"), str):
                raise AppServerError("turn/start did not return a turn id")
            wait_for_turn(str(turn["id"]))
        elif step.get("compact") == {}:
            compact()
        else:
            raise AppServerError("scenario compact step must be exactly {compact: {}}")
    captured = {id(message) for message in messages}
    messages.extend(message for message in compaction_messages if id(message) not in captured)
    return messages, compaction_count


def run_app_server(
    attempt: FixtureAttempt,
    scenario: Mapping[str, Any],
    *,
    snapshot: SkillSnapshot,
    validation_inputs: ValidationInputs,
    sandbox: str = "read-only",
    model: str | None = None,
    reasoning_effort: str | None = None,
    executable: str = "codex",
    auth_cache: Path | None = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    environment: Mapping[str, str] | None = None,
) -> Observation:
    before_files = filesystem_manifest(attempt.workspace)
    before_git = git_state(attempt.workspace)
    state_before = checkpoint_state(attempt.workspace)
    process: subprocess.Popen[str] | None = None
    staged_auth: Path | None = None
    messages: list[dict[str, Any]] = []
    compaction_count = 0
    redactions: tuple[str, ...] = ()
    status = RuntimeStatus(None, "infrastructure-error", ("App Server attempt did not complete",))
    process_environment = _command_environment(attempt)
    if environment:
        process_environment.update(environment)
    secrets = tuple(
        value
        for key, value in process_environment.items()
        if any(marker in key.upper() for marker in ("TOKEN", "SECRET", "PASSWORD", "API_KEY"))
    )
    try:
        marketplace, plugin_name = _stage_plugin(attempt, snapshot, validation_inputs)
        process_environment["PWD"] = str(attempt.workspace)
        _run_plugin_command(
            [executable, "plugin", "marketplace", "add", str(marketplace), "--json"],
            cwd=attempt.workspace,
            environment=process_environment,
            timeout_seconds=timeout_seconds,
        )
        _run_plugin_command(
            [
                executable,
                "plugin",
                "add",
                plugin_name,
                "--marketplace",
                "devquitect-compaction-evaluation",
                "--json",
            ],
            cwd=attempt.workspace,
            environment=process_environment,
            timeout_seconds=timeout_seconds,
        )
        if auth_cache is not None:
            staged_auth = _stage_auth_cache(auth_cache, attempt.codex_home)
        process = subprocess.Popen(
            [executable, "--dangerously-bypass-hook-trust", "app-server", "--stdio"],
            cwd=attempt.workspace,
            env=process_environment,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
        )
        messages, compaction_count = _drive(
            process,
            scenario,
            cwd=attempt.workspace,
            sandbox=sandbox,
            model=model or DEFAULT_TEST_MODEL,
            reasoning_effort=reasoning_effort or DEFAULT_TEST_REASONING_EFFORT,
            timeout_seconds=timeout_seconds,
        )
        status = RuntimeStatus(0, "success")
    except (AppServerError, OSError, subprocess.TimeoutExpired) as error:
        status = RuntimeStatus(
            None, "infrastructure-error", (redact_text(str(error), secrets).value,)
        )
    finally:
        if staged_auth is not None:
            staged_auth.unlink(missing_ok=True)
        if process is not None:
            if process.poll() is None:
                process.terminate()
            try:
                stderr = process.communicate(timeout=5)[1]
            except subprocess.TimeoutExpired:
                process.kill()
                stderr = process.communicate()[1]
            if stderr:
                redacted = redact_text(stderr.decode("utf-8", errors="replace"), secrets)
                redactions = tuple(sorted(set(redactions) | set(redacted.redactions)))
                if status.classification != "success":
                    status = RuntimeStatus(
                        status.exit_code,
                        status.classification,
                        status.errors + (str(redacted.value)[:2_000],),
                    )
    events, final, terminal, parse_errors, event_redactions = parse_jsonl_events(
        "\n".join(json.dumps(message) for message in messages), secrets=secrets
    )
    if status.classification == "success" and (parse_errors or not terminal):
        status = RuntimeStatus(0, "infrastructure-error", parse_errors)
    redactions = tuple(sorted(set(redactions) | set(event_redactions)))
    return Observation(
        status,
        events,
        final,
        before_files,
        filesystem_manifest(attempt.workspace),
        before_git,
        git_state(attempt.workspace),
        {
            "before": state_before,
            "after": checkpoint_state(attempt.workspace),
            "compaction_count": compaction_count,
        },
        redactions,
        terminal,
    )
