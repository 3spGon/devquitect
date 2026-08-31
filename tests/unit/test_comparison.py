from __future__ import annotations

from devquitect_quality.comparison import classify_results


def record(classification: str, failures: list[str] | None = None) -> dict[str, object]:
    return {"classification": classification, "critical_failures": failures or []}


def test_comparison_classifications_and_critical_precedence() -> None:
    assert classify_results((record("pass"),), (record("pass"),)) == "equivalent"
    assert classify_results((record("fail"),), (record("pass"),)) == "improvement"
    assert classify_results((record("pass"),), (record("fail", ["authorization"]),)) == "regression"
    declaration = {"reviewed": True, "updated_cases": ["authorization"]}
    assert (
        classify_results((record("pass"),), (record("fail", ["authorization"]),), declaration)
        == "regression"
    )
    assert classify_results((record("pass"),), (record("inconclusive"),)) == "inconclusive"


def test_reviewed_declaration_requires_updated_cases() -> None:
    stable = (record("fail"),)
    candidate = (record("pass"),)
    assert classify_results(stable, candidate, {"reviewed": True}) == "improvement"
    assert (
        classify_results(stable, candidate, {"reviewed": True, "updated_cases": ["case"]})
        == "contract-change"
    )
