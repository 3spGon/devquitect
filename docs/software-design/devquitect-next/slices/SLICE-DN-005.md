---
schema_version: 1
session: devquitect-next
slice: SLICE-DN-005
plan_revision: 3
plan_digest: 9ff4314ccaba6eb0aa226330185fab221608f4977870f4d8bf9382161c206c52
verified_at: '2026-10-05T04:53:45.246977+00:00'
inputs_digest: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
environment:
  python: 3.14.7
  PyYAML: 6.0.3
criteria:
  AC-DN-009:
    action: Review the assembled local candidate and preserved verifier contract.
    expected: The assembled candidate has current credential-free evidence for changed contracts and leaves
      verify_slice.py and its YAML verification contract unchanged.
    method: Run all inventory checks; compare the distributed verifier with the installed 0.8.0 script
      and inspect the cumulative Git diff.
    observed: All six approved inventory commands pass at the current assembled-input digest. The cumulative
      change is limited to CI workflows, schema/producer/contracts, guidance/context and delivery records.
      Distributed verifier bytes, skills, authority map, cases, approved plan, dependencies, canonical
      report/promotion schemas and packaging version enforcement are unchanged.
    status: PASS
    evidence: CHECK-DN-013
  AC-DN-010:
    action: Refresh only System Context sections affected by observed CI implementation.
    expected: The System Context reflects only verified implementation evidence.
    method: Review the context diff against current test evidence and read-only GitHub observations.
    observed: System Context revision 16 records actual protected PR 3/main source evidence and its limitations.
      The assembled context refresh passed protected PR 4 and independently verified final-main run 37265160752;
      its tracked input bytes match the current checkout. DN-006 remains outside implemented scope.
    status: PASS
    evidence: CHECK-DN-023
  AC-DN-013:
    action: Verify smoke tests on all three hosted Python 3.12 platforms.
    expected: Compaction recovery, relevant CLI contracts, and path-sensitive packaging smoke tests pass
      on Linux, macOS, and Windows with Python 3.12.
    method: Local workflow/CLI contracts plus actual GitHub attempt-specific results.
    observed: 'PR 4 run 37264944492 and final-main run 37265160752, each attempt 1, passed all three mandatory
      variants plus aggregate. Each ran 89 smoke/contracts. Actual final platform metadata: macos26/20260907.0351.1:
      Python 3.12.10, pass; ubuntu24/20260927.320.1: Python 3.12.14, pass; win25-vs2026/20260925.250.1:
      Python 3.12.10, pass. Local suite also passed 89 cases; Windows-specific Bash discovery, native
      CLI preflight and LF whitespace fixture failures were corrected without skipping contracts.'
    status: PASS
    evidence: CHECK-DN-023
  AC-DN-014:
    action: Verify manual behavioral separation and non-run/refusal states.
    expected: The manual behavioral workflow is separate from deterministic required checks and cannot
      substitute for a failed deterministic gate.
    method: Inspect both workflows and run authorization/configuration/exact-SHA preflight and required
      aggregate positive/negative fixtures without launching a model.
    observed: 71 deterministic CI contracts pass, including separate workflow_dispatch authorization/configuration/exact-reviewed-main
      preflight and explicit not-run state. Behavioral has a separate job/environment and API-key-only
      command; normal required CI contains no behavioral step or model credentials. No workflow dispatch/model
      call or DN-004 row/ledger mutation occurred. Aggregate positive/negative cases reject all non-success
      platform states.
    status: PASS
    evidence: CHECK-DN-023
  AC-DN-015:
    action: Observe clean hosted checkout/tool/workflow and PR versus final-main identities.
    expected: Clean CI evidence identifies the exact tested commit and installed tool revision, distinguishing
      PR integration/head/base identities from the independently verified final candidate SHA.
    method: Execute source/lock-byte and strict metadata fixtures; obtain matching hosted PR and push
      evidence.
    observed: Actual PR 4 index records integration 57d2a4e0cb6a26d80122797d9228a7472021cacb, head 66d90c0674f17d876f0bcc45029b9df21327ac86
      and base 1fb3c2f9a42cfb1861ab058fb257b1d1447e1930 separately. Independent push run 37265160752 attempt
      1 records final source/workflow/installed quality-tool SHA 80bfa04b1d26c08d87ad5c421928c5a088ec4ffa,
      refs/heads/main and null PR. Strict indexes and all downloaded file sizes/digests validate. Every
      result is from the same run/attempt/source; fixtures reject mismatched source/tool/lock/workflow
      and missing/malformed metadata.
    status: PASS
    evidence: CHECK-DN-023
  AC-DN-019:
    action: Verify clean credential-free quality in the locked hosted Python 3.12 environment.
    expected: Quality runs structural validation, credential-free tests, Ruff, and event-base whitespace
      checks from the locked Python 3.12 environment without model credentials or write permissions.
    method: Workflow contract tests, real local whitespace repositories (including divergent PR and empty-tree
      first-push), local repository suite, then hosted quality job.
    observed: Final-main quality succeeded on source 80bfa04b1d26c08d87ad5c421928c5a088ec4ffa with actual
      Python 3.12.14, uv 0.12.10, uv sync --locked --all-groups and contents read. Archived check.json
      reports pass, behavioral false and validation source exactly that SHA; actual identity/check/Ruff/event-base
      whitespace command records all exit 0. PR merge-base and first-push empty-tree positive/negative
      fixtures pass. The workflow uses pinned actions and no model secrets or write permissions.
    status: PASS
    evidence: CHECK-DN-023
  AC-DN-020:
    action: Verify two canonical Linux builds on the same exact candidate and locked toolchain.
    expected: Two independent canonical builds of the same commit, version, and locked toolchain have
      equal ZIP SHA-256 and deterministic entry manifests.
    method: Real local immutable rebuilds and actual package CLI/index tests; obtain hosted Linux two-build
      artifacts.
    observed: 'Canonical final-main Linux job ran both existing package commands for source 80bfa04b1d26c08d87ad5c421928c5a088ec4ffa/version
      0.8.0 in dist/first and dist/second; both exit 0 and strict equal-ZIP/byte-identical-entry-manifest
      guard exit 0. Downloaded ZIP SHA-256 aa2deeb6dffb68ca28f31db03953bcf4ef46225e2b776fecdc51e7259a868ceb;
      manifest/report digests and strict index validate. Actual canonical toolchain: {"compression_runtime":
      "1.3", "lock_sha256": "ead42ea78041d842287fc1135edf3e6a407ee68c354936e30bfc3c5002a50e5a", "python":
      "3.12.14", "quality_source_commit": "80bfa04b1d26c08d87ad5c421928c5a088ec4ffa", "quality_version":
      "0.1.0", "runner_image": "ubuntu24/20260927.320.1", "uv": "uv 0.12.10 (x86_64-unknown-linux-gnu)"}.
      Negative contracts reject reused roots, differing ZIPs/manifests and source/version drift.'
    status: PASS
    evidence: CHECK-DN-023
  AC-DN-021:
    action: Verify effective protected main merge gates.
    expected: Effective main protection requires successful quality, all mandatory platform-smoke variants,
      and package checks, prevents force push and deletion, and never treats failed, cancelled, or skipped
      mandatory jobs as verified.
    method: Execute always-run aggregate shell with each non-success/missing platform result; inspect
      effective main protection/rulesets using read-only GitHub API.
    observed: 'Effective main protection was applied under explicit user authorization and read back after
      both merges/final-main runs: strict Devquitect / quality, Devquitect / platform-smoke and Devquitect
      / package checks bound to Actions app 15368; PR integration required; enforce_admins true; force
      push/deletion false. Both PRs integrated only after all six jobs succeeded. Earlier Windows failures
      caused aggregate failure and BLOCKED merge state. All 15 non-success/missing-variant fixtures reject
      acceptance; final hosted jobs all conclude success.'
    status: PASS
    evidence: CHECK-DN-023
checks:
  CHECK-DN-013:
    command: uv run devquitect check --source working-tree --report .devquitect-reports/check.json
    cwd: .
    started_at: '2026-10-05T04:45:51.235638+00:00'
    finished_at: '2026-10-05T04:46:26.367857+00:00'
    exit_code: 0
    status: PASS
    observed: check result=pass; behavioral=False; fast suite exit=0
    inputs_before: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
    inputs_after: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
  CHECK-DN-014:
    command: uv run ruff check src tests
    cwd: .
    started_at: '2026-10-05T04:46:27.503883+00:00'
    finished_at: '2026-10-05T04:46:27.557458+00:00'
    exit_code: 0
    status: PASS
    observed: All checks passed!
    inputs_before: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
    inputs_after: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
  CHECK-DN-015:
    command: git diff --check
    cwd: .
    started_at: '2026-10-05T04:46:28.664872+00:00'
    finished_at: '2026-10-05T04:46:28.671152+00:00'
    exit_code: 0
    status: PASS
    observed: No output; diff is whitespace-clean.
    inputs_before: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
    inputs_after: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
  CHECK-DN-019:
    command: uv run pytest tests/unit/test_compaction_recovery_hook.py tests/unit/test_packaging.py tests/contract
    cwd: .
    started_at: '2026-10-05T04:46:29.768753+00:00'
    finished_at: '2026-10-05T04:46:51.194452+00:00'
    exit_code: 0
    status: PASS
    observed: 89 smoke/contract tests passed locally on macOS/Python 3.14.7.
    inputs_before: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
    inputs_after: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
  CHECK-DN-020:
    command: uv run pytest tests/integration/test_check_command.py
    cwd: .
    started_at: '2026-10-05T04:46:52.507674+00:00'
    finished_at: '2026-10-05T04:48:41.454826+00:00'
    exit_code: 0
    status: PASS
    observed: Six check-command integration tests passed with stable HEAD and input fingerprint.
    inputs_before: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
    inputs_after: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
  CHECK-DN-023:
    command: uv run pytest tests/contract/test_ci_workflow_contract.py
    cwd: .
    started_at: '2026-10-05T04:48:42.662411+00:00'
    finished_at: '2026-10-05T04:49:04.668562+00:00'
    exit_code: 0
    status: PASS
    observed: 71 CI workflow/producer positive and negative contract tests passed.
    inputs_before: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
    inputs_after: 43f6f2c2b6020b0c92812c9d701417b24902b57e384a82224b9babc677f9b465
---

# SLICE-DN-005 — current acceptance evidence

Approved plan revision 3; authorized implementation on 2026-10-04 in
`codex/slice-dn-005-continuous-verification`. The user's subsequent `autorizo` explicitly covered
candidate commits/pushes/PRs, main protection and integration after passing required CI.
Model-backed execution, credential configuration, publication, promotion and DN-006 are excluded.
The delivery checkpoint owns the supported closure status.

## Source and hosted verification

| Event | Run / attempt | Tested source | Outcome |
| --- | --- | --- | --- |
| pull_request | [37264198908](https://github.com/3spGon/devquitect/actions/runs/37264198908) / 1 | `e5883c7bb2f112d7f81061553d7555f70a720c7a` | All six jobs success; artifacts validated |
| push | [37264541061](https://github.com/3spGon/devquitect/actions/runs/37264541061) / 1 | `1fb3c2f9a42cfb1861ab058fb257b1d1447e1930` | All six jobs success; artifacts validated |
| pull_request | [37264944492](https://github.com/3spGon/devquitect/actions/runs/37264944492) / 1 | `57d2a4e0cb6a26d80122797d9228a7472021cacb` | All six jobs success; artifacts validated |
| push | [37265160752](https://github.com/3spGon/devquitect/actions/runs/37265160752) / 1 | `80bfa04b1d26c08d87ad5c421928c5a088ec4ffa` | All six jobs success; artifacts validated |

PR 4 integration `57d2a4e0cb6a26d80122797d9228a7472021cacb`, head `66d90c0674f17d876f0bcc45029b9df21327ac86` and base
`1fb3c2f9a42cfb1861ab058fb257b1d1447e1930` are distinct. Its protected merge produced exact final main `80bfa04b1d26c08d87ad5c421928c5a088ec4ffa`;
the independent push run above verifies that SHA, not the PR head or merely an equal tree.
Actual run/job/artifact metadata and downloaded results are retained locally in ignored
`.devquitect-reports/hosted-<run-id>/observation.json` and its `artifacts/` directory.
All six artifacts per run use source-and-attempt names, are unexpired and retain 30 days.

## Final-main artifacts and environment

Canonical Linux: Python 3.12.14, uv 0.12.10, zlib 1.3,
quality 0.1.0 from `80bfa04b1d26c08d87ad5c421928c5a088ec4ffa`, image `ubuntu24/20260927.320.1`,
lock SHA-256 `ead42ea78041d842287fc1135edf3e6a407ee68c354936e30bfc3c5002a50e5a`. Local verifier/check environment:
macOS, Python 3.14.7, PyYAML 6.0.3. Local working-tree evidence is development verification;
actual hosted source identities come from immutable Git commits.

| Payload | Bytes | SHA-256 |
| --- | ---: | --- |
| manifest: `devquitect-0.8.0.manifest.json` | 5750 | `a21cc4b131ce69487aba61886ae18d63db8f51a9f495667b1f94e2fe3a917244` |
| report: `package.json` | 7005 | `581032704449d152b5df8e8a402d9ec79045dbf115b13b99bc78be84cb24b994` |
| zip: `devquitect-0.8.0.zip` | 60484 | `aa2deeb6dffb68ca28f31db03953bcf4ef46225e2b776fecdc51e7259a868ceb` |

| GitHub artifact | ID | Container digest | Expires (UTC) |
| --- | ---: | --- | --- |
| `platform-smoke-Linux-80bfa04b1d26c08d87ad5c421928c5a088ec4ffa-attempt-1` | 11326227154 | `sha256:6dffcb3cbd4ce6544efc3a1a3e6a6f19464d8e0a107b09f30b430cab0196cad1` | 2026-11-04T04:49:51Z |
| `quality-80bfa04b1d26c08d87ad5c421928c5a088ec4ffa-attempt-1` | 11326167278 | `sha256:eb67229e02e35222c1aa242122d3014070e7c96b8370777a4c1dfbd2a589d11c` | 2026-11-04T04:50:03Z |
| `platform-smoke-Windows-80bfa04b1d26c08d87ad5c421928c5a088ec4ffa-attempt-1` | 11326117650 | `sha256:f4db7fb5f490aa772a2359f2bc4b3d725dada141e08c68284ef23d5c3e7c1889` | 2026-11-04T04:51:28Z |
| `platform-smoke-macOS-80bfa04b1d26c08d87ad5c421928c5a088ec4ffa-attempt-1` | 11325997642 | `sha256:103557721d5c754343db4fdee03a79068ef1ee8a441fcab16acd352caabcc484` | 2026-11-04T04:50:23Z |
| `package-diagnostics-80bfa04b1d26c08d87ad5c421928c5a088ec4ffa-attempt-1` | 11325911812 | `sha256:f5d900581f42dea58f81c04d5595f284905fc9782f25a9cfb6e36fec71d0c1c4` | 2026-11-04T04:49:38Z |
| `package-80bfa04b1d26c08d87ad5c421928c5a088ec4ffa-attempt-1` | 11325806994 | `sha256:0e6e057a881e02e3a8adb77d348242acb4ad4b6a847f819d6ef28e463adffb13` | 2026-11-04T04:49:37Z |

Payload and uploaded-container digests are separate identities. Both canonical build commands
ran against the same full SHA/version in independent roots; their command records and strict
equal-ZIP/byte-identical-manifest guard succeeded. Index own digest is deliberately excluded.

## Scope, failures and preserved contracts

Hosted attempts 37263102048 and 37263858064 failed Windows and their aggregate; protection
blocked integration. Corrected Git Bash discovery across cmd/mingw64 layouts, native Codex
availability for Python, and LF fixture bytes without weakening or skipping smoke tests.
One local integration observation was discarded after HEAD changed during the test; another
was diagnostic because inputs changed during correction. All six final inventory observations
above were rerun with stable HEAD and matching before/after fingerprints.

The cumulative implementation changes nine approved files. The pre-existing approved plan
amendment was preserved, including identical DN-001 through DN-004 inventories; their verified
states/history remain intact. Distributed verify_slice.py equals the installed 0.8.0 script
byte-for-byte; no verifier/YAML contract, skill, case, authority map, dependency, plugin version,
public CLI, report/promotion schema, release consumer or DN-004 behavioral row was changed.
Optional Graphify code state was refreshed without an LLM and remains ignored.

System Context refers to the actually verified implementation baseline and owns no slice status.
Credential-free CHECK-DN-013/014/015/019/020/023 all passed at the declared current digest;
89 smoke/contracts, six integration tests and 71 CI-specific cases overlap. Effective main
protection requires strict Actions-app-bound quality/platform aggregate/package success and PR
integration, applies to administrators, and prohibits force push and deletion. Behavioral is
manual and optional; it cannot replace a deterministic failure and was not dispatched.
