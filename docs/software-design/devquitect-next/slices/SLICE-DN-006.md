---
schema_version: 1
session: devquitect-next
slice: SLICE-DN-006
plan_revision: 3
plan_digest: 9ff4314ccaba6eb0aa226330185fab221608f4977870f4d8bf9382161c206c52
verified_at: '2026-10-05T16:52:20.035856+00:00'
inputs_digest: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
environment:
  python: 3.14.7
  PyYAML: 6.0.3
  host: local macOS
  uv_cache: /private/tmp/devquitect-dn006-uv-cache
criteria:
  AC-DN-011:
    action: Bind manual readiness to an immutable candidate without publication authority.
    expected: Exact-candidate hosted readiness consumes successful push/main CI and never publishes, tags or promotes.
    method: Review workflow permissions and execute fixture contracts, real API replay and hosted candidate dispatch.
    observed: Local workflow contracts and existing-main replay pass; only contents/actions read are declared and approval fields remain null. The new workflow is not present remotely and no DN-006 candidate commit, final-main CI or hosted dispatch exists. Hosted acceptance remains pending.
    status: NO VERIFICADO
    evidence: CHECK-DN-021
  AC-DN-012:
    action: Consume optional independently authorized behavioral rows without model execution.
    expected: Each model/host/runtime/effort/suite/repetition row preserves its own verdict; no row overrides deterministic failure.
    method: Execute evaluation/comparison pass, fail, inconclusive and not-run cases and invalid index/candidate/model/authorization cases.
    observed: All fixtures pass, including behavioral pass alongside a failed mandatory platform. Missing/undeclared/altered/noncanonical/empty reports and wrong source/model/effort/verdict are rejected; unexecuted rows cannot invent runtime. No model call or ledger mutation occurred.
    status: PASS
    evidence: CHECK-DN-021
  AC-DN-016:
    action: Verify observed GitHub repository, workflow, run, attempt, jobs and artifacts.
    expected: The complete exact new candidate has successful quality, three platform variants, aggregate and package with unique producer-bound artifacts.
    method: Bounded mocked transport fixtures plus authenticated read-only existing-main replay; require a subsequent hosted new-candidate run.
    observed: Fixtures and real run 37265160752 attempt 1 passed six-job/six-artifact provenance, container digests and safe extraction for source 80bfa04b1d26c08d87ad5c421928c5a088ec4ffa. This is evidence for adapter behavior, not hosted CI acceptance of the uncommitted DN-006 implementation. New-candidate CI is pending.
    status: NO VERIFICADO
    evidence: CHECK-DN-022
  AC-DN-017:
    action: Bind downloaded package bytes, index, manifest and report to the evaluated rebuild.
    expected: Source SHA/snapshot, committed/requested/packaged/index version, lock/tool identities, ZIP and manifest all agree for the new candidate.
    method: Real fixture Git/package/index builds and tampering cases; shared-policy replay of actual existing-main package; hosted candidate readiness.
    observed: All functional cases pass. Real existing-main version 0.8.0 replay matched ZIP sha256:aa2deeb6dffb68ca28f31db03953bcf4ef46225e2b776fecdc51e7259a868ceb to two local rebuilds and produced ZIP/manifest/unapproved proposal privately. Version mismatch is policy exit 1; altered payloads fail without eligible output. Exact DN-006 candidate package evidence is still pending.
    status: NO VERIFICADO
    evidence: CHECK-DN-021
  AC-DN-018:
    action: Emit canonical timestamped eligibility and an unchanged unapproved promotion object.
    expected: The actual hosted run retains CI/package/prior-release/optional behavioral references with null approval fields and no publication.
    method: Validate schemas, stdout/file equality, private-output/report-write-failure fixtures and actual hosted readiness artifacts.
    observed: Local schema, staged-output and report-write failure cases pass; real historical-main replay preserves null approved_by/approved_at. Read-only repository retention inspection returned days 90 and maximum_allowed_days 90, supporting requested 30-day retention. Actual DN-006 hosted proposal/retention evidence and the dependent verified-candidate System Context refresh remain pending.
    status: NO VERIFICADO
    evidence: CHECK-DN-021
  AC-DN-022:
    action: Verify explicit immutable previous-release compatibility and unchanged legacy defaults.
    expected: A lower-version strict ancestor permits a post-bump candidate; omitted option retains parent-based policy with no network access.
    method: Test real fixture Git histories, lower/non-increasing versions, missing/unrelated/same-commit baselines and legacy no-network behavior.
    observed: All cases pass. The real API replay also consumed candidate 80bfa04b1d26c08d87ad5c421928c5a088ec4ffa/version 0.8.0 against explicit ancestor 86c7cd9f0fcecd1b4faebeb24fdeafcf558a91b9/version 0.7.0. Legacy omission retains its original two-file ZIP/proposal output and immediate-parent behavior; existing migration guard cases pass in the credential-free suite.
    status: PASS
    evidence: CHECK-DN-021
  AC-DN-023:
    action: Reject invalid or incomplete evidence and distinguish failure classes.
    expected: Wrong source/workflow/attempt, incomplete jobs, missing/expired/altered evidence and unsafe transport never qualify; configuration, policy and infrastructure have distinct diagnostic exits.
    method: Run positive/negative transport and CLI/shared-policy cases, including pagination, redirects, limits, retries and failed report persistence.
    observed: 41 transport and 140 focused tests pass. Mandatory job failure/skip/cancellation or mixed attempts are rejected; missing digest, expiration, altered ZIP/index/manifest and unsafe/duplicate/symlink/oversized archives fail closed. HTTPS API-issued redirects omit tokens on storage, requests use 30 seconds and at most three transient retries. CLI exits 1 policy, 2 configuration and 3 unavailable with canonical non-passing reports and no eligible output; both canonical schemas are unchanged.
    status: PASS
    evidence: CHECK-DN-022
checks:
  CHECK-DN-016:
    command: uv run devquitect check --source working-tree --report .devquitect-reports/check.json
    cwd: .
    started_at: '2026-10-05T16:50:08.740800+00:00'
    finished_at: '2026-10-05T16:51:18.847119+00:00'
    exit_code: 0
    status: PASS
    observed: Canonical check result pass; behavioral false; validation and fast suite exit 0.
    inputs_before: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
    inputs_after: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
  CHECK-DN-017:
    command: uv run ruff check src tests
    cwd: .
    started_at: '2026-10-05T16:51:19.057996+00:00'
    finished_at: '2026-10-05T16:51:19.135908+00:00'
    exit_code: 0
    status: PASS
    observed: All checks passed.
    inputs_before: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
    inputs_after: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
  CHECK-DN-018:
    command: git diff --check
    cwd: .
    started_at: '2026-10-05T16:51:19.337506+00:00'
    finished_at: '2026-10-05T16:51:19.346911+00:00'
    exit_code: 0
    status: PASS
    observed: Diff is whitespace-clean.
    inputs_before: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
    inputs_after: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
  CHECK-DN-021:
    command: uv run pytest tests/integration/test_release_check.py tests/unit/test_packaging.py tests/contract
    cwd: .
    started_at: '2026-10-05T16:51:19.550962+00:00'
    finished_at: '2026-10-05T16:52:18.468117+00:00'
    exit_code: 0
    status: PASS
    observed: 140 tests passed, including real fixture package downloads, prior-release, behavioral and workflow/CLI contracts.
    inputs_before: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
    inputs_after: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
  CHECK-DN-022:
    command: uv run pytest tests/unit/test_github_evidence.py
    cwd: .
    started_at: '2026-10-05T16:52:18.681261+00:00'
    finished_at: '2026-10-05T16:52:20.035856+00:00'
    exit_code: 0
    status: PASS
    observed: 41 credential-free transport/provenance cases passed.
    inputs_before: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
    inputs_after: 2268c65104da1de7fea7b90d6cca70a421e1d6b28d873f55219b6b79ca367cd3
---

# NO VERIFICADO — SLICE-DN-006

The 2026-10-05 request authorizes this slice on a new branch, with implementation-only scope.
Local implementation is functional and all five exact inventory commands pass at the fingerprint
above. Three criteria have full deterministic observations; four conservatively remain unverified
until the new exact candidate's hosted readiness is observed. No supported close is attempted
while those observations are absent. Prior slice evidence, approved plan, inventory, verifier,
skills, schemas, dependency lock, plugin version and behavioral ledgers are unchanged.

## Scope review against the approved plan

Material changes: `.github/workflows/release-readiness.yml`, `github_evidence.py`, shared
`promotion.py`, additive `cli.py`, release integration/transport/workflow contracts and contributor
guidance. Reused existing source freezing, deterministic packager, check policy, canonical report
builder and atomic writer. No new dependency, schema version, release manager, model run, tag,
push, publication, deployment or promotion approval was introduced.

The consumer fetches all selected artifacts itself rather than accepting a caller's trusted JSON.
It verifies complete authenticated attempt metadata, transport/container and package/file identities,
actual committed lock identity, separate compatibility baseline and optional canonical behavioral
rows. CI output is finalized only after complete policy/report success; existing user output is
preserved, and local default output/report behavior remains compatible.

## Actual read-only API replay (diagnostic, not hosted DN-006 acceptance)

On 2026-10-05, current local code authenticated through the existing GitHub CLI session and
consumed [main run 37265160752](https://github.com/3spGon/devquitect/actions/runs/37265160752),
attempt 1, repository `3spGon/devquitect`, workflow `.github/workflows/ci.yml`, candidate
`80bfa04b1d26c08d87ad5c421928c5a088ec4ffa`. `GitHubEvidence.collect` observed all six successful
jobs and six uniquely identified unexpired artifacts, checked their API-provided container digests
and safely extracted their expected members. Shared `release_check` then evaluated version 0.8.0
against explicit prior-release ancestor `86c7cd9f0fcecd1b4faebeb24fdeafcf558a91b9` (0.7.0).
Downloaded ZIP SHA-256 matched both evaluated rebuilds:
`aa2deeb6dffb68ca28f31db03953bcf4ef46225e2b776fecdc51e7259a868ceb`.
ZIP, manifest and promotion proposal were produced together; both approval fields were null.
Temporary replay downloads/outputs were removed and no token was recorded.

Read-only `gh api repos/3spGon/devquitect/actions/permissions/artifact-and-log-retention` returned
`{"days":90,"maximum_allowed_days":90}`. Workflow listing returned no remote
`.github/workflows/release-readiness.yml`. These API observations establish transport behavior and
retention support; they cannot turn a working-tree implementation into a reviewed immutable hosted
candidate. No dispatch or remote mutation was performed.

## Remaining external gate and recovery

The new workflow and tool code are local and uncommitted. Implementation authority explicitly
excludes commit/push/merge and other external actions. Completion requires separate authority to
commit this concrete diff, push/open its PR, integrate only after protected CI passes, then observe
independent final-main CI and manually dispatch readiness for that exact new SHA. The resulting
proposal must remain unapproved. Candidate version and the lower immutable previous-release
reference must be recorded separately; a version bump or publication is not assumed here.

After successful hosted readiness, refresh only System Context's affected release/evidence,
compatibility, verification and limitation sections using that verified candidate. Rerun affected
inventory checks after the refresh, update current criterion/fingerprint evidence, run the unchanged
supported check and close with the current checkpoint revision. The System Context's existing
verified DN-005 baseline remains intact until that dependency is satisfied.

The initial sandbox uv cache refusal and executor timeout were infrastructure limitations,
resolved using the existing environment with an accessible cache and a tracked process. Final
checks all exit 0; no local implementation failure remains. Generated logs and timestamp/fingerprint
capture are in ignored `.devquitect-reports/`, not product state.
