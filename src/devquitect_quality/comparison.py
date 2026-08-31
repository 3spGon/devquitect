"""Stable/candidate pairing and safety-dominant comparison classification."""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .models import SkillSnapshot, SkillSource
from .sources import freeze_source

ComparisonClass = Literal[
    "equivalent", "improvement", "regression", "contract-change", "variable", "inconclusive"
]


@dataclass(frozen=True, slots=True)
class FrozenPair:
    stable: SkillSnapshot
    candidate: SkillSnapshot


def freeze_pair(stable: SkillSource, candidate: SkillSource, destination: Path) -> FrozenPair:
    """Freeze both identities before either can execute."""

    return FrozenPair(
        freeze_source(stable, destination / "stable"),
        freeze_source(candidate, destination / "candidate"),
    )


def classify_results(
    stable: Sequence[Mapping[str, Any]],
    candidate: Sequence[Mapping[str, Any]],
    declaration: Mapping[str, Any] | None = None,
) -> ComparisonClass:
    stable_classes = {str(record["classification"]) for record in stable}
    candidate_classes = {str(record["classification"]) for record in candidate}
    if "inconclusive" in stable_classes | candidate_classes:
        return "inconclusive"
    if len(stable_classes) != 1 or len(candidate_classes) != 1:
        return "variable"
    stable_class = next(iter(stable_classes))
    candidate_class = next(iter(candidate_classes))
    critical_candidate_failure = any(record.get("critical_failures") for record in candidate)
    if stable_class == candidate_class:
        return "equivalent"
    if stable_class == "pass" and candidate_class == "fail":
        return "regression"
    if critical_candidate_failure:
        return "regression"
    if declaration and declaration.get("reviewed") and declaration.get("updated_cases"):
        return "contract-change"
    if stable_class == "fail" and candidate_class == "pass":
        return "improvement"
    return "regression"


def pair_records(
    stable: Sequence[Mapping[str, Any]], candidate: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    stable_by_case = {str(record["case_id"]): record for record in stable}
    candidate_by_case = {str(record["case_id"]): record for record in candidate}
    records: list[dict[str, Any]] = []
    for case_id in sorted(stable_by_case.keys() | candidate_by_case.keys()):
        stable_record = stable_by_case.get(case_id)
        candidate_record = candidate_by_case.get(case_id)
        classification: ComparisonClass = (
            "inconclusive"
            if stable_record is None or candidate_record is None
            else classify_results((stable_record,), (candidate_record,))
        )
        records.append(
            {
                "comparison_id": str(uuid.uuid4()),
                "case_id": case_id,
                "classification": classification,
                "stable": stable_record,
                "candidate": candidate_record,
            }
        )
    return records
