# Corpus Reconcile v0.1.1

Deterministic pilot engine for corpus inventory, fixity, exact-byte duplicate families, email attachment indexing, lineage, deterministic sampling, and gated Drive transaction planning.

## Safety boundary
- Public-safe code only: no matter facts, private Drive IDs, email addresses, or source files.
- Transaction vocabulary: RENAME, MOVE, RENAME_MOVE, COPY.
- DELETE, SHARE, permission changes, overwrite, and source-byte alteration are unsupported.
- Hash = fixity, not authenticity/truth/admissibility.
- Google-native objects use Drive identity + revision/version basis; deliberate exports use `EXPORT_SHA256`, never a claimed native raw SHA-256.
- AI classifications are review inputs, not canonical truth.
- `UNKNOWN`, sticky-protected, quarantined, path-escape, and collision-bearing objects fail closed for mutation planning.

## Identity model
- Ordinary binary `CONTENT_ID = sha256:<digest>`.
- `FILE_INSTANCE_ID` is assigned only at first observation using UUIDv5 over a stable root namespace + original relative path + first-observation SHA-256.
- Exact duplicates at different original paths share `CONTENT_ID` but retain distinct `FILE_INSTANCE_ID`s.
- After approved moves/renames or an in-place byte change, the instance registry preserves the existing `FILE_INSTANCE_ID`; a byte change produces a new `CONTENT_ID` observation rather than a new physical-instance identity.
- Exact-hash families do **not** auto-select a canonical survivor.

## G0-G5 sequence
`FULL ROOT READ ONLY -> G0 protection -> full census -> deterministic 25-50 object Source Set -> dry-run manifest -> G1 inventory -> G2 fixity -> G3 relationship/collision -> G4 reversibility -> G5 canary/idempotency -> HITL -> 3-5 mutable-derivative canary`.

The production filesystem census remains read-only until the parent control plane authorizes exact transaction IDs after G0-G5.

## Quick test
```bash
python -m pytest -q
python -m corpus_reconcile.cli inventory fixtures/test_corpus \
  --matter PILOT \
  --root-id ROOT-PILOT-001 \
  --run-id RUN-PILOT-001 \
  --run-seed G0G5-v1 \
  --sample-size 50 > pilot-output.json
python -m corpus_reconcile.cli parse-eml fixtures/test_corpus/email/001_message.eml
```

For subsequent runs, supply the parent-controlled instance registry with `--instance-registry` so previously observed instances retain identity across moves/renames and permitted in-place work-product changes.

## Operating split
- GitHub: one generic code/schema/test implementation lineage.
- Cowork: deterministic local execution against the declared local/synced corpus after parent release.
- Drive API: cloud object identity, metadata, revisions, and stored-file checksums.
- ChatGPT Work + Sheets/Docs: orchestration, access enforcement, Source Sets, HITL, and control-state updates.
- Other models may critique or propose patches; they do not create competing census engines.

See `docs/HANDOFF.md` and `docs/G0-G5_CONTROL_AMENDMENT.md`.
