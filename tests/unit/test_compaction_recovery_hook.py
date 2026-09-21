from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
HOOK = ROOT / "hooks/compaction_recovery.py"


def run_hook(cwd: Path, payload: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        cwd=ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )


def make_repo(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    (tmp_path / "docs/software-design").mkdir(parents=True)
    return tmp_path


def add_checkpoint(
    root: Path, name: str, *, status: str = "active", body: str | None = None
) -> None:
    session = root / "docs/software-design" / name
    session.mkdir()
    content = body or (
        "---\n"
        "schema_version: 3\n"
        "skill: project-plan-execution\n"
        f"session: {name}\n"
        f"delivery_status: {status}\n"
        "plan: 08-implementation-plan.md\n"
        "---\n\n# Delivery checkpoint\n"
    )
    (session / "09-delivery-status.md").write_text(content, encoding="utf-8")


def event(root: Path) -> dict[str, str]:
    return {"hook_event_name": "SessionStart", "source": "compact", "cwd": str(root)}


def test_non_compact_events_are_silent(tmp_path: Path) -> None:
    result = run_hook(make_repo(tmp_path), {**event(tmp_path), "source": "startup"})
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_no_active_checkpoint_is_silent(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    add_checkpoint(root, "completed", status="complete")
    result = run_hook(root, event(root))
    assert result.returncode == 0
    assert result.stdout == ""


def test_one_active_checkpoint_emits_bounded_recovery_context(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    add_checkpoint(root, "delivery")
    result = run_hook(root, event(root))
    payload = json.loads(result.stdout)
    context = payload["hookSpecificOutput"]["additionalContext"]
    assert result.returncode == 0
    assert payload["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    assert "docs/software-design/delivery/09-delivery-status.md" in context
    assert "reconcile" in context
    assert len(result.stdout.encode()) <= 4096
    assert "delivery_status" not in context


def test_hook_config_is_one_synchronous_compact_handler() -> None:
    config = json.loads((ROOT / "hooks/hooks.json").read_text(encoding="utf-8"))
    groups = config["hooks"]["SessionStart"]
    assert len(groups) == 1
    assert groups[0]["matcher"] == "^compact$"
    handlers = groups[0]["hooks"]
    assert len(handlers) == 1
    assert handlers[0] == {
        "type": "command",
        "command": 'python3 "$PLUGIN_ROOT/hooks/compaction_recovery.py"',
        "commandWindows": 'py -3 "%PLUGIN_ROOT%\\hooks\\compaction_recovery.py"',
        "timeout": 10,
        "additionalContextLimit": 1200,
    }
    assert "yaml" not in (ROOT / "hooks/compaction_recovery.py").read_text(encoding="utf-8")


def test_multiple_checkpoints_stop_without_silent_selection(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    add_checkpoint(root, "one")
    add_checkpoint(root, "two")
    result = run_hook(root, event(root))
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert result.returncode == 0
    assert "ambiguous" in context
    assert "one/09-delivery-status.md" in context
    assert "two/09-delivery-status.md" in context


def test_malformed_plausible_checkpoint_is_ambiguous(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    add_checkpoint(
        root,
        "malformed",
        body="---\nskill: project-plan-execution\ndelivery_status: [active]\n---\n",
    )
    result = run_hook(root, event(root))
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert result.returncode == 0
    assert "ambiguous" in context
    assert "malformed/09-delivery-status.md" in context


def test_discovery_does_not_follow_escaping_session_symlink(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    outside = tmp_path / "outside"
    (outside / "docs/software-design").mkdir(parents=True)
    add_checkpoint(outside, "secret")
    (root / "docs/software-design/escape").symlink_to(outside / "docs/software-design/secret")
    result = run_hook(root, event(root))
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert result.returncode == 0
    assert "ambiguous" in context
    assert "escape/09-delivery-status.md" in context
    assert "secret" not in result.stderr


def test_output_reports_omitted_candidates_within_bound(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    for index in range(80):
        add_checkpoint(root, f"delivery-{index:03d}-with-a-long-session-name")
    result = run_hook(root, event(root))
    payload = json.loads(result.stdout)
    context = payload["hookSpecificOutput"]["additionalContext"]
    assert result.returncode == 0
    assert len(result.stdout.encode()) <= 4096
    assert "Omitted" in context


@pytest.mark.parametrize(
    "payload", [None, [], "compact", {"hook_event_name": "SessionStart", "source": "compact"}]
)
def test_invalid_input_fails_without_success_context(tmp_path: Path, payload: object) -> None:
    result = run_hook(make_repo(tmp_path), payload)
    assert result.returncode != 0
    assert result.stdout == ""
    assert "compaction recovery unavailable" in result.stderr
