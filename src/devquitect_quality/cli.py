"""Command-line entry point for Devquitect quality tooling."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from .models import SkillSource
from .reporting import (
    build_validation_report,
    render_text,
    serialize_json,
    validation_record,
    write_report_atomic,
)
from .sources import SourceError, freeze_source, remove_snapshot
from .validate import (
    ValidationConfigurationError,
    load_validation_inputs,
    validate_report_schema,
    validate_snapshot,
)


def _repository_root() -> Path:
    process = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise SourceError(process.stderr.strip() or "current directory is not a Git repository")
    return Path(process.stdout.strip()).resolve()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="devquitect")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate skills and plugin inputs offline")
    validate.add_argument("--source", required=True)
    validate.add_argument("--format", choices=("json", "text"), default="text")
    validate.add_argument("--report", type=Path)
    return parser


def _source_identity(source: SkillSource, snapshot_id: str | None = None) -> dict[str, object]:
    identity: dict[str, object] = {"kind": source.kind, "selector": source.selector}
    if snapshot_id:
        identity["snapshot_id"] = snapshot_id
    return identity


def _configuration_failure(
    source: SkillSource, error: ValidationConfigurationError | SourceError
) -> dict[str, object]:
    if isinstance(error, ValidationConfigurationError):
        record = validation_record(error.code, error.path, error.message)
    else:
        record = validation_record("source.invalid", "skills", str(error))
    return build_validation_report(source=_source_identity(source), records=[record])


def _emit(report: dict[str, object], output_format: str, report_path: Path | None) -> None:
    if report_path is not None:
        write_report_atomic(report_path, report)
    if output_format == "json":
        sys.stdout.write(serialize_json(report))
    else:
        sys.stderr.write(render_text(report))


def _run_validate(args: argparse.Namespace) -> int:
    try:
        repository = _repository_root()
    except SourceError as error:
        source = SkillSource.from_selector(args.source, Path.cwd())
        report = _configuration_failure(source, error)
        _emit(report, args.format, args.report)
        return 2

    source = SkillSource.from_selector(args.source, repository)
    snapshot_root: Path | None = None
    try:
        inputs = load_validation_inputs(source)
        with tempfile.TemporaryDirectory(prefix="devquitect-validate-") as temporary:
            snapshot_root = Path(temporary) / "snapshot"
            snapshot = freeze_source(source, snapshot_root)
            records = validate_snapshot(snapshot, inputs)
            report = build_validation_report(
                source=_source_identity(source, snapshot.snapshot_id), records=records
            )
            validate_report_schema(report, inputs)
    except (SourceError, ValidationConfigurationError) as error:
        report = _configuration_failure(source, error)
        _emit(report, args.format, args.report)
        return 2
    finally:
        if snapshot_root is not None and snapshot_root.exists():
            remove_snapshot(snapshot_root)

    _emit(report, args.format, args.report)
    return 0 if report["result"] == "pass" else 1


def main(argv: list[str] | None = None) -> int:
    """Run the repository-owned command surface."""

    args = _parser().parse_args(argv)
    if args.command == "validate":
        return _run_validate(args)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
