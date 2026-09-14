# Instruction Governance Architecture

Status: Review
Last updated: 2026-09-10

## Confirmed

### Components

| Component | Responsibility |
| --- | --- |
| Authority map | External, versioned list of cross-file critical contract IDs, owners, and permitted secondary paths. |
| Structural validator | Validates the authority map and existing local-reference rules without interpreting prose. |
| Deterministic promotion | Requires credential-free checks, immutable source/artifact identity, and maintainer approval. It never consumes calibration results. |
| Calibration runner | Optional isolated model execution that writes an immutable behavior-calibration report. |
| Calibration report | Review-only evidence; records skill snapshot, model/runtime, suite, repetitions, dimension outcomes, and optional summary score. |

### Boundaries and flow

`validate` reads the authority map and reports deterministic violations. `check`, packaging, and
release eligibility consume deterministic evidence only. A separately invoked calibration runner
may create a report; it has no path to change promotion eligibility. Review tooling may compare
reports only when model/runtime and suite identities match.

### Data and lifecycle

A calibration report is append-only evidence identified by its skill snapshot, model/runtime,
suite digest, and run identity. It contains no raw credentials or unbounded transcripts. Missing
reports mean unknown calibration for that configuration. Reports can be retained or deleted under
local evidence policy without changing a release decision.

### Interfaces

- Authority map: contract ID, owner path, permitted secondary paths.
- Calibration report: snapshot ID, model, runtime, suite ID/digest, repetitions, dimension
  results, summary score optional, timestamps, and bounded evidence references.
- Promotion input: deterministic report IDs and immutable package/source identities only.

## Assumptions

- Existing JSON report conventions and isolated runner are reused; no external service or new
  dependency is needed.

## Open decisions

None.
