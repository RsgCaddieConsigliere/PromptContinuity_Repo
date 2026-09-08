# Validation Status — corpus-reconcile v0.1.2

## Historical validation

- The original pre-amendment v0.1 local regression suite executed successfully at 7/7 before the G0-G5 amendment.
- The G0-G5 / identity amendment expanded the suite to 12 tests in v0.1.1.
- GitHub Actions run `34199502357` for commit `95048fff43c9024bd4b9127251fed7088efb2485` completed successfully, including package installation, compile, and the corpus-reconcile regression-test step.
- GitHub Actions run `34199654951` subsequently completed successfully on the accepted v0.1.1 state.

These results remain historical context only and do not substitute for validation of a changed implementation.

## v0.1.2 iteration-2 delta

v0.1.2 adds guarded single-byte-stream handling for special parsers:

- EML headers, raw MIME SHA-256, and attachment hashes are bound to one guarded byte observation.
- ZIP container SHA-256 and member hashes are bound to one guarded byte observation.
- The regression suite expanded from 12 to 14 tests to cover those invariants.

## Accepted execution baseline

`EXECUTION_BASELINE_COMMIT = 77e0fe03d100830458068d770d2466e1b259d4b9`

GitHub Actions `Control Plane CI` run `34201155378` completed **SUCCESS** on that exact baseline. The job successfully completed package installation, corpus-reconcile compilation, the v0.1.2 regression-test step, sandbox regression tests, JSON-schema parsing, and the public-control-plane identifier guard.

This commit is the pinned runtime target for the next Cowork census.

### Baseline-lock rule

Execution consumers MUST pin the exact validated `EXECUTION_BASELINE_COMMIT`, not a floating branch name or later documentation-only head.

A later branch commit does **not** supersede the execution baseline merely because it is newer. Promote a new execution baseline only when:

1. implementation code, schemas, tests, packaging, or runtime behavior materially changes and the applicable CI gate passes; or
2. the parent orchestrator explicitly promotes another already-validated implementation commit.

Documentation-only or control-commentary commits may advance the branch without retargeting Cowork. This separates implementation validation from documentation chronology and prevents avoidable moving-target handoffs.

## Current released action

The next authorized execution remains only the Cowork **FULL-ROOT READ-ONLY census** using the pinned execution baseline above, with explicit `ROOT_ID`, unique `RUN_ID`, parent-controlled `RUN_SEED`, and prior instance/sticky-protection registry.

Cowork must preserve its configuration, implementation commit SHA, output directory, and generated manifests as run evidence. A local smoke re-run of the test suite is optional environment confirmation, not a prerequisite.

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
