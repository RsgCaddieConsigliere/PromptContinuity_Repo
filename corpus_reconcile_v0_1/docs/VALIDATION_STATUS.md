# Validation Status — corpus-reconcile v0.1.1

## Current status

- The original pre-amendment v0.1 local regression suite executed successfully at 7/7 before the G0-G5 amendment.
- The G0-G5 / identity amendment expands the suite to 12 tests.
- The v0.1.1 patch was applied and statically read back through GitHub connectors only.
- The amended 12-test suite has **not yet been executed** in this connector-only pass.

Therefore, the earlier PR description stating that 7/7 tests passed applies only to the predecessor code state and must not be treated as validation of v0.1.1.

## Required release gate before Cowork production census

Cowork (or another authorized Python runtime) must execute:

```bash
python -m pytest -q
```

Expected minimum result: all 12 current tests pass.

Then run a bounded synthetic/read-only census with explicit `ROOT_ID`, `RUN_ID`, `RUN_SEED`, and instance registry. Preserve the command, stdout/stderr, package commit SHA, and generated output manifest as run evidence.

## Required gate before mutation canary

In addition to the test pass:

1. full-root read-only census completes without unhandled exceptions;
2. G0 protection classification is applied;
3. 25-50 object deterministic stratified Source Set is generated;
4. dry-run transaction manifest is reviewed;
5. G1-G5 pass;
6. parent HITL approves exact transaction IDs;
7. canary is limited to 3-5 eligible mutable work products/derivatives;
8. post-operation readback/fixity and idempotency rerun pass.

PR remains draft until those gates are satisfied.
