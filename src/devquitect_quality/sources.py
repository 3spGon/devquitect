"""Resolve and freeze Git or working-tree skill sources."""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import shutil
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .models import SkillSnapshot, SkillSource, SnapshotFile, SnapshotSkill

SKILLS_ROOT = "skills"
REQUIRED_SKILL_FILE = "SKILL.md"


class SourceError(ValueError):
    """The selected source cannot produce a safe, identifiable snapshot."""


@dataclass(frozen=True, slots=True)
class _SourceEntry:
    path: str
    mode: str
    content: bytes


def _git(repository: Path, *args: str, text: bool = False) -> bytes | str:
    process = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=False,
        capture_output=True,
        text=text,
    )
    if process.returncode != 0:
        stderr = process.stderr.strip()
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        raise SourceError(stderr or f"git {' '.join(args)} failed")
    return process.stdout


def _ensure_repository(repository: Path) -> None:
    if not repository.is_dir():
        raise SourceError(f"repository does not exist: {repository}")
    result = _git(repository, "rev-parse", "--show-toplevel", text=True).strip()
    if Path(result).resolve() != repository:
        raise SourceError(f"repository root must be the Git top level: {repository}")


def _resolve_commit(repository: Path, selector: str) -> str:
    if not selector or selector.startswith("-"):
        raise SourceError(f"invalid Git selector: {selector!r}")
    return _git(repository, "rev-parse", "--verify", f"{selector}^{{commit}}", text=True).strip()


def _validate_relative_path(path: str) -> PurePosixPath:
    try:
        relative = PurePosixPath(path)
    except ValueError as error:
        raise SourceError(f"invalid source path: {path!r}") from error
    if (
        not path
        or "\x00" in path
        or relative.is_absolute()
        or ".." in relative.parts
        or relative.parts[0] != SKILLS_ROOT
        or len(relative.parts) < 3
    ):
        raise SourceError(f"unsafe or undeclared source path: {path!r}")
    return relative


def _validate_symlink(path: str, target_bytes: bytes) -> str:
    try:
        target = target_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SourceError(f"symlink target is not UTF-8: {path}") from error
    if not target or "\x00" in target or PurePosixPath(target).is_absolute():
        raise SourceError(f"unsafe symlink target for {path}: {target!r}")
    normalized = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
    if normalized != SKILLS_ROOT and not normalized.startswith(f"{SKILLS_ROOT}/"):
        raise SourceError(f"symlink escapes skills root: {path} -> {target}")
    return target


def _git_entries(repository: Path, commit: str) -> list[_SourceEntry]:
    raw = _git(repository, "ls-tree", "-r", "-z", "--full-tree", commit, "--", SKILLS_ROOT)
    assert isinstance(raw, bytes)
    entries: list[_SourceEntry] = []
    for record in raw.split(b"\x00"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        if not separator:
            raise SourceError("Git returned an invalid tree record")
        try:
            mode_bytes, object_type, object_id = metadata.split(b" ", 2)
            path = raw_path.decode("utf-8")
            mode = mode_bytes.decode("ascii")
        except (ValueError, UnicodeDecodeError) as error:
            raise SourceError("Git tree contains an unsupported path or record") from error
        _validate_relative_path(path)
        if object_type != b"blob" or mode not in {"100644", "100755", "120000"}:
            raise SourceError(f"unsupported Git entry: {mode} {path}")
        content = _git(repository, "cat-file", "blob", object_id.decode("ascii"))
        assert isinstance(content, bytes)
        if mode == "120000":
            _validate_symlink(path, content)
        entries.append(_SourceEntry(path=path, mode=mode, content=content))
    return sorted(entries, key=lambda entry: entry.path)


def _working_tree_entries(repository: Path) -> list[_SourceEntry]:
    raw = _git(
        repository,
        "ls-files",
        "-z",
        "--cached",
        "--others",
        "--exclude-standard",
        "--",
        SKILLS_ROOT,
    )
    assert isinstance(raw, bytes)
    paths: set[str] = set()
    for raw_path in raw.split(b"\x00"):
        if not raw_path:
            continue
        try:
            path = raw_path.decode("utf-8")
        except UnicodeDecodeError as error:
            raise SourceError("working tree contains a non-UTF-8 skill path") from error
        _validate_relative_path(path)
        paths.add(path)

    entries: list[_SourceEntry] = []
    for path in sorted(paths):
        source_path = repository.joinpath(*PurePosixPath(path).parts)
        if not os.path.lexists(source_path):
            continue
        file_stat = source_path.lstat()
        if stat.S_ISLNK(file_stat.st_mode):
            target = os.readlink(source_path)
            content = os.fsencode(target)
            _validate_symlink(path, content)
            mode = "120000"
        elif stat.S_ISREG(file_stat.st_mode):
            content = source_path.read_bytes()
            mode = "100755" if file_stat.st_mode & stat.S_IXUSR else "100644"
        else:
            raise SourceError(f"unsupported working-tree entry: {path}")
        entries.append(_SourceEntry(path=path, mode=mode, content=content))
    return entries


def _canonical_digest(records: list[dict[str, object]]) -> str:
    serialized = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _snapshot_files(entries: list[_SourceEntry]) -> tuple[SnapshotFile, ...]:
    return tuple(
        SnapshotFile(
            path=entry.path,
            mode=entry.mode,
            size=len(entry.content),
            sha256=hashlib.sha256(entry.content).hexdigest(),
        )
        for entry in entries
    )


def _snapshot_skills(files: tuple[SnapshotFile, ...]) -> tuple[SnapshotSkill, ...]:
    by_skill: dict[str, list[SnapshotFile]] = {}
    for file in files:
        parts = PurePosixPath(file.path).parts
        by_skill.setdefault(parts[1], []).append(file)

    skills: list[SnapshotSkill] = []
    for name, skill_files in sorted(by_skill.items()):
        root = f"{SKILLS_ROOT}/{name}"
        required_path = f"{root}/{REQUIRED_SKILL_FILE}"
        if required_path not in {file.path for file in skill_files}:
            raise SourceError(f"skill has no {REQUIRED_SKILL_FILE}: {name}")
        records = [
            {
                **file.as_dict(),
                "path": str(PurePosixPath(file.path).relative_to(root)),
            }
            for file in skill_files
        ]
        skills.append(
            SnapshotSkill(
                name=name,
                path=root,
                content_digest=_canonical_digest(records),
                files=tuple(file.path for file in skill_files),
            )
        )
    if not skills:
        raise SourceError("source contains no skills")
    return tuple(skills)


def _prepare_destination(destination: Path) -> None:
    if destination.exists():
        if not destination.is_dir() or any(destination.iterdir()):
            raise SourceError(f"snapshot destination must be absent or empty: {destination}")
    else:
        destination.mkdir(parents=True)


def _materialize(entries: list[_SourceEntry], destination: Path) -> None:
    _prepare_destination(destination)
    for entry in entries:
        relative = _validate_relative_path(entry.path)
        output = destination.joinpath(*relative.parts)
        output.parent.mkdir(parents=True, exist_ok=True)
        if entry.mode == "120000":
            target = _validate_symlink(entry.path, entry.content)
            output.symlink_to(target)
        else:
            output.write_bytes(entry.content)
            output.chmod(0o555 if entry.mode == "100755" else 0o444)
    directories = sorted(
        (path for path in destination.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        directory.chmod(0o555)
    destination.chmod(0o555)


def freeze_source(source: SkillSource, destination: Path | str) -> SkillSnapshot:
    """Freeze declared skill inputs into a content-addressed read-only snapshot."""

    repository = source.repository_root.resolve()
    _ensure_repository(repository)
    commit_selector = "HEAD" if source.kind == "working-tree" else source.selector
    resolved_commit = _resolve_commit(repository, commit_selector)

    if source.kind == "working-tree":
        entries = _working_tree_entries(repository)
        dirty = bool(
            _git(
                repository,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                SKILLS_ROOT,
            )
        )
        release_eligible = False
    elif source.kind == "git-ref":
        entries = _git_entries(repository, resolved_commit)
        dirty = False
        release_eligible = True
    else:
        raise SourceError(f"unsupported source kind: {source.kind}")

    files = _snapshot_files(entries)
    skills = _snapshot_skills(files)
    file_records = [file.as_dict() for file in files]
    content_digest = _canonical_digest(file_records)
    snapshot_root = Path(destination).resolve()
    _materialize(entries, snapshot_root)
    return SkillSnapshot(
        snapshot_root=snapshot_root,
        source_kind=source.kind,
        source_selector=source.selector,
        resolved_commit=resolved_commit,
        dirty=dirty,
        release_eligible_source=release_eligible,
        content_digest=content_digest,
        snapshot_id=f"sha256:{content_digest}",
        working_tree_fingerprint=content_digest if source.kind == "working-tree" else None,
        files=files,
        skills=skills,
    )


def thaw_snapshot(snapshot_root: Path | str) -> None:
    """Restore owner-write permissions so a temporary snapshot can be removed."""

    root = Path(snapshot_root)
    if not os.path.lexists(root):
        return
    if root.is_symlink() or not root.is_dir():
        raise SourceError(f"snapshot root is not a directory: {root}")
    root.chmod(0o755)
    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        path.chmod(0o755 if path.is_dir() else 0o644)


def remove_snapshot(snapshot_root: Path | str) -> None:
    """Remove a temporary snapshot after restoring cleanup permissions."""

    root = Path(snapshot_root)
    thaw_snapshot(root)
    shutil.rmtree(root)
