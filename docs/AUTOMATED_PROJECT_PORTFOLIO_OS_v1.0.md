# Automated Project Portfolio OS v1.0

Date: 2026-09-04
Status: ADOPTED FOR PILOT / APPEND-ONLY CONTROL

## Objective
Turn project files into a continuously maintainable portfolio in which deterministic automation handles inventory/hash/delta work, specialist AIs handle bounded extraction/synthesis, high-value claims are source-verified, and every project advances against explicit completion gates.

`FILES -> MANIFEST -> STRUCTURED OBJECTS -> JOBS -> VERIFIED STATE -> DELIVERABLES -> COMPLETION`

## Architecture

- **Data plane:** native/official files in Drive/local repositories. AI summaries never replace them.
- **Control plane:** Git-versioned generic schemas, prompts, scripts, policies, validation tests, project contracts, and handoff formats.
- **Project-state plane:** per-project manifests, source registers, issue/task registers, facts/quotes/events, gaps/conflicts/decisions, artifact registry, and current capsule.
- **Compute plane:** ChatGPT Work, Claude Cowork, Gemini/Drive, Gemini Notebook, scripts, and other bounded workers.
- **Verification/governance plane:** ChatGPT Chat plus HITL/domain professional for source promotion, conflicts, professional judgment, release, and destructive changes.
- **Presentation plane:** Docs, PDFs, Sheets, court/attorney packets, reports, and dashboards built from controlled objects.

## Core efficiency rules

1. **Inventory once; process by delta.** Hash byte-addressable files once, cache deterministic extraction keyed to asset hash, and process NEW/MODIFIED/MOVED/MISSING records after baseline.
2. **Separate content identity from semantic source identity.** Use `ASSET-SHA256-*` for deterministic byte identity and `SRC-######` for the permanent semantic source object.
3. **Progressive disclosure to AI.** Send a Project Capsule, object IDs, and the job's candidate set rather than replaying a full corpus or chat history.
4. **Exception-driven review.** Automation returns deltas, conflicts, gaps, and proposed changes. Human/high-cost AI attention goes to exceptions.
5. **Project Completion Contracts.** Each project defines target outcome and explicit gates; automation selects jobs that close blocking gates instead of continuing open-ended research.
6. **One writer, many reviewers.** One execution platform mutates a shared tree per job. Other models review immutable manifests/snapshots and return proposals.
7. **Live-vs-frozen cloud sources.** Google-native files are mutable. Strict source locks require frozen exports/snapshots with hashes plus parent Drive file/revision metadata.
8. **Policy as code.** Important status transitions should be machine validated.

## Project object

Minimum state:

- `PROJECT_ID`
- `TARGET_OUTCOME`
- `COMPLETION_CONTRACT`
- `STATUS / PHASE`
- `SOURCE_ROOT(S)`
- `CURRENT_SOURCE_FREEZE`
- `CURRENT_CAPSULE`
- `NEXT_ACTION`
- `OPEN_GAPS / CONFLICTS / DECISIONS`
- `VERIFICATION_QUEUE`
- `RELEASE_QUEUE`
- `ACTIVE_WRITER`
- `NEXT_BEST_PLATFORM`
- `LAST_BASELINE_SCAN`
- `LAST_DELTA_SCAN`

## Job object

A job is the atomic unit of automation:

- `JOB_ID`
- `PROJECT_ID / ISSUE_ID`
- `OBJECTIVE`
- `INPUT_REFS`
- `SOURCE_FREEZE_ID`
- `DEPENDENCIES`
- `WRITER_PLATFORM`
- `REVIEWER_PLATFORM`
- `ALLOWED_OPERATIONS`
- `PROHIBITED_OPERATIONS`
- `OUTPUT_SCHEMA`
- `VERIFICATION_GATE`
- `HITL_GATE`
- `STATUS`
- `CHANGE_MANIFEST`

Large vague prompts should be decomposed into bounded jobs.

## Portfolio scheduler

Recommend one next action per active project. Rank using observable factors: external deadline, downstream gates unlocked, source readiness, automation fit, HITL availability, cost of delay, and exception burden. Do not use ungrounded model confidence percentages as completion gates.

## Platform specialization

- **ChatGPT Chat:** verification, reasoning, ambiguity, adversarial review, professional/procedural analysis, governance, promotion/hold/reject.
- **ChatGPT Work:** bounded multi-step execution, connected-app work, artifact generation, scheduled recurring work, supported event-triggered jobs.
- **Claude Cowork:** filesystem/workspace orchestration, large folder audits, migrations, scheduled connector/cloud work.
- **Gemini / Drive:** Google-native discovery, source-set research, citations, Drive Projects, organization suggestions.
- **Gemini Notebook:** bounded source-grounded issue notebooks; use immutable snapshots for strict evidence freezes.
- **Google Docs:** narrative/presentation layer.
- **Google Sheets:** structured registers, calculations, queues, status views, CSV/JSONL staging.
- **GitHub:** generic control-plane versioning, scripts, schemas, tests, and change review. Do not store sensitive evidence in a public control repository.

## Cloud automation pattern

`SCHEDULE/TRIGGER -> CREATE/SELECT JOB -> READ APPROVED CLOUD SOURCES -> RETURN DELTA/EXCEPTIONS -> VERIFY/HITL -> WRITE APPROVED STATE`

Good recurring jobs include portfolio digests, deadline/stale-source queues, unresolved gap/conflict/decision reports, verification-candidate queues, and duplicate/supersession candidate reports.

## Google Drive source control

Record both cloud identity and exact content state:

- `drive_file_id`
- `drive_revision_id / modified_time` where available
- `source_mode`
- `snapshot_export_format`
- `snapshot_sha256`
- `parent_src_id`

Binary files can be hashed after download/sync. Live Docs/Sheets/Slides need snapshot export when immutable historical content matters.

## Token/context optimization

- `PROJECT_CAPSULE.md` replaces replaying chat history.
- JSONL uses one semantic object per line.
- Candidate queues replace whole-corpus review.
- Extraction caches are keyed by asset hash.
- Only exceptions and promotion candidates go to high-cost review.
- Cross-AI handoffs use IDs and explicit return schemas.
- Deep re-audit is triggered by material source/state changes, conflicts, release gates, or migration risk rather than arbitrary turn counts.

## Accuracy / evaluation loop

Measure: unchanged-file skip rate, extraction-cache hit rate, duplicate bytes avoided, source-verified promotion rate, false-promotion reversals, gap aging, conflict closure rate, stale-authority count, exception-free jobs, artifact convergence, percentage of active projects with an explicit next action, and completion-gate closure count.

Maintain small golden regression cases for critical invariants such as hash/dedup, moved-file detection, quote-lock prerequisites, and project COMPLETE prerequisites.

## Rollout

1. Version schemas/scripts in GitHub; keep evidence out of the public repository.
2. Pilot one copied project with baseline inventory/hash/dedup/extraction.
3. Run a genuine source-lock pilot on a small set of native files.
4. Register active projects and create Completion Contracts.
5. Create cloud-scheduled portfolio/deadline/stale-queue jobs.
6. Use Gemini/Notebook for bounded source synthesis, Claude for independent red-team, ChatGPT for verification/governance, and Work/Cowork for approved execution.
7. Process deltas only and regenerate compact project capsules after material state changes.
