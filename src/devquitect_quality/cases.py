"""Versioned YAML behavioral case loading and selection."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class CaseError(ValueError):
    """A case collection is invalid or cannot satisfy a selection."""


@dataclass(frozen=True, slots=True)
class EvalCase:
    data: Mapping[str, Any]
    path: Path
    digest: str

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def repetitions(self) -> int:
        return int(self.data["repetitions"])


def load_cases(root: Path, schema_path: Path) -> tuple[EvalCase, ...]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    cases: list[EvalCase] = []
    identifiers: set[str] = set()
    for path in sorted(root.glob("*.yaml")):
        raw = path.read_bytes()
        value = yaml.safe_load(raw)
        errors = sorted(validator.iter_errors(value), key=lambda error: list(error.path))
        if errors:
            raise CaseError(f"{path}: {errors[0].message}")
        identifier = str(value["id"])
        if identifier in identifiers:
            raise CaseError(f"duplicate case id: {identifier}")
        identifiers.add(identifier)
        cases.append(EvalCase(value, path, hashlib.sha256(raw).hexdigest()))
    if not cases:
        raise CaseError(f"no cases found under {root}")
    return tuple(cases)


def select_cases(
    cases: tuple[EvalCase, ...], *, suite: str | None = None, case_id: str | None = None
) -> tuple[EvalCase, ...]:
    if suite and case_id:
        raise CaseError("choose either suite or case, not both")
    selected = cases
    if suite:
        selected = tuple(case for case in cases if suite in case.data["tags"])
    if case_id:
        selected = tuple(case for case in cases if case.id == case_id)
    if not selected:
        raise CaseError(f"selection matched no cases: {suite or case_id}")
    return selected
