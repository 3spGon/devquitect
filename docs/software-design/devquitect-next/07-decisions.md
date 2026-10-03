# Devquitect Next decisions

Status: Approved
Last updated: 2026-09-22

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

## Open decisions

None. Gate 1 approved the initial model families; technical configuration and evidence handling are defined in the architecture and interface contracts.
