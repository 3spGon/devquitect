"""Credential-free CI contracts; hosted acceptance is deliberately separate."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

from devquitect_quality import reporting
from devquitect_quality.packaging import build_package
from devquitect_quality.reporting import (
    build_artifact_report,
    build_ci_package_evidence,
    ci_identity,
    ci_whitespace,
    write_report_atomic,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/ci-evidence.schema.json"
WORKFLOW = ROOT / ".github/workflows/ci.yml"


def workflow(path=WORKFLOW):
    # BaseLoader preserves GitHub's YAML 1.2 `on` key (SafeLoader uses YAML 1.1).
    return yaml.load(path.read_text(), Loader=yaml.BaseLoader)


def bash():
    # Windows' system bash launches WSL; these contracts use the runner's Git Bash.
    if sys.platform == "win32":
        return str(Path(shutil.which("git")).resolve().parents[1] / "bin/bash.exe")
    return "bash"


def test_ci_triggers_jobs_locked_toolchain_and_read_only_permissions():
    ci = workflow()
    assert set(ci["on"]) == {"pull_request", "push"}
    assert ci["on"]["push"]["branches"] == ["main"]
    assert ci["permissions"] == {"contents": "read"}
    assert ci["env"] == {
        "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.autocrlf",
        "GIT_CONFIG_VALUE_0": "false",
    }
    jobs = ci["jobs"]
    assert jobs["quality"]["name"] == "Devquitect / quality"
    assert jobs["package"]["name"] == "Devquitect / package"
    assert jobs["platform-smoke"]["name"] == "Devquitect / platform-smoke"
    for id, os_name in [("ubuntu", "ubuntu"), ("macos", "macos"), ("windows", "windows")]:
        job = jobs[f"platform-{id}"]
        assert job["runs-on"] == f"{os_name}-latest"
        assert job["name"] == f"Devquitect / platform-smoke ({os_name}-latest)"
    assert "secrets." not in WORKFLOW.read_text()
    assert "--behavioral" not in WORKFLOW.read_text()
    assert "working-tree" not in WORKFLOW.read_text()
    for id, job in jobs.items():
        assert "permissions" not in job
        assert "continue-on-error" not in job
        if id == "platform-smoke":
            continue
        steps = job["steps"]
        checkout = next(s for s in steps if s.get("uses", "").startswith("actions/checkout@"))
        assert checkout["with"] == {
            "ref": "${{ github.sha }}", "fetch-depth": "0", "persist-credentials": "false",
        }
        python = next(s for s in steps if s.get("uses", "").startswith("actions/setup-python@"))
        assert python["with"]["python-version"] == "3.12"
        uv = next(s for s in steps if s.get("uses", "").startswith("astral-sh/setup-uv@"))
        assert uv["with"] == {"version": "0.12.10", "enable-cache": "false"}
        assert any(s.get("run") == "uv sync --locked --all-groups" for s in steps)
        for step in steps:
            if "uses" in step:
                assert re.fullmatch(r"[A-Za-z0-9_/-]+@[0-9a-f]{40}", step["uses"])
        uploads = [s for s in steps if s.get("uses", "").startswith("actions/upload-artifact@")]
        assert uploads
        for step in uploads:
            assert step["if"] == "${{ always() }}"
            assert step["with"]["retention-days"] == "30"
            assert "${{ github.sha }}-attempt-${{ github.run_attempt }}" in step["with"]["name"]
            assert step["with"]["if-no-files-found"] == "error"


def test_ci_required_commands_and_independent_build_roots():
    jobs = workflow()["jobs"]
    quality = "\n".join(s.get("run", "") for s in jobs["quality"]["steps"])
    assert "devquitect check --source HEAD --report .devquitect-reports/check.json" in quality
    assert "uv run ruff check src tests" in quality
    assert "reporting whitespace" in quality
    for os_name in ("ubuntu", "macos", "windows"):
        smoke = "\n".join(s.get("run", "") for s in jobs[f"platform-{os_name}"]["steps"])
        assert (
            "pytest tests/unit/test_compaction_recovery_hook.py "
            "tests/unit/test_packaging.py tests/contract"
        ) in smoke
        native = next(s for s in jobs[f"platform-{os_name}"]["steps"]
                      if s.get("name") == "Expose native Windows Codex executable")
        assert native["if"] == "runner.os == 'Windows'" and native["shell"] == "pwsh"
        assert "codex.exe" in native["run"] and "GITHUB_PATH" in native["run"]
        assert "$nativeCodex.Count -ne 1" in native["run"]
    package = "\n".join(s.get("run", "") for s in jobs["package"]["steps"])
    assert package.count('devquitect package --source "$GITHUB_SHA"') == 2
    assert "--output dist/first" in package and "--output dist/second" in package
    assert "reporting package --first dist/first --second dist/second" in package


@pytest.mark.parametrize("bad", ["failure", "cancelled", "skipped", "", "missing"])
@pytest.mark.parametrize("variant", ["UBUNTU_RESULT", "MACOS_RESULT", "WINDOWS_RESULT"])
def test_aggregate_rejects_every_non_success_variant(bad, variant):
    job = workflow()["jobs"]["platform-smoke"]
    assert job["if"] == "${{ always() }}"
    assert job["needs"] == ["platform-ubuntu", "platform-macos", "platform-windows"]
    step = job["steps"][0]
    env = {**os.environ, **dict.fromkeys(step["env"], "success"), variant: bad}
    result = subprocess.run([bash(), "-e", "-c", step["run"]], env=env, check=False)
    assert result.returncode != 0


def test_aggregate_accepts_only_complete_success():
    step = workflow()["jobs"]["platform-smoke"]["steps"][0]
    assert subprocess.run(
        [bash(), "-e", "-c", step["run"]],
        env={**os.environ, **dict.fromkeys(step["env"], "success")}, check=False,
    ).returncode == 0


@pytest.fixture
def package_inputs(tmp_path):
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    plugin = json.loads(subprocess.check_output(
        ["git", "show", f"{sha}:.codex-plugin/plugin.json"], cwd=ROOT, text=True
    ))
    first, second = tmp_path / "first", tmp_path / "second"
    artifacts = [build_package(ROOT, sha, plugin["version"], root) for root in (first, second)]
    artifact = artifacts[0]
    report = build_artifact_report(
        report_type="package",
        inputs={"source": {"source_commit": sha, "snapshot_id": artifact.snapshot_id},
                "version": plugin["version"]},
        records=[], evidence_manifest=[artifact.as_dict()],
    )
    write_report_atomic(first / "package.json", report)
    identity = {
        "schema_version": 1, "repository": "3spGon/devquitect",
        "workflow_path": ".github/workflows/ci.yml", "workflow_commit": sha,
        "run_id": 42, "run_attempt": 2, "event": "push", "ref": "refs/heads/main",
        "source_commit": sha, "pr": None,
        "toolchain": {
            "python": "3.12.12", "uv": "uv 0.12.10", "quality_version": "0.1.0",
            "quality_source_commit": sha, "compression_runtime": "1.2.13",
            "runner_image": "ubuntu24/fixture", "lock_sha256": "a" * 64,
        },
    }
    return identity, first, second


def index(inputs):
    identity, first, second = inputs
    return build_ci_package_evidence(identity, first, second, first / "package.json", SCHEMA)


def test_two_real_builds_produce_schema_valid_bound_index(package_inputs):
    document = index(package_inputs)
    jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text())).validate(document)
    for entry in document["files"].values():
        path = package_inputs[1] / entry["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
        assert path.stat().st_size == entry["size"]
    assert len(document["files"]) == 3
    assert "ci-evidence.json" not in [item["path"] for item in document["files"].values()]


def test_internal_package_entrypoint_accepts_the_real_cli_report(package_inputs, tmp_path):
    identity, first, second = package_inputs
    version = json.loads(next(first.glob("*.manifest.json")).read_text())["version"]
    process = subprocess.run([
        sys.executable, "-m", "devquitect_quality.cli", "package",
        "--source", identity["source_commit"], "--version", version,
        "--output", str(first), "--report", str(first / "package.json"),
    ], cwd=ROOT, capture_output=True, text=True, check=False)
    assert process.returncode == 0, process.stderr
    (tmp_path / "schemas").mkdir()
    (tmp_path / "schemas/ci-evidence.schema.json").write_bytes(SCHEMA.read_bytes())
    write_report_atomic(tmp_path / ".devquitect-reports/identity.json", identity)
    process = subprocess.run([
        sys.executable, "-m", "devquitect_quality.reporting", "package",
        "--first", str(first), "--second", str(second),
    ], cwd=tmp_path, capture_output=True, text=True, check=False)
    assert process.returncode == 0, process.stderr
    document = json.loads((first / "ci-evidence.json").read_text())
    jsonschema.validate(document, json.loads(SCHEMA.read_text()))


def test_package_index_requires_independent_roots(package_inputs):
    identity, first, _ = package_inputs
    with pytest.raises(ValueError, match="independent output roots"):
        build_ci_package_evidence(identity, first, first, first / "package.json", SCHEMA)


@pytest.mark.parametrize("mutation", ["source", "tool", "zip", "manifest", "report", "missing"])
def test_index_rejects_wrong_identity_and_differing_rebuilds(package_inputs, mutation):
    identity, first, second = package_inputs
    if mutation in {"source", "tool"}:
        target = identity if mutation == "source" else identity["toolchain"]
        target["source_commit" if mutation == "source" else "quality_source_commit"] = "f" * 40
    elif mutation == "zip":
        next(second.glob("*.zip")).write_bytes(b"tampered")
    elif mutation == "manifest":
        path = next(second.glob("*.manifest.json"))
        path.write_bytes(path.read_bytes() + b" ")
    elif mutation == "report":
        path = first / "package.json"
        data = json.loads(path.read_text())
        data["result"] = "fail"
        write_report_atomic(path, data)
    else:
        next(second.glob("*.manifest.json")).unlink()
    with pytest.raises(ValueError):
        index(package_inputs)


@pytest.mark.parametrize("field,value", [
    ("run_attempt", 0), ("run_id", "42"), ("workflow_commit", "main"),
    ("repository", "bad"), ("source_commit", "short"), ("unexpected", True),
    ("pr", {}), ("ref", "refs/heads/topic"), ("toolchain", {}),
])
def test_schema_rejects_malformed_or_unknown_metadata(package_inputs, field, value):
    document = index(package_inputs)
    document[field] = value
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, json.loads(SCHEMA.read_text()))


@pytest.mark.parametrize("path", ["../outside", "/absolute", "C:/escape", "a/../b", "a\\b"])
def test_schema_rejects_unsafe_file_paths(package_inputs, path):
    document = index(package_inputs)
    document["files"]["zip"]["path"] = path
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, json.loads(SCHEMA.read_text()))


def test_pr_distinguishes_integration_head_base_from_final_push(package_inputs):
    document = index(package_inputs)
    document.update(event="pull_request", ref="refs/pull/12/merge", pr={
        "integration_commit": document["source_commit"],
        "head_commit": "a" * 40, "base_commit": "b" * 40,
    })
    jsonschema.validate(document, json.loads(SCHEMA.read_text()))
    document["pr"] = None
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, json.loads(SCHEMA.read_text()))


def test_identity_rejects_wrong_checkout_before_collecting_metadata(monkeypatch):
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with pytest.raises(ValueError, match="tested commit"):
        ci_identity(ROOT, {"GITHUB_SHA": "f" * 40})
    with pytest.raises(ValueError, match="installed quality tool"):
        ci_identity(ROOT / "tests", {"GITHUB_SHA": sha})


@pytest.fixture
def identity_checkout(tmp_path, monkeypatch):
    (tmp_path / "src/devquitect_quality").mkdir(parents=True)
    (tmp_path / "schemas").mkdir()
    (tmp_path / "schemas/ci-evidence.schema.json").write_bytes(SCHEMA.read_bytes())
    installed = tmp_path / "src/devquitect_quality/reporting.py"
    installed.write_text("# installed fixture\n")
    (tmp_path / "uv.lock").write_text("fixture lock\n")
    for args in [("init", "-q"), ("config", "user.name", "CI"),
                 ("config", "user.email", "ci@example.invalid"), ("add", "."),
                 ("commit", "-qm", "fixture")]:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)
    sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True
    ).strip()
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"before": "0" * 40}))
    env = {
        "GITHUB_SHA": sha, "GITHUB_REPOSITORY": "3spGon/devquitect",
        "GITHUB_EVENT_NAME": "push", "GITHUB_EVENT_PATH": str(event),
        "GITHUB_REF": "refs/heads/main", "GITHUB_WORKFLOW_SHA": sha,
        "GITHUB_WORKFLOW_REF": "3spGon/devquitect/.github/workflows/ci.yml@refs/heads/main",
        "GITHUB_RUN_ID": "42", "GITHUB_RUN_ATTEMPT": "2",
        "ImageOS": "fixture", "ImageVersion": "observed-image",
    }
    monkeypatch.setattr(reporting, "__file__", str(installed))
    monkeypatch.setattr(reporting.platform, "python_version", lambda: "3.12.12")
    return tmp_path, env


@pytest.mark.parametrize("event", ["push", "pull_request"])
def test_identity_observes_clean_installed_source_and_separate_pr_shas(identity_checkout, event):
    path, env = identity_checkout
    if event == "pull_request":
        env.update(GITHUB_EVENT_NAME=event, GITHUB_REF="refs/pull/12/merge")
        Path(env["GITHUB_EVENT_PATH"]).write_text(json.dumps({
            "pull_request": {"head": {"sha": "a" * 40}, "base": {"sha": "b" * 40}},
        }))
    identity = ci_identity(path, env)
    assert identity["source_commit"] == env["GITHUB_SHA"]
    assert identity["toolchain"]["quality_source_commit"] == env["GITHUB_SHA"]
    assert identity["toolchain"]["lock_sha256"] == hashlib.sha256(
        (path / "uv.lock").read_bytes()
    ).hexdigest()
    if event == "pull_request":
        assert identity["pr"] == {
            "integration_commit": env["GITHUB_SHA"],
            "head_commit": "a" * 40, "base_commit": "b" * 40,
        }
    else:
        assert identity["pr"] is None


@pytest.mark.parametrize("field,value", [
    ("GITHUB_RUN_ATTEMPT", "0"), ("GITHUB_RUN_ID", "bad"),
    ("GITHUB_WORKFLOW_SHA", "main"), ("GITHUB_REPOSITORY", "bad"),
    ("GITHUB_REF", "refs/heads/topic"), ("ImageVersion", None),
    ("GITHUB_WORKFLOW_REF", "3spGon/devquitect/.github/workflows/other.yml@refs/heads/main"),
])
def test_identity_rejects_invalid_or_missing_actual_metadata(identity_checkout, field, value):
    path, env = identity_checkout
    if value is None:
        env.pop(field)
    else:
        env[field] = value
    with pytest.raises((ValueError, KeyError, jsonschema.ValidationError)):
        ci_identity(path, env)


@pytest.mark.parametrize("file", ["uv.lock", "src/devquitect_quality/reporting.py"])
def test_identity_rejects_installed_bytes_different_from_commit(identity_checkout, file):
    path, env = identity_checkout
    (path / file).write_bytes((path / file).read_bytes().replace(b"\n", b"\r\n"))
    with pytest.raises(ValueError, match="bytes differ"):
        ci_identity(path, env)


def test_identity_rejects_tracked_changes_and_wrong_python(identity_checkout, monkeypatch):
    path, env = identity_checkout
    monkeypatch.setattr(reporting.platform, "python_version", lambda: "3.14.7")
    with pytest.raises(jsonschema.ValidationError):
        ci_identity(path, env)
    (path / "schemas/ci-evidence.schema.json").write_text("{}")
    with pytest.raises(ValueError, match="tracked changes"):
        ci_identity(path, env)


@pytest.mark.parametrize("event", ["push", "pull_request", "first-push"])
def test_event_base_whitespace_positive_and_negative(tmp_path, event):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=tmp_path, text=True).strip()
    git("init", "-q")
    git("config", "user.name", "CI fixture")
    git("config", "user.email", "ci@example.invalid")
    path = tmp_path / "file.txt"
    path.write_text("clean\n", newline="\n")
    git("add", ".")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    if event == "pull_request":
        payload = {"pull_request": {"base": {"sha": base}, "head": {"sha": base}}}
    else:
        payload = {"before": "0" * 40 if event == "first-push" else base}
    actual_event = "push" if event == "first-push" else event
    assert ci_whitespace(tmp_path, actual_event, payload) == 0
    path.write_text("introduced whitespace \n", newline="\n")
    git("add", ".")
    git("commit", "-qm", "bad whitespace")
    assert ci_whitespace(tmp_path, actual_event, payload) != 0


def test_pr_whitespace_starts_at_head_base_merge_base(tmp_path):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=tmp_path, text=True).strip()
    git("init", "-q")
    git("config", "user.name", "CI fixture")
    git("config", "user.email", "ci@example.invalid")
    (tmp_path / "initial.txt").write_text("clean\n")
    git("add", ".")
    git("commit", "-qm", "initial")
    initial = git("rev-parse", "HEAD")
    git("checkout", "-qb", "topic")
    (tmp_path / "topic.txt").write_text("clean topic\n")
    git("add", ".")
    git("commit", "-qm", "topic")
    head = git("rev-parse", "HEAD")
    git("checkout", "-qb", "base", initial)
    (tmp_path / "base.txt").write_text("whitespace introduced since merge-base \n")
    git("add", ".")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    git("merge", "--no-ff", "topic", "-m", "integration")
    assert ci_whitespace(tmp_path, "pull_request", {
        "pull_request": {"base": {"sha": base}, "head": {"sha": head}},
    }) != 0


@pytest.mark.parametrize("code", [0, 1, 2, 3])
def test_result_records_observed_exit_and_missing_checks_as_non_passing(tmp_path, code):
    def run(*args):
        return subprocess.run(
            [sys.executable, "-m", "devquitect_quality.reporting", *args],
            cwd=tmp_path, capture_output=True, text=True, check=False,
        )
    result = run("run", "--job", "test", "--", sys.executable, "-c", f"raise SystemExit({code})")
    assert result.returncode == code, result.stderr
    record = json.loads((tmp_path / ".devquitect-reports/steps/test.json").read_text())
    assert record["exit_code"] == code
    write_report_atomic(tmp_path / ".devquitect-reports/identity.json", {"source_commit": "a" * 40})
    result = run("result", "--job", "quality", "--checks", "test")
    assert result.returncode == (0 if code == 0 else 1), result.stderr
    result = run("result", "--job", "quality", "--checks", "test", "missing")
    assert result.returncode == 1
    report = json.loads((tmp_path / ".devquitect-reports/result.json").read_text())
    assert report["checks"]["missing"] == {"status": "not-run", "exit_code": None}
    assert report["result"] == "fail"


def test_behavioral_is_separate_manual_and_api_key_only():
    path = ROOT / ".github/workflows/behavioral.yml"
    data = workflow(path)
    assert set(data["on"]) == {"workflow_dispatch"}
    assert data["permissions"] == {"contents": "read"}
    assert data["on"]["workflow_dispatch"]["inputs"]["authorized"]["default"] == "false"
    job = data["jobs"]["review"]
    assert job["environment"] == "behavioral-review"
    assert job["name"] not in [job["name"] for job in workflow()["jobs"].values()]
    text = path.read_text()
    assert "--auth-mode api-key" in text and "chatgpt-cache-local" not in text
    assert "--model gpt-5.6-luna --reasoning-effort high" in text
    assert 'test "$REVIEWED_SOURCE" = "$GITHUB_SHA"' in text
    assert 'test "$GITHUB_REF" = refs/heads/main' in text
    assert "not-run" in text


def test_behavioral_missing_configuration_is_an_explicit_non_run(tmp_path):
    step = workflow(ROOT / ".github/workflows/behavioral.yml")["jobs"]["review"]["steps"][0]
    env = {**os.environ, "AUTHORIZED": "false", "API_KEY": "", "ENABLED": "false",
           "AUTHORIZATION_REFERENCE": "", "GITHUB_OUTPUT": (tmp_path / "outputs").as_posix()}
    process = subprocess.run([bash(), "-e", "-c", step["run"]], cwd=tmp_path, env=env)
    assert process.returncode == 0
    report = json.loads((tmp_path / ".devquitect-reports/not-run.json").read_text())
    assert report["verdict"] == "not-run"
    assert report["observed_runtime"] is None and report["reports"] == []
    assert (tmp_path / "outputs").read_text().strip() == "ready=false"


@pytest.mark.parametrize("source,ref,exit_code", [
    ("a" * 40, "refs/heads/main", 0),
    ("b" * 40, "refs/heads/main", 1),
    ("main", "refs/heads/main", 1),
    ("a" * 40, "refs/heads/topic", 1),
])
def test_behavioral_preflight_requires_exact_reviewed_main_sha(tmp_path, source, ref, exit_code):
    step = workflow(ROOT / ".github/workflows/behavioral.yml")["jobs"]["review"]["steps"][0]
    env = {**os.environ, "AUTHORIZED": "true", "API_KEY": "fixture", "ENABLED": "true",
           "AUTHORIZATION_REFERENCE": "fixture-authorization", "REVIEWED_SOURCE": source,
           "GITHUB_REF": ref, "GITHUB_SHA": "a" * 40,
           "GITHUB_OUTPUT": (tmp_path / "outputs").as_posix()}
    process = subprocess.run([bash(), "-e", "-c", step["run"]], cwd=tmp_path, env=env)
    assert process.returncode == exit_code
    if exit_code == 0:
        assert (tmp_path / "outputs").read_text().strip() == "ready=true"
