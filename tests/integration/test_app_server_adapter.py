from __future__ import annotations

from pathlib import Path

from devquitect_quality.app_server_adapter import run_app_server
from devquitect_quality.fixtures import materialize_attempt
from devquitect_quality.models import SkillSource
from devquitect_quality.sources import freeze_source
from devquitect_quality.validate import load_validation_inputs

ROOT = Path(__file__).parents[2]
SCENARIO = {
    "version": 1,
    "steps": [{"prompt": "inspect"}, {"compact": {}}, {"prompt": "continue"}],
}


def _fake_codex(path: Path) -> Path:
    path.write_text(
        """#!/usr/bin/env python3
import json
import os
import sys

mode = os.environ.get('FAKE_MODE', '')
log = os.environ.get('FAKE_LOG')
if len(sys.argv) > 1 and sys.argv[1] == 'plugin':
    if log:
        with open(log, 'a', encoding='utf-8') as handle:
            handle.write(' '.join(sys.argv[1:]) + '\\n')
    if mode == 'setup-failure':
        print(os.environ.get('FAKE_SECRET', 'setup failure'), file=sys.stderr)
        raise SystemExit(7)
    raise SystemExit(0)

def emit(value):
    sys.stdout.write(json.dumps(value) + '\\n')
    sys.stdout.flush()

for line in sys.stdin:
    message = json.loads(line)
    method = message.get('method')
    if method == 'initialize':
        emit({'id': message['id'], 'result': {}})
    elif method == 'thread/start':
        emit({'id': message['id'], 'result': {'thread': {'id': 'thr-test'}}})
    elif method == 'turn/start':
        emit({'id': message['id'], 'result': {'turn': {'id': 'turn-test'}}})
        emit({'method': 'item/completed', 'params': {'threadId': 'thr-test', 'item': {
            'type': 'agent_message', 'text': 'continued'}}})
        emit({'method': 'turn/completed', 'params': {
            'threadId': 'thr-test', 'turn': {'id': 'turn-test'}}})
    elif method == 'thread/compact/start':
        emit({'id': message['id'], 'result': {}})
        if mode == 'timeout':
            continue
        if mode == 'malformed':
            sys.stdout.write('not-json\\n')
            sys.stdout.flush()
            continue
        thread_id = 'wrong-thread' if mode == 'wrong-thread' else 'thr-test'
        item = {'id': 'compact-test', 'type': 'contextCompaction', 'status': 'inProgress'}
        emit({'method': 'item/started', 'params': {'threadId': thread_id, 'item': item}})
        item['status'] = 'completed'
        emit({'method': 'item/completed', 'params': {'threadId': thread_id, 'item': item}})
        emit({'method': 'turn/completed', 'params': {
            'threadId': thread_id, 'turn': {'id': 'compact-turn'}}})
""",
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


def _run(tmp_path: Path, *, mode: str = ""):
    tmp_path.mkdir(parents=True, exist_ok=True)
    source = SkillSource.from_selector("working-tree", ROOT)
    inputs = load_validation_inputs(source)
    snapshot = freeze_source(source, tmp_path / "snapshot")
    fake = _fake_codex(tmp_path / "fake-codex")
    environment = {"FAKE_MODE": mode, "FAKE_LOG": str(tmp_path / "commands.log")}
    with materialize_attempt(snapshot, ROOT / "evals/fixtures/compaction-recovery") as attempt:
        return run_app_server(
            attempt,
            SCENARIO,
            snapshot=snapshot,
            validation_inputs=inputs,
            executable=str(fake),
            timeout_seconds=1,
            environment=environment,
        )


def test_app_server_protocol_orders_prompts_and_compaction_and_cleans_up(tmp_path: Path) -> None:
    observation = _run(tmp_path)

    assert observation.runtime_status.classification == "success"
    assert observation.terminal_event_seen
    assert observation.persistent_state["compaction_count"] == 1
    assert {
        event.detail["item_id"]
        for event in observation.events
        if event.category == "compaction"
    } == {"compact-test"}
    assert observation.final_response == "continued"
    commands = (tmp_path / "commands.log").read_text(encoding="utf-8").splitlines()
    assert len(commands) == 2
    assert "marketplace add" in commands[0]
    assert "plugin add" in commands[1]


def test_app_server_rejects_wrong_thread_timeout_and_malformed_messages(tmp_path: Path) -> None:
    for index, mode in enumerate(("wrong-thread", "timeout", "malformed")):
        observation = _run(tmp_path / str(index), mode=mode)
        assert observation.runtime_status.classification == "infrastructure-error"
        assert observation.runtime_status.errors


def test_plugin_setup_failure_is_redacted(tmp_path: Path) -> None:
    secret = "setup-secret-value"
    source = SkillSource.from_selector("working-tree", ROOT)
    inputs = load_validation_inputs(source)
    snapshot = freeze_source(source, tmp_path / "snapshot")
    fake = _fake_codex(tmp_path / "fake-codex")
    with materialize_attempt(snapshot, ROOT / "evals/fixtures/compaction-recovery") as attempt:
        observation = run_app_server(
            attempt,
            SCENARIO,
            snapshot=snapshot,
            validation_inputs=inputs,
            executable=str(fake),
            timeout_seconds=1,
            environment={"FAKE_MODE": "setup-failure", "FAKE_SECRET": secret},
        )

    assert observation.runtime_status.classification == "infrastructure-error"
    assert secret not in " ".join(observation.runtime_status.errors)
