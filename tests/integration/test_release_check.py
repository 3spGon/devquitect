from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from devquitect_quality.packaging import build_package
from devquitect_quality.promotion import PromotionError, release_check

SKILLS = ("project-plan-execution", "software-idea-to-project", "targeted-refactoring")


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def package_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    (repository / ".codex-plugin").mkdir(parents=True)
    (repository / ".codex-plugin/plugin.json").write_text(
        '{"name":"devquitect","version":"0.1.0","skills":"./skills/"}\n',
        encoding="utf-8",
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
        '{"name":"devquitect","version":"0.2.0","skills":"./skills/"}\n',
        encoding="utf-8",
    )
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "release input")
    return repository


def write_evidence(
    root: Path,
    snapshot_id: str,
    *,
    candidate_kind: str = "git-ref",
    evaluation_result: str = "pass",
    critical_failures: list[str] | None = None,
) -> None:
    root.mkdir()
    evaluation = {
        "schema_version": 1,
        "report_type": "evaluation",
        "result": evaluation_result,
        "inputs": {"source": {"kind": "git-ref", "snapshot_id": snapshot_id}},
        "records": [
            {
                "classification": evaluation_result,
                "critical_failures": critical_failures or [],
                "eligibility": "release-eligible",
                "run_id": "run-1",
            }
        ],
    }
    comparison = {
        "schema_version": 1,
        "report_type": "comparison",
        "result": "pass",
        "inputs": {"candidate": {"kind": candidate_kind, "snapshot_id": snapshot_id}},
        "records": [
            {
                "case_id": "self-hosting",
                "classification": "equivalent",
                "comparison_id": "comparison-1",
            }
        ],
    }
    (root / "evaluation.json").write_text(json.dumps(evaluation), encoding="utf-8")
    (root / "comparison.json").write_text(json.dumps(comparison), encoding="utf-8")


def test_release_check_rebuilds_and_emits_unapproved_schema_valid_proposal(
    tmp_path: Path,
) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(evidence, package.snapshot_id)

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
    ("candidate_kind", "evaluation_result", "critical_failures", "message"),
    [
        ("working-tree", "pass", [], "clean-candidate comparison"),
        ("git-ref", "inconclusive", [], "not passing"),
        ("git-ref", "pass", ["write"], "critical or unresolved"),
    ],
)
def test_release_check_blocks_ineligible_evidence(
    tmp_path: Path,
    candidate_kind: str,
    evaluation_result: str,
    critical_failures: list[str],
    message: str,
) -> None:
    repository = package_repository(tmp_path)
    package = build_package(repository, "HEAD", "0.2.0", tmp_path / "probe")
    evidence = tmp_path / "evidence"
    write_evidence(
        evidence,
        package.snapshot_id,
        candidate_kind=candidate_kind,
        evaluation_result=evaluation_result,
        critical_failures=critical_failures,
    )
    with pytest.raises(PromotionError, match=message):
        release_check(repository, "HEAD", "0.2.0", evidence, tmp_path / "release")
