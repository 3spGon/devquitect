"""Codex CLI adapter with explicit isolation and failure classification."""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from .fixtures import FixtureAttempt
from .observations import (
    Observation,
    RuntimeStatus,
    checkpoint_state,
    filesystem_manifest,
    git_state,
    parse_jsonl_events,
)
from .redaction import redact_text

DEFAULT_TEST_MODEL = "gpt-5.6-luna"
DEFAULT_TEST_REASONING_EFFORT = "high"
REQUIRED_FLAGS = (
    "--ephemeral",
    "--json",
    "--cd",
    "--sandbox",
    "--ignore-user-config",
    "--ignore-rules",
)
SAFE_SANDBOXES = frozenset({"read-only", "workspace-write"})
DISABLED_DISCOVERY_FEATURES = ("plugins", "apps", "plugin_sharing")


@dataclass(frozen=True, slots=True)
class CodexPreflight:
    valid: bool
    version: str
    errors: tuple[str, ...]


def _stage_auth_cache(source: Path, codex_home: Path) -> Path:
    source_descriptor = -1
    target_descriptor = -1
    target_created = False
    target = codex_home / "auth.json"
    try:
        source_descriptor = os.open(
            source,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
        source_stat = os.fstat(source_descriptor)
        if not stat.S_ISREG(source_stat.st_mode):
            raise ValueError("Codex authentication cache must be a regular file")
        getuid = getattr(os, "getuid", None)
        if getuid is not None and source_stat.st_uid != getuid():
            raise ValueError("Codex authentication cache must be owned by the current user")
        if stat.S_IMODE(source_stat.st_mode) & 0o077:
            raise ValueError("Codex authentication cache must not be accessible by group or others")
        codex_home_stat = codex_home.lstat()
        if (
            not stat.S_ISDIR(codex_home_stat.st_mode)
            or codex_home.is_symlink()
            or (getuid is not None and codex_home_stat.st_uid != getuid())
        ):
            raise ValueError("isolated Codex home must be an owned directory")
        codex_home.chmod(0o700)
        target_descriptor = os.open(
            target,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        target_created = True
        os.fchmod(target_descriptor, 0o600)
        with os.fdopen(source_descriptor, "rb") as source_handle:
            source_descriptor = -1
            with os.fdopen(target_descriptor, "wb") as target_handle:
                target_descriptor = -1
                shutil.copyfileobj(source_handle, target_handle)
        if stat.S_IMODE(target.stat().st_mode) & 0o077:
            raise ValueError("staged Codex authentication must be owner-only")
        return target
    except BaseException:
        if source_descriptor != -1:
            os.close(source_descriptor)
        if target_descriptor != -1:
            os.close(target_descriptor)
        if target_created:
            target.unlink(missing_ok=True)
        raise


def preflight_codex(executable: str = "codex") -> CodexPreflight:
    """Verify the runtime and capabilities assumed by the approved adapter."""

    try:
        version_run = subprocess.run(
            [executable, "--version"], check=False, capture_output=True, text=True
        )
        help_run = subprocess.run(
            [executable, "exec", "--help"], check=False, capture_output=True, text=True
        )
    except OSError as error:
        return CodexPreflight(False, "unavailable", (str(error),))
    version = version_run.stdout.strip().removeprefix("codex-cli ")
    errors: list[str] = []
    if version_run.returncode != 0:
        errors.append(version_run.stderr.strip() or "codex --version failed")
    elif not version:
        errors.append("codex --version returned no version")
    help_text = help_run.stdout + help_run.stderr
    if help_run.returncode != 0:
        errors.append("codex exec --help failed")
    for flag in REQUIRED_FLAGS:
        if flag not in help_text:
            errors.append(f"Codex CLI is missing required flag {flag}")
    return CodexPreflight(not errors, version, tuple(errors))


def build_command(
    attempt: FixtureAttempt,
    turns: Sequence[str],
    *,
    sandbox: str = "read-only",
    model: str | None = None,
    reasoning_effort: str | None = None,
    executable: str = "codex",
) -> list[str]:
    if sandbox not in SAFE_SANDBOXES:
        raise ValueError(f"release-ineligible sandbox is forbidden: {sandbox}")
    command = [
        executable,
        "exec",
        "--ephemeral",
        "--json",
        "--cd",
        str(attempt.workspace),
        "--sandbox",
        sandbox,
        "--ignore-user-config",
        "--ignore-rules",
    ]
    for feature in DISABLED_DISCOVERY_FEATURES:
        command.extend(["--disable", feature])
    selected_model = model or DEFAULT_TEST_MODEL
    selected_effort = reasoning_effort or DEFAULT_TEST_REASONING_EFFORT
    command.extend(["--model", selected_model])
    command.extend(["--config", f'model_reasoning_effort="{selected_effort}"'])
    command.append("\n\n".join(turns))
    return command


def run_codex(
    attempt: FixtureAttempt,
    turns: Sequence[str],
    *,
    sandbox: str = "read-only",
    model: str | None = None,
    reasoning_effort: str | None = None,
    executable: str = "codex",
    environment: Mapping[str, str] | None = None,
    auth_cache: Path | None = None,
    timeout_seconds: int = 600,
) -> Observation:
    """Run one fresh attempt; adapter/auth/service failures remain inconclusive."""

    before_files = filesystem_manifest(attempt.workspace)
    before_git = git_state(attempt.workspace)
    state_before = checkpoint_state(attempt.workspace)
    preflight = preflight_codex(executable)
    if not preflight.valid:
        return Observation(
            RuntimeStatus(None, "infrastructure-error", preflight.errors),
            (),
            None,
            before_files,
            before_files,
            before_git,
            before_git,
            {"before": state_before, "after": state_before},
            (),
            False,
        )
    command = build_command(
        attempt,
        turns,
        sandbox=sandbox,
        model=model,
        reasoning_effort=reasoning_effort,
        executable=executable,
    )
    process_environment = dict(os.environ)
    if environment:
        process_environment.update(environment)
    process_environment["CODEX_HOME"] = str(attempt.codex_home)
    secrets = tuple(
        value
        for key, value in process_environment.items()
        if any(marker in key.upper() for marker in ("TOKEN", "SECRET", "PASSWORD", "API_KEY"))
    )
    staged_auth: Path | None = None
    try:
        if auth_cache is not None:
            staged_auth = _stage_auth_cache(auth_cache, attempt.codex_home)
        try:
            process = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                env=process_environment,
                timeout=timeout_seconds,
            )
            events, final, terminal, parse_errors, redactions = parse_jsonl_events(
                process.stdout, secrets=secrets
            )
            errors = list(parse_errors[:20])
            if process.stderr.strip():
                stderr = redact_text(process.stderr.strip(), secrets)
                redactions = tuple(sorted(set(redactions) | set(stderr.redactions)))
                bounded_stderr = str(stderr.value)
                if len(bounded_stderr) > 2_000:
                    bounded_stderr = bounded_stderr[:2_000] + "…[truncated]"
                errors.append(bounded_stderr)
            classification = (
                "success"
                if process.returncode == 0 and terminal and not parse_errors
                else "infrastructure-error"
            )
            status = RuntimeStatus(process.returncode, classification, tuple(errors))
        except (OSError, subprocess.TimeoutExpired) as error:
            events, final, terminal, redactions = (), None, False, ()
            status = RuntimeStatus(None, "infrastructure-error", (str(error),))
    finally:
        if staged_auth is not None:
            staged_auth.unlink(missing_ok=True)
    return Observation(
        status,
        events,
        final,
        before_files,
        filesystem_manifest(attempt.workspace),
        before_git,
        git_state(attempt.workspace),
        {"before": state_before, "after": checkpoint_state(attempt.workspace)},
        redactions,
        terminal,
    )
