# AI_LEGAL_OS - LEGAL REVIEW PRACTICE OVERLAY

Status: `NONCANONICAL_ADOPTION_CANDIDATE`
Seat: `GPTA`
Project: `PRJ-000`
Source Set: `SS-PRJ000-YTLEGAL-001-v1.0`
Canonical write authority: `NOT_GRANTED`
Source mutation authority: `NOT_GRANTED`

## Purpose

Operationalize the useful practices in the supplied Claude-for-legal materials without displacing AI_LEGAL_OS source lineage, archive boundaries, stable IDs, bounded Source Sets, conflict/errata preservation, verification gates, or GPTR I03 control authority.

## 1. Task brief contract

Every material legal task should state, at minimum:

1. `SEAT / ROLE`
2. `RECIPIENT / AUDIENCE`
3. `PURPOSE / OUTCOME`
4. `MATTER CONTEXT`
5. `SOURCE_SET_ID / VERSION`
6. `FACTS / INPUTS` - source-backed or explicitly labeled allegation/inference/unknown
7. `REGISTER / TONE`
8. `OUTPUT STRUCTURE`
9. `SCOPE IN / SCOPE OUT`
10. `STOP CONDITION`
11. `CONSTRAINTS`
12. `VERIFICATION INSTRUCTION`

For fresh-document tasks, include a fail-closed orientation instruction: identify the supplied objects and do not begin merits analysis until the named Source Set is present.

## 2. Matter intake sequence

For a newly bounded matter set:

`SOURCE INTAKE -> COLD ORIENTATION -> EVENT/CHRONOLOGY EXTRACTION -> PARTY/ENTITY MAP -> ISSUE MAP -> GAP/CONFLICT CHECK`

The orientation output is derivative. Chronology entries must remain source-backed event assertions; party/issue maps do not promote allegations or inferences to facts.

## 3. Multi-document discipline

- Give every object a stable source ID/provider ID before substantive comparison.
- State document roles and reading order when sequence matters.
- Ask cross-document questions explicitly; do not assume automatic comparison.
- Prefer structured extraction before summary: dates, actors, obligations, defined terms, amounts, deadlines, source locators, and version deltas.
- Preserve `LOCATED`, `OPENED`, `REVIEWED`, and `VERIFIED` as distinct coverage states.

## 4. Four-pass substantive document review

For each in-scope substantive document, use:

1. `WHAT_IS_IN_IT` - contents, parties, operative provisions, what the source actually establishes.
2. `UNUSUAL_OR_DEPARTURE` - unusual terms or departures; any market/custom characterization is separately verifiable.
3. `AMBIGUOUS` - language or facts capable of multiple readings; identify who benefits from each reading only when supportable.
4. `MISSING_OR_GAP` - missing expected content, chronology discontinuities, referenced-but-not-present materials, and expected-source hypotheses.

Exceptions: exact byte duplicates are not re-reviewed; archive directories are preserved/indexed and content review is skipped; `0000X-Files-Restricted` is never traversed.

## 5. Chained drafting sequence

Default high-value chain:

`ORIENTATION -> ISSUE LIST -> STRUCTURE -> SECTION/DRAFT -> ACCURACY READ -> ADVERSARIAL READ -> AUDIENCE READ -> VERIFICATION -> RELEASE GATE`

Each stage is preserved as a derivative with predecessor/successor lineage. No newest-draft-wins assumption.

## 6. Opposition / adverse read

Before material work that an opposing party, court, regulator, counterparty, or client will rely on:

- identify the strongest argument against the proposed position;
- identify weak points and adverse factual characterizations;
- identify authority that may undermine, distinguish, or limit the position;
- identify evidentiary/source gaps the other side can exploit;
- identify likely cross-examination or credibility attacks when relevant;
- classify outputs into `FACT`, `ALLEGATION`, `INFERENCE`, `UNKNOWN/GAP`, and `RESEARCH_QUESTION` or a more precise existing AI_LEGAL_OS status.

Every material weakness must receive a disposition: `ADDRESS / ACKNOWLEDGE / RESEARCH / CONFLICT / GAP / ACCEPTED_RISK / REQUIRES_COUNSEL`.

## 7. Court-facing stress test

For substantive court-facing work, add four independent reads:

- `OPPOSITION_READ`
- `JUDICIAL_READ`
- `AUTHORITY_QUEUE_READ`
- `FACTUAL_ACCURACY_READ`

The authority read does not verify authority by itself. It populates or audits the authority verification queue. Filing-grade authority verification remains primary/research-source based.

## 8. Contract/document profiles

Reusable structured profiles may include:

- client obligations with clause/source locator, trigger/deadline, and consequence;
- defined terms plus undefined-use candidates;
- redline/version comparison with every substantive change and material/cosmetic classification;
- notice-compliance checklist with source clause, event facts, and jurisdictional verification flags.

For negotiation redrafts, small priority sets may improve usability, but the full issue ledger must remain available so material issues are not suppressed.

## 9. Advice-letter profile

Before drafting an advice letter, the responsible human/control seat supplies or approves:

- client sophistication/context;
- legal position;
- recommendation;
- decision/action the client faces;
- risk of inaction/wrong decision;
- desired and undesired register/tone.

Then run separate `ACCURACY`, `CLARITY`, and `CLIENT_SPECIFICITY` reads. AI expresses and tests the advice; it does not acquire professional accountability for the recommendation.

## 10. Verification and release

`[VERIFY]` is adopted as a visible task marker, mapped to the existing verification queue.

Before `COUNSEL_READY`, client delivery, filing, service, signature, or other external release:

- material factual assertions are source-checked;
- authority verification is complete to the required dimensions;
- material quotations/pinpoints are verified;
- jurisdiction/currency issues are cleared;
- material conflicts/adverse facts are resolved or expressly accepted by the authorized reviewer;
- blocking `[VERIFY]` items are zero.

Internal drafts may retain unresolved verification flags. They must not be mislabeled release-ready.

## 11. Naming adoption boundary

The date-first naming convention is useful for chronological sorting but is subordinate to source identity.

Adopt only for new derivative/work-product display names, for example:

`<STABLE_ID>__2026-09-10__short-description__v0.1.ext`

Do not rename registered source originals solely to achieve date sorting. Provider IDs and original filenames remain provenance fields.

## 12. Delegation boundary

AI may: read bounded sets, extract, structure, compare, draft, summarize, generate issue/gap hypotheses, stress-test, and propose deltas.

Authorized humans/control seats retain: strategic judgment, professional advice ownership, settlement/advocacy decisions, filing/signature/service, source mutation approval, and canonical promotion.

## 13. Automation implications

Priority implementation deltas:

1. fail-closed archive/restricted non-traversal in local census/hash tooling;
2. conservative lineage inference when same-hash move candidates are ambiguous;
3. dry-run-only naming/move planners that operate on derivatives/work products until copied-canary/HITL promotion;
4. task-packet templates that embed Source Set ID, structured brief, four-pass/adversarial profile, and verification queue output;
5. release-gate checks that count unresolved blocking verification/conflict items rather than trusting a model-generated readiness label.

## Promotion posture

This overlay is a GPTA implementation candidate. It does not rewrite GPTR I03 canonical state and does not authorize source mutation.
