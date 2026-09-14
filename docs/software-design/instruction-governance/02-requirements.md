# Instruction Governance Requirements

Status: Approved
Last updated: 2026-09-10

## Confirmed

- **REQ-IG-01:** Each cross-file critical contract has one normative owner. Secondary documents
  may route, explain, test, or present that contract but must not redefine it.
- **REQ-IG-02:** A small external authority map lists only cross-file critical contracts, their
  owner paths, and permitted secondary roles.
- **REQ-IG-03:** Repository validation checks that authority-map IDs are unique, owner and
  reference paths exist, and declared secondary roles are permitted.
- **REQ-IG-04:** Each critical contract has external deterministic coverage, including a relevant
  negative case when the violation is observable. Tests and evaluation fixtures remain outside
  the packaged `skills/` tree.
- **REQ-IG-05:** The initiative must not require registration or metadata for every instruction,
  or attempt to infer arbitrary prose duplication or contradiction with a static linter.
- **REQ-IG-06:** Critical deterministic assertions for authorization, scoped mutation,
  durable state, and ownership are promotion-blocking.
- **REQ-IG-07:** Runtime and judge/infrastructure failures are recorded as inconclusive,
  never silently passed or counted as behavioral regressions.
- **REQ-IG-08:** Model-backed scenarios produce optional behavior-calibration reports and never
  block promotion.
- **REQ-IG-09:** Reports record skill version, model/runtime, suite version, repetitions,
  outcomes, and a dimension profile; a score compares only equal configurations.
- **REQ-IG-10:** Promotion requires the complete credential-free suite, immutable-source and
  artifact identity, and explicit maintainer approval; it does not require model evidence.
- **REQ-IG-11:** Broad model sweeps are governed as periodic calibration or major-release
  evidence rather than a default promotion prerequisite.
- **REQ-IG-12:** Repository guidance identifies skill and quality-tooling changes as deliberate
  product-contract evolution, keeps entrypoints concise, and directs contributors to external
  deterministic tests and baseline comparison for model-execution evidence.

## Assumptions

- Existing cases, schemas, and report formats can be extended without changing the core
  deterministic-first classification rule.
- The authority map and its validator live outside the packaged `skills/` tree.

## Open decisions

None.
