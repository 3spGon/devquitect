# Instruction Governance Data Model

Status: Review
Last updated: 2026-09-10

## Confirmed

### Authority map

One external YAML document contains `schema_version` and unique `contracts`. Each contract has
`id`, `owner_path`, and `secondary_paths`. Paths are repository-relative and must exist. The map
does not encode prose or individual instructions.

### Calibration report

One JSON report contains `schema_version`, `report_type: behavior-calibration`, `run_id`,
`skill_snapshot_id`, `skill_version`, `model`, `runtime`, `suite_id`, `suite_digest`,
`repetitions`, `dimensions`, optional `summary_score`, `generated_at`, and bounded evidence
references. A comparison is valid only when model, runtime, suite digest, and repetition count
match. Absence is `unknown`, never `fail`.

Reports are append-only local evidence. Credentials and raw transcripts are excluded; caller
retention/deletion does not affect promotion records.

## Open decisions

None.
