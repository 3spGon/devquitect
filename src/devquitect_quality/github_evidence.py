"""Read-only, bounded GitHub Actions evidence transport for release readiness."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import stat
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

API = "https://api.github.com"
WORKFLOW = ".github/workflows/ci.yml"
SHA = re.compile(r"[0-9a-f]{40}")
MAX_COMPRESSED = 64 * 1024 * 1024
MAX_EXPANDED = 128 * 1024 * 1024
JOBS = {
    "quality": "Devquitect / quality",
    "Linux": "Devquitect / platform-smoke (ubuntu-latest)",
    "macOS": "Devquitect / platform-smoke (macos-latest)",
    "Windows": "Devquitect / platform-smoke (windows-latest)",
    "aggregate": "Devquitect / platform-smoke",
    "package": "Devquitect / package",
}


class EvidencePolicyError(ValueError):
    """Observed evidence cannot qualify the candidate."""


class EvidenceConfigurationError(ValueError):
    """Unsupported candidate selection or local configuration."""


class EvidenceUnavailableError(RuntimeError):
    """Authenticated verification could not be performed."""


def timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError
        return parsed
    except (ValueError, AttributeError) as error:
        raise EvidencePolicyError("invalid evidence timestamp") from error


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", value
    ):
        raise EvidencePolicyError("unsafe evidence path")
    if any(part in {".", ".."} for part in value.split("/")):
        raise EvidencePolicyError("unsafe evidence path")
    return value


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError
        return value
    except (OSError, UnicodeError, ValueError) as error:
        raise EvidencePolicyError(f"invalid evidence JSON: {path.name}") from error


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class GitHubEvidence:
    """Fetch observations from authenticated endpoints, never an imported registry."""

    def __init__(self) -> None:
        self.token = os.environ.get("GH_TOKEN")
        if not self.token:
            raise EvidenceUnavailableError("read-only GH_TOKEN is required")
        self.opener = urllib.request.build_opener(_NoRedirect())

    def _request(self, url: str, *, storage: bool = False) -> tuple[bytes, Any]:
        parsed = urllib.parse.urlsplit(url)
        if (
            parsed.scheme != "https" or parsed.username or parsed.password or parsed.fragment
            or not parsed.hostname or parsed.port not in {None, 443}
            or (not storage and parsed.netloc != "api.github.com")
        ):
            raise EvidencePolicyError("unsafe API URL or redirect")
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"}
        if not storage:
            headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(4):  # Initial request plus at most three transient retries.
            try:
                request = urllib.request.Request(url, headers=headers)
                with self.opener.open(request, timeout=30) as response:
                    data = response.read(MAX_COMPRESSED + 1)
                    if len(data) > MAX_COMPRESSED:
                        raise EvidencePolicyError("artifact exceeds compressed size limit")
                    return data, response.headers
            except urllib.error.HTTPError as error:
                if error.code in {301, 302, 303, 307, 308}:
                    if storage:
                        raise EvidencePolicyError("storage redirect is not API-issued") from None
                    return b"", error.headers
                if error.code in {404, 410}:
                    raise EvidencePolicyError("required evidence is missing or expired") from None
                if error.code not in {429, 500, 502, 503, 504} or attempt == 3:
                    raise EvidenceUnavailableError(f"GitHub HTTP {error.code}") from None
            except (urllib.error.URLError, TimeoutError, OSError):
                if attempt == 3:
                    raise EvidenceUnavailableError("GitHub transport unavailable") from None
            time.sleep(2 ** attempt)
        raise AssertionError("unreachable retry state")

    def json(self, url: str) -> dict[str, Any]:
        raw, headers = self._request(url)
        if headers.get("Location"):
            raise EvidencePolicyError("metadata redirects are unsupported")
        try:
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise ValueError
            return value
        except (ValueError, UnicodeError) as error:
            raise EvidenceUnavailableError("GitHub returned malformed metadata") from error

    def pages(self, url: str, field: str) -> list[dict[str, Any]]:
        rows = []
        total = None
        for page in range(1, 101):
            value = self.json(f"{url}?per_page=100&page={page}")
            count, batch = value.get("total_count"), value.get(field)
            if (
                type(count) is not int or count < 0 or count > 10000
                or not isinstance(batch, list) or len(batch) > 100
                or (total is not None and count != total)
                or any(not isinstance(row, dict) for row in batch)
            ):
                raise EvidencePolicyError("invalid or changing pagination")
            total = count
            rows.extend(batch)
            ids = [row.get("id") for row in rows]
            if any(type(id) is not int or id <= 0 for id in ids) or len(set(ids)) != len(ids):
                raise EvidencePolicyError("duplicate or invalid paginated IDs")
            if len(rows) == total:
                return rows
            if len(rows) > total or not batch:
                raise EvidencePolicyError("incomplete pagination")
        raise EvidencePolicyError("pagination exceeds limit")

    def download(self, url: str, expected_digest: str) -> bytes:
        if not isinstance(expected_digest, str) or not re.fullmatch(
            r"sha256:[0-9a-f]{64}", expected_digest
        ):
            raise EvidencePolicyError("missing or invalid artifact-container digest")
        raw, headers = self._request(url)
        location = headers.get("Location")
        if location:
            # Only this authenticated API response may authorize a storage URL.
            raw, _ = self._request(location, storage=True)
        if f"sha256:{hashlib.sha256(raw).hexdigest()}" != expected_digest:
            raise EvidencePolicyError("artifact-container digest mismatch")
        return raw

    def collect(
        self, repository: str, source: str, run_id: int, attempt: int, root: Path
    ) -> dict[str, Any]:
        base = f"{API}/repos/{repository}/actions"
        run = self.json(f"{base}/runs/{run_id}/attempts/{attempt}")
        if not isinstance(run.get("repository"), dict) or not isinstance(run.get("path"), str):
            raise EvidencePolicyError("malformed CI run provenance")
        if any(run.get(key) != expected for key, expected in {
            "id": run_id, "run_attempt": attempt, "head_sha": source,
            "event": "push", "head_branch": "main", "status": "completed",
            "conclusion": "success",
        }.items()) or run.get("repository", {}).get("full_name") != repository:
            raise EvidencePolicyError("CI run provenance or conclusion mismatch")
        workflow_id = run.get("workflow_id")
        if type(workflow_id) is not int or workflow_id <= 0:
            raise EvidencePolicyError("invalid workflow ID")
        workflow = self.json(f"{base}/workflows/{workflow_id}")
        if workflow.get("path") != WORKFLOW or run.get("path", "").split("@")[0] != WORKFLOW:
            raise EvidencePolicyError("unexpected CI workflow")
        jobs = self.pages(f"{base}/runs/{run_id}/attempts/{attempt}/jobs", "jobs")
        validate_jobs(jobs, source, run_id, attempt)
        artifacts = self.pages(f"{base}/runs/{run_id}/artifacts", "artifacts")
        selected = []
        for kind in ("quality", "Linux", "macOS", "Windows", "package", "diagnostics"):
            prefix = (f"platform-smoke-{kind}" if kind in {"Linux", "macOS", "Windows"}
                      else "package-diagnostics" if kind == "diagnostics" else kind)
            name = f"{prefix}-{source}-attempt-{attempt}"
            matching = [row for row in artifacts if row.get("name") == name]
            if len(matching) != 1:
                raise EvidencePolicyError(f"missing or ambiguous artifact: {prefix}")
            row = matching[0]
            producer = next(job for job in jobs if job["name"] == JOBS.get(kind, JOBS["package"]))
            validate_artifact(row, producer, source, run_id)
            url = f"{base}/artifacts/{row['id']}/zip"
            if row.get("archive_download_url") != url:
                raise EvidencePolicyError("unexpected artifact download URL")
            raw = self.download(url, row.get("digest"))
            target = root / kind
            target.mkdir()
            extract_archive(raw, target, kind)
            selected.append({**row, "kind": kind})
        return {
            "repository": repository, "source_commit": source, "workflow_path": WORKFLOW,
            "workflow_commit": source, "run_id": run_id, "run_attempt": attempt,
            "jobs": jobs, "artifacts": selected,
        }


def validate_jobs(jobs: list[dict[str, Any]], source: str, run_id: int, attempt: int) -> None:
    if any(not isinstance(row.get("name"), str) for row in jobs):
        raise EvidencePolicyError("invalid mandatory job name")
    if len(jobs) != len(JOBS) or {row.get("name") for row in jobs} != set(JOBS.values()):
        raise EvidencePolicyError("CI attempt is partial or has unexpected jobs")
    for job in jobs:
        if any(job.get(key) != value for key, value in {
            "head_sha": source, "run_id": run_id, "run_attempt": attempt,
            "status": "completed", "conclusion": "success",
        }.items()) or timestamp(job.get("started_at")) > timestamp(job.get("completed_at")):
            raise EvidencePolicyError("mandatory job failed or belongs to another attempt")


def validate_artifact(row: dict, job: dict, source: str, run_id: int) -> None:
    workflow = row.get("workflow_run", {})
    if not isinstance(workflow, dict):
        raise EvidencePolicyError("invalid artifact provenance")
    if (
        row.get("expired") is not False
        or timestamp(row.get("expires_at")) <= datetime.now(UTC)
        or not (timestamp(job.get("started_at")) <= timestamp(row.get("created_at"))
                <= timestamp(job.get("completed_at")))
        or workflow.get("id") != run_id or workflow.get("head_sha") != source
        or workflow.get("head_branch") != "main"
        or type(row.get("size_in_bytes")) is not int
        or not 0 < row["size_in_bytes"] <= MAX_COMPRESSED
    ):
        raise EvidencePolicyError("expired, oversized or mixed-attempt artifact")


def extract_archive(raw: bytes, root: Path, kind: str) -> None:
    """Validate the entire container before materializing any member."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if len(raw) > MAX_COMPRESSED or not 0 < len(entries) <= 1024:
                raise EvidencePolicyError("archive limits exceeded")
            names = [safe_relative(entry.filename) for entry in entries]
            if (len(set(names)) != len(names)
                or sum(entry.file_size for entry in entries) > MAX_EXPANDED):
                raise EvidencePolicyError("duplicate entries or expanded size limit exceeded")
            for entry in entries:
                mode = entry.external_attr >> 16
                if stat.S_IFMT(mode) not in {0, stat.S_IFREG} or entry.flag_bits & 1:
                    raise EvidencePolicyError("unsupported archive entry or symlink")
                name = entry.filename
                allowed = (
                    bool(re.fullmatch(
                        r"devquitect-[0-9]+\.[0-9]+\.[0-9]+\.(zip|manifest\.json)", name
                    ))
                    or name in {"package.json", "ci-evidence.json"}
                ) if kind == "package" else (
                    name in {"identity.json", "result.json", "check.json"}
                    or bool(re.fullmatch(
                        r"steps/(identity|check|ruff|whitespace|smoke|build-first|build-second|index)"
                        r"\.json", name
                    ))
                )
                if not allowed:
                    raise EvidencePolicyError("unexpected archive member")
            for entry in entries:
                path = root / entry.filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(archive.read(entry))
    except (zipfile.BadZipFile, RuntimeError, EOFError) as error:
        raise EvidencePolicyError("invalid artifact archive") from error


def validate_selection(
    checkout: Path, source: str, repository: str, run_id: int, attempt: int,
    previous_release: str | None, evidence: Path, output: Path,
) -> None:
    if (
        not SHA.fullmatch(source) or not previous_release or not SHA.fullmatch(previous_release)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
        or type(run_id) is not int or run_id <= 0 or type(attempt) is not int or attempt <= 0
    ):
        raise EvidenceConfigurationError("CI requires full SHAs, owner/repo, positive run/attempt")
    if (not evidence.is_dir() or evidence.is_symlink() or any(evidence.iterdir())
        or output.exists() or output.is_symlink()):
        raise EvidenceConfigurationError("CI evidence must be empty and output must not exist")
    if evidence.resolve() == output.resolve() or evidence.resolve() in output.resolve().parents:
        raise EvidenceConfigurationError("output and evidence roots must be separate")
    try:
        remote = subprocess.check_output(
            ["git", "-C", str(checkout), "remote", "get-url", "origin"], text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as error:
        raise EvidenceConfigurationError("checkout needs a GitHub origin remote") from error
    if remote not in {f"https://github.com/{repository}.git", f"https://github.com/{repository}",
                      f"git@github.com:{repository}.git", f"ssh://git@github.com/{repository}.git"}:
        raise EvidenceConfigurationError("repository does not match checkout origin")
