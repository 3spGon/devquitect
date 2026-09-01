from __future__ import annotations

import os
import subprocess
from pathlib import Path

from devquitect_quality import SkillSource, freeze_source, thaw_snapshot
from devquitect_quality.assertions import evaluate_assertion
from devquitect_quality.codex_adapter import run_codex
from devquitect_quality.fixtures import materialize_attempt


def git(repository: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repository), *args], check=True, capture_output=True)


def snapshot(tmp_path: Path):
    repository = tmp_path / "source"
    skill = repository / "skills" / "example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: example\n---\n", encoding="utf-8"
    )
    git(repository, "init", "-q")
    git(repository, "config", "user.name", "Test")
    git(repository, "config", "user.email", "test@example.invalid")
    git(repository, "add", "skills")
    git(repository, "commit", "-qm", "source")
    snapshot_root = tmp_path / "snapshot"
    return freeze_source(
        SkillSource.from_selector("HEAD", repository), snapshot_root
    ), snapshot_root


def fake_codex(path: Path) -> Path:
    path.write_text(
        """#!/usr/bin/env python3
import json, os, pathlib, sys
if '--version' in sys.argv:
    print('codex-cli 0.139.0')
elif '--help' in sys.argv:
    print('--ephemeral --json --cd --sandbox --ignore-user-config --ignore-rules')
else:
    workspace = pathlib.Path(sys.argv[sys.argv.index('--cd') + 1])
    assert (pathlib.Path(os.environ['CODEX_HOME']) / 'auth.json').is_file()
    (workspace / 'unexpected.txt').write_text('write despite read-only')
    print(json.dumps({'type': 'thread.started', 'thread_id': 'fake'}))
    print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'done'}}))
    print(json.dumps({'type': 'turn.completed'}))
    print('api_key=supersecretvalue' + 'x' * 3000, file=sys.stderr)
""",
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


def test_fake_adapter_run_is_normalized_and_read_only_violation_fails(tmp_path: Path) -> None:
    source, snapshot_root = snapshot(tmp_path)
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "README.md").write_text("fixture", encoding="utf-8")
    executable = fake_codex(tmp_path / "fake-codex")
    auth_cache = tmp_path / "auth.json"
    auth_cache.write_text('{"tokens":"not-a-real-secret"}', encoding="utf-8")
    auth_cache.chmod(0o600)
    try:
        with materialize_attempt(source, fixture) as attempt:
            observation = run_codex(
                attempt,
                ["Inspect only"],
                sandbox="read-only",
                executable=os.fspath(executable),
                auth_cache=auth_cache,
            )
            assertion = evaluate_assertion({"type": "allowed-paths", "paths": []}, observation)
        assert observation.runtime_status.classification == "success"
        assert observation.final_response == "done"
        assert all("supersecretvalue" not in error for error in observation.runtime_status.errors)
        assert len(observation.runtime_status.errors[-1]) < 2_100
        assert observation.redactions
        assert assertion.status == "fail"
        assert "unexpected.txt" in assertion.observed["violations"]
        assert not (attempt.codex_home / "auth.json").exists()
    finally:
        thaw_snapshot(snapshot_root)
