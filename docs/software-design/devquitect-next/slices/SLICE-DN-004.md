---
schema_version: 1
session: devquitect-next
slice: SLICE-DN-004
plan_revision: 2
plan_digest: fe4e049a196667e91b59807f1fc2670b105fde5ea56c8daff0136b3bb0b33e3e
verified_at: '2026-10-02T18:28:49Z'
inputs_digest: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
environment:
  python: 3.14.7
  PyYAML: 6.0.3
criteria:
  AC-DN-007:
    action: Verify per-skill implicit policy and explicit invocation precedence without expanding authority.
    expected: >-
      Execution declares allow_implicit_invocation false; definition, QUICK, and targeted refactoring
      declare true. Explicit invocation remains available and takes precedence over matching,
      without granting implementation or suppressing scope checks.
    method: >-
      Trace materialize_attempt copying snapshot skills and native metadata to the isolated host.
      Parse all four agents/openai.yaml files in the focused contract test, verify actual boolean
      policy values and explicit default prompts, inspect the authority map and canonical invocation
      guidance, and retain explicit-positive/implicit-negative representative cases.
    observed: >-
      All four metadata policy tests passed: execution false, definition true, QUICK true, and
      refactoring true. Each explicit default prompt names its own skill. The precedence and
      scope test passed, including QUICK's existing refusal to expand authority or suppress escalation.
      Definition and execution metadata changed; QUICK and refactoring already matched the plan.
      Structural validation accepted metadata, ownership, packaging, and all cases. No universal
      router was introduced. This verifies the native configuration and contract, not a live
      model-backed host selection in the initial verification. The separately authorized follow-up
      passed all twelve candidate cases on gpt-5.6-luna/high with the corrected supervisor configuration.
    status: PASS
    evidence: CHECK-DN-010
  AC-DN-008:
    action: Verify reproducible independent evidence rows for the five approved canonical models.
    expected: >-
      Each row identifies its model, host, runtime, effort, suite revision, repetitions, reports,
      authorization, and independent verdict. Comparisons share one change group, source pair,
      and representative suite, never pool results, and retain configuration differences.
    method: >-
      Parse the actual fenced ledger matrix, recompute its revision from twelve sorted case IDs
      and case-file SHA-256 values, check the five canonical models and required fields, trace
      group/baseline/candidate references, and run positive/negative matrix assertions through
      evaluate_assertion using safe synthetic output and one violation for every required field.
    observed: >-
      The matrix test passed for gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, gpt-6-sol, and gpt-6-luna.
      All rows have the same twelve-case suite revision e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0,
      intended repetitions 1, null unobserved host/runtime/effort, empty reports, not-authorized,
      and independent not-run verdicts. The documented run contract requires actual names/versions,
      high effort where supported, actual repetitions, report and source/case identities, and
      independent results. Safe synthetic outputs passed both final-json cases; each missing or
      invalid criterion field failed critically. Negative guidance rejects pooling, model-only claims
      for differing configurations, invented evidence, release approval, and adapter failures as passes.
      Three ledger groups bind immutable baseline dff146543c870a56b55d1ed339eeb95f6397653f to the actual
      candidate file hashes, all independently recomputed and matched. No row claims a behavioral
      result in the initial inventory. Two separately authorized observed rows now retain both
      supervisor configurations without pooling; the corrected row has ten equivalences and two improvements.
      Comparisons require separate authorization and are not a completion prerequisite
      for this implementation slice under approved plan revision 2.
    status: PASS
    evidence: CHECK-DN-010
checks:
  CHECK-DN-010:
    command: uv run devquitect check --source working-tree --report .devquitect-reports/check.json
    cwd: .
    started_at: '2026-10-02T18:28:33.002Z'
    finished_at: '2026-10-02T18:28:48.658Z'
    exit_code: 0
    status: PASS
    observed: Structural validation and fast credential-free suite passed; report result pass, behavioral false.
    inputs_before: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
    inputs_after: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
  CHECK-DN-011:
    command: uv run ruff check src tests
    cwd: .
    started_at: '2026-10-02T18:28:48.658Z'
    finished_at: '2026-10-02T18:28:48.719Z'
    exit_code: 0
    status: PASS
    observed: All checks passed!
    inputs_before: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
    inputs_after: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
  CHECK-DN-012:
    command: git diff --check
    cwd: .
    started_at: '2026-10-02T18:28:48.719Z'
    finished_at: '2026-10-02T18:28:48.730Z'
    exit_code: 0
    status: PASS
    observed: No output; the diff is whitespace-clean.
    inputs_before: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
    inputs_after: 1f27d92b4177e4b66018b664ed28097d6d21e7579a074095c076279f7cc4d151
---

# PASS — SLICE-DN-004 evidence

Branch: `codex/slice-dn-004-invocation-matrix`. The user's 2026-10-02 authorization covers
only local DN-004 implementation and verification. Definition gates and plan revision 2
were approved; DN-003 was verified. DN-005, DN-006, behavioral comparisons, release actions,
commits, and pushes were not authorized or performed during the original slice execution.

## Functional and cumulative review

`uv run --offline pytest tests/unit/test_invocation_matrix_contract.py -q` passed all 9 tests
after the final implementation. Tests inspect actual host metadata, source guidance, matrix
fields and case hashes, and execute deterministic assertions against synthetic observations.
This is credential-free functional coverage, not evidence of model behavior. Test-file SHA-256:
`75247657d5653ba740c2ac7902dfd844eedcc0c38e75b5a4715444f8579e3427`.

Material changes: execution and definition `agents/openai.yaml`, the existing definition
`implementation-planning.md` reference, `authority-map.yaml`, three external cases, the focused
contract tests, append-only records in both ledgers, and this slice's delivery checkpoint/evidence.
The candidate hashes in all three new ledger groups matched current files. Existing QUICK and
refactoring metadata already met the policy and needed no mutation.

Final diff review mapped metadata/precedence to AC-DN-007 and the matrix/guidance/ledger/cases
to AC-DN-008. The plan, verifier script, verification inventory, dependencies, and unrelated
source code are unchanged. The entrypoints stay concise; detailed guidance uses the already
referenced planning owner. No fourth router or new runtime dependency was added.

## Verification recovery and limits

uv's default global cache was denied by the sandbox on the initial snapshot attempt. All passing
commands used `UV_CACHE_DIR=/private/tmp/dn004-uv-cache` and offline resolution, with no installation.
Ruff found one 101-character test line; it was split and relevant checks rerun successfully.
There are no unresolved implementation failures or external acceptance blockers. Pending matrix
rows intentionally supply no model comparison or release eligibility; future behavioral runs
require separate user authorization and new observed rows.

## Authorized v0.8.0 follow-up on 2026-10-02

The user's later instruction authorized v0.8.0 preparation, local candidate/evidence commits,
and relevant supervised comparisons. Candidate dc936180ed2a854c9f6ac65aa9e21559f4a7e2af
contains the compared skill snapshot. BC-DN-004-001 appends two independent observed rows:
the outer restricted supervisor had four shared functional failures; removing that outer restriction
while preserving model sandboxes produced twelve candidate passes, ten equivalent pairs, two
matrix improvements, and no regression. All 24 reports record credential cleanup handled/cleaned.
One model, one repetition per source/case, and differing supervisor configurations support no
cross-model or variance claim. The prior failures remain visible and are not counted as passes.

The skill source, positive/negative cases, case-suite digest, verifier, and plan inventory did
not change. Appending ledger evidence changed the declared input fingerprint, so current focused
tests (9 passed), credential-free check, Ruff, and diff check were rerun with the new digest.
The supported check/close path must accept this refreshed evidence before the final evidence commit.
Release preparation and promotion provenance are recorded in docs/releases/v0.8.0.md.
