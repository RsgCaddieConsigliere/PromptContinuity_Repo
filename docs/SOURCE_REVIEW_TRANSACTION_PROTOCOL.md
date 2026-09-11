# Source Review Transaction Protocol

Status: noncanonical implementation candidate.

## Goal

Make each bounded source-review pass auditable, append-only, and safe to reuse without silently losing contradictory, adverse, deprecated, or unused information.

## Transaction sequence

1. Freeze a bounded Source Set manifest.
2. Compute source identity and fixity before substantive processing.
3. Parse/extract using a format-appropriate deterministic path and record complete coverage locators.
4. Produce exactly one source-review receipt per Source Set member.
5. Extract candidate facts, chronology events, authorities, exhibits, witnesses, conflicts, errata, missing-evidence leads, and VERIFY tasks with source locators.
6. Independently review proposed deltas before materialized current views are refreshed.
7. Append accepted, rejected, conflicting, deprecated, and no-use dispositions; never delete predecessor events.
8. Regenerate only the affected current views and packet sections.
9. Run integrity and evidentiary completeness tests.
10. Mark the source review-complete or archive-eligible only when coverage proof, lineage, and disposition are complete. A review-complete state does not authorize moving or deleting the source.

## Required distinctions

- LOCATED != OPENED != VERIFIED.
- Extraction completeness != factual truth.
- Source proposition != verified fact.
- Authority candidate != current controlling authority.
- Exact duplicate != independent corroboration.
- Review-complete != archive move authorized.
- Archive status != canonical truth.

## Minimum receipt fields

`SOURCE_REVIEW_ID | SOURCE_SET_ID | SOURCE_ID | ORIGINAL_FILENAME | SHA256 | REVIEW_METHOD | REVIEW_STATUS | COVERAGE_STATUS | COVERAGE_LOCATORS | FINDINGS_DISPOSITION | ARCHIVE_DISPOSITION | REVIEW_RUN_ID`

Use additional fields for pages, lines, sheets, parser/OCR version, reviewer identity, derived row IDs, conflicts, errata, rejected findings, and derivative destinations when available.

## Current-view rule

The append-only event history is the authoritative review history. Current fact, chronology, authority, exhibit, claim-element, conflict, missing-evidence, and readiness tables are materialized working views and may change as new evidence is verified. Predecessor rows remain traceable through stable identifiers and review events.

## Release rule

A source-review transaction may pass extraction and ledger tests while the legal packet remains blocked. Release requires the route-specific legal, authority, evidentiary, attorney/HITL, and no-submission gates.
