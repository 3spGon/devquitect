from __future__ import annotations

import subprocess
from pathlib import Path

from devquitect_quality import SkillSource, freeze_source, thaw_snapshot
from devquitect_quality.fixtures import materialize_attempt


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def make_snapshot(tmp_path: Path):
    repository = tmp_path / "source"
    skill = repository / "skills" / "isolated-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: isolated-skill\ndescription: test\n---\n", encoding="utf-8"
    )
    git(repository, "init", "-q")
    git(repository, "config", "user.name", "Fixture Test")
    git(repository, "config", "user.email", "fixture@example.invalid")
    git(repository, "add", "skills")
    git(repository, "commit", "-qm", "snapshot")
    root = tmp_path / "snapshot"
    return freeze_source(SkillSource.from_selector("HEAD", repository), root), root


def test_attempts_have_independent_workspace_config_skill_and_evidence_namespaces(
    tmp_path: Path,
) -> None:
    snapshot, snapshot_root = make_snapshot(tmp_path)
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "seed.txt").write_text("same", encoding="utf-8")
    try:
        first = materialize_attempt(snapshot, fixture, parent=tmp_path / "attempts")
        second = materialize_attempt(snapshot, fixture, parent=tmp_path / "attempts")
        try:
            (first.workspace / "only-first.txt").write_text("private", encoding="utf-8")
            (first.codex_home / "config.toml").write_text("model='first'", encoding="utf-8")

            assert not (second.workspace / "only-first.txt").exists()
            assert not (second.codex_home / "config.toml").exists()
            assert first.workspace != second.workspace
            assert first.codex_home != second.codex_home
            assert first.skills_root != second.skills_root
            assert first.namespace != second.namespace
        finally:
            first.cleanup()
            second.cleanup()
    finally:
        thaw_snapshot(snapshot_root)
