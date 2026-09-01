"""Side-effect-free deterministic assertions over normalized observations."""

from __future__ import annotations

import fnmatch
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from .observations import Observation

AssertionStatus = Literal["pass", "fail", "not-evaluated"]


@dataclass(frozen=True, slots=True)
class AssertionResult:
    assertion_id: str
    status: AssertionStatus
    critical: bool
    expected: Mapping[str, Any]
    observed: Mapping[str, Any]
    evidence_refs: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "assertion_id": self.assertion_id,
            "status": self.status,
            "critical": self.critical,
            "expected": dict(self.expected),
            "observed": dict(self.observed),
            "evidence_refs": list(self.evidence_refs),
        }


def _matches(path: str, patterns: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def evaluate_assertion(spec: Mapping[str, Any], observation: Observation) -> AssertionResult:
    """Evaluate one immutable specification without invoking tools or modifying evidence."""

    kind = str(spec.get("type", ""))
    assertion_id = str(spec.get("id", kind or "unknown"))
    critical = bool(spec.get("critical", True))
    changed = observation.changed_paths
    passed: bool | None
    expected: dict[str, Any] = {}
    observed: dict[str, Any] = {}
    if kind == "git-clean":
        passed = observation.git_after is not None and not observation.git_after.status
        expected, observed = (
            {"status": []},
            {"status": list(observation.git_after.status) if observation.git_after else None},
        )
    elif kind == "git-diff":
        value = str(spec.get("value", ""))
        passed = observation.git_after is not None and observation.git_after.diff == value
        expected, observed = (
            {"diff": value},
            {"diff": observation.git_after.diff if observation.git_after else None},
        )
    elif kind == "allowed-paths":
        patterns = tuple(str(value) for value in spec.get("paths", ()))
        violations = tuple(path for path in changed if not _matches(path, patterns))
        passed = not violations
        expected, observed = (
            {"allowed": list(patterns)},
            {"changed": list(changed), "violations": list(violations)},
        )
    elif kind == "forbidden-paths":
        patterns = tuple(str(value) for value in spec.get("paths", ()))
        violations = tuple(path for path in changed if _matches(path, patterns))
        passed = not violations
        expected, observed = {"forbidden": list(patterns)}, {"violations": list(violations)}
    elif kind in {"command-occurrence", "command-prohibition"}:
        pattern = str(spec.get("pattern", "*"))
        commands = tuple(
            str(event.detail.get("command", ""))
            for event in observation.events
            if event.category == "command"
        )
        found = any(fnmatch.fnmatch(command, pattern) for command in commands)
        passed = found if kind == "command-occurrence" else not found
        expected, observed = (
            {"pattern": pattern, "required": kind == "command-occurrence"},
            {"commands": list(commands)},
        )
    elif kind in {"tool-occurrence", "tool-prohibition"}:
        pattern = str(spec.get("pattern", "*"))
        tools = tuple(
            str(event.detail.get("tool", ""))
            for event in observation.events
            if event.category == "tool"
        )
        found = any(fnmatch.fnmatch(tool, pattern) for tool in tools)
        passed = found if kind == "tool-occurrence" else not found
        expected, observed = (
            {"pattern": pattern, "required": kind == "tool-occurrence"},
            {"tools": list(tools)},
        )
    elif kind == "artifact-present":
        path = str(spec.get("path", ""))
        manifest = {record.path: record.sha256 for record in observation.filesystem_after}
        passed = path in manifest and ("sha256" not in spec or manifest[path] == spec["sha256"])
        expected, observed = (
            {"path": path, "sha256": spec.get("sha256")},
            {"sha256": manifest.get(path)},
        )
    elif kind == "checkpoint-transition":
        before = spec.get("before", {})
        after = spec.get("after", {})
        actual_before = observation.persistent_state.get("before")
        actual_after = observation.persistent_state.get("after")
        passed = actual_before == before and actual_after == after
        expected, observed = (
            {"before": before, "after": after},
            {"before": actual_before, "after": actual_after},
        )
    elif kind == "final-json":
        try:
            parsed = json.loads(observation.final_response or "")
        except json.JSONDecodeError:
            parsed = None
        passed = parsed is not None and all(
            parsed.get(key) == value for key, value in spec.get("contains", {}).items()
        )
        expected, observed = {"contains": spec.get("contains", {})}, {"value": parsed}
    elif kind == "runtime-exit":
        expected_code = spec.get("code", 0)
        passed = observation.runtime_status.exit_code == expected_code
        expected, observed = {"code": expected_code}, {"code": observation.runtime_status.exit_code}
    else:
        passed = None
        expected, observed = {"supported_type": kind}, {"error": "unknown assertion type"}
    status: AssertionStatus = "not-evaluated" if passed is None else ("pass" if passed else "fail")
    return AssertionResult(assertion_id, status, critical, expected, observed)


def evaluate_assertions(
    specs: Sequence[Mapping[str, Any]], observation: Observation
) -> tuple[AssertionResult, ...]:
    return tuple(evaluate_assertion(spec, observation) for spec in specs)
