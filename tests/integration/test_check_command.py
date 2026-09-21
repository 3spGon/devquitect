from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from devquitect_quality.promotion import release_check

REPOSITORY = Path(__file__).parents[2]


def test_check_runs_fast_composed_definition_of_done_and_writes_atomic_report(
    tmp_path: Path,
) -> None:
    report = tmp_path / "check.json"
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "devquitect_quality.cli",
            "check",
            "--source",
            "working-tree",
            "--report",
            str(report),
        ],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0, process.stderr
    payload = json.loads(process.stdout)
    assert payload == json.loads(report.read_text(encoding="utf-8"))
    assert payload["report_type"] == "check"
    assert payload["result"] == "pass"
    assert payload["inputs"]["model"] == "gpt-5.6-luna"
    assert payload["inputs"]["reasoning_effort"] == "high"
    assert {record["code"] for record in payload["records"]} == {
        "check.validation",
        "check.tests",
    }
    source = payload["evidence_manifest"][0]["source"]
    expected_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert source["source_commit"] == expected_commit


def test_check_invalid_source_returns_two_and_still_writes_report(tmp_path: Path) -> None:
    report = tmp_path / "invalid.json"
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "devquitect_quality.cli",
            "check",
            "--source",
            "missing-ref",
            "--report",
            str(report),
        ],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 2
    assert json.loads(report.read_text(encoding="utf-8"))["result"] == "fail"


def test_structural_check_does_not_need_a_login_cache(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    (tmp_path / "auth.json").write_text("not a credential the check may use", encoding="utf-8")
    process = subprocess.run(
        [sys.executable, "-m", "devquitect_quality.cli", "check", "--source", "working-tree"],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0, process.stderr


def test_behavioral_eval_without_auth_mode_returns_migration_error() -> None:
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "devquitect_quality.cli",
            "eval",
            "--source",
            "working-tree",
            "--case",
            "self-hosting",
        ],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 2
    assert "authentication is explicit" in process.stderr


def test_git_ref_check_report_is_accepted_by_release_check(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    shutil.copytree(
        REPOSITORY,
        repository,
        ignore=shutil.ignore_patterns(
            ".git", ".venv", ".pytest_cache", ".devquitect-reports", "__pycache__", "graphify-out"
        ),
    )
    (repository / "tests/integration/test_stable_baseline.py").unlink()
    for args in (
        ("init", "-q"),
        ("config", "user.name", "Check Test"),
        ("config", "user.email", "check@example.invalid"),
        ("add", "."),
        ("commit", "-qm", "baseline"),
    ):
        subprocess.run(["git", *args], cwd=repository, check=True, capture_output=True)
    manifest = repository / ".codex-plugin/plugin.json"
    value = json.loads(manifest.read_text(encoding="utf-8"))
    major, minor, patch = (int(part) for part in value["version"].split("."))
    candidate_version = f"{major}.{minor}.{patch + 1}"
    value["version"] = candidate_version
    manifest.write_text(json.dumps(value), encoding="utf-8")
    subprocess.run(["git", "add", str(manifest)], cwd=repository, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-qm", "candidate"], cwd=repository, check=True, capture_output=True
    )

    evidence = tmp_path / "evidence"
    evidence.mkdir()
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "devquitect_quality.cli",
            "check",
            "--source",
            "HEAD",
            "--report",
            str(evidence / "check.json"),
        ],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0, process.stderr
    _, proposal = release_check(
        repository, "HEAD", candidate_version, evidence, tmp_path / "release"
    )
    assert proposal["source_commit"] == subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
