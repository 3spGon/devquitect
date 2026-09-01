from __future__ import annotations

import pytest

from devquitect_quality.promotion import (
    PromotionError,
    compatibility_impact,
    validate_compatibility,
)


@pytest.mark.parametrize(
    ("previous", "candidate", "impact"),
    [("1.2.3", "1.2.4", "patch"), ("1.2.3", "1.3.0", "minor"), ("1.2.3", "2.0.0", "major")],
)
def test_semantic_version_policy(previous: str, candidate: str, impact: str) -> None:
    assert compatibility_impact(previous, candidate) == impact


def test_non_increasing_version_is_rejected() -> None:
    with pytest.raises(PromotionError, match="greater"):
        compatibility_impact("1.2.3", "1.2.3")


def test_persistent_schema_change_requires_migration_or_recovery() -> None:
    with pytest.raises(PromotionError, match="migration or recovery"):
        validate_compatibility(impact="major", persistent_schema_changed=True, migration_refs=[])
    validate_compatibility(
        impact="major",
        persistent_schema_changed=True,
        migration_refs=["evals/cases/recovery.yaml"],
    )
