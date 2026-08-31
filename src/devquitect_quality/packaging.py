"""Deterministic plugin packaging from immutable Git commits."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .models import SkillSource
from .sources import SourceError, freeze_source

PLUGIN_MANIFEST = ".codex-plugin/plugin.json"
EXPECTED_SKILLS = {
    "project-plan-execution",
    "software-idea-to-project",
    "targeted-refactoring",
}
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
DENIED_PARTS = {".DS_Store", "__pycache__", ".pytest_cache"}
DENIED_SUFFIXES = {".zip", ".tar", ".gz", ".pyc"}


class PackageError(ValueError):
    """A source cannot produce an eligible deterministic plugin package."""


@dataclass(frozen=True, slots=True)
class PackageEntry:
    path: str
    size: int
    mode: str
    sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "size": self.size,
            "mode": self.mode,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class PackageArtifact:
    plugin_name: str
    version: str
    source_commit: str
    snapshot_id: str
    artifact_path: Path
    artifact_digest: str
    entries: tuple[PackageEntry, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "plugin_name": self.plugin_name,
            "version": self.version,
            "source_commit": self.source_commit,
            "snapshot_id": self.snapshot_id,
            "toolchain": "devquitect-quality/0.1.0",
            "entries": [entry.as_dict() for entry in self.entries],
            "artifact_digest": self.artifact_digest,
        }


def _git(repository: Path, *args: str, text: bool = False) -> bytes | str:
    process = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=False,
        capture_output=True,
        text=text,
    )
    if process.returncode != 0:
        error = process.stderr.strip()
        if isinstance(error, bytes):
            error = error.decode("utf-8", errors="replace")
        raise PackageError(error or "Git source resolution failed")
    return process.stdout


def _resolve_commit(repository: Path, selector: str) -> str:
    if selector == "working-tree" or not selector or selector.startswith("-"):
        raise PackageError("release source must be an immutable Git ref, not working-tree")
    root = _git(repository, "rev-parse", "--show-toplevel", text=True).strip()
    if Path(root).resolve() != repository.resolve():
        raise PackageError("release source repository must be the Git top level")
    return _git(repository, "rev-parse", "--verify", f"{selector}^{{commit}}", text=True).strip()


def _safe_path(path: str) -> PurePosixPath:
    relative = PurePosixPath(path)
    allowed = path == PLUGIN_MANIFEST or (
        len(relative.parts) >= 3 and relative.parts[0] == "skills"
    )
    if (
        not path
        or "\x00" in path
        or relative.is_absolute()
        or ".." in relative.parts
        or not allowed
    ):
        raise PackageError(f"unsafe or undeclared package entry: {path!r}")
    if DENIED_PARTS.intersection(relative.parts) or relative.suffix in DENIED_SUFFIXES:
        raise PackageError(f"machine-local or archive input is not packageable: {path}")
    return relative


def _tree_entries(repository: Path, commit: str) -> list[tuple[str, str, bytes]]:
    raw = _git(
        repository,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        commit,
        "--",
        PLUGIN_MANIFEST,
        "skills",
    )
    assert isinstance(raw, bytes)
    entries: list[tuple[str, str, bytes]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        if not separator:
            raise PackageError("Git returned an invalid tree record")
        try:
            mode_bytes, object_type, object_id = metadata.split(b" ", 2)
            path = raw_path.decode("utf-8")
            mode = mode_bytes.decode("ascii")
        except (ValueError, UnicodeDecodeError) as error:
            raise PackageError("Git tree contains an unsupported entry") from error
        _safe_path(path)
        if object_type != b"blob" or mode not in {"100644", "100755"}:
            raise PackageError(f"unsupported package entry: {mode} {path}")
        content = _git(repository, "cat-file", "blob", object_id.decode("ascii"))
        assert isinstance(content, bytes)
        entries.append((path, mode, content))
    return sorted(entries)


def _normalize_manifest(content: bytes, version: str) -> bytes:
    try:
        manifest = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PackageError("plugin manifest must be valid UTF-8 JSON") from error
    if manifest.get("name") != "devquitect" or manifest.get("skills") != "./skills/":
        raise PackageError("plugin manifest must declare devquitect and ./skills/")
    if manifest.get("version") != version:
        raise PackageError(
            f"requested version {version} does not match committed plugin manifest "
            f"version {manifest.get('version')!r}"
        )
    return content


def build_package(repository: Path, selector: str, version: str, output: Path) -> PackageArtifact:
    """Build one normalized ZIP and its deterministic entry manifest."""

    if not SEMVER.fullmatch(version):
        raise PackageError(f"version must be stable semantic version X.Y.Z: {version!r}")
    repository = repository.resolve()
    commit = _resolve_commit(repository, selector)
    source = SkillSource.from_selector(commit, repository)
    try:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="devquitect-package-snapshot-") as temporary:
            snapshot = freeze_source(source, Path(temporary) / "snapshot")
    except SourceError as error:
        raise PackageError(str(error)) from error
    entries = _tree_entries(repository, commit)
    paths = {path for path, _, _ in entries}
    if PLUGIN_MANIFEST not in paths:
        raise PackageError(f"source commit has no {PLUGIN_MANIFEST}")
    skills = {
        PurePosixPath(path).parts[1]
        for path in paths
        if path.startswith("skills/") and path.endswith("/SKILL.md")
    }
    if skills != EXPECTED_SKILLS:
        raise PackageError(
            f"source must contain exactly the declared skills: {sorted(EXPECTED_SKILLS)}"
        )

    normalized: list[tuple[str, str, bytes]] = []
    package_entries: list[PackageEntry] = []
    for path, mode, content in entries:
        if path == PLUGIN_MANIFEST:
            content = _normalize_manifest(content, version)
        normalized.append((path, mode, content))
        package_entries.append(
            PackageEntry(
                path=path,
                size=len(content),
                mode=mode,
                sha256=hashlib.sha256(content).hexdigest(),
            )
        )

    output.mkdir(parents=True, exist_ok=True)
    artifact_path = output / f"devquitect-{version}.zip"
    with zipfile.ZipFile(
        artifact_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path, mode, content in normalized:
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if mode == "100755" else 0o644) << 16
            archive.writestr(info, content, compresslevel=9)
    digest = f"sha256:{hashlib.sha256(artifact_path.read_bytes()).hexdigest()}"
    artifact = PackageArtifact(
        plugin_name="devquitect",
        version=version,
        source_commit=commit,
        snapshot_id=snapshot.snapshot_id,
        artifact_path=artifact_path,
        artifact_digest=digest,
        entries=tuple(package_entries),
    )
    manifest_path = output / f"devquitect-{version}.manifest.json"
    manifest_path.write_text(
        json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return artifact
