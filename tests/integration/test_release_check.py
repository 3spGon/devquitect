from __future__ import annotations

import hashlib
import io
import json
import subprocess
import zipfile
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from devquitect_quality import cli
from devquitect_quality import github_evidence as gh
from devquitect_quality.packaging import build_package
from devquitect_quality.promotion import PromotionError, release_check
from devquitect_quality.reporting import build_artifact_report, build_ci_package_evidence

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
    "ci-evidence.schema.json",
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
    assert {path.suffix for path in (tmp_path / "release").iterdir()} == {".zip", ".json"}
    assert len(list((tmp_path / "release").iterdir())) == 2
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


@pytest.fixture
def candidate_ci(tmp_path, monkeypatch):
    """Real Git, rebuilds, canonical producer and download bytes; only HTTP is replaced."""
    repository = package_repository(tmp_path)
    baseline = git(repository, "rev-parse", "HEAD^")
    git(repository, "remote", "add", "origin", "https://github.com/owner/repo.git")
    (repository / "uv.lock").write_text("fixture locked toolchain\n")
    git(repository, "add", ".")
    git(repository, "commit", "-qm", "post-bump candidate")
    source = git(repository, "rev-parse", "HEAD")
    first, second = tmp_path / "first", tmp_path / "second"
    package = build_package(repository, source, "0.2.0", first)
    build_package(repository, source, "0.2.0", second)
    identity = dict(
        schema_version=1, repository="owner/repo", workflow_path=gh.WORKFLOW,
        workflow_commit=source, run_id=42, run_attempt=2, source_commit=source,
        event="push", ref="refs/heads/main", pr=None,
        toolchain=dict(python="3.12.12", uv="uv 0.12.10", quality_version="0.1.0",
                       quality_source_commit=source, compression_runtime="1.2.13",
                       runner_image="ubuntu/fixture",
                       lock_sha256=gh.digest(repository / "uv.lock")),
    )
    (first / "package.json").write_text(json.dumps(build_artifact_report(
        report_type="package", inputs={"source": {"source_commit": source,
                                                  "snapshot_id": package.snapshot_id},
                                       "version": "0.2.0"}, records=[], evidence_manifest=[],
    )))
    index = build_ci_package_evidence(identity, first, second, first / "package.json",
                                     repository / "schemas/ci-evidence.schema.json")
    (first / "ci-evidence.json").write_text(json.dumps(index))
    quality = tmp_path / "quality"
    write_evidence(quality, package.snapshot_id, source)
    roots = {"quality": quality, "package": first}
    for kind in ("Linux", "macOS", "Windows", "diagnostics"):
        roots[kind] = tmp_path / kind
        roots[kind].mkdir()
    for kind, root in roots.items():
        if kind == "package":
            continue
        checks = ({"identity", "check", "ruff", "whitespace"} if kind == "quality"
                  else {"identity", "build-first", "build-second", "index"}
                  if kind == "diagnostics" else {"identity", "smoke"})
        (root / "identity.json").write_text(json.dumps(identity))
        (root / "result.json").write_text(json.dumps({
            **identity, "result": "pass",
            "job": "quality" if kind == "quality" else (
                "package" if kind == "diagnostics" else "platform-smoke"
            ), "checks": {
                name: {"status": "pass", "exit_code": 0} for name in checks
            },
        }))
    jobs = [dict(id=i, name=name, run_id=42, run_attempt=2, head_sha=source,
                 status="completed", conclusion="success",
                 started_at="2026-10-05T00:00:00Z", completed_at="2026-10-05T01:00:00Z")
            for i, name in enumerate(gh.JOBS.values(), 1)]
    base = f"{gh.API}/repos/owner/repo/actions"
    artifacts, raw_by_url = [], {}
    metadata = {
        f"{base}/runs/42/attempts/2": dict(
            id=42, run_attempt=2, head_sha=source, event="push", head_branch="main",
            status="completed", conclusion="success", repository={"full_name": "owner/repo"},
            workflow_id=7, path=gh.WORKFLOW,
        ),
        f"{base}/workflows/7": {"path": gh.WORKFLOW},
        f"{base}/runs/42/attempts/2/jobs?per_page=100&page=1": {"total_count": 6, "jobs": jobs},
        f"{base}/runs/42/artifacts?per_page=100&page=1": {"total_count": 6, "artifacts": artifacts},
    }

    def refresh():
        artifacts.clear()
        for i, (kind, root) in enumerate(roots.items(), 11):
            prefix = (f"platform-smoke-{kind}" if kind in {"Linux", "macOS", "Windows"}
                      else "package-diagnostics" if kind == "diagnostics" else kind)
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as zipped:
                for path in root.iterdir():
                    zipped.writestr(path.name, path.read_bytes())
            raw = buffer.getvalue()
            url = f"{base}/artifacts/{i}/zip"
            raw_by_url[url] = raw
            artifacts.append(dict(
                id=i, name=f"{prefix}-{source}-attempt-2", expired=False,
                created_at="2026-10-05T00:30:00Z", expires_at="2099-01-01T00:00:00Z",
                size_in_bytes=len(raw), digest=f"sha256:{hashlib.sha256(raw).hexdigest()}",
                archive_download_url=url,
                workflow_run={"id": 42, "head_sha": source, "head_branch": "main"},
            ))
    refresh()
    monkeypatch.setenv("GH_TOKEN", "fixture-read-only")
    calls = []

    def request(self, url, *, storage=False):
        calls.append(url)
        return (json.dumps(metadata[url]).encode() if url in metadata else raw_by_url[url]), {}

    monkeypatch.setattr(gh.GitHubEvidence, "_request", request)
    evidence = tmp_path / "fresh-evidence"
    evidence.mkdir()
    monkeypatch.setattr(cli, "_repository_root", lambda: repository)
    return dict(repository=repository, source=source, baseline=baseline, package=package,
                evidence=evidence, output=tmp_path / "release", roots=roots, index=index,
                metadata=metadata, artifacts=artifacts, jobs=jobs, refresh=refresh, calls=calls)


def run_ci(case, **overrides):
    values = dict(source=case["source"], version="0.2.0", repository="owner/repo",
                  ci_run_id="42", ci_run_attempt="2", previous_release=case["baseline"],
                  evidence=str(case["evidence"]), output=str(case["output"]))
    values.update(overrides)
    args = ["release-check"]
    for key, value in values.items():
        if value is not None:
            args.extend(["--" + key.replace("_", "-"), value])
    return cli.main(args)


def test_ci_release_check_downloads_and_binds_real_rebuilds_post_bump(candidate_ci, capsys):
    case = candidate_ci
    assert run_ci(case) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["result"] == "pass"
    proposal = next(item["promotion"] for item in report["evidence_manifest"]
                    if "promotion" in item)
    assert proposal["approved_by"] is None and proposal["approved_at"] is None
    assert proposal["run_ids"] == ["42"]
    assert len(list(case["output"].iterdir())) == 3
    assert ((case["output"] / "devquitect-0.2.0.zip").read_bytes()
            == case["package"].artifact_path.read_bytes())
    assert any(item.get("behavioral", [{}])[0].get("verdict") == "not-run"
               for item in report["evidence_manifest"] if "behavioral" in item)
    schemas = case["repository"] / "schemas"
    Draft202012Validator(json.loads((schemas / "report.schema.json").read_text())).validate(report)
    Draft202012Validator(json.loads(
        (schemas / "promotion-record.schema.json").read_text()
    )).validate(proposal)


@pytest.mark.parametrize("bad", ["zip", "manifest", "snapshot", "version", "index-attempt",
                                 "quality-source", "platform", "package-report"])
def test_shared_policy_rejects_authenticated_but_invalid_payloads(candidate_ci, capsys, bad):
    case = candidate_ci
    root = case["roots"]["package"]
    if bad == "zip":
        (root / "devquitect-0.2.0.zip").write_bytes(b"tampered")
    elif bad == "manifest":
        path = root / "devquitect-0.2.0.manifest.json"
        value = json.loads(path.read_text())
        value["artifact_digest"] = "sha256:" + "0" * 64
        path.write_text(json.dumps(value))
        entry = case["index"]["files"]["manifest"]
        entry.update(sha256=gh.digest(path), size=path.stat().st_size)
        (root / "ci-evidence.json").write_text(json.dumps(case["index"]))
    elif bad in {"snapshot", "version", "index-attempt"}:
        case["index"][{"snapshot": "snapshot_id", "version": "version",
                       "index-attempt": "run_attempt"}[bad]] = {
                           "snapshot": "sha256:" + "0" * 64, "version": "1.0.0", "index-attempt": 1,
                       }[bad]
        (root / "ci-evidence.json").write_text(json.dumps(case["index"]))
    elif bad in {"quality-source", "platform"}:
        path = case["roots"]["quality" if bad == "quality-source" else "Windows"] / "result.json"
        value = json.loads(path.read_text())
        value["source_commit" if bad == "quality-source" else "result"] = (
            "b" * 40 if bad == "quality-source" else "fail"
        )
        path.write_text(json.dumps(value))
    else:
        path = root / "package.json"
        value = json.loads(path.read_text())
        value["inputs"]["source"]["source_commit"] = "b" * 40
        path.write_text(json.dumps(value))
        case["index"]["files"]["report"].update(sha256=gh.digest(path), size=path.stat().st_size)
        (root / "ci-evidence.json").write_text(json.dumps(case["index"]))
    case["refresh"]()
    assert run_ci(case) == 1
    assert json.loads(capsys.readouterr().out)["result"] == "fail"
    assert not case["output"].exists()


@pytest.mark.parametrize("overrides", [
    {"ci_run_attempt": None}, {"previous_release": None}, {"source": "HEAD"},
    {"ci_run_id": "bad"}, {"ci_run_attempt": "0"}, {"repository": "other/repo"},
])
def test_ci_configuration_failures_have_reports_and_no_output(candidate_ci, capsys, overrides):
    assert run_ci(candidate_ci, **overrides) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["result"] == "fail" and report["evidence_manifest"] == []
    assert not candidate_ci["output"].exists()


def test_ci_preserves_existing_output_and_rejects_report_inside_it(candidate_ci, capsys):
    case = candidate_ci
    case["output"].mkdir()
    existing = case["output"] / "user.txt"
    existing.write_text("preserve")
    assert run_ci(case, report=str(case["output"] / "user.txt")) == 2
    assert existing.read_text() == "preserve"
    assert json.loads(capsys.readouterr().out)["result"] == "fail"


def test_ci_missing_token_is_infrastructure_and_keeps_diagnostic_report(
    candidate_ci, monkeypatch, capsys,
):
    monkeypatch.delenv("GH_TOKEN")
    path = candidate_ci["output"].parent / "diagnostic.json"
    assert run_ci(candidate_ci, report=str(path)) == 3
    assert json.loads(path.read_text())["result"] == "inconclusive"
    assert json.loads(capsys.readouterr().out)["records"][0]["code"] == "release-check.3"
    assert not candidate_ci["output"].exists()


def test_explicit_baseline_supports_post_bump_legacy_and_never_uses_network(
    candidate_ci, monkeypatch,
):
    case = candidate_ci
    monkeypatch.setattr(gh.GitHubEvidence, "collect", lambda *args: pytest.fail("network"))
    with pytest.raises(PromotionError, match="greater"):
        release_check(case["repository"], case["source"], "0.2.0",
                      case["roots"]["quality"], case["output"])
    release_check(case["repository"], case["source"], "0.2.0", case["roots"]["quality"],
                  case["output"], previous_release=case["baseline"])
    assert not case["calls"]


@pytest.mark.parametrize("baseline", ["candidate", "missing", "unrelated"])
def test_explicit_baseline_rejects_nonancestor_and_unreadable_refs(candidate_ci, baseline):
    case = candidate_ci
    value = case["source"] if baseline == "candidate" else "f" * 40
    if baseline == "unrelated":
        git(case["repository"], "checkout", "--orphan", "unrelated")
        git(case["repository"], "commit", "-qm", "unrelated history")
        value = git(case["repository"], "rev-parse", "HEAD")
    with pytest.raises(PromotionError, match="ancestor"):
        release_check(case["repository"], case["source"], "0.2.0", case["roots"]["quality"],
                      case["output"], previous_release=value)


def behavioral_directory(case, verdict="pass", report_type="evaluation"):
    root = case["output"].parent / "behavioral"
    root.mkdir()
    row = dict(model_id="gpt-5.6-luna", host="fixture-host", runtime="fixture-runtime",
               reasoning_effort="high", suite_revision="sha256:" + "d" * 64,
               repetitions=1, authorization="fixture-human-authorization",
               verdict=verdict, reports=[])
    if verdict == "not-run":
        row.update(host=None, runtime=None, reasoning_effort=None)
    else:
        report = build_artifact_report(
            report_type=report_type,
            inputs={"candidate" if report_type == "comparison" else "source": {
                "source_commit": case["source"], "snapshot_id": case["package"].snapshot_id,
            }}, result=verdict, records=[{
                "code": f"behavioral.{verdict}", "severity": "info", "path": "evals/test",
                "message": "Simulated executed observation; no real model was called",
                **({"candidate": {"model": row["model_id"],
                                  "reasoning_effort": row["reasoning_effort"]}}
                   if report_type == "comparison" else
                   {"model": row["model_id"], "reasoning_effort": row["reasoning_effort"]}),
            }], evidence_manifest=[],
        )
        path = root / "model.json"
        path.write_text(json.dumps(report))
        row["reports"] = [{"path": "model.json", "sha256": gh.digest(path)}]
    (root / "rows.json").write_text(json.dumps({"rows": [row]}))
    return root, row


@pytest.mark.parametrize("verdict", ["pass", "fail", "inconclusive", "not-run"])
@pytest.mark.parametrize("report_type", ["evaluation", "comparison"])
def test_optional_behavioral_verdicts_stay_independent(candidate_ci, capsys, verdict, report_type):
    root, row = behavioral_directory(candidate_ci, verdict, report_type)
    assert run_ci(candidate_ci, behavioral_evidence=str(root)) == 0
    report = json.loads(capsys.readouterr().out)
    assert next(item["behavioral"] for item in report["evidence_manifest"]
                if "behavioral" in item) == [row]
    assert report["result"] == "pass"


@pytest.mark.parametrize("bad", ["undeclared", "missing", "digest", "candidate", "schema",
                                 "authorization", "runtime", "unsafe", "model", "verdict",
                                 "empty-report"])
def test_invalid_behavioral_indexes_cannot_be_attached(candidate_ci, capsys, bad):
    root, row = behavioral_directory(candidate_ci)
    path = root / "model.json"
    if bad == "undeclared":
        (root / "extra.json").write_text("{}")
    elif bad == "missing":
        path.unlink()
    elif bad == "digest":
        row["reports"][0]["sha256"] = "0" * 64
    elif bad in {"authorization", "runtime"}:
        row[bad] = None
    elif bad == "unsafe":
        row["reports"][0]["path"] = "../escape.json"
    else:
        report = json.loads(path.read_text())
        if bad == "candidate":
            report["inputs"]["source"]["source_commit"] = "b" * 40
        elif bad == "schema":
            report.pop("generated_at")
        elif bad == "verdict":
            report["result"] = "fail"
        elif bad == "empty-report":
            report["records"] = []
        else:
            report["records"] = [dict(
                code="evaluation.pass", severity="info", path="evals/test",
                message="fixture", model="gpt-6-luna", reasoning_effort="high",
            )]
        path.write_text(json.dumps(report))
        row["reports"][0]["sha256"] = gh.digest(path)
    (root / "rows.json").write_text(json.dumps({"rows": [row]}))
    assert run_ci(candidate_ci, behavioral_evidence=str(root)) == 1
    assert json.loads(capsys.readouterr().out)["result"] == "fail"
    assert not candidate_ci["output"].exists()


def test_behavioral_pass_cannot_override_deterministic_failure(candidate_ci, capsys):
    root, _ = behavioral_directory(candidate_ci)
    candidate_ci["jobs"][1]["conclusion"] = "failure"
    assert run_ci(candidate_ci, behavioral_evidence=str(root)) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["result"] == "fail" and report["evidence_manifest"] == []
    assert not candidate_ci["output"].exists()


def test_unexecuted_behavioral_row_cannot_claim_runtime(candidate_ci, capsys):
    root, row = behavioral_directory(candidate_ci, "not-run")
    row["runtime"] = "invented"
    (root / "rows.json").write_text(json.dumps({"rows": [row]}))
    assert run_ci(candidate_ci, behavioral_evidence=str(root)) == 1
    assert json.loads(capsys.readouterr().out)["result"] == "fail"


def test_ci_report_matches_stdout_and_is_written_before_output_finalization(candidate_ci, capsys):
    path = candidate_ci["output"].parent / "readiness.json"
    assert run_ci(candidate_ci, report=str(path)) == 0
    assert json.loads(path.read_text()) == json.loads(capsys.readouterr().out)
    assert candidate_ci["output"].is_dir()


def test_failed_report_write_leaves_no_output_or_staging(candidate_ci, monkeypatch, capsys):
    from devquitect_quality import promotion

    def fail(*args):
        raise PermissionError("fixture report write denied")

    monkeypatch.setattr(promotion, "write_report_atomic", fail)
    path = candidate_ci["output"].parent / "readiness.json"
    assert run_ci(candidate_ci, report=str(path)) == 3
    assert json.loads(capsys.readouterr().out)["result"] == "inconclusive"
    assert not candidate_ci["output"].exists()
    assert not list(candidate_ci["output"].parent.glob(".readiness-*"))


def test_existing_evidence_cannot_be_reused_in_ci_mode(candidate_ci, capsys):
    (candidate_ci["evidence"] / "stale.json").write_text("{}")
    assert run_ci(candidate_ci) == 2
    assert not candidate_ci["calls"]
    assert json.loads(capsys.readouterr().out)["result"] == "fail"


def test_ci_committed_version_mismatch_is_policy_rejection(candidate_ci, capsys):
    assert run_ci(candidate_ci, version="1.0.0") == 1
    assert json.loads(capsys.readouterr().out)["records"][0]["code"] == "release-check.1"
    assert not candidate_ci["output"].exists() and not candidate_ci["calls"]


def test_behavioral_option_requires_ci_selectors(candidate_ci, capsys):
    root, _ = behavioral_directory(candidate_ci)
    assert run_ci(candidate_ci, repository=None, ci_run_id=None, ci_run_attempt=None,
                  behavioral_evidence=str(root)) == 2
    assert not candidate_ci["calls"]
    assert json.loads(capsys.readouterr().out)["result"] == "fail"
