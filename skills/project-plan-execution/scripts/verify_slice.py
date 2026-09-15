#!/usr/bin/env python3
"""Validate and close evidence for an approved delivery slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

EXIT_INVALID = 1
EXIT_UNSUPPORTED = 2
FRONTMATTER = re.compile(r"\A---\n(?P<data>.*?)\n---\n(?P<body>.*)\Z", re.S)


class DuplicateKeyLoader(yaml.SafeLoader):
    pass


class ConcurrentChangeError(RuntimeError):
    """A validated input changed before the atomic checkpoint replacement."""


def _mapping(
    loader: DuplicateKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


DuplicateKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _load_yaml(text: str, label: str) -> Any:
    try:
        return yaml.load(text, Loader=DuplicateKeyLoader)
    except (yaml.YAMLError, ValueError) as exc:
        raise ValueError(f"invalid YAML in {label}: {exc}") from exc


def _frontmatter(path: Path) -> tuple[dict[str, Any], str, bytes]:
    raw = path.read_bytes()
    match = FRONTMATTER.match(raw.decode("utf-8"))
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    data = _load_yaml(match.group("data"), str(path))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return data, match.group("body"), raw


def _repo_root(session: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(session), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError("Git repository is required")
    return Path(result.stdout.strip()).resolve()


def _relative(root: Path, value: str, *, allow_missing: bool = False) -> Path:
    raw = PurePosixPath(value)
    if not value or raw.is_absolute() or ".." in raw.parts:
        raise ValueError(f"unsafe path: {value!r}")
    path = root
    for part in raw.parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f"symlinks are unsupported: {value}")
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {value!r}") from exc
    if not allow_missing and not path.exists():
        raise ValueError(f"missing path: {value}")
    return path


def _plan(session: Path) -> tuple[dict[str, Any], str, Path, int, str]:
    plan_path = session / "08-implementation-plan.md"
    text = plan_path.read_text(encoding="utf-8")
    status_match = re.search(r"^Status:\s*(\S+)\s*$", text, re.M)
    revision_match = re.search(r"^Plan revision:\s*(\d+)\s*$", text, re.M)
    if not status_match or status_match.group(1) != "Approved":
        raise ValueError("plan is not Approved")
    if not revision_match or int(revision_match.group(1)) < 1:
        raise ValueError("plan revision is missing or invalid")
    match = re.search(r"```devquitect-verification\s*\n(.*?)\n```", text, re.S)
    if not match:
        raise ValueError("plan is missing devquitect-verification inventory")
    inventory = _load_yaml(match.group(1), str(plan_path))
    if not isinstance(inventory, dict) or inventory.get("schema_version") != 1:
        raise ValueError("unsupported verification inventory")
    _validate_inventory(inventory)
    return inventory, text, plan_path, int(revision_match.group(1)), status_match.group(1)


def _validate_inventory(inventory: dict[str, Any]) -> None:
    slices = inventory.get("slices")
    if not isinstance(slices, dict) or not slices:
        raise ValueError("verification inventory must contain slices")
    slice_ids = set(slices)
    for slice_id, spec in slices.items():
        if not isinstance(slice_id, str) or not re.fullmatch(r"SLICE-[A-Za-z0-9][A-Za-z0-9_-]*", slice_id):
            raise ValueError(f"invalid slice ID: {slice_id!r}")
        if not isinstance(spec, dict):
            raise ValueError(f"slice {slice_id} must be a mapping")
        dependencies = spec.get("depends_on")
        if not isinstance(dependencies, list) or any(
            not isinstance(dependency, str) for dependency in dependencies
        ):
            raise ValueError(f"slice {slice_id} dependencies must be a list of IDs")
        if any(dependency not in slice_ids for dependency in dependencies):
            raise ValueError(f"slice {slice_id} has an unknown dependency")
        criteria = spec.get("criteria")
        if not isinstance(criteria, dict) or not criteria:
            raise ValueError(f"slice {slice_id} must declare criteria")
        for criterion_id, criterion in criteria.items():
            if not isinstance(criterion_id, str) or not isinstance(criterion, dict):
                raise ValueError(f"slice {slice_id} has invalid criteria")
            if not isinstance(criterion.get("text"), str) or not criterion["text"].strip():
                raise ValueError(f"criterion {criterion_id} must have text")
            if not isinstance(criterion.get("requirement"), str) or not criterion["requirement"].strip():
                raise ValueError(f"criterion {criterion_id} must have a requirement")
        checks = spec.get("checks")
        if not isinstance(checks, dict) or not checks:
            raise ValueError(f"slice {slice_id} must declare checks")
        for check_id, check in checks.items():
            if (
                not isinstance(check_id, str)
                or not isinstance(check, dict)
                or not isinstance(check.get("command"), str)
                or not check["command"].strip()
                or not isinstance(check.get("cwd"), str)
                or not check["cwd"].strip()
                or PurePosixPath(check["cwd"]).is_absolute()
                or ".." in PurePosixPath(check["cwd"]).parts
            ):
                raise ValueError(f"check {check_id} has invalid command or cwd")
        inputs = spec.get("inputs")
        if not isinstance(inputs, list) or any(not isinstance(value, str) for value in inputs):
            raise ValueError(f"slice {slice_id} inputs must be a list of paths")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(slice_id: str) -> None:
        if slice_id in visiting:
            raise ValueError("verification inventory contains a dependency cycle")
        if slice_id in visited:
            return
        visiting.add(slice_id)
        for dependency in slices[slice_id]["depends_on"]:
            visit(dependency)
        visiting.remove(slice_id)
        visited.add(slice_id)

    for slice_id in slices:
        visit(slice_id)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_ignored(root: Path, path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "--no-index", "--quiet", "--", str(path)],
        capture_output=True,
    )
    return result.returncode == 0


def _input_inventory(root: Path, session: Path, inputs: list[Any]) -> list[dict[str, str]]:
    files: dict[str, Path | None] = {}
    session_rel = session.relative_to(root).as_posix()
    excluded = {f"{session_rel}/09-delivery-status.md"}
    for declared in inputs:
        if not isinstance(declared, str):
            raise ValueError("inputs must contain relative paths")
        target = _relative(root, declared, allow_missing=True)
        if not target.exists():
            files[declared] = None
            continue
        if target.is_dir():
            all_paths = sorted(target.rglob("*"))
            for candidate in all_paths:
                if candidate.is_symlink():
                    raise ValueError(f"symlinks are unsupported: {candidate.relative_to(root)}")
            candidates = [p for p in all_paths if p.is_file()]
            explicit_file = False
        else:
            candidates = [target]
            explicit_file = True
        for candidate in candidates:
            rel = candidate.relative_to(root).as_posix()
            if (
                rel in excluded
                or rel.startswith(f"{session_rel}/slices/")
                or rel.startswith(".git/")
                or any(part in {"__pycache__", ".pytest_cache"} for part in Path(rel).parts)
                or Path(rel).name == ".DS_Store"
                or rel.startswith(".devquitect-reports/")
            ):
                continue
            if candidate.is_symlink():
                raise ValueError(f"symlinks are unsupported: {rel}")
            if not explicit_file and _git_ignored(root, candidate):
                continue
            files[rel] = candidate
    records: list[dict[str, str]] = []
    for rel in sorted(files):
        path = files[rel]
        if path is None:
            records.append({"path": rel, "kind": "absent", "mode": "", "sha256": ""})
            continue
        mode = "executable" if os.access(path, os.X_OK) else "regular"
        records.append(
            {"path": rel, "kind": "file", "mode": mode, "sha256": _sha256(path.read_bytes())}
        )
    return records


def _digest(records: list[dict[str, str]]) -> str:
    return _sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode())


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _detail(session: Path, slice_id: str) -> tuple[dict[str, Any], str, bytes]:
    return _frontmatter(session / "slices" / f"{slice_id}.md")


def _definition(session: Path) -> dict[str, Any]:
    definition, _, _ = _frontmatter(session / "00-status.md")
    for key, expected in {
        "phase": "complete",
        "phase_status": "complete",
        "gate_1": "approved",
        "gate_2": "approved",
    }.items():
        if definition.get(key) != expected:
            raise ValueError(f"definition.{key} must be {expected!r}")
    return definition


def _timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed


def _validate(
    session: Path, slice_id: str
) -> tuple[dict[str, Any], list[dict[str, str]], dict[str, Any], Path, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    try:
        inventory, plan_text, plan_path, plan_revision, _ = _plan(session)
        root = _repo_root(session)
        try:
            _definition(session)
        except ValueError as exc:
            issues.append(_issue("definition.invalid", "00-status.md", str(exc)))
        tracker_path = session / "09-delivery-status.md"
        tracker, _, tracker_bytes = _frontmatter(tracker_path)
        slice_plan = inventory.get("slices", {}).get(slice_id)
        if not isinstance(slice_plan, dict):
            issues.append(
                _issue("slice.unknown", f"plan.slices.{slice_id}", "slice is not declared")
            )
            return tracker, issues, {}, plan_path, []
        if tracker.get("plan_revision") != plan_revision:
            issues.append(
                _issue(
                    "plan.revision",
                    "tracker.plan_revision",
                    f"tracker does not match approved plan revision {plan_revision}",
                )
            )
        if slice_id not in tracker.get("authorized_slices", []):
            issues.append(
                _issue("slice.unauthorized", "tracker.authorized_slices", "slice is not authorized")
            )
        slice_state = tracker.get("slices", {}).get(slice_id, {})
        if slice_state.get("acceptance") == "pending":
            issues.append(
                _issue(
                    "acceptance.pending",
                    f"tracker.slices.{slice_id}.acceptance",
                    "required acceptance is still pending",
                )
            )
        plan_digest = _sha256(plan_text.encode())
        try:
            detail, _, _ = _detail(session, slice_id)
        except (OSError, ValueError) as exc:
            issues.append(_issue("detail.invalid", f"slices/{slice_id}.md", str(exc)))
            return tracker, issues, {}, plan_path, []
        if (
            detail.get("schema_version") != 1
            or detail.get("session") != session.name
            or detail.get("slice") != slice_id
        ):
            issues.append(
                _issue("detail.identity", f"slices/{slice_id}.md", "detail identity is invalid")
            )
        if not isinstance(detail.get("environment"), dict):
            issues.append(
                _issue("detail.environment", f"slices/{slice_id}.md", "environment must be a mapping")
            )
        try:
            _timestamp(detail.get("verified_at"), "verified_at")
        except ValueError as exc:
            issues.append(_issue("detail.timestamp", f"slices/{slice_id}.md", str(exc)))
        if detail.get("plan_revision") != plan_revision or detail.get("plan_digest") != plan_digest:
            issues.append(
                _issue(
                    "detail.plan", f"slices/{slice_id}.md", "detail does not match approved plan"
                )
            )
        criteria = detail.get("criteria")
        expected_criteria = slice_plan.get("criteria", {})
        expected_checks = slice_plan.get("checks", {})
        if not isinstance(criteria, dict) or set(criteria) != set(expected_criteria):
            issues.append(
                _issue(
                    "criteria.coverage", "criteria", "criteria IDs do not exactly match the plan"
                )
            )
        for criterion_id in expected_criteria:
            item = criteria.get(criterion_id) if isinstance(criteria, dict) else None
            if (
                not isinstance(item, dict)
                or any(
                    not isinstance(item.get(field), str) or not item[field].strip()
                    for field in ("action", "expected", "method", "evidence")
                )
                or item.get("status") != "PASS"
                or not isinstance(item.get("observed"), str)
                or not item["observed"].strip()
            ):
                issues.append(
                    _issue(
                        "criteria.unsatisfied",
                        f"criteria.{criterion_id}",
                        "criterion must include required fields and a PASS observation",
                    )
                )
            elif item.get("evidence") not in expected_checks:
                evidence_ref = PurePosixPath(str(item["evidence"]))
                evidence_path = session / Path(*evidence_ref.parts)
                unsafe_evidence = evidence_ref.is_absolute() or ".." in evidence_ref.parts
                if unsafe_evidence or not evidence_path.is_file() or evidence_path.is_symlink():
                    issues.append(
                        _issue(
                            "criteria.evidence",
                            f"criteria.{criterion_id}.evidence",
                            "evidence must reference a declared check or an existing local file",
                        )
                    )
        checks = detail.get("checks")
        if not isinstance(checks, dict) or set(checks) != set(expected_checks):
            issues.append(
                _issue("checks.coverage", "checks", "check IDs do not exactly match the plan")
            )
        current_records = _input_inventory(root, session, slice_plan.get("inputs", []))
        current_digest = _digest(current_records)
        if detail.get("inputs_digest") != current_digest:
            issues.append(_issue("evidence.stale", "inputs_digest", "input evidence is stale"))
        for check_id, expected in expected_checks.items():
            item = checks.get(check_id) if isinstance(checks, dict) else None
            if not isinstance(item, dict):
                issues.append(
                    _issue("check.missing", f"checks.{check_id}", "check evidence is missing")
                )
                continue
            if item.get("command") != expected.get("command") or item.get("cwd") != expected.get(
                "cwd"
            ):
                issues.append(
                    _issue(
                        "check.identity",
                        f"checks.{check_id}",
                        "check command or cwd differs from the plan",
                    )
                )
            if (
                item.get("status") != "PASS"
                or item.get("exit_code") != 0
                or not str(item.get("observed", "")).strip()
            ):
                issues.append(
                    _issue(
                        "check.unsatisfied",
                        f"checks.{check_id}",
                        "check is not PASS with exit code 0",
                    )
                )
            try:
                started = _timestamp(item.get("started_at"), f"checks.{check_id}.started_at")
                finished = _timestamp(item.get("finished_at"), f"checks.{check_id}.finished_at")
                if finished < started:
                    raise ValueError("finished_at precedes started_at")
                if item.get("inputs_before") is None or item.get("inputs_after") is None:
                    raise ValueError("input fingerprints are required")
            except ValueError as exc:
                issues.append(_issue("check.evidence", f"checks.{check_id}", str(exc)))
            if (
                item.get("inputs_before") != current_digest
                or item.get("inputs_after") != current_digest
            ):
                issues.append(
                    _issue("check.stale", f"checks.{check_id}", "check input digest is stale")
                )
        for dependency in slice_plan.get("depends_on", []):
            if tracker.get("slices", {}).get(dependency, {}).get("status") != "verified":
                issues.append(
                    _issue(
                        "dependency.pending",
                        f"plan.slices.{slice_id}.depends_on",
                        f"dependency {dependency} is not verified",
                    )
                )
        if tracker.get("slices", {}).get(slice_id, {}).get("status") not in {
            "in-progress",
            "implemented",
            "verified",
        }:
            issues.append(
                _issue(
                    "transition.invalid",
                    f"tracker.slices.{slice_id}.status",
                    "slice is not ready to close",
                )
            )
        return tracker, issues, detail, plan_path, current_records
    except (OSError, RuntimeError, ValueError) as exc:
        issues.append(_issue("runtime.invalid", "", str(exc)))
        return {}, issues, {}, session / "08-implementation-plan.md", []


def _result(
    operation: str,
    session: Path,
    slice_id: str,
    result: str,
    issues: list[dict[str, str]],
    records: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "operation": operation,
        "session": session.name,
        "slice": slice_id,
        "result": result,
        "inputs_digest": _digest(records) if records else None,
        "issues": issues,
    }


def _snapshot(session: Path, slice_id: str) -> tuple[dict[str, Any], int]:
    try:
        inventory, plan_text, _, _, _ = _plan(session)
        root = _repo_root(session)
        item = inventory.get("slices", {}).get(slice_id)
        if not isinstance(item, dict):
            raise ValueError(f"unknown slice: {slice_id}")
        records = _input_inventory(root, session, item.get("inputs", []))
        result = {
            "schema_version": 1,
            "operation": "snapshot",
            "session": session.name,
            "slice": slice_id,
            "result": "PASS",
            "plan_digest": _sha256(plan_text.encode()),
            "inputs_digest": _digest(records),
            "inputs": records,
            "issues": [],
        }
        return result, 0
    except (OSError, RuntimeError, ValueError) as exc:
        return _result(
            "snapshot",
            session,
            slice_id,
            "UNSUPPORTED",
            [_issue("runtime.invalid", "", str(exc))],
            [],
        ), EXIT_UNSUPPORTED


def _check(session: Path, slice_id: str) -> tuple[dict[str, Any], int]:
    tracker, issues, _, _, records = _validate(session, slice_id)
    code = _exit_for_issues(issues)
    return _result(
        "check", session, slice_id, "PASS" if not issues else "FAIL", issues, records
    ), code


def _exit_for_issues(issues: list[dict[str, str]]) -> int:
    if not issues:
        return 0
    unsupported = {
        "runtime.invalid",
        "detail.invalid",
        "detail.identity",
        "detail.environment",
        "detail.timestamp",
        "plan.revision",
        "slice.unknown",
        "slice.unauthorized",
        "revision.conflict",
        "summary.delimiters",
    }
    return EXIT_UNSUPPORTED if any(issue["code"] in unsupported for issue in issues) else EXIT_INVALID


def _replace_atomic(path: Path, content: bytes, expected: bytes | None = None) -> None:
    if expected is not None and path.read_bytes() != expected:
        raise ConcurrentChangeError(f"{path} changed during close")
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(content)
        temp = Path(handle.name)
    os.replace(temp, path)


def _close(session: Path, slice_id: str, expected_revision: int) -> tuple[dict[str, Any], int]:
    tracker_path = session / "09-delivery-status.md"
    original_tracker = tracker_path.read_bytes()
    original_plan = (session / "08-implementation-plan.md").read_bytes()
    original_definition = (session / "00-status.md").read_bytes()
    original_detail = (session / "slices" / f"{slice_id}.md").read_bytes()
    tracker, issues, detail, _, records = _validate(session, slice_id)
    if tracker.get("revision") != expected_revision:
        issues.append(
            _issue("revision.conflict", "tracker.revision", "expected revision does not match")
        )
    if issues:
        return _result("close", session, slice_id, "FAIL", issues, records), _exit_for_issues(issues)
    if tracker.get("slices", {}).get(slice_id, {}).get("status") == "verified":
        return _result("close", session, slice_id, "PASS", [], records), 0
    if tracker_path.read_bytes() != original_tracker:
        issues.append(_issue("revision.conflict", "tracker", "tracker changed during close"))
    if (session / "08-implementation-plan.md").read_bytes() != original_plan:
        issues.append(_issue("revision.conflict", "plan", "plan changed during close"))
    if (session / "00-status.md").read_bytes() != original_definition:
        issues.append(_issue("revision.conflict", "00-status.md", "definition changed during close"))
    if (session / "slices" / f"{slice_id}.md").read_bytes() != original_detail:
        issues.append(_issue("revision.conflict", "detail", "evidence changed during close"))
    try:
        inventory, _, _, _, _ = _plan(session)
        current_inputs = _input_inventory(
            _repo_root(session), session, inventory["slices"][slice_id].get("inputs", [])
        )
        if _digest(current_inputs) != _digest(records):
            issues.append(
                _issue("revision.conflict", "inputs", "declared inputs changed during close")
            )
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        issues.append(_issue("runtime.invalid", "inputs", str(exc)))
    if issues:
        return _result("close", session, slice_id, "FAIL", issues, records), _exit_for_issues(issues)
    _, body, original = _frontmatter(tracker_path)
    history = ""
    if "\n## Delivery history\n" in body:
        body, history = body.split("\n## Delivery history\n", 1)
        history = "\n## Delivery history\n" + history
    starts, ends = (
        body.count("<!-- devquitect:slice-close:start -->"),
        body.count("<!-- devquitect:slice-close:end -->"),
    )
    if starts > 1 or ends > 1 or starts != ends:
        return _result(
            "close",
            session,
            slice_id,
            "UNSUPPORTED",
            [
                _issue(
                    "summary.delimiters",
                    "tracker.body",
                    "summary delimiters are duplicated or incomplete",
                )
            ],
            records,
        ), EXIT_UNSUPPORTED
    now = _now()
    front, _, _ = _frontmatter(tracker_path)
    front["revision"] = expected_revision + 1
    front["last_updated"] = now
    front["slices"][slice_id]["status"] = "verified"
    front["slices"][slice_id]["evidence"] = f"slices/{slice_id}.md"
    front["current_slice"] = None
    front["next_action"] = "Select the next ready authorized slice"
    summary = (
        "<!-- devquitect:slice-close:start -->\n\n"
        f"Verified {slice_id} at {now}; evidence: `slices/{slice_id}.md`.\n\n"
        "<!-- devquitect:slice-close:end -->"
    )
    if starts == 1:
        body = re.sub(
            r"<!-- devquitect:slice-close:start -->.*?<!-- devquitect:slice-close:end -->",
            summary,
            body,
            count=1,
            flags=re.S,
        )
    else:
        body = body.rstrip() + "\n\n" + summary + "\n"
    body += history
    payload = "---\n" + yaml.safe_dump(front, sort_keys=False).strip() + "\n---\n" + body
    if payload.encode() == original:
        return _result("close", session, slice_id, "PASS", [], records), 0
    try:
        _replace_atomic(tracker_path, payload.encode(), expected=original_tracker)
    except ConcurrentChangeError as exc:
        return (
            _result(
                "close",
                session,
                slice_id,
                "UNSUPPORTED",
                [_issue("revision.conflict", "tracker", str(exc))],
                records,
            ),
            EXIT_UNSUPPORTED,
        )
    return _result("close", session, slice_id, "PASS", [], records), 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("snapshot", "check", "close"))
    parser.add_argument("--session", required=True, type=Path)
    parser.add_argument("--slice", required=True, dest="slice_id")
    parser.add_argument("--expected-revision", type=int)
    args = parser.parse_args(argv)
    args.session = args.session.resolve()
    try:
        if args.operation == "snapshot":
            result, code = _snapshot(args.session, args.slice_id)
        elif args.operation == "check":
            result, code = _check(args.session, args.slice_id)
        else:
            if args.expected_revision is None:
                parser.error("close requires --expected-revision")
            result, code = _close(args.session, args.slice_id, args.expected_revision)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return code
    except Exception as exc:  # keep runtime diagnostics on stderr and machine output stable
        print(f"verify_slice: {exc}", file=sys.stderr)
        return EXIT_UNSUPPORTED


if __name__ == "__main__":
    raise SystemExit(main())
