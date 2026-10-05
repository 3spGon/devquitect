"""Bounded transport/provenance cases, entirely credential-free."""

from __future__ import annotations

import hashlib
import io
import json
import stat
import urllib.error
import zipfile
from email.message import Message

import pytest

from devquitect_quality import github_evidence as gh

SOURCE = "a" * 40
REPOSITORY = "owner/repo"
BASE = f"{gh.API}/repos/{REPOSITORY}/actions"


def archive(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        for name, content in members:
            zipped.writestr(name, content)
    return buffer.getvalue()


def job_rows(source=SOURCE):
    return [dict(id=i, name=name, run_id=42, run_attempt=2, head_sha=source,
                 status="completed", conclusion="success",
                 started_at="2026-10-05T00:00:00Z", completed_at="2026-10-05T01:00:00Z")
            for i, name in enumerate(gh.JOBS.values(), 1)]


@pytest.fixture
def transport(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "fixture-read-only")
    client = gh.GitHubEvidence()
    run = dict(id=42, run_attempt=2, head_sha=SOURCE, event="push", head_branch="main",
               status="completed", conclusion="success", workflow_id=7, path=gh.WORKFLOW,
               repository={"full_name": REPOSITORY})
    artifacts, downloads = [], {}
    for i, prefix in enumerate(("quality", "platform-smoke-Linux", "platform-smoke-macOS",
                                "platform-smoke-Windows", "package", "package-diagnostics"), 11):
        raw = archive([("ci-evidence.json" if prefix == "package" else "identity.json", "{}")])
        url = f"{BASE}/artifacts/{i}/zip"
        downloads[url] = raw
        artifacts.append(dict(id=i, name=f"{prefix}-{SOURCE}-attempt-2", expired=False,
                              created_at="2026-10-05T00:30:00Z", expires_at="2099-01-01T00:00:00Z",
                              size_in_bytes=len(raw),
                              digest=f"sha256:{hashlib.sha256(raw).hexdigest()}",
                              archive_download_url=url,
                              workflow_run={"id": 42, "head_sha": SOURCE, "head_branch": "main"}))
    metadata = {
        f"{BASE}/runs/42/attempts/2": run,
        f"{BASE}/workflows/7": {"path": gh.WORKFLOW},
        f"{BASE}/runs/42/attempts/2/jobs?per_page=100&page=1": {
            "total_count": 6, "jobs": job_rows(),
        },
        f"{BASE}/runs/42/artifacts?per_page=100&page=1": {
            "total_count": 6, "artifacts": artifacts,
        },
    }
    calls = []

    def request(url, *, storage=False):
        calls.append((url, storage))
        return (json.dumps(metadata[url]).encode() if url in metadata else downloads[url]), {}

    monkeypatch.setattr(client, "_request", request)
    return client, metadata, downloads, calls


def test_complete_authenticated_attempt_collects_six_distinct_artifacts(transport, tmp_path):
    client, _, _, calls = transport
    observation = client.collect(REPOSITORY, SOURCE, 42, 2, tmp_path)
    assert len(observation["jobs"]) == len(observation["artifacts"]) == 6
    assert observation["workflow_commit"] == SOURCE
    assert (tmp_path / "package/ci-evidence.json").is_file()
    assert len(calls) == 10


@pytest.mark.parametrize("field,value", [
    ("head_sha", "b" * 40), ("run_attempt", 1), ("event", "pull_request"),
    ("head_branch", "topic"), ("conclusion", "failure"), ("status", "in_progress"),
    ("repository", {"full_name": "other/repo"}), ("path", ".github/workflows/evil.yml"),
    ("repository", None), ("path", None),
])
def test_collect_rejects_wrong_candidate_run_or_workflow(transport, tmp_path, field, value):
    client, metadata, _, _ = transport
    metadata[f"{BASE}/runs/42/attempts/2"][field] = value
    with pytest.raises(gh.EvidencePolicyError):
        client.collect(REPOSITORY, SOURCE, 42, 2, tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("bad", ["partial", "attempt", "cancelled", "skipped", "duplicate"])
def test_complete_jobs_cannot_mix_partial_reruns(bad):
    jobs = job_rows()
    if bad == "partial":
        jobs.pop()
    elif bad == "attempt":
        jobs[1]["run_attempt"] = 1
    elif bad == "duplicate":
        jobs[1] = jobs[0]
    else:
        jobs[1]["conclusion"] = bad
    with pytest.raises(gh.EvidencePolicyError):
        gh.validate_jobs(jobs, SOURCE, 42, 2)


@pytest.mark.parametrize("bad", ["missing", "expired", "digest", "altered", "time", "url"])
def test_collect_rejects_unavailable_or_tampered_artifacts(transport, tmp_path, bad):
    client, metadata, downloads, _ = transport
    rows = metadata[f"{BASE}/runs/42/artifacts?per_page=100&page=1"]["artifacts"]
    if bad == "missing":
        rows.pop()
        metadata[f"{BASE}/runs/42/artifacts?per_page=100&page=1"]["total_count"] = 5
    elif bad == "expired":
        rows[0]["expires_at"] = "2020-01-01T00:00:00Z"
    elif bad == "digest":
        rows[0].pop("digest")
    elif bad == "altered":
        downloads[rows[0]["archive_download_url"]] += b"tamper"
    elif bad == "time":
        rows[0]["created_at"] = "2026-10-04T00:00:00Z"
    else:
        rows[0]["archive_download_url"] = "https://evil.invalid/download"
    with pytest.raises(gh.EvidencePolicyError):
        client.collect(REPOSITORY, SOURCE, 42, 2, tmp_path)


@pytest.mark.parametrize("name", ["../escape", "/escape", "C:/escape", "a\\b", "evil.py"])
def test_archive_rejects_unsafe_and_unexpected_members(tmp_path, name):
    with pytest.raises(gh.EvidencePolicyError):
        gh.extract_archive(archive([(name, "data")]), tmp_path, "quality")
    assert not list(tmp_path.iterdir())


def test_archive_rejects_duplicate_symlink_and_all_limits(tmp_path, monkeypatch):
    with pytest.raises(gh.EvidencePolicyError, match="limits"):
        gh.extract_archive(archive([(f"member-{i}.json", "") for i in range(1025)]),
                           tmp_path, "quality")
    with pytest.warns(UserWarning), pytest.raises(gh.EvidencePolicyError):
        gh.extract_archive(archive([("identity.json", "a"), ("identity.json", "b")]),
                           tmp_path, "quality")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        info = zipfile.ZipInfo("identity.json")
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        zipped.writestr(info, "target")
    with pytest.raises(gh.EvidencePolicyError):
        gh.extract_archive(buffer.getvalue(), tmp_path, "quality")
    raw = archive([("identity.json", "x" * 10)])
    monkeypatch.setattr(gh, "MAX_EXPANDED", 5)
    with pytest.raises(gh.EvidencePolicyError):
        gh.extract_archive(raw, tmp_path, "quality")
    monkeypatch.setattr(gh, "MAX_COMPRESSED", 5)
    with pytest.raises(gh.EvidencePolicyError):
        gh.extract_archive(raw, tmp_path, "quality")
    with pytest.raises(gh.EvidencePolicyError):
        gh.extract_archive(b"not zip", tmp_path, "quality")


def test_pagination_is_complete_and_rejects_duplicate_or_changing_totals(transport, monkeypatch):
    client, _, _, _ = transport
    pages = [{"total_count": 2, "jobs": [{"id": 1}]},
             {"total_count": 2, "jobs": [{"id": 2}]}]
    monkeypatch.setattr(client, "json", lambda _: pages.pop(0))
    assert client.pages(BASE, "jobs") == [{"id": 1}, {"id": 2}]
    for second in ({"total_count": 2, "jobs": [{"id": 1}]},
                   {"total_count": 3, "jobs": [{"id": 2}]},
                   {"total_count": 2, "jobs": []}):
        pages[:] = [{"total_count": 2, "jobs": [{"id": 1}]}, second]
        with pytest.raises(gh.EvidencePolicyError):
            client.pages(BASE, "jobs")


@pytest.mark.parametrize("status,exception", [(404, gh.EvidencePolicyError),
                                             (410, gh.EvidencePolicyError),
                                             (403, gh.EvidenceUnavailableError),
                                             (503, gh.EvidenceUnavailableError)])
def test_http_status_distinguishes_policy_from_unavailability(monkeypatch, status, exception):
    monkeypatch.setenv("GH_TOKEN", "fixture")
    monkeypatch.setattr(gh.time, "sleep", lambda _: None)
    client = gh.GitHubEvidence()
    calls = []

    def open(request, timeout):
        calls.append((request, timeout))
        raise urllib.error.HTTPError(request.full_url, status, "test", {}, None)

    monkeypatch.setattr(client.opener, "open", open)
    with pytest.raises(exception):
        client._request(BASE)
    assert len(calls) == (4 if status == 503 else 1)
    assert all(timeout == 30 for _, timeout in calls)


def test_transient_retry_can_recover_and_metadata_redirect_is_rejected(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "fixture")
    monkeypatch.setattr(gh.time, "sleep", lambda _: None)
    client = gh.GitHubEvidence()
    calls = []

    class Response(io.BytesIO):
        headers = {}

    def open(request, timeout):
        calls.append(request)
        if len(calls) < 3:
            raise urllib.error.URLError("temporary")
        return Response(b"{}")

    monkeypatch.setattr(client.opener, "open", open)
    assert client.json(BASE) == {} and len(calls) == 3
    monkeypatch.setattr(client, "_request", lambda _: (b"", {"Location": "https://storage.invalid"}))
    with pytest.raises(gh.EvidencePolicyError):
        client.json(BASE)


@pytest.mark.parametrize("url", ["http://storage.invalid/file", "https://user@storage.invalid/file",
                                 "https://storage.invalid:444/file", "file:///etc/passwd"])
def test_redirect_policy_rejects_unsafe_storage_urls(monkeypatch, url):
    monkeypatch.setenv("GH_TOKEN", "fixture")
    client = gh.GitHubEvidence()
    with pytest.raises(gh.EvidencePolicyError):
        client._request(url, storage=True)


def test_api_issued_redirect_never_forwards_token_to_storage(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "fixture-secret")
    client = gh.GitHubEvidence()
    calls = []
    content = b"verified zip bytes"
    location = "https://storage.invalid/signed"

    class Response(io.BytesIO):
        headers = {}

    def open(request, timeout):
        calls.append(request)
        if request.full_url.startswith(gh.API):
            headers = Message()
            headers["Location"] = location
            raise urllib.error.HTTPError(request.full_url, 302, "redirect", headers, None)
        return Response(content)

    monkeypatch.setattr(client.opener, "open", open)
    assert client.download(BASE, f"sha256:{hashlib.sha256(content).hexdigest()}") == content
    assert calls[0].get_header("Authorization") == "Bearer fixture-secret"
    assert calls[1].get_header("Authorization") is None
    assert isinstance(client.opener, urllib.request.OpenerDirector)


def test_missing_token_and_non_api_urls_cannot_verify(monkeypatch):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    with pytest.raises(gh.EvidenceUnavailableError):
        gh.GitHubEvidence()
    monkeypatch.setenv("GH_TOKEN", "fixture")
    with pytest.raises(gh.EvidencePolicyError):
        gh.GitHubEvidence()._request("https://evil.invalid/metadata")


def test_timestamp_and_json_validation_are_fail_closed(tmp_path):
    for value in (None, "bad", "2026-10-05"):
        with pytest.raises(gh.EvidencePolicyError):
            gh.timestamp(value)
    for value in ("[]", "null", "bad"):
        path = tmp_path / "report.json"
        path.write_text(value)
        with pytest.raises(gh.EvidencePolicyError):
            gh.read_json(path)
