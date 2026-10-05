"""Manual readiness workflow and failure-report contracts."""

import json
import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/release-readiness.yml"


def workflow():
    return yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)


def test_readiness_is_manual_read_only_locked_and_does_not_publish():
    value = workflow()
    assert set(value["on"]) == {"workflow_dispatch"}
    assert set(value["on"]["workflow_dispatch"]["inputs"]) == {
        "candidate_sha", "version", "ci_run_id", "ci_run_attempt", "previous_release_sha",
    }
    assert value["permissions"] == {"contents": "read", "actions": "read"}
    steps = value["jobs"]["readiness"]["steps"]
    checkout = next(s for s in steps if s.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"] == {"ref": "${{ inputs.candidate_sha }}", "fetch-depth": "0",
                                "persist-credentials": "false"}
    text = WORKFLOW.read_text()
    assert "uv sync --locked --all-groups" in text
    assert 'test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"' in text
    for forbidden in ("contents: write", "actions: write", "git push", "git tag",
                      "gh release", "--behavioral", "devquitect eval", "devquitect compare"):
        assert forbidden not in text
    for step in steps:
        if "uses" in step:
            assert re.fullmatch(r"[A-Za-z0-9_/-]+@[0-9a-f]{40}", step["uses"])
        assert "${{ inputs." not in step.get("run", "")
    call = next(s for s in steps if "devquitect release-check" in s.get("run", ""))
    assert call["env"] == {"GH_TOKEN": "${{ github.token }}"}
    assert '"$GH_TOKEN"' not in call["run"]
    for option in ("repository", "ci-run-id", "ci-run-attempt", "previous-release"):
        assert f"--{option}" in call["run"]
    upload = steps[-1]
    assert upload["if"] == "${{ always() }}"
    assert upload["with"]["retention-days"] == "30"


@pytest.mark.parametrize("bad", ["source", "version", "attempt", "ref", "baseline", None])
def test_workflow_preflight_validates_inputs_without_shell_interpolation(tmp_path, bad):
    env = {**os.environ, "GITHUB_REF": "refs/heads/main", "CANDIDATE_SHA": "a" * 40,
           "PREVIOUS_RELEASE_SHA": "b" * 40, "CANDIDATE_VERSION": "1.0.0",
           "CI_RUN_ID": "42", "CI_RUN_ATTEMPT": "1"}
    if bad:
        field = {"source": "CANDIDATE_SHA", "version": "CANDIDATE_VERSION",
                 "attempt": "CI_RUN_ATTEMPT", "ref": "GITHUB_REF",
                 "baseline": "PREVIOUS_RELEASE_SHA"}[bad]
        env[field] = "$(touch injected)"
    # These scripts are pure Python heredocs, so no platform-specific shell is needed.
    script = workflow()["jobs"]["readiness"]["steps"][0]["run"].split("<<'PY'\n")[1]
    script = script.rsplit("\nPY", 1)[0]
    import sys

    process = subprocess.run([sys.executable, "-c", script], env=env, cwd=tmp_path, check=False)
    assert process.returncode == (2 if bad else 0)
    assert not (tmp_path / "injected").exists()
    if bad:
        report = json.loads((tmp_path / ".devquitect-reports/release-readiness.json").read_text())
        schema = json.loads((ROOT / "schemas/report.schema.json").read_text())
        Draft202012Validator(schema).validate(report)
        assert report["result"] == "fail" and report["evidence_manifest"] == []
