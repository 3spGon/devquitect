from __future__ import annotations

import json
from pathlib import Path

from devquitect_quality import SkillSource, freeze_source, thaw_snapshot

STABLE_COMMIT = "264f4648ae1e699168347eb8e5945459bfbd0e27"
EXPECTED_SKILLS = {
    "project-plan-execution",
    "software-idea-to-project",
    "targeted-refactoring",
}


def test_recorded_stable_baseline_rebuilds_identically(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[2]
    recorded = json.loads((repository / "baselines/stable-n.json").read_text(encoding="utf-8"))
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first = freeze_source(SkillSource.from_selector(STABLE_COMMIT, repository), first_root)
    second = freeze_source(SkillSource.from_selector(STABLE_COMMIT, repository), second_root)
    try:
        assert first.as_manifest() == second.as_manifest()
        assert recorded["source_commit"] == STABLE_COMMIT
        assert recorded["snapshot"] == first.as_manifest()
        assert recorded["expected_skills"] == sorted(EXPECTED_SKILLS)
        assert {skill.name for skill in first.skills} == EXPECTED_SKILLS
        assert first.release_eligible_source is True
        assert first.working_tree_fingerprint is None
    finally:
        thaw_snapshot(first_root)
        thaw_snapshot(second_root)

