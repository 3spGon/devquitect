# Instruction Governance Interfaces

Status: Review
Last updated: 2026-09-10

## Confirmed

- `devquitect validate` additionally validates the authority map and returns normal deterministic
  validation records.
- `devquitect calibrate` is an explicitly invoked model-backed command that writes a
  `behavior-calibration` JSON report. It returns calibration execution status only.
- `devquitect release-check` accepts deterministic evidence only and rejects calibration reports
  as promotion evidence. It remains the owner of promotion proposals.
- Report comparison is read-only and reports `comparable`, `not-comparable`, or `unknown`; it
  cannot change release eligibility.

## Open decisions

None.
