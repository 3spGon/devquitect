"""Command-line entry point for Devquitect quality tooling."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from .cases import CaseError, load_cases, select_cases
from .codex_adapter import discover_auth_cache
from .comparison import freeze_pair, pair_records
from .evaluation import run_case
from .models import SkillSource
from .packaging import PackageError, build_package
from .promotion import PromotionError, release_check
from .reporting import (
    build_artifact_report,
    build_comparison_report,
    build_evaluation_report,
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
    evaluate = commands.add_parser("eval", help="run isolated behavioral cases")
    evaluate.add_argument("--source", required=True)
    selection = evaluate.add_mutually_exclusive_group()
    selection.add_argument("--suite")
    selection.add_argument("--case")
    evaluate.add_argument("--model")
    evaluate.add_argument("--reasoning-effort")
    evaluate.add_argument("--report", type=Path)
    compare = commands.add_parser("compare", help="compare stable and candidate behavior")
    compare.add_argument("--stable", required=True)
    compare.add_argument("--candidate", required=True)
    comparison_selection = compare.add_mutually_exclusive_group()
    comparison_selection.add_argument("--suite")
    comparison_selection.add_argument("--case")
    compare.add_argument("--report", type=Path)
    package = commands.add_parser("package", help="build a deterministic plugin archive")
    package.add_argument("--source", required=True)
    package.add_argument("--version", required=True)
    package.add_argument("--output", required=True, type=Path)
    package.add_argument("--report", type=Path)
    release = commands.add_parser("release-check", help="verify release eligibility")
    release.add_argument("--source", required=True)
    release.add_argument("--version", required=True)
    release.add_argument("--evidence", required=True, type=Path)
    release.add_argument("--output", required=True, type=Path)
    release.add_argument("--report", type=Path)
    check = commands.add_parser("check", help="run the integrated contributor definition of done")
    check.add_argument("--source", default="working-tree")
    check.add_argument("--behavioral", action="store_true")
    check.add_argument("--report", type=Path)
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


def _run_eval(args: argparse.Namespace) -> int:
    try:
        repository = _repository_root()
        source = SkillSource.from_selector(args.source, repository)
        cases = select_cases(
            load_cases(repository / "evals/cases", repository / "schemas/eval-case.schema.json"),
            suite=args.suite,
            case_id=args.case,
        )
        with tempfile.TemporaryDirectory(prefix="devquitect-eval-") as temporary:
            snapshot = freeze_source(source, Path(temporary) / "snapshot")
            records = [
                record
                for case in cases
                for record in run_case(
                    case,
                    snapshot,
                    repository,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    auth_cache=discover_auth_cache(),
                )
            ]
        report = build_evaluation_report(
            source=_source_identity(source, snapshot.snapshot_id), records=records
        )
    except (SourceError, CaseError, ValueError) as error:
        sys.stderr.write(f"evaluation configuration error: {error}\n")
        return 2
    if args.report:
        write_report_atomic(args.report, report)
    sys.stdout.write(serialize_json(report))
    return {"pass": 0, "fail": 1, "inconclusive": 3}[report["result"]]


def _run_compare(args: argparse.Namespace) -> int:
    try:
        repository = _repository_root()
        stable_source = SkillSource.from_selector(args.stable, repository)
        candidate_source = SkillSource.from_selector(args.candidate, repository)
        cases = select_cases(
            load_cases(repository / "evals/cases", repository / "schemas/eval-case.schema.json"),
            suite=args.suite,
            case_id=args.case,
        )
        auth_cache = discover_auth_cache()
        with tempfile.TemporaryDirectory(prefix="devquitect-compare-") as temporary:
            pair = freeze_pair(stable_source, candidate_source, Path(temporary))
            stable_records = [
                record
                for case in cases
                for record in run_case(case, pair.stable, repository, auth_cache=auth_cache)
            ]
            candidate_records = [
                record
                for case in cases
                for record in run_case(case, pair.candidate, repository, auth_cache=auth_cache)
            ]
        records = pair_records(stable_records, candidate_records)
        report = build_comparison_report(
            stable=_source_identity(stable_source, pair.stable.snapshot_id),
            candidate=_source_identity(candidate_source, pair.candidate.snapshot_id),
            records=records,
        )
    except (SourceError, CaseError, ValueError) as error:
        sys.stderr.write(f"comparison configuration error: {error}\n")
        return 2
    if args.report:
        write_report_atomic(args.report, report)
    sys.stdout.write(serialize_json(report))
    return {"pass": 0, "fail": 1, "inconclusive": 3}[report["result"]]


def _run_package(args: argparse.Namespace) -> int:
    try:
        repository = _repository_root()
        artifact = build_package(repository, args.source, args.version, args.output)
    except (SourceError, PackageError) as error:
        sys.stderr.write(f"package configuration error: {error}\n")
        return 2
    report = build_artifact_report(
        report_type="package",
        inputs={
            "source": {
                "kind": "git-ref",
                "selector": args.source,
                "source_commit": artifact.source_commit,
                "snapshot_id": artifact.snapshot_id,
            },
            "version": args.version,
        },
        records=[],
        evidence_manifest=[artifact.as_dict()],
    )
    if args.report:
        write_report_atomic(args.report, report)
    sys.stdout.write(serialize_json(report))
    return 0


def _run_release_check(args: argparse.Namespace) -> int:
    try:
        repository = _repository_root()
        artifact, proposal = release_check(
            repository, args.source, args.version, args.evidence, args.output
        )
    except PackageError as error:
        sys.stderr.write(f"release-check configuration error: {error}\n")
        return 2
    except PromotionError as error:
        sys.stderr.write(f"release-check policy failure: {error}\n")
        return 1
    report = build_artifact_report(
        report_type="release-check",
        inputs={
            "source": {
                "kind": "git-ref",
                "selector": args.source,
                "source_commit": artifact.source_commit,
                "snapshot_id": artifact.snapshot_id,
            },
            "version": args.version,
        },
        records=[],
        evidence_manifest=[artifact.as_dict(), {"promotion": proposal}],
    )
    if args.report:
        write_report_atomic(args.report, report)
    sys.stdout.write(serialize_json(report))
    return 0


def _nested_command(repository: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "devquitect_quality.cli", *arguments],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
    )


def _check_record(code: str, path: str, message: str, *, passed: bool) -> dict[str, str]:
    return {
        "code": code,
        "severity": "info" if passed else "error",
        "path": path,
        "message": message,
    }


def _run_check(args: argparse.Namespace) -> int:
    records: list[dict[str, str]] = []
    evidence: list[dict[str, object]] = []
    result = "pass"
    exit_code = 0
    try:
        repository = _repository_root()
    except SourceError as error:
        repository = Path.cwd()
        records.append(_check_record("check.source", "skills", str(error), passed=False))
        result, exit_code = "fail", 2
    else:
        validation = _nested_command(
            repository, ["validate", "--source", args.source, "--format", "json"]
        )
        try:
            validation_report = json.loads(validation.stdout)
        except json.JSONDecodeError:
            validation_report = None
        if validation_report is not None:
            evidence.append(
                {
                    "report_type": "validation",
                    "result": validation_report.get("result"),
                    "source": validation_report.get("inputs", {}).get("source", {}),
                }
            )
        if validation.returncode != 0:
            records.append(
                _check_record(
                    "check.validation",
                    "skills",
                    "structural validation did not pass",
                    passed=False,
                )
            )
            result = "fail"
            exit_code = 2 if validation.returncode == 2 else 1
        else:
            records.append(
                _check_record(
                    "check.validation", "skills", "structural validation passed", passed=True
                )
            )

        if exit_code == 0:
            tests = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/unit",
                    "tests/integration",
                    "tests/contract",
                    "--ignore=tests/integration/test_check_command.py",
                    "-q",
                ],
                cwd=repository,
                check=False,
                capture_output=True,
                text=True,
            )
            tests_passed = tests.returncode == 0
            records.append(
                _check_record(
                    "check.tests",
                    "tests",
                    "fast credential-free test suite passed"
                    if tests_passed
                    else "fast credential-free test suite failed",
                    passed=tests_passed,
                )
            )
            evidence.append({"suite": "fast", "exit_code": tests.returncode})
            if not tests_passed:
                result, exit_code = "fail", 1

        if exit_code == 0 and args.behavioral:
            evaluation = _nested_command(
                repository, ["eval", "--source", args.source, "--suite", "critical"]
            )
            if evaluation.returncode != 0:
                result = "inconclusive" if evaluation.returncode == 3 else "fail"
                exit_code = evaluation.returncode if evaluation.returncode in {1, 2, 3} else 3
                records.append(
                    _check_record(
                        "check.behavioral-evaluation",
                        "evals/cases",
                        "trusted critical evaluation did not pass",
                        passed=False,
                    )
                )
            else:
                evaluation_report = json.loads(evaluation.stdout)
                evidence.append(
                    {
                        "report_type": "evaluation",
                        "result": evaluation_report["result"],
                        "source": evaluation_report["inputs"]["source"],
                        "run_ids": sorted(
                            record["run_id"]
                            for record in evaluation_report["records"]
                            if record.get("run_id")
                        ),
                        "case_digests": sorted(
                            {record["case_digest"] for record in evaluation_report["records"]}
                        ),
                    }
                )
                baseline = json.loads(
                    (repository / "baselines/stable-n.json").read_text(encoding="utf-8")
                )
                stable = str(baseline["source_commit"])
                comparison = _nested_command(
                    repository,
                    [
                        "compare",
                        "--stable",
                        stable,
                        "--candidate",
                        args.source,
                        "--suite",
                        "self-hosting",
                    ],
                )
                if comparison.returncode != 0:
                    result = "inconclusive" if comparison.returncode == 3 else "fail"
                    exit_code = (
                        comparison.returncode if comparison.returncode in {1, 2, 3} else 3
                    )
                    records.append(
                        _check_record(
                            "check.behavioral-comparison",
                            "evals/cases/self-hosting.yaml",
                            "trusted clean-candidate comparison did not pass",
                            passed=False,
                        )
                    )
                else:
                    comparison_report = json.loads(comparison.stdout)
                    evidence.append(
                        {
                            "report_type": "comparison",
                            "result": comparison_report["result"],
                            "candidate": comparison_report["inputs"]["candidate"],
                            "comparison_ids": sorted(
                                record["comparison_id"]
                                for record in comparison_report["records"]
                            ),
                        }
                    )
                    records.append(
                        _check_record(
                            "check.behavioral",
                            "evals/cases",
                            "trusted evaluation and comparison passed",
                            passed=True,
                        )
                    )

    report = build_artifact_report(
        report_type="check",
        inputs={"source": args.source, "behavioral": args.behavioral},
        records=records,
        evidence_manifest=evidence,
        result=result,
    )
    if args.report:
        write_report_atomic(args.report, report)
    sys.stdout.write(serialize_json(report))
    return exit_code


def main(argv: list[str] | None = None) -> int:
    """Run the repository-owned command surface."""

    args = _parser().parse_args(argv)
    if args.command == "validate":
        return _run_validate(args)
    if args.command == "eval":
        return _run_eval(args)
    if args.command == "compare":
        return _run_compare(args)
    if args.command == "package":
        return _run_package(args)
    if args.command == "release-check":
        return _run_release_check(args)
    if args.command == "check":
        return _run_check(args)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
