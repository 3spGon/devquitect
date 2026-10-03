from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from devquitect_quality.packaging import build_package
from devquitect_quality.promotion import PromotionError, release_check

SKILLS = (
    "project-plan-execution",
    "quick-change",
    "software-idea-to-project",
    "targeted-refactoring",
)
SCHEMAS = (
    "eval-case.schema.json",
    "report.schema.json",
    "promotion-record.schema.json",
    "authority-map.schema.json",
    "calibration-report.schema.json",
)


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def package_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    (repository / ".codex-plugin").mkdir(parents=True)
    schemas = repository / "schemas"
    schemas.mkdir()
    source_schemas = Path(__file__).parents[2] / "schemas"
    for name in SCHEMAS:
        (schemas / name).write_bytes((source_schemas / name).read_bytes())
    (repository / ".codex-plugin/plugin.json").write_text(
        '{"name":"devquitect","version":"0.1.0","skills":"./skills/",'
        '"hooks":"./hooks/hooks.json"}\n',
        encoding="utf-8",
    )
    (repository / "hooks").mkdir()
    (repository / "hooks/hooks.json").write_text("{}\n", encoding="utf-8")
    (repository / "hooks/compaction_recovery.py").write_text(
        "#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8"
    )
    for name in SKILLS:
        skill = repository / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\n---\n", encoding="utf-8"
        )
    git(repository, "init", "-q")
    git(repository, "config", "user.name", "Release Test")
    git(repository, "config", "user.email", "release@example.invalid")
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "baseline input")
    manifest = repository / ".codex-plugin/plugin.json"
    manifest.write_text(
        '{"name":"devquitect","version":"0.2.0","skills":"./skills/",'
        '"hooks":"./hooks/hooks.json"}\n',
        encoding="utf-8",
    )
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "release input")
    return repository


def write_evidence(
    root: Path,
    snapshot_id: str,
    source_commit: str,
    *,
    source_kind: str = "git-ref",
    result: str = "pass",
    report_type: str = "check",
) -> None:
    root.mkdir()
    report = {
        "schema_version": 1,
        "report_type": report_type,
        "generated_at": "2026-09-14T00:00:00+00:00",
        "toolchain": {"package": "devquitect-quality", "version": "0.1.0"},
        "result": result,
        "inputs": {"behavioral": False},
        "records": [
            {
                "code": "check.validation",
                "severity": "info",
                "path": "skills",
                "message": "structural validation passed",
            },
            {
                "code": "check.tests",
                "severity": "info",
                "path": "tests",
                "message": "fast tests passed",
            },
        ],
        "evidence_manifest": [
            {
                "report_type": "validation",
                "result": "pass",
                "source": {
                    "kind": source_kind,
                    "snapshot_id": snapshot_id,
                    "source_commit": source_commit,
                },
            },
            {"suite": "fast", "exit_code": 0},
        ],
        "redactions": [],
    }
    (root / "check.json").write_text(json.dumps(report), encoding="utf-8")


def test_release_check_rebuilds_and_emits_unapproved_schema_valid_proposal(
    tmp_path: Path,
) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(evidence, package.snapshot_id, package.source_commit)

    artifact, proposal = release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")

    assert artifact.artifact_path.is_file()
    assert proposal["package_digest"] == artifact.artifact_digest
    assert proposal["approved_by"] is None
    assert proposal["approved_at"] is None
    schema = json.loads(
        (Path(__file__).parents[2] / "schemas/promotion-record.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(proposal)


@pytest.mark.parametrize(
    ("source_kind", "result", "message"),
    [
        ("working-tree", "pass", "credential-free check"),
        ("git-ref", "fail", "not passing"),
    ],
)
def test_release_check_blocks_ineligible_evidence(
    tmp_path: Path,
    source_kind: str,
    result: str,
    message: str,
) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(
        evidence,
        package.snapshot_id,
        package.source_commit,
        source_kind=source_kind,
        result=result,
    )
    with pytest.raises(PromotionError, match=message):
        release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")


def test_release_check_ignores_calibration_evidence(tmp_path: Path) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(evidence, package.snapshot_id, package.source_commit)
    (evidence / "calibration.json").write_text(
        json.dumps({"report_type": "behavior-calibration"}), encoding="utf-8"
    )

    release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")


@pytest.mark.parametrize("missing", ["records", "suite"])
def test_release_check_blocks_incomplete_credential_free_check(
    tmp_path: Path, missing: str
) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(evidence, package.snapshot_id, package.source_commit)
    report_path = evidence / "check.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if missing == "records":
        report["records"] = report["records"][:1]
    else:
        report["evidence_manifest"] = report["evidence_manifest"][:1]
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(PromotionError, match="incomplete"):
        release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")


def test_release_check_blocks_evidence_from_a_different_commit_with_same_snapshot(
    tmp_path: Path,
) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(evidence, package.snapshot_id, git(repository, "rev-parse", "HEAD^"))

    with pytest.raises(PromotionError, match="matches the source snapshot"):
        release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")


def test_release_check_binds_hook_only_commit_even_when_snapshot_is_unchanged(
    tmp_path: Path,
) -> None:
    repository = package_repository(tmp_path)
    previous = build_package(repository, "HEAD", "0.2.0", tmp_path / "previous")
    handler = repository / "hooks/compaction_recovery.py"
    handler.write_text(handler.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "hook-only change")
    current = build_package(repository, "HEAD", "0.2.0", tmp_path / "current")
    assert previous.snapshot_id == current.snapshot_id
    assert previous.source_commit != current.source_commit
    evidence = tmp_path / "evidence"
    write_evidence(evidence, previous.snapshot_id, previous.source_commit)

    with pytest.raises(PromotionError, match="matches the source snapshot"):
        release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")


def test_release_check_blocks_noncanonical_check_evidence(tmp_path: Path) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(evidence, package.snapshot_id, package.source_commit)
    report_path = evidence / "check.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    del report["generated_at"]
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(PromotionError, match="not canonical"):
        release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")
