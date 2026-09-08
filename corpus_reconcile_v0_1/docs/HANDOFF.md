# Corpus Reconcile v0.1.1 — Cowork + ChatGPT Work Handoff

## Controlling release state
`READ_ONLY / DRY_RUN ONLY` until G0-G5 + parent HITL pass.

The first live Cowork run performs a full-root read-only census, protection classification inputs, deterministic fixity/identity capture, exact-byte family detection, deterministic 25–50 object Source Set selection, and a dry-run transaction manifest. It does not rename, move, copy, delete, overwrite, change permissions, or alter source bytes.

## Identity
- Ordinary binary `CONTENT_ID = sha256:<digest>`.
- `FILE_INSTANCE_ID` is assigned once at first observation from stable root namespace + original relative path + first-observation SHA-256.
- Existing instances are thereafter resolved from the parent-controlled instance registry / transaction ledger.
- A permitted in-place byte change to a mutable work product keeps `FILE_INSTANCE_ID` and creates a new observed `CONTENT_ID`.
- A `SOURCE_IMMUTABLE` byte change is an integrity conflict and blocks the object.
- Exact duplicates share `CONTENT_ID` but remain separate physical instances.

## Protection gate
Minimum classes:
`SOURCE_IMMUTABLE`, `MUTABLE_WORK_PRODUCT`, `DERIVATIVE`, `QUARANTINE`, `UNKNOWN`.

`UNKNOWN`, sticky-protected, quarantined (unless expressly tested), path-escape, collision-bearing, and unstable/hash-error objects are non-mutable by default.

## Transaction state machine
`DRAFT -> HITL_PENDING -> APPROVED -> PRECONDITION_CHECK -> EXECUTING -> APPLIED -> READBACK_VERIFIED -> CLOSED`

Exceptional states: `STALE`, `CONFLICT`, `FAILED`, `CANCELLED`, `ROLLBACK_PENDING -> ROLLED_BACK`.

Transaction vocabulary is `RENAME`, `MOVE`, `RENAME_MOVE`, `COPY`. `CREATE_COPY` is only a display synonym; `COPY` is the v0.1 canonical enum. DELETE, SHARE, permission changes, overwrite, and source-byte alteration are unsupported.

### Preconditions before any mutation
1. Persistent `FILE_INSTANCE_ID` resolves uniquely.
2. Drive ID/current filesystem object is the expected instance.
3. Current parent/path and name equal the approved precondition state.
4. Current fixity/revision basis equals the approved expected value.
5. Technical capability allows the action.
6. User authorization allows the action.
7. Protection class is eligible and no sticky/path-escape/collision block exists.
8. Exact transaction ID remains human-approved and unexpired.

After provider success, immediately read back by Drive ID or filesystem identity. Metadata-only rename/move must preserve content fixity. COPY must produce a distinct physical object with expected source-derived fixity. Any mismatch becomes `CONFLICT` and freezes the run.

## G0-G5 sequence
1. Full-root READ-ONLY census.
2. G0 protection classification / sticky-source application.
3. Deterministic stratified 25–50 object Source Set.
4. DRAFT transaction manifest only.
5. G1 inventory conservation.
6. G2 fixity baseline.
7. G3 relationship + collision control.
8. G4 reversibility.
9. G5 canary + idempotency preflight.
10. Parent HITL approval.
11. Only then: 3–5 `MUTABLE_WORK_PRODUCT` / `DERIVATIVE` canary transactions.
12. Post-operation fixity/readback and idempotency rerun.
13. Parent SCALE or HOLD decision.

## Cowork role
Run deterministic analysis against the declared local/synced corpus using a unique RUN_ID output directory outside the source corpus. Historical run outputs are never overwritten. Symlinks are inventoried and not blindly followed. Hidden files are inventoried except explicit OS-noise exclusions, which remain recorded with reasons. Return exceptions rather than guessing.

Required first-run outputs:
- persistent file-instance registry rows;
- per-run source-object observations;
- exact duplicate families with no automatic canonical survivor;
- parsed EML/attachment relationships where present;
- ZIP member manifests where present;
- deterministic stratified Source Set;
- DRAFT transaction manifest;
- exceptions/HITL queue;
- idempotency evidence on rerun.

## ChatGPT Work / parent control role
1. Resolve source roots by stable ID, not filename alone.
2. Load user authorization separately from provider capabilities.
3. Create `RUN_ID`, `ROOT_ID`, `RUN_SEED`, and `SOURCE_SET_ID`.
4. Supply prior instance registry / sticky protection state to Cowork.
5. Populate Drive metadata and Gmail-native identifiers when those connectors are in scope.
6. Stored binary: prefer Drive-reported SHA-256 where available. Google-native: Drive ID + revision/version basis; selected exports use `EXPORT_SHA256`, never native-raw labeling.
7. Exact-hash families are deterministic structural groups only. Canonical survivor selection requires provenance/lineage analysis and HITL where consequential.
8. Execute only exact APPROVED transaction IDs in authorized scopes.
9. One write owner executes; all mutations get readback and append-only transaction events.

## Concurrency
One `WRITE_OWNER` per controlled object/run. Secondary AI seats are review-only unless write scopes are explicitly non-overlapping.

## Source/proposition rules
Hash proves fixity only. AI repetition is not corroboration. OCR/exports/AI summaries are derivative relationships. Rejected propositions remain regression objects and cannot be promoted without new primary-source evidence.
