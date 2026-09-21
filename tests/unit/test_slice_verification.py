from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

import yaml

SCRIPT = Path(__file__).parents[2] / "skills/project-plan-execution/scripts/verify_slice.py"


def run(repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], cwd=repository, capture_output=True, text=True
    )


def make_session(tmp_path: Path, *, status: str = "in-progress") -> tuple[Path, dict]:
    repository = tmp_path / "repo"
    session = repository / "docs/software-design/demo"
    (repository / "src").mkdir(parents=True)
    session.mkdir(parents=True)
    (repository / "src/input.txt").write_text("stable\n", encoding="utf-8")
    (session / "08-implementation-plan.md").write_text(
        """# Plan

Status: Approved
Plan revision: 1

## SLICE-001 — Demo

```devquitect-verification
schema_version: 1
slices:
  SLICE-001:
    depends_on: []
    criteria:
      AC-001:
        text: works
        requirement: REQ-001
    checks:
      CHECK-001:
        command: python -c pass
        cwd: .
    inputs:
      - src
```
""",
        encoding="utf-8",
    )
    (session / "00-status.md").write_text(
        "---\nphase: complete\nphase_status: complete\ngate_1: approved\ngate_2: approved\n---\n",
        encoding="utf-8",
    )
    tracker = """---
schema_version: 3
session: demo
revision: 3
plan_revision: 1
authorized_slices: [SLICE-001]
delivery_status: active
current_slice: SLICE-001
next_action: test
pending_user_action: null
execution_frontier:
  last_completed: []
  in_progress:
    action: test
    paths:
      - src/input.txt
  do_not_repeat: []
  pending_verification:
    - python -c pass
slices:
  SLICE-001:
    status: STATUS
    acceptance: not-required
ownership:
  state: held
---

# Delivery checkpoint

Keep this body.
""".replace("STATUS", status)
    (session / "09-delivery-status.md").write_text(tracker, encoding="utf-8")
    subprocess.run(["git", "-C", str(repository), "init", "-q"], check=True)
    snapshot = json.loads(
        run(repository, "snapshot", "--session", str(session), "--slice", "SLICE-001").stdout
    )
    return session, snapshot


def set_tracker_version(session: Path, version: int, *, delivery_status: str = "active") -> None:
    tracker = session / "09-delivery-status.md"
    text = tracker.read_text(encoding="utf-8")
    text = text.replace("schema_version: 3", f"schema_version: {version}")
    text = text.replace("delivery_status: active", f"delivery_status: {delivery_status}")
    tracker.write_text(text, encoding="utf-8")


def write_detail(
    session: Path, snapshot: dict, *, status: str = "PASS", plan_revision: int = 1
) -> None:
    detail = {
        "schema_version": 1,
        "session": "demo",
        "slice": "SLICE-001",
        "plan_revision": plan_revision,
        "plan_digest": sha256((session / "08-implementation-plan.md").read_bytes()).hexdigest(),
        "verified_at": "2026-09-14T21:00:00Z",
        "inputs_digest": snapshot["inputs_digest"],
        "environment": {"python": sys.version.split()[0]},
        "criteria": {
            "AC-001": {
                "action": "run",
                "expected": "works",
                "method": "test",
                "observed": "observed",
                "status": status,
                "evidence": "CHECK-001",
            }
        },
        "checks": {
            "CHECK-001": {
                "command": "python -c pass",
                "cwd": ".",
                "started_at": "2026-09-14T21:00:00Z",
                "finished_at": "2026-09-14T21:00:01Z",
                "exit_code": 0,
                "status": status,
                "observed": "passed" if status == "PASS" else "failed",
                "inputs_before": snapshot["inputs_digest"],
                "inputs_after": snapshot["inputs_digest"],
            }
        },
    }
    (session / "slices").mkdir()
    (session / "slices/SLICE-001.md").write_text(
        "---\n" + yaml.safe_dump(detail, sort_keys=False) + "---\n\nEvidence.\n", encoding="utf-8"
    )


def test_snapshot_and_check_accept_valid_detail(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot)
    result = run(session.parents[2], "check", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 0, result.stderr + result.stdout
    assert json.loads(result.stdout)["result"] == "PASS"


def test_snapshot_rejects_plan_slice_missing_from_inventory(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    plan = session / "08-implementation-plan.md"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace(
            "```devquitect-verification", "## SLICE-002 — Omitted\n\n```devquitect-verification"
        ),
        encoding="utf-8",
    )
    result = run(session.parents[2], "snapshot", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 2
    assert "plan slice inventory mismatch" in result.stdout
    assert "missing from inventory: SLICE-002" in result.stdout


def test_check_rejects_stale_inputs_and_fail_evidence(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot, status="FAIL")
    before = (session / "09-delivery-status.md").read_bytes()
    (session.parents[2] / "src/input.txt").write_text("changed\n", encoding="utf-8")
    result = run(session.parents[2], "check", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 1
    assert "criteria.unsatisfied" in result.stdout and "evidence.stale" in result.stdout
    assert (session / "09-delivery-status.md").read_bytes() == before


def test_close_is_atomic_and_preserves_body_then_is_idempotent(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot)
    repository = session.parents[2]
    before = (session / "09-delivery-status.md").read_bytes()
    bad = run(
        repository,
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "2",
    )
    assert bad.returncode == 2 and (session / "09-delivery-status.md").read_bytes() == before
    good = run(
        repository,
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "3",
    )
    assert good.returncode == 0, good.stderr + good.stdout
    closed = (session / "09-delivery-status.md").read_text(encoding="utf-8")
    assert "status: verified" in closed and "Keep this body." in closed
    assert closed.count("devquitect:slice-close:start") == 1
    second = run(
        repository,
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "4",
    )
    assert (
        second.returncode == 0
        and (session / "09-delivery-status.md").read_text(encoding="utf-8") == closed
    )


def test_duplicate_yaml_is_rejected_without_writing(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    plan = session / "08-implementation-plan.md"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace(
            "schema_version: 1", "schema_version: 1\nschema_version: 1"
        ),
        encoding="utf-8",
    )
    result = run(session.parents[2], "snapshot", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 2 and "duplicate YAML key" in result.stdout


def test_close_requires_approved_gates_and_non_pending_acceptance(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot)
    (session / "00-status.md").write_text(
        "---\nphase: complete\nphase_status: complete\ngate_1: pending\ngate_2: approved\n---\n",
        encoding="utf-8",
    )
    tracker = session / "09-delivery-status.md"
    before = tracker.read_bytes()
    tracker.write_text(
        tracker.read_text(encoding="utf-8").replace(
            "acceptance: not-required", "acceptance: pending"
        ),
        encoding="utf-8",
    )
    before = tracker.read_bytes()
    result = run(
        session.parents[2],
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "3",
    )
    assert result.returncode == 1
    assert "definition.gate_1" in result.stdout and "acceptance.pending" in result.stdout
    assert tracker.read_bytes() == before


def test_check_requires_complete_criterion_and_check_evidence(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot)
    detail = session / "slices/SLICE-001.md"
    text = detail.read_text(encoding="utf-8")
    for field in ("action", "expected", "method", "evidence", "started_at", "finished_at"):
        text = text.replace(f"{field}: ", f"omitted_{field}: ")
    detail.write_text(text, encoding="utf-8")
    result = run(session.parents[2], "check", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 1
    assert "criteria.unsatisfied" in result.stdout and "check.evidence" in result.stdout


def test_plan_revision_is_read_from_approved_plan(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    plan = session / "08-implementation-plan.md"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace("Plan revision: 1", "Plan revision: 2"),
        encoding="utf-8",
    )
    tracker = session / "09-delivery-status.md"
    tracker.write_text(
        tracker.read_text(encoding="utf-8").replace("plan_revision: 1", "plan_revision: 2"),
        encoding="utf-8",
    )
    snapshot = json.loads(
        run(
            session.parents[2], "snapshot", "--session", str(session), "--slice", "SLICE-001"
        ).stdout
    )
    write_detail(session, snapshot, plan_revision=2)
    result = run(session.parents[2], "check", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 0, result.stderr + result.stdout


def test_symlinked_input_directory_is_rejected(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    repository = session.parents[2]
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret", encoding="utf-8")
    (repository / "link").symlink_to(outside, target_is_directory=True)
    plan = session / "08-implementation-plan.md"
    plan.write_text(plan.read_text(encoding="utf-8").replace("- src", "- link"), encoding="utf-8")
    result = run(repository, "snapshot", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 2 and "symlinks are unsupported" in result.stdout


def test_close_rejects_tracker_change_at_atomic_write(tmp_path: Path, monkeypatch) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot)
    spec = importlib.util.spec_from_file_location("verify_slice", SCRIPT)
    assert spec and spec.loader
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    original = verifier._replace_atomic

    def race(path: Path, content: bytes, expected: bytes | None = None) -> None:
        path.write_bytes(path.read_bytes() + b"\nexternal change\n")
        original(path, content, expected=expected)

    monkeypatch.setattr(verifier, "_replace_atomic", race)
    result, code = verifier._close(session, "SLICE-001", 3)
    assert code == 2 and result["result"] == "UNSUPPORTED"
    assert "revision.conflict" in json.dumps(result)
    assert "external change" in (session / "09-delivery-status.md").read_text(encoding="utf-8")


def test_active_legacy_operations_require_migration_without_writing(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    set_tracker_version(session, 2)
    repository = session.parents[2]
    before = (session / "09-delivery-status.md").read_bytes()
    for operation in ("snapshot", "check"):
        result = run(repository, operation, "--session", str(session), "--slice", "SLICE-001")
        assert result.returncode == 2
        assert "tracker.migration-required" in result.stdout
        assert (session / "09-delivery-status.md").read_bytes() == before
    result = run(
        repository,
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "3",
    )
    assert result.returncode == 2 and "tracker.migration-required" in result.stdout
    assert (session / "09-delivery-status.md").read_bytes() == before


def test_completed_legacy_checkpoint_remains_readable_and_unchanged(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path, status="verified")
    write_detail(session, snapshot)
    set_tracker_version(session, 2, delivery_status="complete")
    repository = session.parents[2]
    before = (session / "09-delivery-status.md").read_bytes()
    result = run(repository, "check", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 0
    result = run(
        repository,
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "3",
    )
    assert result.returncode == 0
    assert (session / "09-delivery-status.md").read_bytes() == before


def test_unknown_tracker_version_is_unsupported_without_writing(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    set_tracker_version(session, 99)
    tracker = session / "09-delivery-status.md"
    before = tracker.read_bytes()
    result = run(session.parents[2], "snapshot", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 2 and "tracker.schema-unsupported" in result.stdout
    assert tracker.read_bytes() == before


def test_v3_frontier_rejects_invalid_and_duplicate_paths(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    tracker = session / "09-delivery-status.md"
    text = tracker.read_text(encoding="utf-8").replace(
        "- src/input.txt",
        "- ../outside\n      - src/input.txt\n      - src/input.txt",
    )
    tracker.write_text(text, encoding="utf-8")
    result = run(session.parents[2], "snapshot", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 2
    assert result.stdout.count("tracker.frontier-invalid") >= 2
    assert tracker.read_text(encoding="utf-8") == text


def test_v3_frontier_requires_typed_fields_and_action_for_partial_work(tmp_path: Path) -> None:
    session, _ = make_session(tmp_path)
    tracker = session / "09-delivery-status.md"
    text = tracker.read_text(encoding="utf-8").replace(
        "last_completed: []", "last_completed: wrong"
    ).replace(
        "    action: test", "    action: ''"
    )
    tracker.write_text(text, encoding="utf-8")
    result = run(session.parents[2], "check", "--session", str(session), "--slice", "SLICE-001")
    assert result.returncode == 2
    assert "tracker.frontier-invalid" in result.stdout


def test_v3_close_clears_frontier_and_preserves_unknown_data(tmp_path: Path) -> None:
    session, snapshot = make_session(tmp_path)
    write_detail(session, snapshot)
    tracker = session / "09-delivery-status.md"
    text = tracker.read_text(encoding="utf-8").replace(
        "ownership:\n  state: held", "ownership:\n  state: held\nunknown_field: preserve-me"
    )
    tracker.write_text(text, encoding="utf-8")
    result = run(
        session.parents[2],
        "close",
        "--session",
        str(session),
        "--slice",
        "SLICE-001",
        "--expected-revision",
        "3",
    )
    assert result.returncode == 0, result.stderr + result.stdout
    closed = yaml.safe_load(
        (session / "09-delivery-status.md")
        .read_text(encoding="utf-8")
        .split("---", 2)[1]
    )
    assert closed["unknown_field"] == "preserve-me"
    assert closed["execution_frontier"]["last_completed"] == []
    assert closed["execution_frontier"]["in_progress"] is None
    assert closed["execution_frontier"]["pending_verification"] == []
