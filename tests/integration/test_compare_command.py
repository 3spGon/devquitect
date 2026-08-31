from __future__ import annotations

import subprocess
from pathlib import Path

from devquitect_quality.comparison import freeze_pair, pair_records
from devquitect_quality.models import SkillSource
from devquitect_quality.sources import thaw_snapshot


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def test_pair_freezes_both_sources_before_candidate_edits_and_uses_distinct_roots(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    skill = repository / "skills/example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: test\n---\n", encoding="utf-8"
    )
    git(repository, "init", "-q")
    git(repository, "config", "user.name", "Compare Test")
    git(repository, "config", "user.email", "compare@example.invalid")
    git(repository, "add", "skills")
    git(repository, "commit", "-qm", "stable")
    pair = freeze_pair(
        SkillSource.from_selector("HEAD", repository),
        SkillSource.from_selector("working-tree", repository),
        tmp_path / "pair",
    )
    try:
        original = pair.candidate.content_digest
        (skill / "SKILL.md").write_text("changed after freeze", encoding="utf-8")
        assert pair.stable.snapshot_root != pair.candidate.snapshot_root
        assert pair.candidate.content_digest == original
        records = pair_records(
            ({"case_id": "self-hosting", "classification": "pass", "critical_failures": []},),
            ({"case_id": "self-hosting", "classification": "pass", "critical_failures": []},),
        )
        assert records[0]["classification"] == "equivalent"
    finally:
        thaw_snapshot(pair.stable.snapshot_root)
        thaw_snapshot(pair.candidate.snapshot_root)
