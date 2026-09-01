from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from devquitect_quality.models import SkillSource
from devquitect_quality.sources import freeze_source, remove_snapshot
from devquitect_quality.validate import (
    ValidationConfigurationError,
    load_directory_inputs,
    load_validation_inputs,
    validate_snapshot,
    validate_structure,
)

FIXTURE = Path(__file__).parents[1] / "fixtures/valid-plugin"
REPOSITORY = Path(__file__).parents[2]


def _copy_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "plugin"
    shutil.copytree(FIXTURE, root)
    return root


def _validate(root: Path) -> list[dict[str, str]]:
    return validate_structure(root / "skills", load_directory_inputs(root))


def _codes(records: list[dict[str, str]]) -> set[str]:
    return {record["code"] for record in records}


def test_current_skills_and_plugin_metadata_are_valid(tmp_path: Path) -> None:
    source = SkillSource.from_selector("working-tree", REPOSITORY)
    snapshot = freeze_source(source, tmp_path / "snapshot")
    try:
        assert validate_snapshot(snapshot, load_validation_inputs(source)) == []
    finally:
        remove_snapshot(snapshot.snapshot_root)


def test_valid_structural_fixture_passes(tmp_path: Path) -> None:
    assert _validate(_copy_fixture(tmp_path)) == []


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("invalid-frontmatter", "frontmatter.invalid"),
        ("name-mismatch", "skill.name-mismatch"),
        ("duplicate-name", "skill.duplicate-name"),
        ("missing-reference", "reference.missing"),
        ("unexpected-file", "package.unexpected-file"),
        ("unsafe-reference", "reference.unsafe-path"),
        ("invalid-presentation", "presentation.invalid"),
        ("invalid-membership", "plugin.invalid-membership"),
    ],
)
def test_quality_failures_have_specific_machine_records(
    tmp_path: Path, mutation: str, expected_code: str
) -> None:
    root = _copy_fixture(tmp_path)
    skill = root / "skills/example-skill"
    skill_file = skill / "SKILL.md"
    if mutation == "invalid-frontmatter":
        skill_file.write_text("name: example-skill\n", encoding="utf-8")
    elif mutation == "name-mismatch":
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "name: example-skill", "name: another-skill"
            ),
            encoding="utf-8",
        )
    elif mutation == "duplicate-name":
        shutil.copytree(skill, root / "skills/copy-skill")
    elif mutation == "missing-reference":
        (skill / "references/guide.md").unlink()
    elif mutation == "unexpected-file":
        (skill / "undeclared.txt").write_text("not allowlisted", encoding="utf-8")
    elif mutation == "unsafe-reference":
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "references/guide.md", "../../outside.md"
            ),
            encoding="utf-8",
        )
    elif mutation == "invalid-presentation":
        (skill / "agents/openai.yaml").write_text("interface: {}\n", encoding="utf-8")
    elif mutation == "invalid-membership":
        manifest = root / ".codex-plugin/plugin.json"
        value = json.loads(manifest.read_text(encoding="utf-8"))
        value["skills"] = "skills"
        manifest.write_text(json.dumps(value), encoding="utf-8")

    records = _validate(root)

    assert expected_code in _codes(records)
    relevant = next(record for record in records if record["code"] == expected_code)
    assert not relevant["path"].startswith("/")
    assert ".." not in _path_parts(relevant["path"])


def _path_parts(path: str) -> tuple[str, ...]:
    return tuple(path.split("/"))


def test_unsupported_schema_is_an_invalid_configuration(tmp_path: Path) -> None:
    root = _copy_fixture(tmp_path)
    schema_path = root / "schemas/report.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["x-devquitect-schema-version"] = 2
    schema_path.write_text(json.dumps(schema), encoding="utf-8")

    with pytest.raises(ValidationConfigurationError) as raised:
        _validate(root)

    assert raised.value.code == "schema.unsupported-version"
    assert raised.value.path == "schemas/report.schema.json"


def test_malformed_case_and_missing_fixture_are_reported(tmp_path: Path) -> None:
    root = _copy_fixture(tmp_path)
    shutil.copy(
        REPOSITORY / "schemas/eval-case.schema.json",
        root / "schemas/eval-case.schema.json",
    )
    case_directory = root / "evals/cases"
    case_directory.mkdir(parents=True)
    (case_directory / "bad-case.yaml").write_text(
        "schema_version: 1\nid: bad-case\nfixture: absent-fixture\n",
        encoding="utf-8",
    )

    records = _validate(root)

    assert "case.schema-invalid" in _codes(records)
    assert "case.missing-fixture" in _codes(records)
