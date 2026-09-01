"""Offline structural validation for Devquitect skills and plugin inputs."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .models import SkillSnapshot, SkillSource
from .reporting import validation_record

SUPPORTED_SCHEMA_VERSION = 1
PLUGIN_MANIFEST_PATH = ".codex-plugin/plugin.json"
PLUGIN_PREFIX = ".codex-plugin/"
SCHEMA_PREFIX = "schemas/"
CASE_PREFIX = "evals/cases/"
FIXTURE_PREFIX = "evals/fixtures/"
RUBRIC_PREFIX = "evals/rubrics/"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


class ValidationConfigurationError(ValueError):
    """The validator cannot safely interpret its schema or configuration."""

    def __init__(self, code: str, path: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message


@dataclass(frozen=True, slots=True)
class ValidationInputs:
    """Non-skill structural inputs frozen in memory for one validation run."""

    files: Mapping[str, bytes]


def _safe_path(path: str) -> PurePosixPath:
    normalized = PurePosixPath(path)
    if (
        not path
        or "\x00" in path
        or normalized.is_absolute()
        or ".." in normalized.parts
    ):
        raise ValueError(f"unsafe path: {path!r}")
    return normalized


def _git(repository: Path, *args: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=False,
        capture_output=True,
    )
    if process.returncode != 0:
        message = process.stderr.decode("utf-8", errors="replace").strip()
        raise ValidationConfigurationError(
            "source.read-failed", "skills", message or "could not read selected source"
        )
    return process.stdout


def load_validation_inputs(source: SkillSource) -> ValidationInputs:
    """Read all non-skill validation inputs once from the selected source."""

    repository = source.repository_root
    wanted_prefixes = (
        PLUGIN_PREFIX,
        SCHEMA_PREFIX,
        CASE_PREFIX,
        FIXTURE_PREFIX,
        RUBRIC_PREFIX,
    )
    files: dict[str, bytes] = {}
    if source.kind == "working-tree":
        plugin_directory = repository / PLUGIN_PREFIX.rstrip("/")
        candidates: list[Path] = []
        if plugin_directory.exists():
            candidates.extend(path for path in plugin_directory.rglob("*") if path.is_file())
        for root_name in (
            SCHEMA_PREFIX.rstrip("/"),
            CASE_PREFIX.rstrip("/"),
            FIXTURE_PREFIX.rstrip("/"),
            RUBRIC_PREFIX.rstrip("/"),
        ):
            root = repository / root_name
            if root.exists():
                candidates.extend(path for path in root.rglob("*") if path.is_file())
        for path in candidates:
            if not path.exists():
                continue
            relative = path.relative_to(repository).as_posix()
            _safe_path(relative)
            if path.is_symlink():
                raise ValidationConfigurationError(
                    "source.unsafe-path", relative, "validation input may not be a symlink"
                )
            files[relative] = path.read_bytes()
    else:
        raw_paths = _git(
            repository,
            "ls-tree",
            "-r",
            "--name-only",
            "-z",
            source.selector,
            "--",
            PLUGIN_PREFIX.rstrip("/"),
            SCHEMA_PREFIX.rstrip("/"),
            CASE_PREFIX.rstrip("/"),
            FIXTURE_PREFIX.rstrip("/"),
            RUBRIC_PREFIX.rstrip("/"),
        )
        for raw_path in raw_paths.split(b"\x00"):
            if not raw_path:
                continue
            try:
                relative = raw_path.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ValidationConfigurationError(
                    "source.unsafe-path", "skills", "source contains a non-UTF-8 path"
                ) from error
            _safe_path(relative)
            if not any(
                relative == prefix or relative.startswith(prefix)
                for prefix in wanted_prefixes
            ):
                continue
            files[relative] = _git(repository, "show", f"{source.selector}:{relative}")
    return ValidationInputs(files=dict(sorted(files.items())))


def load_directory_inputs(plugin_root: Path | str) -> ValidationInputs:
    """Load validation inputs from a fixture directory for focused tests."""

    root = Path(plugin_root)
    source = SkillSource.from_selector("working-tree", root)
    return load_validation_inputs(source)


def _parse_json(files: Mapping[str, bytes], path: str) -> Any:
    try:
        return json.loads(files[path])
    except KeyError as error:
        raise ValidationConfigurationError(
            "plugin.missing-manifest", path, "required plugin manifest is missing"
        ) from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationConfigurationError(
            "configuration.invalid-json", path, f"invalid JSON: {error}"
        ) from error


def _parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return None, f"SKILL.md must be UTF-8: {error}"
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, "SKILL.md must begin with YAML frontmatter"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "SKILL.md frontmatter is not closed"
    try:
        value = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        return None, f"invalid YAML frontmatter: {error}"
    if not isinstance(value, dict):
        return None, "SKILL.md frontmatter must be a mapping"
    return value, None


def _local_references(skill_file: Path) -> list[str]:
    text = skill_file.read_text(encoding="utf-8")
    references: list[str] = []
    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        references.append(target.split("#", 1)[0])
    return references


def _validate_schemas(files: Mapping[str, bytes]) -> dict[str, Any]:
    schemas: dict[str, Any] = {}
    required = {
        "schemas/eval-case.schema.json",
        "schemas/report.schema.json",
        "schemas/promotion-record.schema.json",
    }
    missing = sorted(required - files.keys())
    if missing:
        raise ValidationConfigurationError(
            "schema.missing", missing[0], "required repository schema is missing"
        )
    for path in sorted(name for name in files if name.startswith(SCHEMA_PREFIX)):
        schema = _parse_json(files, path)
        if not isinstance(schema, dict):
            raise ValidationConfigurationError(
                "schema.invalid", path, "schema root must be an object"
            )
        version = schema.get("x-devquitect-schema-version")
        if version != SUPPORTED_SCHEMA_VERSION:
            raise ValidationConfigurationError(
                "schema.unsupported-version",
                path,
                f"schema version {version!r} is unsupported; expected 1",
            )
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            raise ValidationConfigurationError(
                "schema.invalid", path, f"invalid JSON Schema: {error.message}"
            ) from error
        schemas[path] = schema
    return schemas


def _validate_cases(
    files: Mapping[str, bytes], schemas: Mapping[str, Any]
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    validator = Draft202012Validator(schemas["schemas/eval-case.schema.json"])
    identifiers: Counter[str] = Counter()
    parsed: list[tuple[str, Any]] = []
    for path in sorted(name for name in files if name.startswith(CASE_PREFIX)):
        if not path.endswith((".yaml", ".yml", ".json")):
            records.append(
                validation_record(
                    "package.unexpected-file", path, "case directory contains an unsupported file"
                )
            )
            continue
        try:
            value = (
                json.loads(files[path])
                if path.endswith(".json")
                else yaml.safe_load(files[path])
            )
        except (UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError) as error:
            records.append(validation_record("case.invalid", path, f"invalid case: {error}"))
            continue
        parsed.append((path, value))
        if isinstance(value, dict) and isinstance(value.get("id"), str):
            identifiers[value["id"]] += 1
    for path, value in parsed:
        errors = sorted(validator.iter_errors(value), key=lambda error: list(error.path))
        for error in errors:
            location = ".".join(str(part) for part in error.path)
            message = f"{location}: {error.message}" if location else error.message
            records.append(validation_record("case.schema-invalid", path, message))
        if isinstance(value, dict) and identifiers[value.get("id", "")] > 1:
            records.append(
                validation_record("case.duplicate-id", path, "case id must be repository-unique")
            )
        if not isinstance(value, dict):
            continue
        fixture = value.get("fixture")
        if isinstance(fixture, str):
            try:
                fixture_path = _safe_path(fixture).as_posix().rstrip("/")
            except ValueError:
                records.append(
                    validation_record("case.unsafe-fixture", path, "fixture reference is unsafe")
                )
            else:
                fixture_root = f"{FIXTURE_PREFIX}{fixture_path}"
                if not any(
                    name == fixture_root or name.startswith(f"{fixture_root}/")
                    for name in files
                ):
                    records.append(
                        validation_record(
                            "case.missing-fixture", path, f"fixture {fixture!r} does not resolve"
                        )
                    )
        rubric = value.get("semantic_rubric")
        if isinstance(rubric, str):
            try:
                rubric_path = _safe_path(rubric).as_posix().rstrip("/")
            except ValueError:
                records.append(
                    validation_record("case.unsafe-rubric", path, "rubric reference is unsafe")
                )
            else:
                candidates = {
                    f"{RUBRIC_PREFIX}{rubric_path}",
                    f"{RUBRIC_PREFIX}{rubric_path}.yaml",
                    f"{RUBRIC_PREFIX}{rubric_path}.yml",
                    f"{RUBRIC_PREFIX}{rubric_path}.json",
                }
                if not candidates.intersection(files):
                    records.append(
                        validation_record(
                            "case.missing-rubric", path, f"rubric {rubric!r} does not resolve"
                        )
                    )
    return records


def validate_structure(
    skill_root: Path | str, inputs: ValidationInputs
) -> list[dict[str, str]]:
    """Return repository quality failures; raise only for invalid validator configuration."""

    root = Path(skill_root)
    files = inputs.files
    schemas = _validate_schemas(files)
    manifest = _parse_json(files, PLUGIN_MANIFEST_PATH)
    if not isinstance(manifest, dict):
        raise ValidationConfigurationError(
            "plugin.invalid-manifest", PLUGIN_MANIFEST_PATH, "manifest root must be an object"
        )

    records: list[dict[str, str]] = []
    for path in sorted(name for name in files if name.startswith(PLUGIN_PREFIX)):
        if path != PLUGIN_MANIFEST_PATH:
            records.append(
                validation_record(
                    "package.unexpected-file",
                    path,
                    "only plugin.json is allowed inside .codex-plugin",
                )
            )
    for key in ("name", "version", "description", "skills"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            records.append(
                validation_record(
                    "plugin.missing-field",
                    PLUGIN_MANIFEST_PATH,
                    f"required field {key!r} is missing",
                )
            )
    plugin_name = manifest.get("name")
    if isinstance(plugin_name, str) and not NAME_PATTERN.fullmatch(plugin_name):
        records.append(
            validation_record(
                "plugin.invalid-name", PLUGIN_MANIFEST_PATH, "plugin name must use kebab-case"
            )
        )
    plugin_version = manifest.get("version")
    if isinstance(plugin_version, str) and not SEMVER_PATTERN.fullmatch(plugin_version):
        records.append(
            validation_record(
                "plugin.invalid-version",
                PLUGIN_MANIFEST_PATH,
                "plugin version must use MAJOR.MINOR.PATCH semantic versioning",
            )
        )
    skills_pointer = manifest.get("skills")
    if skills_pointer != "./skills/":
        records.append(
            validation_record(
                "plugin.invalid-membership",
                PLUGIN_MANIFEST_PATH,
                "skills must declare the repository skill root as './skills/'",
            )
        )

    if not root.is_dir():
        records.append(validation_record("skills.missing", "skills", "skills directory is missing"))
        return records + _validate_cases(files, schemas)

    names: list[tuple[str, str]] = []
    directories: list[Path] = []
    for entry in sorted(root.iterdir()):
        if entry.is_symlink():
            records.append(
                validation_record(
                    "package.unsafe-path",
                    f"skills/{entry.name}",
                    "skill root entry may not be a symlink",
                )
            )
        elif entry.is_dir():
            directories.append(entry)
        else:
            records.append(
                validation_record(
                    "package.unexpected-file",
                    f"skills/{entry.name}",
                    "skills root may contain only declared skill directories",
                )
            )
    for directory in directories:
        skill_relative = f"skills/{directory.name}"
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file() or skill_file.is_symlink():
            records.append(
                validation_record(
                    "frontmatter.missing",
                    f"{skill_relative}/SKILL.md",
                    "required SKILL.md is missing",
                )
            )
            continue
        frontmatter, error = _parse_frontmatter(skill_file)
        if error:
            records.append(
                validation_record(
                    "frontmatter.invalid", f"{skill_relative}/SKILL.md", error
                )
            )
            frontmatter = None
        if frontmatter is not None:
            name = frontmatter.get("name")
            description = frontmatter.get("description")
            if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
                records.append(
                    validation_record(
                        "frontmatter.invalid-name",
                        f"{skill_relative}/SKILL.md",
                        "frontmatter name is required and must use kebab-case",
                    )
                )
            else:
                names.append((name, f"{skill_relative}/SKILL.md"))
                if name != directory.name:
                    records.append(
                        validation_record(
                            "skill.name-mismatch",
                            f"{skill_relative}/SKILL.md",
                            (
                                f"frontmatter name {name!r} does not match "
                                f"directory {directory.name!r}"
                            ),
                        )
                    )
            if not isinstance(description, str) or not description.strip():
                records.append(
                    validation_record(
                        "frontmatter.missing-description",
                        f"{skill_relative}/SKILL.md",
                        "frontmatter description is required",
                    )
                )
            elif "use" not in description.lower() or "do not use" not in description.lower():
                records.append(
                    validation_record(
                        "frontmatter.activation-boundaries",
                        f"{skill_relative}/SKILL.md",
                        "description must state positive and negative activation boundaries",
                    )
                )

        references: set[str] = set()
        for reference in _local_references(skill_file):
            try:
                relative = _safe_path(reference)
            except ValueError:
                records.append(
                    validation_record(
                        "reference.unsafe-path",
                        f"{skill_relative}/SKILL.md",
                        f"local reference is unsafe: {reference!r}",
                    )
                )
                continue
            target = directory.joinpath(*relative.parts)
            try:
                target.resolve().relative_to(directory.resolve())
            except ValueError:
                records.append(
                    validation_record(
                        "reference.unsafe-path",
                        f"{skill_relative}/SKILL.md",
                        f"local reference escapes the skill: {reference!r}",
                    )
                )
                continue
            if not target.is_file() or target.is_symlink():
                records.append(
                    validation_record(
                        "reference.missing",
                        f"{skill_relative}/{relative.as_posix()}",
                        "referenced local resource does not exist as a regular file",
                    )
                )
            else:
                references.add(relative.as_posix())

        presentation = directory / "agents/openai.yaml"
        presentation_relative = f"{skill_relative}/agents/openai.yaml"
        if not presentation.is_file() or presentation.is_symlink():
            records.append(
                validation_record(
                    "presentation.missing",
                    presentation_relative,
                    "presentation metadata is required",
                )
            )
        else:
            try:
                metadata = yaml.safe_load(presentation.read_text(encoding="utf-8"))
                interface = metadata["interface"]
                for field in ("display_name", "short_description", "default_prompt"):
                    if not isinstance(interface.get(field), str) or not interface[field].strip():
                        raise ValueError(f"interface.{field} must be a non-empty string")
            except (UnicodeDecodeError, yaml.YAMLError, KeyError, TypeError, ValueError) as error:
                records.append(
                    validation_record("presentation.invalid", presentation_relative, str(error))
                )

        allowed = {"SKILL.md", "agents/openai.yaml", *references}
        for path in sorted(item for item in directory.rglob("*") if not item.is_dir()):
            relative = path.relative_to(directory).as_posix()
            if path.is_symlink():
                records.append(
                    validation_record(
                        "package.unsafe-path",
                        f"{skill_relative}/{relative}",
                        "package input may not be a symlink",
                    )
                )
            elif relative not in allowed:
                records.append(
                    validation_record(
                        "package.unexpected-file",
                        f"{skill_relative}/{relative}",
                        "file is not an allowlisted skill input or referenced resource",
                    )
                )

    counts = Counter(name for name, _ in names)
    for name, path in names:
        if counts[name] > 1:
            records.append(
                validation_record(
                    "skill.duplicate-name", path, f"skill name {name!r} is not unique"
                )
            )

    records.extend(_validate_cases(files, schemas))
    return sorted(records, key=lambda record: (record["path"], record["code"], record["message"]))


def validate_snapshot(snapshot: SkillSnapshot, inputs: ValidationInputs) -> list[dict[str, str]]:
    """Validate one immutable skill snapshot and its frozen structural inputs."""

    return validate_structure(snapshot.snapshot_root / "skills", inputs)


def validate_report_schema(report: Mapping[str, Any], inputs: ValidationInputs) -> None:
    """Ensure generated canonical output conforms to the repository report schema."""

    schemas = _validate_schemas(inputs.files)
    try:
        Draft202012Validator(schemas["schemas/report.schema.json"]).validate(report)
    except ValidationError as error:
        raise ValidationConfigurationError(
            "report.schema-invalid", "schemas/report.schema.json", error.message
        ) from error
