# Devquitect Next architecture

Status: Approved
Last updated: 2026-10-03

## Confirmed

### Current architecture

Devquitect currently distributes three skills with distinct entrypoints and a Python quality package. `project-plan-execution` delegates accepted-slice state transitions to the distributed `verify_slice.py` guard, which reads a YAML inventory and requires Python 3.12+ plus PyYAML.

The DN-005 / DN-006 amendment uses the current checkout as its affected baseline: four skills are now declared, `devquitect check` composes structural and credential-free tests, packaging rejects committed-version mismatch, and `release-check` rebuilds twice and binds check evidence to the same commit/snapshot. No GitHub workflows exist yet in this checkout. The earlier three-skill description represents the original initiative baseline, not a claim that delivered QUICK is absent.

### Proposed architecture

| Component | Responsibility | Preserved boundary |
| --- | --- | --- |
| Lean skill entrypoints | State each entrypoint's outcome, authorization, escalation, and completion policy once. | References retain detailed mechanics and canonical state rules. |
| `quick-change` skill | Execute an authorized, localized change after focused discovery and relevant verification. | It escalates rather than deciding product, architecture, migration, or durable-work questions. |
| Existing definition, refactoring, and delivery skills | Own their current domains. | No skill silently assumes another skill's authority. |
| Existing `verify_slice.py` | Preserve the current Python/PyYAML, YAML-inventory, snapshot/check/close verification boundary. | This initiative neither changes nor migrates it. |

The host may choose `quick-change` implicitly from its description. There is no universal router skill in 0.7.0. A consumer may add a short `AGENTS.md` routing convention if it needs local enforcement beyond normal skill selection.

### Expanded v2 components

| Component | Responsibility | Boundary |
| --- | --- | --- |
| Workflow-depth selector | Select lightweight, standard, or rigorous depth for every initiative from observable impact and risk. | It replaces no approval boundary and does not authorize implementation. |
| Durable-root resolver | Resolve an explicitly configured definition root; otherwise use the detected repository default while discovering existing sessions in both locations. | It preserves existing session paths and never silently migrates them. |
| Invocation policy | Declare implicit activation per skill: definition, QUICK, and refactoring may be eligible; approved-plan execution requires explicit invocation. | Host matching remains advisory; explicit user invocation takes precedence. |
| Prompt-change ledger | Record the disposition and evidence for every staged change group. | Snapshot and Git identities own exact source text; comparison and calibration reports own observed evidence. |
| Evaluation matrix | Run each authorized behavioral comparison with one declared model/host configuration at a time. | Results from differing models, hosts, suite versions, or repetitions are not merged into one verdict. |

### Resolved operating design

- **Workflow depth:** retain `change_profile` for compatibility and add one optional `workflow_depth` field to every persistent session. Its values are `lightweight`, `standard`, and `rigorous`; omitted legacy values mean `standard`. A system-change profile records the same selected depth rather than replacing its existing classification fields.
- **Durable root:** the current `docs/software-design` remains the default. A caller may explicitly provide one repository-relative definition root; the resolver stores that root in the session, checks the recorded root first on resume, and searches the default only for legacy discovery. A collision between viable sessions is surfaced for user selection. No session is moved automatically.
- **Invocation:** definition, QUICK, and targeted-refactoring may opt into host implicit matching through their metadata; `project-plan-execution` is explicit-only. An explicit skill mention wins over matching.
- **Prompt changes:** a change group has an immutable baseline snapshot, one named rule group, the unchanged representative deterministic cases, and—only when separately authorized—a comparison on one declared model/host configuration. A regression or inconclusive result retains the prior wording.
- **Evidence matrix:** initial rows use canonical model IDs `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`. GPT-5.6 rows are the prior-generation baseline; GPT-6 Sol/Luna are additive rows. Every row fixes and records model ID, host, runtime, reasoning effort (`high` where supported), case-suite revision, repetitions, and report references. Comparisons reuse the same prompt-change group and representative cases. Each row has its own verdict; results are never pooled. If host/runtime/effort differ or cannot be matched, record the difference and do not claim a direct model-only comparison. Behavioral runs remain separately authorized.

### Delivery flow

```text
authorized local change → quick-change → focused inspection → edit → relevant validation → result
                                      │
                                      └─ material complexity → appropriate existing skill

approved plan → existing verify_slice.py → snapshot / check / atomic close → verified tracker state
```

## Assumptions

The existing skill packaging can distribute an additional skill and compatibility helper without adding a new host integration.

The repository can store the ledger as a versioned Markdown document without adding a new runtime parser; immutable snapshots and existing reports provide reproducibility.

## Approved DN-005 / DN-006 technical design

Gate 1 approved R-11 through R-14 and the user explicitly approved Gate 2 on 2026-10-03. This is the approved technical treatment; none of the new workflows or interfaces is implemented by this document.

| Owner | Responsibility | Trust boundary |
| --- | --- | --- |
| `.github/workflows/ci.yml` (new) | Run quality, three platform variants, their aggregate, and canonical Linux packaging; upload attempt-specific evidence. | `contents: read`, no model secrets, reviewed workflow definition, pinned third-party actions. |
| `.github/workflows/behavioral.yml` (new) | Dispatch one explicitly authorized DN-004 configuration using existing model-backed commands. | Manual only; supported API-key authentication in its dedicated job; no subscription cache on unattended runners. |
| `.github/workflows/release-readiness.yml` (new) | Checkout the explicit reviewed repository candidate, install its locked tooling, invoke CI-aware `release-check`, and upload the result. | Manual only; `contents: read` and `actions: read`, no write/publication/model permissions. |
| `src/devquitect_quality/github_evidence.py` (new) | Read GitHub REST run/attempt/jobs/artifacts metadata, download and verify selected artifact bytes, safely materialize evidence, and return normalized provenance. | Fixed GitHub API origin, repository matching the checked-out Git remote, read-only `GH_TOKEN`; no arbitrary caller-supplied download URLs or execution of artifact contents. |
| Existing `promotion.py` and `cli.py` | Enforce complete CI identity and downloaded-package binding, invoke existing rebuild/check policy, and allow an explicit prior-release ref. | A workflow cannot bypass policy by supplying its own passing JSON; legacy local calls preserve defaults. |
| Existing `reporting.py` | Emit the canonical `release-check` envelope with CI/readiness entries in `evidence_manifest`. | Existing report schema/version and unapproved promotion-record schema remain unchanged. |

Use the standard library for HTTP, hashing, JSON, temporary roots, and ZIP handling; existing jsonschema validates the new evidence document. No new dependency, service, release database, or second evaluator is required.

### CI producer and operational gates

The workflow name is `Devquitect`; literal job check names are `Devquitect / quality`, `Devquitect / platform-smoke (ubuntu-latest)`, `Devquitect / platform-smoke (macos-latest)`, `Devquitect / platform-smoke (windows-latest)`, `Devquitect / platform-smoke`, and `Devquitect / package`. The three required names are quality, aggregate platform-smoke, and package. The aggregate executes with an always-run condition and explicitly requires all three variants to succeed. Normal jobs can run concurrently; package success by itself does not make the candidate eligible.

Every producer uploads a uniquely named artifact with suffix `<candidate-sha>-attempt-<run-attempt>`: quality contains canonical `check.json`; each platform contains its result and execution identity; package contains the canonical ZIP, deterministic manifest, package report, and `ci-evidence.json`. Each producer records actual `git rev-parse HEAD`, repository, run/attempt, workflow identity, and toolchain. Failed jobs upload diagnostic reports when possible, but eligibility still rejects their conclusions. Partial-job reruns are not accepted as a complete attempt; rerun all jobs or start a fresh run.

PR CI tests the checked-out integration SHA and separately records head/base; push CI tests the final `main` SHA. Readiness initially accepts a successful `push` CI attempt for `main` whose SHA exactly matches the candidate; no PR merge-SHA equivalence is needed. If merge queue is enabled, add its event and maintain the same gates. The exact whitespace range is the merge-base of PR head/base through tested HEAD, or valid push before/after; for a first push with no before commit, check the introduced tree against Git's empty tree.

Quality and matrix jobs install Python 3.12 with the committed `uv.lock`; record actual Python patch, uv, compression runtime, dependency-lock digest, and runner image. Package rebuilds use independent temporary output roots. Readiness must reproduce the selected canonical ZIP; a different toolchain that changes bytes fails explicitly instead of weakening digest equality.

Main protection is an external setting verified during delivery: the three required names, PR integration, no force push, and no deletion. Activation and rollback of these settings need their own authorized remote action. A repository lacking effective protection cannot satisfy AC-DN-021. Workflow definition changes require maintainer review; a runner is independent execution, not proof that malicious or insufficient tests are trustworthy.

### CI consumer, failure isolation, and retention

The GitHub adapter queries the selected attempt's jobs with pagination and fetches artifact metadata from the same repository/run. It requires exact workflow path `.github/workflows/ci.yml`, event `push`, branch `main`, candidate SHA, complete successful required jobs and all variants, unique expected artifacts, non-expiration, and artifact creation within the selected producer job's execution interval. Artifact names alone cannot bind an attempt. Verify the API-provided SHA-256 of the downloaded artifact container, then verify contained file hashes and canonical package identity. Missing digest is unavailable verification, never a pass.

All downloads enter fresh temporary roots. Reject absolute paths, `..`, duplicate entries, symlinks, and unexpected evidence members; bound each archive to 64 MiB compressed, 128 MiB expanded, and 1024 members. Never forward `GH_TOKEN` to an artifact storage redirect; follow only HTTPS redirects issued by the authenticated GitHub artifact endpoint and do not execute extracted content. Network calls have a 30-second timeout and at most three transient retries; authorization errors, malformed evidence, and identity failures are not retried into success.

Request 30-day retention for CI evidence and readiness reports and verify repository policy can support it. GitHub may impose a lower repository/organization limit; if it cannot support the review window, record incomplete operational acceptance rather than claim 30 days. Expiration or deletion requires new matching CI evidence. These are review artifacts, not the durable archive of a published release.

The promotion policy verifies version, exact commit/snapshot, source/manifest/ZIP digests, complete attempt provenance, prior-release compatibility, and optional independent behavioral rows before copying the eligible output. Any policy, input, or infrastructure failure emits a non-passing structured result and no eligible output/proposal; diagnostic reports may still be saved. A changed SHA always starts a new candidate identity. The intended flow remains local checks → PR CI → final-main CI → manual readiness → unapproved proposal → separate human release decision.

## Open decisions

None. The interfaces, evidence representation, policy ownership, stable check names, retention, and failure behavior have Gate 2 approval, and plan revision 3 has separate approval. Effective remote settings and real runner behavior are delivery evidence, not assumed implemented facts.

## Requirement traceability

| Requirement | Technical treatment |
| --- | --- |
| R-01 | Component ownership table and preserved boundaries. |
| R-02 | Lean skill-entrypoint component. |
| R-03, R-04 | `quick-change` component and escalation flow. |
| R-05, R-06 | Preserved verify_slice contract and staged delivery flow. |
| R-07, R-08 | Staged prompt-change protocol and append-only, snapshot-referencing ledger. |
| R-09 | Shared workflow-depth state and durable-root resolver with legacy discovery. |
| R-10 | Per-skill invocation metadata and non-pooled model/host evaluation matrix. |
| R-11, R-12 | CI producer, platform aggregate, clean locked toolchain, canonical rebuilds, and effective merge protection. |
| R-13, R-14 | GitHub evidence adapter, shared promotion policy, compatible CLI extension, retention, and unapproved report output. |
