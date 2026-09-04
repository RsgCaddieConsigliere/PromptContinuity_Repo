# Collaborative Persona Conference Protocol v1.0

Status: ACTIVE / LOW-FRICTION DELTA
Date: 2026-09-04
Purpose: Add a concise cross-platform persona conference to the existing orchestration system without creating a parallel SSOT or open-ended architecture work.

## 1. Trigger
Run this protocol after every substantive iteration that changes a source state, artifact state, filing/submission state, project blocker, platform handoff, or next action.

Do not run it for trivial acknowledgements.

## 2. Participation
Use only personas materially relevant to the current task. Default to 2-5 personas, not the entire registry.

Examples:
- Filing/legal verification: ChatGPT Chat + ChatGPT Work + Claude Red-Team + Human/Counsel gate.
- File corpus processing: Claude Cowork + ChatGPT Work + Drive + ChatGPT verification.
- IRS/FCA source synthesis: ChatGPT Chat + bounded worker + Claude Red-Team + Notebook/Gemini when source-grounded corpus review helps.

## 3. Mandatory contribution from each participating persona
Each persona MUST contribute exactly:

1. RECOMMENDATION — one concrete recommendation that advances the current submission/completion objective.
2. QUESTION — one highest-value question for the other personas/HITL that could materially change the next action, verification state, or release decision.

Optional only when necessary:
- RISK/CONSTRAINT — one short material caveat.

Do not provide hidden chain-of-thought. The conference output is a concise decision-support matrix containing conclusions, questions, source/status references, and next actions only.

## 4. Conference matrix

| Persona | Recommendation | Question | Risk/Constraint (optional) |
|---|---|---|---|
| <persona> | <one action> | <one material question> | <optional> |

## 5. Chair synthesis
The active ChatGPT orchestration persona acts as conference chair unless another platform is explicitly assigned.

The chair MUST output:
- CONSENSUS / AGREEMENT
- DISAGREEMENT / OPEN QUESTION
- CONTROLLING SOURCE OR STATUS
- DECISION OWNER
- SINGLE NEXT ACTION
- BEST EXECUTION SURFACE
- VERIFY / HOLD / RELEASE state

AI-to-AI agreement is never factual corroboration. Native/original/official sources and the controlling SSOT remain authoritative.

## 6. Anti-loop rule
The persona conference exists to reduce uncertainty, not generate more work.

Therefore:
- Each persona gets one recommendation and one question only.
- Maximum one conference per substantive iteration unless a new source, failed QC, human answer, or material conflict enters.
- Do not create new artifacts solely because the conference identified an interesting idea.
- Prefer an existing artifact/register/job when one already fits.
- If the next action is already clear, the conference should confirm it and stop.

## 7. Submission-first precedence
For current priority projects, recommendations must be judged by whether they move one of these outcomes toward completion:

1. California filings for Nenita.
2. IRS Form 211 submission package for Ranier.
3. FCA counsel-ready complaint/evidence/outreach package, with licensed counsel controlling actual qui tam filing.

Workflow-system improvements are PARKED unless they materially reduce time, improve source accuracy, close a blocker, or increase safe automation for those outcomes.

## 8. Meta-prompt rule
After the chair synthesis, produce one copy-ready NEXT ACTION PROMPT when another platform/account/agent would materially accelerate the work.

The prompt should contain only:
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

Do not restate the whole project history when a Project Capsule, Source Freeze, manifest, or artifact ID can carry that context.

## 9. Next-action prompt template

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
- Preserve SOURCE-MISSING / SOURCE-LOCATED / SOURCE-VERIFIED / LOCKED-VERBATIM distinctions.

ALLOWED OPERATIONS:
<read/extract/compare/draft/propose/etc.>

PROHIBITED OPERATIONS:
<delete/overwrite/send/file/assume legal effect/etc.>

REQUIRED OUTPUT:
<artifact or structured result>

DEFINITION OF DONE:
<finite acceptance test>

RETURN / EXCEPTIONS:
Return COMPLETED, BLOCKED, NEEDS-VERIFY, NEEDS-HITL, plus the smallest exception list.

## 10. Dynamic persona adjustment
The chair may add, remove, or retask personas as the work changes. Do not preserve a persona in the conference merely because it participated previously.

The routing question is always:
"Who can complete the next bounded operation fastest and most reliably while preserving source control?"

## 11. User-facing compact form
At the end of substantive responses, use this compact pattern when helpful:

### Persona Conference
| Persona | Recommendation | Question |
|---|---|---|
| ... | ... | ... |

**Chair:** <single next action / best surface / verification state>

**Next Action Prompt:** <copy-ready prompt if cross-platform handoff is useful>

This protocol is a delta to CROSS_AI_PERSONA_ORCHESTRATION_v1.0 and LOW_FRICTION_AGENT_EXECUTION_v1.0. It does not create a separate SSOT.