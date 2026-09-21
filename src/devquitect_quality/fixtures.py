"""Fresh fixture, skill-discovery, configuration, and evidence namespaces."""

from __future__ import annotations

import json
import math
import os
import shutil
import stat
import subprocess
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from .models import SkillSnapshot

ATTEMPT_MARKER = ".devquitect-attempt.json"
DEFAULT_STALE_AGE_SECONDS = 660


def _owned_by_current_user(path: Path) -> bool:
    getuid = getattr(os, "getuid", None)
    return getuid is None or path.stat().st_uid == getuid()


def _secure_directory(path: Path) -> None:
    path.chmod(0o700)
    if not _owned_by_current_user(path) or stat.S_IMODE(path.stat().st_mode) & 0o077:
        raise ValueError(f"temporary attempt directory is not owner-only: {path}")


def _write_attempt_marker(root: Path) -> None:
    marker = root / ATTEMPT_MARKER
    payload = {
        "schema_version": 1,
        "attempt_id": root.name,
        "pid": os.getpid(),
        "created_at": time.time(),
    }
    descriptor = os.open(
        marker,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            json.dump(payload, handle, sort_keys=True)
            handle.write("\n")
    finally:
        if descriptor != -1:
            os.close(descriptor)
    marker.chmod(0o600)


def _process_is_live(pid: int) -> bool:
    if pid <= 0:
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True


def cleanup_stale_attempts(
    parent: Path, *, max_age_seconds: float = DEFAULT_STALE_AGE_SECONDS, now: float | None = None
) -> tuple[Path, ...]:
    """Remove only expired, marked, owned, non-live attempt roots."""

    parent = Path(parent)
    try:
        parent_stat = parent.lstat()
    except OSError:
        return ()
    if not stat.S_ISDIR(parent_stat.st_mode) or parent.is_symlink():
        return ()
    current_time = time.time() if now is None else now
    removed: list[Path] = []
    try:
        entries = tuple(parent.iterdir())
    except OSError:
        return ()
    for root in entries:
        if not root.name.startswith(("attempt-", "devquitect-attempt-")):
            continue
        try:
            root_stat = root.lstat()
            marker = root / ATTEMPT_MARKER
            marker_stat = marker.lstat()
            if (
                root.is_symlink()
                or not stat.S_ISDIR(root_stat.st_mode)
                or not _owned_by_current_user(root)
                or stat.S_IMODE(root_stat.st_mode) & 0o077
                or marker.is_symlink()
                or not stat.S_ISREG(marker_stat.st_mode)
                or not _owned_by_current_user(marker)
                or stat.S_IMODE(marker_stat.st_mode) & 0o077
            ):
                continue
            payload = json.loads(marker.read_text(encoding="utf-8"))
            created_at = payload.get("created_at")
            pid = payload.get("pid")
            if (
                payload.get("schema_version") != 1
                or payload.get("attempt_id") != root.name
                or not isinstance(created_at, (int, float))
                or isinstance(created_at, bool)
                or not math.isfinite(created_at)
                or not isinstance(pid, int)
                or isinstance(pid, bool)
                or pid <= 0
                or current_time - created_at <= max_age_seconds
                or current_time < created_at
                or _process_is_live(pid)
            ):
                continue
            shutil.rmtree(root)
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            continue
        removed.append(root)
    return tuple(removed)


@dataclass(slots=True)
class FixtureAttempt:
    root: Path
    workspace: Path
    codex_home: Path
    skills_root: Path
    evidence_root: Path
    namespace: str
    _temporary: tempfile.TemporaryDirectory[str] | None = None

    def cleanup(self) -> None:
        if self._temporary is not None:
            self._temporary.cleanup()
            self._temporary = None
        elif self.root.exists() and not self.root.is_symlink():
            shutil.rmtree(self.root)

    def __enter__(self) -> FixtureAttempt:
        return self

    def __exit__(self, *_: object) -> None:
        self.cleanup()


def _initialize_git(workspace: Path) -> None:
    subprocess.run(["git", "-C", str(workspace), "init", "-q"], check=True)
    subprocess.run(
        ["git", "-C", str(workspace), "config", "user.name", "Devquitect Fixture"], check=True
    )
    subprocess.run(
        ["git", "-C", str(workspace), "config", "user.email", "fixture@example.invalid"], check=True
    )
    subprocess.run(["git", "-C", str(workspace), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(workspace), "commit", "--allow-empty", "-qm", "fixture baseline"],
        check=True,
    )


def materialize_attempt(
    snapshot: SkillSnapshot,
    fixture: Path,
    *,
    parent: Path | None = None,
    initialize_git: bool = True,
) -> FixtureAttempt:
    """Create one isolated attempt. The caller owns cleanup unless used as a context manager."""

    if not fixture.is_dir():
        raise ValueError(f"fixture directory does not exist: {fixture}")
    temporary: tempfile.TemporaryDirectory[str] | None = None
    if parent is None:
        cleanup_stale_attempts(Path(tempfile.gettempdir()))
        temporary = tempfile.TemporaryDirectory(prefix="devquitect-attempt-")
        root = Path(temporary.name)
    else:
        parent.mkdir(parents=True, exist_ok=True)
        _secure_directory(parent)
        cleanup_stale_attempts(parent)
        root = parent / f"attempt-{uuid.uuid4().hex}"
        root.mkdir(mode=0o700)
    try:
        _secure_directory(root)
        _write_attempt_marker(root)
        workspace = root / "workspace"
        shutil.copytree(fixture, workspace, symlinks=True)
        codex_home = root / "codex-home"
        codex_home.mkdir(mode=0o700)
        skills_root = codex_home / "skills"
        shutil.copytree(snapshot.snapshot_root / "skills", skills_root, symlinks=True)
        skills_root.chmod(0o700)
        for directory in skills_root.rglob("*"):
            if directory.is_dir() and not directory.is_symlink():
                directory.chmod(0o700)
        evidence_root = root / "evidence" / uuid.uuid4().hex
        evidence_root.mkdir(parents=True, mode=0o700)
        if initialize_git:
            _initialize_git(workspace)
        return FixtureAttempt(
            root=root,
            workspace=workspace,
            codex_home=codex_home,
            skills_root=skills_root,
            evidence_root=evidence_root,
            namespace=evidence_root.name,
            _temporary=temporary,
        )
    except BaseException:
        if temporary is not None:
            temporary.cleanup()
        elif root.exists() and not root.is_symlink():
            shutil.rmtree(root)
        raise
