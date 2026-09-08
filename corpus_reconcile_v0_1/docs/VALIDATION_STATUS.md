# Validation Status — corpus-reconcile v0.1.1

## Current status

- The original pre-amendment v0.1 local regression suite executed successfully at 7/7 before the G0-G5 amendment.
- The G0-G5 / identity amendment expands the current suite to 12 tests.
- The v0.1.1 patch was applied and statically read back through GitHub connectors.
- The existing `Control Plane CI` workflow was extended to install, compile, and test `corpus_reconcile_v0_1` whenever this implementation changes.
- GitHub Actions run `34199502357` for commit `95048fff43c9024bd4b9127251fed7088efb2485` completed successfully.
- The workflow job completed successfully, including `Install corpus-reconcile test dependencies`, `Compile corpus-reconcile package`, and `Run corpus-reconcile regression tests`.

The predecessor 7/7 result therefore remains historical context only; current v0.1.1 validation is established by the amended GitHub Actions regression-test step.

## Current release gate

Code-validation is no longer a blocker for the read-only filesystem pilot. The next authorized execution is the Cowork FULL-ROOT READ-ONLY census using the accepted v0.1.1 branch state, with explicit `ROOT_ID`, unique `RUN_ID`, parent-controlled `RUN_SEED`, and prior instance/sticky-protection registry.

Cowork must preserve the command/configuration, implementation commit SHA, output directory, and generated manifests as run evidence. A local smoke re-run of the test suite is optional environment confirmation, not a prerequisite to begin the read-only census.

## Required gate before mutation canary

1. full-root read-only census completes without unhandled exceptions;
2. G0 protection classification / sticky protection state is applied;
3. deterministic 25-50 object stratified Source Set is generated;
4. DRAFT transaction manifest is produced and reviewed;
5. G1-G5 pass;
6. parent HITL approves exact transaction IDs;
7. canary is limited to 3-5 eligible mutable work products/derivatives;
8. post-operation readback/fixity and idempotency rerun pass.

No mutation authority is granted by the CI pass. PR #2 remains draft and should remain unmerged until the bounded live read-only pilot and subsequent release gates are reviewed.
