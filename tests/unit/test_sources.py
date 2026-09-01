from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

import pytest

from devquitect_quality import SkillSource, SourceError, freeze_source, thaw_snapshot


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def create_repository(root: Path) -> tuple[Path, str]:
    repository = root / "repository"
    repository.mkdir()
    git(repository, "init", "-q")
    git(repository, "config", "user.name", "Snapshot Test")
    git(repository, "config", "user.email", "snapshot@example.invalid")
    skill = repository / "skills" / "example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: example\n---\n", encoding="utf-8")
    (skill / "reference.md").write_text("stable\n", encoding="utf-8")
    git(repository, "add", "skills")
    git(repository, "commit", "-qm", "stable skill")
    return repository, git(repository, "rev-parse", "HEAD")


def test_git_snapshot_is_immutable_and_content_addressed(tmp_path: Path) -> None:
    repository, commit = create_repository(tmp_path)
    destination = tmp_path / "snapshot"
    snapshot = freeze_source(SkillSource.from_selector(commit, repository), destination)
    try:
        assert snapshot.resolved_commit == commit
        assert snapshot.release_eligible_source is True
        assert snapshot.dirty is False
        assert snapshot.snapshot_id == f"sha256:{snapshot.content_digest}"
        assert [skill.name for skill in snapshot.skills] == ["example"]
        assert not stat.S_IMODE(destination.stat().st_mode) & stat.S_IWUSR
        skill_mode = (destination / "skills/example/SKILL.md").stat().st_mode
        assert not stat.S_IMODE(skill_mode) & stat.S_IWUSR

        (repository / "skills/example/reference.md").write_text("candidate\n", encoding="utf-8")
        frozen_reference = destination / "skills/example/reference.md"
        assert frozen_reference.read_text(encoding="utf-8") == "stable\n"
        second_destination = tmp_path / "second-snapshot"
        second = freeze_source(SkillSource.from_selector(commit, repository), second_destination)
        try:
            assert second.content_digest == snapshot.content_digest
            assert second.as_manifest() == snapshot.as_manifest()
        finally:
            thaw_snapshot(second_destination)
    finally:
        thaw_snapshot(destination)


def test_working_tree_snapshot_is_always_diagnostic(tmp_path: Path) -> None:
    repository, _ = create_repository(tmp_path)
    clean_destination = tmp_path / "clean-candidate"
    clean = freeze_source(
        SkillSource.from_selector("working-tree", repository), clean_destination
    )
    try:
        assert clean.dirty is False
        assert clean.release_eligible_source is False
        assert clean.working_tree_fingerprint == clean.content_digest
    finally:
        thaw_snapshot(clean_destination)

    (repository / "skills/example/reference.md").write_text("candidate\n", encoding="utf-8")
    dirty_destination = tmp_path / "dirty-candidate"
    snapshot = freeze_source(
        SkillSource.from_selector("working-tree", repository), dirty_destination
    )
    try:
        assert snapshot.source_kind == "working-tree"
        assert snapshot.dirty is True
        assert snapshot.release_eligible_source is False
        assert snapshot.working_tree_fingerprint == snapshot.content_digest
    finally:
        thaw_snapshot(dirty_destination)


def test_rejects_missing_ref_and_nonempty_destination(tmp_path: Path) -> None:
    repository, commit = create_repository(tmp_path)
    with pytest.raises(SourceError, match="unknown revision|Needed a single revision"):
        freeze_source(SkillSource.from_selector("missing-ref", repository), tmp_path / "missing")

    destination = tmp_path / "occupied"
    destination.mkdir()
    (destination / "keep").write_text("user data", encoding="utf-8")
    with pytest.raises(SourceError, match="absent or empty"):
        freeze_source(SkillSource.from_selector(commit, repository), destination)
    assert (destination / "keep").read_text(encoding="utf-8") == "user data"


@pytest.mark.skipif(os.name == "nt", reason="symlink setup differs on Windows")
def test_rejects_symlink_escaping_skills_root(tmp_path: Path) -> None:
    repository, _ = create_repository(tmp_path)
    link = repository / "skills/example/escape"
    link.symlink_to("../../../outside")
    git(repository, "add", "skills/example/escape")
    git(repository, "commit", "-qm", "unsafe symlink")

    with pytest.raises(SourceError, match="symlink escapes skills root"):
        freeze_source(SkillSource.from_selector("HEAD", repository), tmp_path / "snapshot")
