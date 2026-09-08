# corpus-reconcile v0.1.1 — G0-G5 Control Amendment

Status: adopted for the read-only corpus pilot.

## Release state
No corpus mutation is authorized until G0-G5 and parent HITL pass. The first live run is full-root read-only.

## Identity
- `CONTENT_ID` identifies ordinary binary byte content as `sha256:<digest>`.
- `FILE_INSTANCE_ID` identifies one observed physical instance.
- At first observation only: UUIDv5 over stable root namespace + normalized original relative path + first-observation SHA-256.
- Thereafter the parent-controlled instance registry / transaction ledger preserves the instance ID across approved move/rename and permitted in-place work-product byte changes.
- Exact duplicates at different original paths share `CONTENT_ID` but retain separate `FILE_INSTANCE_ID`s.
- `LOGICAL_DOC_ID`, when later used, groups versions/derivatives only from relationship evidence; filename similarity alone is insufficient.

## Protection
Minimum classes: `SOURCE_IMMUTABLE`, `MUTABLE_WORK_PRODUCT`, `DERIVATIVE`, `QUARANTINE`, `UNKNOWN`.

`UNKNOWN` is non-mutable by default. Sticky protection is path-independent. Known protected objects remain protected until a parent-authorized status event changes that classification.

## Fixity
Capture size + mtime_ns before and after local hashing. If either changes, mark `STALE_DURING_SCAN` and reject the hash as a baseline. Hash failures leave the SHA field null and record a separate diagnostic. Google-native wrapper files are not native content hashes; use Drive identity + revision/version basis, and call deliberate export hashes `EXPORT_SHA256`.

## Path / symlink controls
Symlinks are inventoried, not blindly followed. Path escape blocks mutation eligibility. Hidden files are inventoried except explicitly defined OS-noise classes, which remain represented with an exclusion reason.

## Relationships
Supported/candidate relationship vocabulary includes `EXACT_BYTE_DUPLICATE`, `VERSION_PREDECESSOR`, `VERSION_SUCCESSOR`, `FORMAT_DERIVATIVE`, `OCR_DERIVATIVE`, `EMAIL_EXPORT_DERIVATIVE`, `ATTACHMENT_OF`, `ZIP_MEMBER_OF`, `MIRROR`, `CONVENIENCE_COPY`, `NEAR_DUPLICATE_CANDIDATE`. Relationship certainty is explicit.

Exact-byte grouping never auto-selects a canonical survivor.

## Sampling
Sampling occurs only after the full census. Build deterministic strata from protection class, file type, relationship family when available, and exception class. Within strata use deterministic ranking derived from `FILE_INSTANCE_ID + RUN_SEED`. Historical run outputs are append-only and never overwritten.

## Transaction manifest
DRAFT only until HITL. Canonical operation enum: `RENAME`, `MOVE`, `RENAME_MOVE`, `COPY`. DELETE and overwrite are unsupported. Every transaction includes persistent instance identity, expected fixity, protection/eligibility state, collision state, precondition state, and reversal information.

## Canary
After G0-G5 and parent HITL, the first mutation canary is only 3-5 non-sticky, non-quarantined, collision-free `MUTABLE_WORK_PRODUCT` / `DERIVATIVE` objects with stable fixity. Source originals are excluded. Each operation requires post-operation fixity/readback and an idempotency rerun that proposes zero duplicate transactions for already completed changes.

## Tool roles
- GitHub: one generic deterministic implementation lineage.
- Drive API: cloud identity/revision/checksum metadata.
- ChatGPT Work + Sheets/Docs: orchestration, control state, Source Sets, HITL.
- Cowork: deterministic local/synced corpus execution.
- Other models: optional critique/patch proposals only; never independent canonical engines.
