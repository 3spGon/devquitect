"""Fresh fixture, skill-discovery, configuration, and evidence namespaces."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path

from .models import SkillSnapshot


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
        temporary = tempfile.TemporaryDirectory(prefix="devquitect-attempt-")
        root = Path(temporary.name)
    else:
        parent.mkdir(parents=True, exist_ok=True)
        root = parent / f"attempt-{uuid.uuid4().hex}"
        root.mkdir()
    workspace = root / "workspace"
    shutil.copytree(fixture, workspace, symlinks=True)
    codex_home = root / "codex-home"
    skills_root = codex_home / "skills"
    shutil.copytree(snapshot.snapshot_root / "skills", skills_root, symlinks=True)
    evidence_root = root / "evidence" / uuid.uuid4().hex
    evidence_root.mkdir(parents=True)
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
