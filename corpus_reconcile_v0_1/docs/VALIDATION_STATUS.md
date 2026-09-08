# Validation Status — corpus-reconcile v0.1.2

## Historical validation

- The original pre-amendment v0.1 local regression suite executed successfully at 7/7 before the G0-G5 amendment.
- The G0-G5 / identity amendment expanded the suite to 12 tests in v0.1.1.
- GitHub Actions run `34199502357` for commit `95048fff43c9024bd4b9127251fed7088efb2485` completed successfully, including package installation, compile, and the corpus-reconcile regression-test step.
- GitHub Actions run `34199654951` subsequently completed successfully on the accepted v0.1.1 current-head documentation state.

These results are historical validation for v0.1.1 and do not substitute for validation of later code changes.

## v0.1.2 iteration-2 delta

v0.1.2 adds guarded single-byte-stream handling for special parsers:

- EML headers, raw MIME SHA-256, and attachment hashes are bound to one guarded byte observation.
- ZIP container SHA-256 and member hashes are bound to one guarded byte observation.
- The regression suite is expanded from 12 to 14 tests to cover those invariants.

## Current validation state

The v0.1.2 implementation is **PENDING CURRENT-HEAD CI** until the existing `Control Plane CI` workflow completes successfully on the final v0.1.2 branch head.

Do not direct Cowork to a v0.1.2 census until that current-head run succeeds. The previously validated v0.1.1 head remains the last validated execution baseline until then.

## Release gate after v0.1.2 CI success

Once current-head CI passes, the next authorized execution is still only the Cowork FULL-ROOT READ-ONLY census with explicit `ROOT_ID`, unique `RUN_ID`, parent-controlled `RUN_SEED`, and prior instance/sticky-protection registry.

Cowork must preserve its configuration, implementation commit SHA, output directory, and generated manifests as run evidence. A local smoke re-run of the test suite is optional environment confirmation after GitHub CI passes.

## Required gate before mutation canary

1. full-root read-only census completes without unhandled exceptions;
2. G0 protection classification / sticky protection state is applied;
3. deterministic 25-50 object stratified Source Set is generated;
4. DRAFT transaction manifest is produced and reviewed;
5. G1-G5 pass;
6. parent HITL approves exact transaction IDs;
7. canary is limited to 3-5 eligible mutable work products/derivatives;
8. post-operation readback/fixity and idempotency rerun pass.

No mutation authority is granted by CI. PR #2 remains draft and should remain unmerged until the bounded live read-only pilot and subsequent release gates are reviewed.
