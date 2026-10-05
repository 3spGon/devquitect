# Devquitect Next implementation plan

Status: Approved
Plan revision: 3
Last updated: 2026-10-03

## Goal

Deliver lean and traceable skill contracts plus QUICK in 0.7.0; generalized definition continuity and invocation policy in 0.8.0; then credential-free Continuous Verification and exact-candidate Release Readiness for 1.0.0. `verify_slice.py`, its Python/PyYAML dependencies, YAML inventory format, and acceptance behavior are excluded from every slice.

## Definition inputs and constraints

- [Concept](01-concept.md), [requirements](02-requirements.md), [architecture](04-architecture.md), [data model](05-data-model.md), [interfaces](06-api-contracts.md), [decisions](07-decisions.md), and [prompt-change ledger](prompt-change-ledger.md).
- Preserve the three established authority boundaries. Do not introduce a fourth global router.
- Each material prompt change is one named group, with an immutable baseline, the same deterministic cases, and a ledger entry. Behavioral comparison is separately authorized and never substitutes for deterministic failures.
- Do not modify `skills/project-plan-execution/scripts/verify_slice.py`, its YAML inventory contract, or its dependencies.
- No slice is authorized by this plan. Approval must name the intended `SLICE-DN-*` identifiers.

The existing scope through DN-004 was approved under revision 2. The amended concept/requirements received Gate 1 approval, and architecture/data/interfaces/decisions received explicit Gate 2 approval, on 2026-10-03. The user separately approved plan revision 3 on 2026-10-03. It reconciles those approved interfaces, proposed implementation paths, and verification coverage; proposed CLI options and new-file checks become available during authorized delivery, not from this definition update.

The Change Profile remains confirmed, full / rigorous, and cross-cutting. The new surfaces are CI operations, evidence interfaces, security/trust boundaries, quality attributes, and release compatibility. No application code, workflow, guardrail, dependency, remote setting, or release action is implemented by editing this plan.

## Revision 3 review impact

Only `SLICE-DN-005` and `SLICE-DN-006` change. DN-001 through DN-004, AC-DN-001 through AC-DN-008, and their verification inventory remain unchanged. Existing AC-DN-009 through AC-DN-012 retain their meanings; new criteria add CI and candidate-evidence guarantees rather than silently reassign existing identifiers.

The expanded scope invalidated the prior gates; amended Gate 1, Gate 2, and plan revision 3 are now explicitly approved. This completes the revision-3 definition amendment without adding further product scope. `09-delivery-status.md` remains historical delivery authority for revision 2 and is not rewritten by definition work. On later authorized delivery, `project-plan-execution` must reconcile the plan revision and invalidate only affected slice evidence. No execution of DN-005 / DN-006, behavioral comparisons, or remote settings is inferred here.

## SLICE-DN-001 — Lean entrypoints and prompt-change evidence for 0.7.0

Simplify the three existing skill entrypoints so each policy appears once while their authoritative references retain detailed mechanics. Establish the append-only prompt-change ledger and deterministic positive/negative cases for every changed rule group.

Paths: `skills/software-idea-to-project/`, `skills/project-plan-execution/`, `skills/targeted-refactoring/`, `authority-map.yaml`, `evals/cases/`, `docs/skill-change-ledger.md` (new), and `docs/software-design/devquitect-next/prompt-change-ledger.md`.

Outcome: concise entrypoints preserve definition-versus-implementation, plan-execution, and behavior-preserving-refactor boundaries, with reconstructable source and evidence for each simplification.

## SLICE-DN-002 — QUICK route for 0.7.0

Add `quick-change` as an independently discoverable skill for authorized, localized, reversible, directly verifiable work. Its description and deterministic cases distinguish eligible work from mandatory escalation; explicit invocation remains authoritative.

Paths: `skills/quick-change/` (new), `.codex-plugin/plugin.json`, `authority-map.yaml`, and `evals/cases/`.

Outcome: an eligible local change can use QUICK without a universal router, while features, public contracts, persistence, security, migrations, multi-module work, and durable continuity are routed away.

## SLICE-DN-003 — General workflow depth and durable roots for 0.8.0

Generalize workflow-depth selection beyond system-change sessions and add the minimal persistent-state contract for a caller-supplied repository-relative definition root. Preserve legacy session discovery and do not move existing sessions.

Paths: `skills/software-idea-to-project/SKILL.md`, `skills/software-idea-to-project/references/` (including new `workflow-depth.md`), `authority-map.yaml`, and `evals/cases/`.

Outcome: every initiative has proportionate depth, and a resumed persistent session uses its recorded root before default discovery; ambiguous candidates require user selection.

## SLICE-DN-004 — Invocation policy and evaluation matrix for 0.8.0

Declare per-skill implicit-invocation policy in metadata: definition, QUICK, and targeted refactoring may be eligible; `project-plan-execution` is explicit-only. Add the cross-generation model/host matrix and ledger references needed to make the approved GPT-5.6 baseline and GPT-6 Sol/Luna comparisons reproducible without pooling results.

Paths: `skills/*/agents/openai.yaml`, `skills/software-idea-to-project/references/`, `skills/quick-change/`, `authority-map.yaml`, `evals/cases/`, `docs/skill-change-ledger.md`, and `docs/software-design/devquitect-next/prompt-change-ledger.md`.

Outcome: host routing has explicit boundaries, and each behavioral evidence row identifies one canonical model ID, host, runtime, reasoning effort where supported, suite revision, repetitions, report references, and an independent verdict. The initial rows are `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`. Comparisons reuse the same prompt-change group and representative cases. If host, runtime, or effort differs, record it and avoid a model-only claim. This slice runs no behavioral comparison without separate user authorization.

## SLICE-DN-005 — Continuous Verification and Stabilization for 1.0.0

Outcome: a candidate receives independent credential-free verification from clean GitHub runners, a reproducible package, and attributable CI evidence. Preserve stabilization of entrypoint boundaries, QUICK escalation, workflow continuity, invocation policy, ledger completeness, and the unchanged distributed verifier. DN-004 is the prerequisite and remains the behavioral matrix authority.

Verified paths to reuse: `pyproject.toml`, `uv.lock`, `src/devquitect_quality/cli.py`, `src/devquitect_quality/packaging.py`, `src/devquitect_quality/reporting.py`, `hooks/`, `tests/unit/test_compaction_recovery_hook.py`, `tests/unit/test_packaging.py`, `tests/integration/test_check_command.py`, `tests/contract/`, `docs/contributing-skills.md`, and `docs/software-design/system-context.md`.

Proposed paths to create: `.github/workflows/ci.yml`, `.github/workflows/behavioral.yml`, `schemas/ci-evidence.schema.json`, and `tests/contract/test_ci_workflow_contract.py`. DN-005 produces the version-1 CI evidence document using existing reporting/serialization ownership; DN-006 consumes it. Creation of `.github/workflows/release-readiness.yml` and its release behavior belongs to DN-006. Existing `skills/`, `authority-map.yaml`, and `evals/cases/` are touched only to close a demonstrated in-scope contract gap; any critical skill change uses its owner and positive/negative cases.

Delivery scope from the approved technical design:

1. **Quality:** checkout the tested commit with history sufficient for comparisons; set Python 3.12; install pinned `uv` and the locked environment via `uv sync --locked --all-groups`; run `uv run devquitect check --source HEAD --report .devquitect-reports/check.json` and `uv run ruff check src tests`. Verify checkout, installed tooling, and source identity coincide. Run an introduced-whitespace check against the event-specific base, not a hardcoded branch. Save reports even when a step fails, with explicit failure metadata.
2. **Source events:** run CI for `pull_request` and `push` to `main`. Record PR tested integration SHA, head SHA, and base SHA separately. After integration, verify the final `main` SHA independently. Add `merge_group` only if merge queue is enabled. A normal PR check never uses `working-tree` as its primary source.
3. **Platform smoke:** initially use `ubuntu-latest`, `macos-latest`, and `windows-latest`, all on Python 3.12. Run compaction recovery, relevant CLI contracts, path-sensitive packaging, and Windows-specific cases. Reuse `uv run pytest tests/unit/test_compaction_recovery_hook.py tests/contract tests/unit/test_packaging.py`; expand focused cases only where a real platform risk lacks coverage. Do not add a multi-Python matrix.
4. **Package and evidence producer:** on the canonical Linux runner, read the committed plugin version and invoke existing `devquitect package` twice for the same full SHA/version in fresh output roots. Require equal ZIP SHA-256 and deterministic entry manifests. Record actual Python patch, uv, quality-tool/source commit, compression runtime, runner image, and lockfile digest. Generate schema-valid `ci-evidence.json` with package/report file identities as specified in the approved data model; exclude its own recursive file digest. Each job uploads its own artifact using `<candidate-sha>-attempt-<run-attempt>` names: quality contains `check.json`, platform jobs contain their result/identity, and package contains ZIP, manifest, package report, and CI index. Request 30-day retention. These are CI evidence, never public releases. Retain existing committed-version enforcement.
5. **Merge gates:** use literal `Devquitect / quality`, `Devquitect / platform-smoke`, and `Devquitect / package` as required-check names. Matrix variant names append `(ubuntu-latest)`, `(macos-latest)`, or `(windows-latest)` to platform-smoke. The aggregate always executes after dependencies and explicitly requires success from all variants; cancelled/skipped/missing variants cannot pass. Verify effective `main` protection, required checks, no force push, no deletion, and PR integration. If settings require a separately authorized maintainer action, document and report it as pending; do not claim the protected merge gate complete. Repository files alone cannot apply remote protection.
6. **Security and behavioral separation:** normal PR/push jobs use `contents: read`, pinned action revisions, and no model secrets, subscription cache, publishing token, or write rights. The dedicated behavioral workflow is manual (`workflow_dispatch`), never required, and usable only with explicit authorization, a reviewed repository source, and configured supported unattended API-key authentication. Reject supervised-only `chatgpt-cache-local` on CI. It delegates to existing eval/compare/behavioral-check infrastructure and preserves DN-004 rows; no dispatch, credential configuration, or model run is authorized by this slice plan alone. Missing configuration yields a clear non-run state without affecting deterministic PR gates.
7. **Stabilization and baseline:** close deterministic contract gaps without altering `verify_slice.py`, its YAML format, dependencies, or snapshot/check/close semantics. After implementation and verification, refresh only System Context sections affected by actual CI, verification procedures, interfaces, limitations, and preserved behavior, referencing the verified delivery source. Planned CI must not be described as operational before that point.

Positive/negative evidence must exercise a successful clean run and all required platform variants; schema-valid CI index; wrong source identity; malformed/missing metadata; failed/cancelled/skipped required jobs; differing rebuild digests; event-base whitespace failures, including first-push empty-tree comparison; and behavioral workflow separation without credentials. The proposed workflow contract test checks job names, mandatory triggers, read-only permissions, always-run aggregate, attempt-specific artifact names, and 30-day retention. Run it via CHECK-DN-023 after creating it. Local fixtures protect configuration and policy, while actual GitHub runs prove clean-runner/platform behavior. A local green suite alone cannot prove hosted CI or effective protection.

The verification inventory below retains local working-tree checks for development and adds focused tests. Hosted evidence from the exact commit and effective repository settings is additional acceptance evidence recorded in the slice detail. CI input/evidence paths are fingerprints for this slice, not permission to commit generated reports or packages.

## SLICE-DN-006 — Release Readiness and Candidate Evidence for 1.0.0

Outcome: maintainers receive a structured release-eligibility decision and an explicitly unapproved proposal for one exact candidate SHA/version/package. DN-005 is the prerequisite; DN-006 consumes its evidence rather than redefining normal CI.

Verified paths to reuse or extend: `src/devquitect_quality/promotion.py`, `src/devquitect_quality/cli.py`, `src/devquitect_quality/packaging.py`, `src/devquitect_quality/reporting.py`, `schemas/report.schema.json`, `schemas/promotion-record.schema.json`, `tests/integration/test_release_check.py`, `tests/unit/test_packaging.py`, `tests/contract/`, `.codex-plugin/plugin.json`, and `docs/contributing-skills.md`.

Proposed paths to create: `.github/workflows/release-readiness.yml`, `src/devquitect_quality/github_evidence.py`, and `tests/unit/test_github_evidence.py`. Consume `schemas/ci-evidence.schema.json` delivered by DN-005. Generated `.devquitect-reports/` and package outputs are evidence, not new committed application state. `docs/skill-change-ledger.md` and the session's `prompt-change-ledger.md` remain owners of authorized prompt/behavioral rows; readiness must not fabricate observations or overwrite those histories.

Delivery scope from the approved technical design:

1. **Explicit candidate and CLI:** implement approved `release-check` options `--repository`, `--ci-run-id`, `--ci-run-attempt`, `--previous-release`, and optional `--behavioral-evidence`. The three CI selectors are all-or-none; CI mode requires a full source SHA, prior-release SHA, fresh empty evidence directory, and non-existing output directory. Workflow inputs are `candidate_sha`, `version`, `ci_run_id`, `ci_run_attempt`, and `previous_release_sha`; repository is fixed to the current repository. Resolve identity once and install the reviewed candidate's locked tooling. A SHA change requires a new attempt, never tree equivalence.
2. **GitHub adapter:** use standard-library HTTP/JSON/hash/ZIP support and read-only `GH_TOKEN`, without new dependencies. Verify repository against checkout remote; exact workflow path `.github/workflows/ci.yml`; successful `push` on `main`; candidate SHA; complete selected attempt jobs; quality, all three variants, aggregate, and package. Fetch paginated metadata, verify unique expected artifact IDs/names, their producer-job time interval, non-expiration, and API-provided container digest before safe extraction. Refuse missing digest. Use fresh roots, HTTPS-only API-issued redirects without forwarding tokens to storage, 30-second requests, and at most three transient retries. Reject unsafe paths, duplicates, symlinks, unexpected members, and archives beyond 64 MiB compressed / 128 MiB expanded / 1024 entries. Partial/mixed attempts cannot pass.
3. **Package binding:** verify ZIP and manifest file digests, their source SHA/snapshot and version, and requested/committed/packaged/manifest version equality. Run the existing rebuild eligibility policy and compare the downloaded canonical ZIP with the package it actually evaluates. GitHub's artifact-container digest is a separate transport identity, not the Devquitect ZIP digest. Tampering or mismatch must be a deterministic failure, not a warning.
4. **Shared policy:** enforce provenance/completeness and downloaded-package binding in the existing promotion policy using the adapter's observed metadata and actual verified file paths; no caller can bypass it with a purported trusted JSON registry. Keep current report and promotion schemas unchanged. Add CI/package/prior-release/behavioral entries to the canonical report's existing inputs and evidence manifest. Legacy calls without CI selectors make no network request and retain their established behavior.
5. **Compatibility baseline:** `--previous-release` identifies a readable committed ancestor with a lower plugin version. Cover a successful post-bump candidate. Existing callers omitting the option preserve immediate-parent policy. Reject unrelated ancestry, unreadable baseline, non-increasing version, invalid migration evidence when required, and mismatched committed version. The baseline remains distinct from candidate identity.
6. **Behavioral evidence:** the optional separate directory contains `rows.json` with R-10 dimensions, authorization references, independent verdicts, and safe relative canonical-report paths/digests. Validate report schemas and exact candidate snapshot; reject undeclared, missing, malformed, or mismatched supplied reports. Keep `pass`, `fail`, `inconclusive`, and `not-run` independent; absent/unexecuted rows have no reports or observed runtime. Readiness launches no models and optional behavioral verdicts never replace deterministic failures.
7. **Result and operation:** use the approved schema-v1 `release-check` envelope and unchanged unapproved promotion object, retaining null approval fields; `generated_at` records the timestamp. CI mode exits `0` eligible, `1` policy rejection (including missing/expired mandatory evidence), `2` invalid configuration, or `3` unavailable infrastructure. All failures emit non-passing diagnostic reports. Stage ZIP, manifest, and proposal privately and rename the new output directory only after complete success; preserve existing user files. Use `contents: read` and `actions: read`, with no publication rights. Request 30-day CI/readiness artifact retention and verify repository-policy support; expiration requires fresh matching CI.
8. **Baseline and handoff:** after the workflow and shared policy are implemented and verified, refresh System Context's release/evidence capabilities, compatibility policy, verification procedures, and limitations using the verified candidate. Present the proposal for a separate human decision. Do not tag, push, publish, deploy, modify `main`, or approve promotion.

Required deterministic cases include the complete positive candidate path; post-bump candidate with explicit previous-release ancestor; legacy no-network/default compatibility; wrong SHA/snapshot/repository/workflow/attempt; incomplete/partial platform results; expired/missing evidence or digest; altered ZIP/manifest; version mismatch; invalid/unrelated prior-release baseline; unsafe archive/redirect/pagination/retry cases; invalid CLI option combinations and output path; behavioral pass alongside deterministic failure; and failure with no eligible output/proposal. Transport fixtures in the proposed unit test prove adapter policy without credentials. Extend existing release integration/CLI contract tests to exercise the approved flags, exit/report shapes, index validation, and staged-output behavior. A real manual hosted readiness run proves end-to-end consumption without publishing.

The production invocation after implementation is `uv run devquitect release-check --source "$CANDIDATE_SHA" --version "$CANDIDATE_VERSION" --repository "$GITHUB_REPOSITORY" --ci-run-id "$CI_RUN_ID" --ci-run-attempt "$CI_RUN_ATTEMPT" --previous-release "$PREVIOUS_RELEASE_SHA" --evidence .devquitect-reports/ci-input --output dist/readiness --report .devquitect-reports/release-readiness.json`. Inputs must be validated and the evidence directory empty/output absent; the read-only token stays in the environment. This is a parameterized future workflow invocation, not a command to run during planning or an inventory check containing unresolved placeholders.

## Confirmed stack, assumptions, and deferred scope

The verified stack is Python 3.12+, `uv.lock`, pytest, Ruff, existing Git source snapshots, normalized ZIP packaging, and canonical JSON reports. No new dependency or skill is justified by this amendment. Package reproducibility initially means the same source/version/locked toolchain on the canonical runner, not cross-platform byte equality.

Assume GitHub-hosted runners and read-only artifact access are available; delivery must verify them. Effective branch-protection configuration is a separate external action requiring the applicable authorization. The approved review-retention period is 30 days, subject to verified repository support. Missing or expired evidence never passes by assumption. Toolchain/runner drift may invalidate byte equality; record it and rerun matching CI rather than weaken package identity.

Deferred: extra Python versions, public release triggers, automatic deployment/publication, tags, promotion approval, installations, attestations, and a generic release-management platform. No implementation-blocking design decision remains. Hosted execution, effective protection, and retention support are acceptance evidence to obtain during separately authorized delivery.

## Requirement and verification traceability

| Approved requirement | Owning slices | Verification |
| --- | --- | --- |
| R-01, R-02 | DN-001 | AC-DN-001/002 and the credential-free contract cases. |
| R-03, R-04 | DN-002 | AC-DN-003/004 and QUICK positive/escalation cases. |
| R-05 | DN-005 | AC-DN-009 and preserved verifier diff/contract checks. |
| R-06 | DN-005, DN-006 | AC-DN-009/010/011, verified System Context refresh, exact-candidate eligibility. |
| R-07, R-08 | DN-001, DN-004, DN-005 | Rule-group/baseline/case ledger evidence under AC-DN-001/002/008/009; independently authorized comparisons only. |
| R-09 | DN-003 | AC-DN-005/006 and root/depth continuity cases. |
| R-10 | DN-004, DN-005, DN-006 | AC-DN-007/008/012/014 and independent behavioral/index separation cases. |
| R-11 | DN-005 | AC-DN-015/019/021; workflow fixtures, hosted exact-source runs, and effective protection. |
| R-12 | DN-005 | AC-DN-013/020; platform smoke and independent canonical rebuilds. |
| R-13 | DN-006 | AC-DN-016/017/023; transport/promotion fixtures and a hosted exact-attempt readiness run. |
| R-14 | DN-006 | AC-DN-018/022; report/proposal compatibility, legacy and post-bump cases, no-publication dry run. |

Maintainer input/error/recovery states are covered by R-11/R-13/R-14 and the same workflow/CLI fixtures; no graphical artifact is required. New fixture commands below target explicitly proposed files and run once those files are delivered. Local checks prove repository behavior; the slice detail must separately retain actual runner, protection, and retention evidence before acceptance.

## Verification inventory

```devquitect-verification
schema_version: 1
slices:
  SLICE-DN-001:
    depends_on: []
    criteria:
      AC-DN-001:
        text: "The three lean entrypoints preserve their distinct authority boundaries and every material rule-group change has an immutable baseline and ledger entry."
        requirement: R-01
      AC-DN-002:
        text: "Each changed entrypoint rule group has relevant deterministic positive and negative coverage."
        requirement: R-02
    checks:
      CHECK-DN-001:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-002:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-003:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills/software-idea-to-project"
      - "skills/project-plan-execution"
      - "skills/targeted-refactoring"
      - "authority-map.yaml"
      - "evals/cases"
      - "docs/skill-change-ledger.md"
  SLICE-DN-002:
    depends_on: ["SLICE-DN-001"]
    criteria:
      AC-DN-003:
        text: "QUICK is independently discoverable for eligible local changes and escalates every stated disqualifier."
        requirement: R-03
      AC-DN-004:
        text: "QUICK does not introduce a universal fourth routing skill."
        requirement: R-04
    checks:
      CHECK-DN-004:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-005:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-006:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills/quick-change"
      - ".codex-plugin/plugin.json"
      - "authority-map.yaml"
      - "evals/cases"
  SLICE-DN-003:
    depends_on: ["SLICE-DN-002"]
    criteria:
      AC-DN-005:
        text: "Workflow depth is recorded for every initiative, legacy sessions default safely, and configured roots resume without moving existing sessions."
        requirement: R-09
      AC-DN-006:
        text: "Ambiguous persistent-session discovery requires user selection."
        requirement: R-09
    checks:
      CHECK-DN-007:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-008:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-009:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills/software-idea-to-project"
      - "authority-map.yaml"
      - "evals/cases"
  SLICE-DN-004:
    depends_on: ["SLICE-DN-003"]
    criteria:
      AC-DN-007:
        text: "project-plan-execution is explicit-only while other skill policies are declared, and explicit invocation takes precedence."
        requirement: R-10
      AC-DN-008:
        text: "Each authorized behavioral evidence row records one canonical model ID, host, runtime, reasoning effort where supported, suite revision, repetitions, report references, and an independent verdict; the initial model IDs are gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, gpt-6-sol, and gpt-6-luna, compared on the same prompt-change group and representative cases without pooling results."
        requirement: R-10
    checks:
      CHECK-DN-010:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-011:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-012:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills"
      - "authority-map.yaml"
      - "evals/cases"
      - "docs/skill-change-ledger.md"
  SLICE-DN-005:
    depends_on: ["SLICE-DN-004"]
    criteria:
      AC-DN-009:
        text: "The assembled candidate has current credential-free evidence for changed contracts and leaves verify_slice.py and its YAML verification contract unchanged."
        requirement: R-05
      AC-DN-010:
        text: "The System Context reflects only verified implementation evidence."
        requirement: R-06
      AC-DN-013:
        text: "Compaction recovery, relevant CLI contracts, and path-sensitive packaging smoke tests pass on Linux, macOS, and Windows with Python 3.12."
        requirement: R-12
      AC-DN-014:
        text: "The manual behavioral workflow is separate from deterministic required checks and cannot substitute for a failed deterministic gate."
        requirement: R-10
      AC-DN-015:
        text: "Clean CI evidence identifies the exact tested commit and installed tool revision, distinguishing PR integration/head/base identities from the independently verified final candidate SHA."
        requirement: R-11
      AC-DN-019:
        text: "Quality runs structural validation, credential-free tests, Ruff, and event-base whitespace checks from the locked Python 3.12 environment without model credentials or write permissions."
        requirement: R-11
      AC-DN-020:
        text: "Two independent canonical builds of the same commit, version, and locked toolchain have equal ZIP SHA-256 and deterministic entry manifests."
        requirement: R-12
      AC-DN-021:
        text: "Effective main protection requires successful quality, all mandatory platform-smoke variants, and package checks, prevents force push and deletion, and never treats failed, cancelled, or skipped mandatory jobs as verified."
        requirement: R-11
    checks:
      CHECK-DN-013:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-014:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-015:
        command: "git diff --check"
        cwd: "."
      CHECK-DN-019:
        command: "uv run pytest tests/unit/test_compaction_recovery_hook.py tests/unit/test_packaging.py tests/contract"
        cwd: "."
      CHECK-DN-020:
        command: "uv run pytest tests/integration/test_check_command.py"
        cwd: "."
      CHECK-DN-023:
        command: "uv run pytest tests/contract/test_ci_workflow_contract.py"
        cwd: "."
    inputs:
      - ".github/workflows/ci.yml"
      - ".github/workflows/behavioral.yml"
      - "pyproject.toml"
      - "uv.lock"
      - "schemas/ci-evidence.schema.json"
      - "hooks"
      - "src/devquitect_quality"
      - "tests/unit/test_compaction_recovery_hook.py"
      - "tests/unit/test_packaging.py"
      - "tests/integration/test_check_command.py"
      - "tests/contract"
      - "skills"
      - "authority-map.yaml"
      - "evals/cases"
      - ".codex-plugin/plugin.json"
      - "docs/contributing-skills.md"
      - "docs/software-design/system-context.md"
  SLICE-DN-006:
    depends_on: ["SLICE-DN-005"]
    criteria:
      AC-DN-011:
        text: "Release-readiness evidence is bound to an exact candidate and does not publish, tag, or promote it."
        requirement: R-06
      AC-DN-012:
        text: "Authorized behavioral evidence, if present, does not override deterministic failures or combine independent matrix rows."
        requirement: R-10
      AC-DN-016:
        text: "Readiness verifies expected repository/workflow/run/attempt provenance and successful quality, every mandatory platform variant, and package evidence for the exact candidate SHA."
        requirement: R-13
      AC-DN-017:
        text: "Downloaded ZIP and manifest digests, source identity, and requested/committed/packaged/manifest versions match the exact package evaluated by release-check."
        requirement: R-13
      AC-DN-018:
        text: "Readiness emits structured eligibility and an unapproved timestamped promotion proposal with CI and optional behavioral references without tagging, publishing, changing main, or approving promotion."
        requirement: R-14
      AC-DN-022:
        text: "An explicit immutable previous-release reference supports candidates after the version bump while omitted-option callers preserve parent-based compatibility behavior."
        requirement: R-14
      AC-DN-023:
        text: "Deterministic policy rejects wrong-candidate, tampered, missing, expired, partial, cancelled, skipped, or mixed-attempt mandatory evidence and distinguishes policy failure from infrastructure unavailability."
        requirement: R-13
    checks:
      CHECK-DN-016:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-017:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-018:
        command: "git diff --check"
        cwd: "."
      CHECK-DN-021:
        command: "uv run pytest tests/integration/test_release_check.py tests/unit/test_packaging.py tests/contract"
        cwd: "."
      CHECK-DN-022:
        command: "uv run pytest tests/unit/test_github_evidence.py"
        cwd: "."
    inputs:
      - ".github/workflows/release-readiness.yml"
      - ".github/workflows/ci.yml"
      - "src/devquitect_quality/promotion.py"
      - "src/devquitect_quality/github_evidence.py"
      - "src/devquitect_quality/cli.py"
      - "src/devquitect_quality/packaging.py"
      - "src/devquitect_quality/reporting.py"
      - "schemas/report.schema.json"
      - "schemas/promotion-record.schema.json"
      - "schemas/ci-evidence.schema.json"
      - "tests/integration/test_release_check.py"
      - "tests/unit/test_packaging.py"
      - "tests/unit/test_github_evidence.py"
      - "tests/contract"
      - "docs/contributing-skills.md"
      - "docs/software-design/system-context.md"
      - "docs/skill-change-ledger.md"
      - ".codex-plugin/plugin.json"
```

## Rollout and rollback

Each 0.7.0 and 0.8.0 slice is reverted by restoring only its changed skill and contract files. Existing sessions remain in place. `verify_slice.py` is never part of this rollout. 1.0.0 readiness does not tag, publish, or promote; those actions require separate authorization.

DN-005 rolls out workflows and fixture checks before required checks are activated. Verify stable names and real runner evidence, then apply separately authorized remote protection; record any unavailable setting as incomplete acceptance. Rollback requires coordinated workflow/check-name and protection changes so removing a required job does not leave all PRs permanently pending. It does not bypass a failure to merge a candidate.

DN-006 rolls out shared policy with backward-compatible local defaults and fixture evidence before enabling manual readiness. A successful hosted dry run must leave publication and approval fields untouched. Roll back only its workflow, policy/interface extensions, and baseline documentation together; retain historical reports and proposals as evidence of their original candidates. Expired or withdrawn evidence requires a fresh verification, not reinterpretation of old results.
