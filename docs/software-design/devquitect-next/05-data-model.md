# Devquitect Next data model

Status: Approved
Last updated: 2026-10-03

## Confirmed

The approved delivery plan remains the source of truth for slice criteria, dependencies, declared inputs, and plan revision. The delivery checkpoint remains the source of truth for slice lifecycle and evidence. The existing fenced YAML `devquitect-verification` inventory represents the accepted concepts:

- stable `SLICE-*` identifier;
- atomic acceptance criteria;
- exact validation checks and relative working directories;
- dependencies;
- declared input paths.

The verifier retains these transitions:

```text
planned → snapshot (read-only) → check (read-only) → close (atomic) → verified
```

`close` must still reject missing approval, dependencies, criteria, current check evidence, matching fingerprints, or expected tracker revision. It re-reads its inputs before replacing the tracker atomically.

### Prompt-change ledger entry

The ledger is an append-only Markdown table or subsection with one record per evaluated change group. Each record includes:

- stable change identifier and date;
- baseline and candidate source snapshot IDs or Git references;
- affected paths and named rule group;
- disposition for each rule group: retain, move, or remove;
- deterministic case IDs and their result;
- canonical behavioral model ID, host, runtime, reasoning effort when supported, case-suite revision, repetitions, and report reference when authorized;
- verdict: retained, reverted, or inconclusive; and a short rationale.

The record contains no copied prompt body. Snapshot IDs and Git references reconstruct the original and candidate sources; authority-map entries identify the owner when the rule is critical. The initial model IDs are `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`; each model/host/runtime/effort combination is a separate evidence row.

### Workflow and root state

The workflow-depth record applies to all initiative contexts and records selected depth, evidence, and elevation reasons. A persistent session records its resolved root and session-relative path so discovery can find existing work after a root configuration change.

## Assumptions

The existing YAML inventory and verifier schema remain unchanged.

## Approved DN-005 / DN-006 evidence representation

R-13 / R-14 require a candidate record that links repository, full commit SHA, plugin version, source snapshot, quality-tool revision, workflow definition identity, run ID, run attempt, artifact IDs, and canonical package/manifest SHA-256 values. PR records additionally distinguish tested integration SHA, head SHA, and base SHA. GitHub run/job/artifact metadata verifies execution provenance; a file's own asserted SHA is not sufficient.

One selected CI attempt must identify quality, every required platform variant, and package conclusions. A rerun is a distinct attempt. Readiness may select a new successful attempt explicitly but must not combine partial results from several attempts. File digests bind package bytes independently of GitHub's artifact-container digest. Toolchain and runner identities qualify the reproducibility claim.

The exact candidate is immutable for a readiness attempt. Any candidate-SHA change requires new matching CI evidence, including after squash or rebase. The previous-release reference and its version are separate compatibility inputs, not alternative candidate identities. Missing or expired mandatory artifacts mean evidence is unavailable and readiness cannot pass; the recovery is a new matching verification run.

### CI package evidence document

Create `schemas/ci-evidence.schema.json` (proposed, version 1) for the package producer's `ci-evidence.json`. Reject unknown fields and validate these groups:

- `schema_version: 1`, `repository` (`owner/repo`), `workflow_path: .github/workflows/ci.yml`, `workflow_commit` (full Git SHA), positive integer `run_id` / `run_attempt`, `event`, and `ref`.
- `source_commit`, `snapshot_id`, and `version`, using the existing full-SHA, `sha256:` snapshot, and stable-semver formats.
- `pr`: null for push, otherwise tested integration/head/base full SHAs. It records identities separately rather than implying equality.
- `toolchain`: actual Python, uv, quality-package version/source commit, compression runtime, runner image, and `uv.lock` SHA-256.
- `files`: exactly the canonical ZIP, deterministic package manifest, and package report, each with a safe relative `path`, `size`, and `sha256` digest. The index excludes itself to avoid a recursive digest; the authenticated artifact-container digest binds its bytes.

Quality and platform artifacts carry their canonical report/result plus repository/source/workflow/run/attempt metadata. Their bytes are bound by their own authenticated artifact-container digest. The consumer validates these identities against observed API metadata; it never trusts a reported success in place of the actual attempt-specific job conclusion.

### Normalized provenance and readiness output

The adapter returns `repository`, `source_commit`, `workflow_path`, `workflow_commit`, `run_id`, `run_attempt`, the observed completed job IDs/names/conclusions, and selected artifact IDs/names/container digests/creation/expiration times. It also returns safe local file paths and verified file digests. The normalized observation is generated from authenticated API responses, not accepted as a caller-supplied trusted registry.

Keep `schemas/report.schema.json` and `schemas/promotion-record.schema.json` at their current versions. The existing `release-check` envelope's `inputs` records exact source/version and selected CI/prior-release inputs; `evidence_manifest` adds `ci`, `package_identity`, `previous_release`, and `behavioral` entries. The envelope's `generated_at` owns the timestamp and `result` owns eligibility. The existing schema-v1 promotion object retains `approved_by: null` and `approved_at: null`; a `promotion` entry in the report links it to the richer evidence without adding unsupported properties to that object. Thus legacy proposal consumers need no migration.

Behavioral entries retain R-10 dimensions, authorization references, independent `pass`, `fail`, `inconclusive`, or `not-run`, and report digests. Intended settings for an unexecuted row are not observed runtime evidence. Supplied reports must be canonical and match the candidate snapshot; malformed or unrelated supplied evidence is rejected rather than silently attached. Failed or inconclusive optional rows remain visible but cannot change deterministic eligibility. Absent rows are `not-run` with null observed runtime/host/effort and no reports.

Temporary download/materialization roots are removed after bounded processing; outputs are atomically committed only after all mandatory validation. Failure reports may be retained independently but never include an eligible proposal. CI and readiness artifacts request 30-day retention, with actual expiration recorded and repository support checked. No persistent release database or automatic promotion state is introduced.

## Open decisions

None. The user approved this representation at Gate 2 on 2026-10-03. The distributed slice-verifier inventory and DN-001 through DN-004 delivery evidence remain unchanged.
