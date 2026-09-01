from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

import pytest

from devquitect_quality.packaging import PackageError, build_package

SKILLS = ("project-plan-execution", "software-idea-to-project", "targeted-refactoring")


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def package_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    (repository / ".codex-plugin").mkdir(parents=True)
    (repository / ".codex-plugin/plugin.json").write_text(
        '{"name":"devquitect","version":"0.1.0","skills":"./skills/"}\n',
        encoding="utf-8",
    )
    for name in SKILLS:
        skill = repository / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\n---\n", encoding="utf-8"
        )
    git(repository, "init", "-q")
    git(repository, "config", "user.name", "Package Test")
    git(repository, "config", "user.email", "package@example.invalid")
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "baseline input")
    manifest = repository / ".codex-plugin/plugin.json"
    manifest.write_text(
        '{"name":"devquitect","version":"0.2.0","skills":"./skills/"}\n',
        encoding="utf-8",
    )
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "package input")
    return repository


def test_package_is_reproducible_and_contains_only_allowlisted_inputs(tmp_path: Path) -> None:
    repository = package_repository(tmp_path)
    first = build_package(repository, "HEAD", "0.2.0", tmp_path / "first")
    second = build_package(repository, "HEAD", "0.2.0", tmp_path / "second")

    assert first.artifact_digest == second.artifact_digest
    assert first.entries == second.entries
    with zipfile.ZipFile(first.artifact_path) as archive:
        names = archive.namelist()
        assert names == sorted(names)
        assert names[0] == ".codex-plugin/plugin.json"
        assert {Path(name).parts[1] for name in names[1:]} == set(SKILLS)
        assert all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist())


def test_changed_committed_input_changes_artifact_digest(tmp_path: Path) -> None:
    repository = package_repository(tmp_path)
    before = build_package(repository, "HEAD", "0.2.0", tmp_path / "before")
    target = repository / "skills/project-plan-execution/SKILL.md"
    target.write_text(target.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "change input")
    after = build_package(repository, "HEAD", "0.2.0", tmp_path / "after")
    assert before.artifact_digest != after.artifact_digest


def test_package_rejects_working_tree_invalid_semver_and_symlink(tmp_path: Path) -> None:
    repository = package_repository(tmp_path)
    with pytest.raises(PackageError, match="immutable Git ref"):
        build_package(repository, "working-tree", "0.2.0", tmp_path / "working")
    with pytest.raises(PackageError, match="semantic version"):
        build_package(repository, "HEAD", "latest", tmp_path / "version")
    link = repository / "skills/project-plan-execution/escape"
    link.symlink_to("../../../outside")
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "unsafe link")
    with pytest.raises(PackageError, match="symlink escapes|unsupported package entry"):
        build_package(repository, "HEAD", "0.2.0", tmp_path / "link")
