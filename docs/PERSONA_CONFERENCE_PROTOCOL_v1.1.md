# Collaborative Persona Conference Protocol v1.1

Status: RECOMMENDED SUCCESSOR / EXECUTION-FIRST
Date: 2026-09-04
Supersedes for new work: `PERSONA_CONFERENCE_PROTOCOL_v1.0.md`
Companion control: `EXECUTION_FIRST_OPERATING_INVARIANTS_v1.0.md`

## 1. Controlling priority

Every persona optimizes in this order:

1. **EXECUTE** the highest-value ready task.
2. **COMPLETE** a finite deliverable.
3. **REMOVE REPEATED FRICTION** that materially slows multiple tasks or blocks the current deliverable.
4. **IMPROVE INFRASTRUCTURE** only when an observed blocker, repeated failure, or material governance risk justifies it.

If system improvement competes with a finishable deliverable, the deliverable wins unless accuracy, source integrity, confidentiality, or release safety would materially suffer.

## 2. Conference trigger — exception driven

Do **not** run a persona conference after every substantive iteration.

Run it only when at least one trigger is present:
- a material source conflict or verification dispute;
- a consequential release/procedural/professional decision;
- a failed acceptance test or failed QC that changes the next action;
- a new source materially changes state;
- the best execution surface is genuinely unclear;
- two material personas disagree on a next action;
- a human/counsel answer is needed to unblock release.

If the next action is already clear and safe, **skip the conference and execute it**.

## 3. Participation

Use only personas materially relevant to the trigger. Default to 2-4 personas. Never convene the full registry merely for completeness.

Examples:
- Filing/legal verification: ChatGPT verification + drafting worker + human/counsel gate only if needed.
- Corpus processing: Cowork/file-processing worker + ChatGPT verification only when an exception needs adjudication.
- IRS/FCA: bounded writer + source verifier + counsel/professional gate only where legally/procedurally consequential.

## 4. Mandatory contribution

Each participating persona contributes exactly:

1. **RECOMMENDATION** — one concrete action that advances the current completion objective.
2. **QUESTION** — one highest-value question only if the answer could materially change the next action, verification state, or release decision.

Optional only when necessary:
- **RISK/CONSTRAINT** — one short material caveat.

If no material question exists, write `NONE — EXECUTE` rather than inventing one.

Do not provide chain-of-thought. Return conclusions, source/status references, decisions, and actions only.

## 5. Chair synthesis

The active ChatGPT orchestration persona acts as chair unless another surface is explicitly assigned.

The chair returns only:
- CONSENSUS / AGREEMENT
- MATERIAL DISAGREEMENT / OPEN QUESTION, if any
- CONTROLLING SOURCE OR STATUS
- DECISION OWNER
- SINGLE NEXT ACTION
- BEST EXECUTION SURFACE
- VERIFY / HOLD / RELEASE state

AI-to-AI agreement is never factual corroboration. Native/original/official sources and controlling verified objects remain authoritative.

## 6. Anti-loop / friction rule

The conference exists to remove uncertainty, not create work.

Therefore:
- one recommendation per persona;
- one question only when material;
- one conference per trigger event;
- no new artifact solely because an idea is interesting;
- use existing job/register/artifact when one fits;
- no corpus replay when a capsule, manifest, source ID, or delta can carry context;
- no repeated conference after the chair has selected a safe next action;
- no polish-only analysis after acceptance tests pass.

## 7. Pass budget

Default:
- **PASS A — MAKE IT COMPLETE**
- **PASS B — VERIFY AND RELEASE**
- **STOP**

A further pass requires a material trigger: new source, failed QC, professional feedback, factual correction, procedural change, or actual acceptance-test failure.

## 8. Friction-to-automation trigger

Create or modify protocol/automation only when at least one is true:
- current priority deliverable is blocked;
- the same friction occurred at least twice;
- one automation removes a repeated human step across multiple downstream jobs;
- the issue creates material accuracy, provenance, confidentiality, or release risk.

Otherwise: `PARK -> EXECUTE CURRENT JOB`.

## 9. Submission-first precedence

Current output priority:
1. California filings for Nenita.
2. IRS Form 211 submission package for Ranier.
3. FCA counsel-ready factual/evidence/outreach package, with licensed FCA counsel controlling actual qui tam filing and legal pleading decisions.

Workflow improvements remain parked unless they directly reduce time, close a blocker, reduce repeated HITL, improve source accuracy, or increase safe automation for these outcomes.

## 10. Meta-prompt rule

Generate a cross-platform prompt only when another platform/account/agent will materially accelerate the next bounded operation.

Use only:
- ROLE / PERSONA
- OBJECTIVE
- CONTROLLING INPUTS
- CURRENT STATE
- SOURCE / VERIFICATION RULES
- ALLOWED OPERATIONS
- PROHIBITED OPERATIONS
- REQUIRED OUTPUT
- DEFINITION OF DONE
- RETURN / EXCEPTION FORMAT

Do not restate full project history when a capsule, source freeze, manifest, or artifact ID can carry it.

## 11. Execution prompt template

ROLE / PERSONA:
<target persona>

OBJECTIVE:
<one bounded deliverable>

CONTROLLING INPUTS:
<artifact/source IDs or file names>

CURRENT STATE:
<verified / pending / blocker summary>

SOURCE / VERIFICATION RULES:
- Native/original/official sources control.
- AI summaries are derivative.
- Do not promote unsupported facts.
- Preserve explicit verification-status distinctions.

ALLOWED OPERATIONS:
<read/extract/compare/draft/propose/reversible-copy/etc.>

PROHIBITED OPERATIONS:
<delete/overwrite/send/file/disclose/assume legal effect/etc.>

REQUIRED OUTPUT:
<artifact or structured result>

DEFINITION OF DONE:
<finite acceptance test>

RETURN / EXCEPTIONS:
Return COMPLETED, READY, READY-EXCEPT, NEEDS-VERIFY, NEEDS-HITL, exact source requests, and the smallest exception list.

## 12. Dynamic persona routing

Add, remove, or retask personas as the work changes. Do not preserve a persona merely because it participated previously.

Routing question:

> Who can complete the next bounded operation fastest and most reliably while preserving source control?

## 13. User-facing compact form

Use a persona conference in user-facing output only when a trigger in section 2 exists. Otherwise report execution status and next action directly.

When triggered:

| Persona | Recommendation | Material Question |
| --- | --- | --- |
| <persona> | <one action> | <question or NONE — EXECUTE> |

**Chair:** <single next action / best surface / verification state>

## 14. Definition of done

The conference is done when it resolves or cleanly routes the triggering exception and identifies one executable next action. Then stop and execute.
