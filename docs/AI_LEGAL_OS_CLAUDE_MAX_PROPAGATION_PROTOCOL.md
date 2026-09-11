# Claude Max Propagation Protocol v0.1

## Principle
Do not propagate chat history. Propagate bounded state packets.

Each Claude Max chat receives only:
1. project/seat instructions;
2. one task brief;
3. one bounded SOURCE_SET or immutable task ZIP;
4. the minimum source excerpts/files necessary for the assigned review;
5. the return contract.

Each chat must return deltas, not a replacement matter history.

## Standard first-message envelope
```text
SEAT_ID=CLDR
PROJECT_ID=<PRJ-ID>
CHAT_ID=<LOGICAL CHAT ID>
ROLE=<ROLE>
SOURCE_SET_ID=<ID>
SOURCE_SET_VERSION=<VERSION>
CANONICAL_WRITE_AUTHORITY=NOT_GRANTED
SOURCE_MUTATION_AUTHORITY=NOT_GRANTED

Work only from the attached bounded task packet and explicitly listed source objects.
Do not replay historical chats or preload the whole matter.
Never traverse 0000X-Files-Restricted or descendants.
Archive handling: PRESERVE -> INDEX -> SKIP CONTENT REVIEW.
Architecture and Research are live unless directory role says otherwise.
LOCATED != OPENED != VERIFIED. Hash/fixity != truth or legal authority.
Preserve contradictions, errata, adverse evidence, missing evidence, and uncertainty.
Return only material deltas plus the standard return envelope.
Do not rename, move, delete, overwrite, or promote source/canonical objects.
```

## Chat lifecycle
`BOOTSTRAP -> TASK_PACKET -> EXECUTE -> RETURN_ZIP -> GPTA_IMPORT -> CLDR/GPTR DISPOSITION -> CLOSE_OR_NEXT_DELTA`

A chat should be continued when its role remains the same and the next packet is a delta. Create a new chat when the task changes epistemic role, matter boundary, or privilege/access boundary.

## Token control
- Existing project knowledge: durable matter identity, current issue registry, role instructions, stable control rules only.
- Task packet: issue-specific facts/authorities/exhibits or implementation files only.
- Never attach every previous output to every chat.
- GPTA performs bulk extraction; CLDR reviews structured outputs and selected supporting sources; GPTR receives only compact unresolved deltas.

## Return package
Every material Claude run should contain RUN_SUMMARY.md, SOURCE_SET.csv, FILES_OPENED.csv, FILES_NOT_OPENED.csv, DELTAS.csv, ERRATA.md, CONFLICTS.md, ADVERSE_FACTS.md, VERIFY_QUEUE.csv if applicable, NEXT_ACTION.md, and SHA256SUMS.txt.

## Existing versus new chats
Use existing CLDR chats for continuing role-consistent QA. Do not create duplicate chats merely for capacity. Add new chats only where independent generation/review or matter-specialist parallelism materially reduces wall-clock time.
