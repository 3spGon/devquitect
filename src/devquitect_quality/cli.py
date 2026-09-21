"""Command-line entry point for Devquitect quality tooling."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import uuid
from collections import Counter
from pathlib import Path

from .cases import CaseError, load_cases, select_cases
from .codex_adapter import (
    DEFAULT_TEST_MODEL,
    DEFAULT_TEST_REASONING_EFFORT,
    discover_auth_cache,
    preflight_codex,
)
from .comparison import freeze_pair, pair_records
from .evaluation import run_case
from .models import SkillSource
from .packaging import PackageError, build_package
from .promotion import PromotionError, release_check
from .reporting import (
    build_artifact_report,
    build_calibration_report,
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
    validate_calibration_report,
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
    evaluate.add_argument("--model", default=DEFAULT_TEST_MODEL)
    evaluate.add_argument(
        "--reasoning-effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default=DEFAULT_TEST_REASONING_EFFORT,
    )
    evaluate.add_argument("--report", type=Path)
    compare = commands.add_parser("compare", help="compare stable and candidate behavior")
    compare.add_argument("--stable", required=True)
    compare.add_argument("--candidate", required=True)
    comparison_selection = compare.add_mutually_exclusive_group()
    comparison_selection.add_argument("--suite")
    comparison_selection.add_argument("--case")
    compare.add_argument("--report", type=Path)
    calibrate = commands.add_parser(
        "calibrate", help="write optional behavior-calibration evidence"
    )
    calibrate.add_argument("--source", required=True)
    calibration_selection = calibrate.add_mutually_exclusive_group(required=True)
    calibration_selection.add_argument("--suite")
    calibration_selection.add_argument("--case")
    calibrate.add_argument("--model", default=DEFAULT_TEST_MODEL)
    calibrate.add_argument(
        "--reasoning-effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default=DEFAULT_TEST_REASONING_EFFORT,
    )
    calibrate.add_argument("--report", required=True, type=Path)
    compare.add_argument("--model", default=DEFAULT_TEST_MODEL)
    compare.add_argument(
        "--reasoning-effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default=DEFAULT_TEST_REASONING_EFFORT,
    )
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
    check.add_argument("--model", default=DEFAULT_TEST_MODEL)
    check.add_argument(
        "--reasoning-effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default=DEFAULT_TEST_REASONING_EFFORT,
    )
    check.add_argument("--report", type=Path)
    return parser


def _source_identity(
    source: SkillSource,
    snapshot_id: str | None = None,
    source_commit: str | None = None,
) -> dict[str, object]:
    identity: dict[str, object] = {"kind": source.kind, "selector": source.selector}
    if snapshot_id:
        identity["snapshot_id"] = snapshot_id
    if source_commit:
        identity["source_commit"] = source_commit
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
                source=_source_identity(
                    source, snapshot.snapshot_id, snapshot.resolved_commit
                ),
                records=records,
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
        inputs = load_validation_inputs(source)
        cases = select_cases(
            load_cases(repository / "evals/cases", repository / "schemas/eval-case.schema.json"),
            suite=args.suite,
            case_id=args.case,
        )
        with tempfile.TemporaryDirectory(prefix="devquitect-eval-") as temporary:
            snapshot = freeze_source(source, Path(temporary) / "snapshot")
            if any(case.is_scenario for case in cases):
                errors = validate_snapshot(snapshot, inputs)
                if errors:
                    raise ValueError(f"scenario source validation failed: {errors[0]['message']}")
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
                    validation_inputs=inputs,
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
        stable_inputs = load_validation_inputs(stable_source)
        candidate_inputs = load_validation_inputs(candidate_source)
        with tempfile.TemporaryDirectory(prefix="devquitect-compare-") as temporary:
            pair = freeze_pair(stable_source, candidate_source, Path(temporary))
            stable_records = [
                record
                for case in cases
                for record in run_case(
                    case,
                    pair.stable,
                    repository,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    auth_cache=auth_cache,
                    validation_inputs=stable_inputs,
                )
            ]
            candidate_records = [
                record
                for case in cases
                for record in run_case(
                    case,
                    pair.candidate,
                    repository,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    auth_cache=auth_cache,
                    validation_inputs=candidate_inputs,
                )
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


def _calibration_dimensions(records: list[dict[str, object]]) -> dict[str, object]:
    outcomes = Counter(str(record["classification"]) for record in records)
    by_case: dict[str, dict[str, int]] = {}
    for record in records:
        case_id = str(record["case_id"])
        outcome = str(record["classification"])
        case_outcomes = by_case.setdefault(case_id, {})
        case_outcomes[outcome] = case_outcomes.get(outcome, 0) + 1
    return {"outcomes": dict(sorted(outcomes.items())), "cases": dict(sorted(by_case.items()))}


def _calibration_evidence(records: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "run_id": record["run_id"],
            "case_id": record["case_id"],
            "classification": record["classification"],
            "runtime_errors": [str(error)[:500] for error in record["runtime_errors"][:10]],
            "redactions": record["redactions"][:50],
        }
        for record in records[:100]
    ]


def _run_calibrate(args: argparse.Namespace) -> int:
    try:
        repository = _repository_root()
        source = SkillSource.from_selector(args.source, repository)
        inputs = load_validation_inputs(source)
        cases = select_cases(
            load_cases(repository / "evals/cases", repository / "schemas/eval-case.schema.json"),
            suite=args.suite,
            case_id=args.case,
        )
        with tempfile.TemporaryDirectory(prefix="devquitect-calibrate-") as temporary:
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
                    validation_inputs=inputs,
                )
            ]
            suite_digest = hashlib.sha256(
                "".join(case.digest for case in cases).encode("ascii")
            ).hexdigest()
            report = build_calibration_report(
                run_id=str(uuid.uuid4()),
                skill_snapshot_id=snapshot.snapshot_id,
                skill_version=snapshot.resolved_commit,
                model=args.model,
                runtime={"codex_cli": preflight_codex().version},
                suite_id=args.suite or str(args.case),
                suite_digest=suite_digest,
                repetitions=len(records),
                dimensions=_calibration_dimensions(records),
                evidence_references=_calibration_evidence(records),
            )
        validate_calibration_report(report, inputs)
    except (SourceError, CaseError, ValidationConfigurationError, ValueError) as error:
        sys.stderr.write(f"calibration configuration error: {error}\n")
        return 2
    write_report_atomic(args.report, report)
    sys.stdout.write(serialize_json(report))
    return 0


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
                repository,
                [
                    "eval",
                    "--source",
                    args.source,
                    "--suite",
                    "critical",
                    "--model",
                    args.model,
                    "--reasoning-effort",
                    args.reasoning_effort,
                ],
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
                        "--model",
                        args.model,
                        "--reasoning-effort",
                        args.reasoning_effort,
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
        inputs={
            "source": args.source,
            "behavioral": args.behavioral,
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
        },
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
    if args.command == "calibrate":
        return _run_calibrate(args)
    if args.command == "package":
        return _run_package(args)
    if args.command == "release-check":
        return _run_release_check(args)
    if args.command == "check":
        return _run_check(args)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
