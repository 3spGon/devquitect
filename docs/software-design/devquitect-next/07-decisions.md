# Devquitect Next decisions

Status: Approved
Last updated: 2026-10-03

## Confirmed

| Decision | Rationale |
| --- | --- |
| Treat this as a full-depth system change. | It affects all skill contracts, introduces a workflow route, and changes a persisted machine-readable contract. |
| Deliver in staged releases through 1.0.0. | It isolates behavior/routing evolution and reserves stability for demonstrated contracts. |
| Keep QUICK independent from `project-plan-execution`. | The latter is intentionally limited to approved persistent-plan slices; QUICK has a different authorization and lifecycle boundary. |
| Preserve verify_slice exactly as implemented. | The user removed verifier portability and migration from this initiative; its runtime, YAML format, and acceptance contract remain unchanged. |
| Do not add a fourth routing skill in 0.7.0. | A router would duplicate selection work and add overhead before evidence shows implicit skill selection is insufficient. |
| Treat 1.0.0 as a stability release, not 2.0.0. | The product remains on its pre-1.0 public development line and requires evidence before declaring stability. |
| Use an append-only, snapshot-referencing Markdown ledger. | The existing snapshot and report artifacts already own exact text and results; a new parsed store would duplicate them without a consumer. |
| Preserve `change_profile` and add optional common `workflow_depth`. | This generalizes depth without a migration of existing persistent session state. |
| Make the durable root caller-supplied and repository-relative. | It supports alternate locations without inventing a global configuration system. |
| Preserve GPT-5.6 Sol/Terra/Luna as baseline rows and add GPT-6 Sol/Luna as separate evaluation rows. | The user approved this cross-generation scope at Gate 1; retaining the earlier family supports comparison over time while distinct rows prevent pooling incomparable results. |

## Assumptions

The existing verifier remains supported according to its current contract.

## Gate 1 DN-005 / DN-006 decisions

The user approved this operating direction at amended Gate 1 on 2026-10-03. These decisions amend only the future 1.0.0 slices; detailed technical design is submitted separately at Gate 2 and implementation remains separately authorized.

| Decision | Recommendation and rejected alternative |
| --- | --- |
| DEC-DN-011 — Independent deterministic verification | Use clean GitHub Actions CI to repeat existing credential-free tooling. Local evidence remains necessary but is no longer the sole technical authority. Do not replace the existing checker or add a CI platform. |
| DEC-DN-012 — Exact final-candidate identity | Test PR integration and rerun CI for the final SHA on `main`. Readiness requires exact SHA equality. Reject implicit tree equivalence and reuse of pre-squash evidence because they weaken attribution. |
| DEC-DN-013 — Minimal platform and package scope | Smoke-test three OS families on Python 3.12; build the canonical ZIP twice in clean Linux output roots using the same locked toolchain. Defer multi-Python and cross-platform byte-equality claims until evidence requires them. |
| DEC-DN-014 — Provenance plus bytes | Verify repository/workflow/run/attempt/artifact metadata, each mandatory job conclusion, and package/manifest file digests. Reuse the existing rebuild policy and enforce the missing CI-input binding deterministically. A passing self-declared JSON report is insufficient. |
| DEC-DN-015 — Previous-release compatibility | Add an explicit immutable previous-release reference for readiness, preserving parent-based behavior for existing callers that omit it. Requiring every candidate to be the version-bump commit would unnecessarily exclude later fixes. |
| DEC-DN-016 — Operational merge gates | Require stable quality, platform-smoke, and package checks plus effective protection of `main`. Documentation may describe how to activate protection, but DN-005 cannot claim the protected merge gate while activation is pending. |
| DEC-DN-017 — Separate behavioral authority | Establish a manual behavioral workflow with explicit authorization and supported unattended authentication. Keep DN-004's independent rows and do not make model availability or results required PR gates. Readiness consumes existing authorized rows without launching models. |
| DEC-DN-018 — Eligibility is not approval | Emit structured readiness and an unapproved proposal only. Defer public release, tags, installation, publishing credentials, and attestations; they are unnecessary for the requested verification boundary. |

Evidence: the current packager rejects committed-version mismatch; promotion policy rebuilds twice, binds check identity, and compares compatibility with the immediate parent. The requested CI binding and explicit prior-release baseline are additions, not already implemented guarantees. The earlier analysis's statement that packaging rewrites a mismatched version was incorrect and is not carried into this revision.

GitHub documents the [PR integration SHA and workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [required-check behavior](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), and [artifact digests](https://docs.github.com/en/actions/tutorials/store-and-share-data). The project must enforce its own file-digest mismatch as a failure, not depend on a download warning.

## Technical treatment approved at Gate 2

The amended Gate 1 is approved. The technical documents select one additive CI-aware `release-check` interface, a standard-library GitHub evidence adapter, and a version-1 CI evidence schema. Existing canonical report and promotion schemas remain unchanged; richer provenance is carried by report inputs and evidence entries. This avoids migrating legacy proposal consumers or building a second release manager.

The user explicitly approved Gate 2 on 2026-10-03. The new technical treatment and the previously approved operating direction are Approved, without reopening R-11 through R-14.

Require complete reruns, literal stable check names, push/main evidence for the exact release SHA, authenticated artifact-container digests plus contained file identities, and a 30-day review-retention window. Partial reruns and a self-declared passing registry are rejected. The GitHub [attempt-specific jobs endpoint](https://docs.github.com/en/rest/actions/workflow-jobs) and [artifact metadata endpoint](https://docs.github.com/en/rest/actions/artifacts) establish observed provenance. [Artifact retention](https://docs.github.com/en/actions/tutorials/store-and-share-data) is bounded by repository/organization policy, so effective support must be checked at delivery.

The explicit previous-release SHA must be an ancestor with a lower plugin version. Legacy omission preserves parent-based behavior. CI-mode output is staged to a new directory and published locally only after all validation, without overwriting an existing output. Failure reports distinguish policy/configuration/unavailable verification while never producing an eligible proposal. These technical choices have Gate 2 approval and authorize no implementation.

## Open decisions

None. The initial model families, amended Gate 1, Gate 2, and plan revision 3 are approved. Workflow protection must be verified against the target repository during delivery; its present remote state has not been asserted.
