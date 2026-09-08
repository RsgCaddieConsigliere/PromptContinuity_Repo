# Corpus Reconcile v0.1

Deterministic pilot engine for corpus inventory, fixity, exact deduplication, email attachment indexing, lineage, naming proposals, and gated Drive transaction planning.

## Safety boundary
- Public-safe code only: no matter facts, Drive IDs, email addresses, or source files.
- v0.1 executor vocabulary: RENAME, MOVE, RENAME_MOVE, COPY.
- DELETE, SHARE, and permission changes are unsupported.
- Hash = fixity, not authenticity/truth/admissibility.
- Google-native objects use revision/export fixity; never label an export hash as native raw SHA-256.
- AI classifications are review inputs, not canonical truth.

## Quick test
```bash
python -m pytest -q
python -m corpus_reconcile.cli inventory fixtures/test_corpus --matter PILOT > pilot-output.json
python -m corpus_reconcile.cli parse-eml fixtures/test_corpus/email/001_message.eml
```

## Operating split
- GitHub: generic code, schemas, tests, version history.
- Cowork: deterministic local execution on bounded source packages.
- ChatGPT Work + Drive/Sheets/Gmail: cloud orchestration, access enforcement, metadata census, Source Sets, transaction approval/execution/readback.

See `docs/TRANSACTION_STATE_MACHINE.md` and `docs/ORCHESTRATION_CONTRACT.md`.
