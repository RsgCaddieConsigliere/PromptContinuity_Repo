# Corpus Reconcile v0.1 — Cowork + ChatGPT Work Handoff

## Transaction state machine
`DRAFT -> HITL_PENDING -> APPROVED -> PRECONDITION_CHECK -> EXECUTING -> APPLIED -> READBACK_VERIFIED -> CLOSED`

Exceptional states: `STALE`, `CONFLICT`, `FAILED`, `CANCELLED`, `ROLLBACK_PENDING -> ROLLED_BACK`.

v0.1 is fail-closed and intentionally excludes DELETE, SHARE, and permission changes.

### Preconditions before any mutation
1. Drive ID unchanged.
2. Current parent equals approved expected parent.
3. Current name equals approved expected name.
4. Current fixity/revision basis equals approved expected value.
5. Technical capability allows the action.
6. User authorization allows the action.
7. Object is outside policy read-only roots.
8. Exact transaction ID remains human-approved.

After provider success, immediately read back by Drive ID. Metadata-only rename/move must preserve content fixity. COPY must create a new Drive ID with expected source-derived fixity. Any mismatch becomes CONFLICT and freezes the run.

## Cowork role
Run deterministic analysis inside one dedicated working folder. v0.1 must not mutate canonical Drive content. Inputs are this package plus a bounded source package and private runtime config supplied outside GitHub. Outputs: source-object inventory, exact duplicate families, parsed EML/attachment hashes, ZIP member manifests, and exceptions. If lineage is ambiguous, emit `HITL_REQUIRED` instead of choosing a canonical object.

## ChatGPT Work role
1. Resolve source roots by Drive ID, not filename.
2. Load authorization policy separately from Drive capabilities.
3. Create `RUN_ID` and `SOURCE_SET_ID`; first live run is `READ_ONLY`.
4. Populate Drive metadata and Gmail-native identifiers into the control plane.
5. Stored binary: use Drive-reported SHA-256 when available. Google-native: Drive ID + revision/version + modified time; selected exports use `EXPORT_SHA256`, never native-raw labeling.
6. Exact-hash families are deterministic. Version/format/OCR/semantic families remain candidates until reviewed.
7. Write proposed rename/move rows only; no mutation from prose instructions.
8. Human approves exact transaction IDs with approver + timestamp.
9. One write owner executes approved transactions only in authorized scopes.
10. Read back every mutation by Drive ID and log immutable transaction events.

## Concurrency
One `WRITE_OWNER` per controlled object/run. Secondary AI seats are review-only unless write scopes are explicitly non-overlapping.

## Source/proposition rules
Hash proves fixity only. AI repetition is not corroboration. OCR/exports/AI summaries are derivative relationships. Rejected propositions remain regression objects and cannot be promoted without new primary-source evidence.
