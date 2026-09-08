# Iteration 2 Review Delta — v0.1.2

Status: proposed controlling patch within the existing corpus-reconcile lineage. This document does not create a second census engine or release mutation authority.

## Review method

Two external AI-generated analyses were treated as DERIVATIVE_REVIEW_INPUTS. Agreement with prior AI output is not corroboration. Only source-backed or implementation-tested deltas are promoted; time-sensitive legal, product, pricing, plan, and quota assertions remain separately verifiable.

## ADOPT

1. **One implementation lineage.** GitHub remains the canonical generic implementation. AI systems may critique or propose patches but do not independently create competing census engines.
2. **Full census before sampling.** G0 protection and a full-root READ_ONLY census precede the deterministic stratified 25–50 object Source Set.
3. **Fixity binds derived metadata to the same byte observation.** EML parsing and ZIP member manifests must be computed from the exact guarded byte stream whose SHA-256 is recorded. A second file read cannot silently become the basis for metadata or member hashes.
4. **Provider metadata is an adapter layer.** Drive file IDs, versions/revisions, stored-binary checksums, activity records, and app properties may strengthen object identity/provenance, but they do not replace the canonical corpus schema or user authorization controls.
5. **Near-duplicate results are advisory.** Similarity, fuzzy-name, OCR-text, or perceptual matches may create investigation candidates only; they never create deletion, canonical-survivor, or mutation authority.
6. **AI-generated legal drafts require a separate release gate.** An AI draft may be produced only into a review/staging destination and remains unreviewed/not-for-filing until human release controls are satisfied. This is an orchestration/release status, not a G0 ProtectionClass.

## ADOPT WITH MODIFICATION

1. **Apps Script:** use as a bounded Drive/Gmail metadata, checksum, checkpointing, and orchestration adapter when useful. Do not make Apps Script a competing SSOT or canonical reconciliation engine.
2. **Copy-before-reorganization:** mandatory for immutable/native source preservation when a derivative working copy is required. It is not a blanket instruction to create duplicate copies of every object. Eligible MUTABLE_WORK_PRODUCT/DERIVATIVE rename or move remains separately gated by G0–G5 and parent HITL.
3. **External dedupe/e-discovery tools:** if ever used, classify their output as TOOL_CROSSCHECK or formal collection/production support as applicable. Another tool agreeing with SHA-256 groups does not constitute evidentiary corroboration.
4. **Google-native exports:** export SHA-256 is timestamp/format-bound fixity for the export, never NATIVE_RAW_SHA256 for the live Google-native object. Creating preserved exports is a separate collection/release decision and is not part of the READ_ONLY census.
5. **Email identity:** retain Gmail provider message ID and RFC Message-ID as separate fields. Raw EML SHA-256 identifies the captured byte stream; no single provider/message identifier substitutes for all three layers.

## PARK

- Third-party duplicate-cleaner procurement or installation.
- E-discovery platform migration absent an actual production/discovery/authenticity trigger.
- ssdeep/TLSH/OCR/perceptual near-duplicate engine until census evidence shows enough unresolved near-duplicate volume to justify it.
- Automatic freezing/export of all Google-native objects during the census.
- Vendor-specific overnight drafting architecture as a corpus-reconcile dependency.

## VERIFY BEFORE ADOPTION

Time-sensitive legal rules, pending legislation, vendor plan limits, pricing, scheduling behavior, compliance/audit coverage, and product feature claims must be checked against current primary sources at the point they materially affect a decision. They are not embedded as corpus-engine invariants merely because an AI analysis reported them.

## AI draft release state — orchestration layer

Recommended fail-closed progression for AI-generated legal work product:

`AI_GENERATED_UNREVIEWED -> SOURCE_RECONCILED -> CITATIONS_VERIFIED -> FIGURES_VERIFIED -> ATTORNEY_REVIEWED -> RELEASE_ELIGIBLE`

Any unresolved source conflict, citation defect, material figure mismatch, or required attorney review blocks progression. No state in this sequence authorizes filing, service, sending, or external publication by itself.

## v0.1.2 implementation delta

- Added guarded single-byte-stream reads for parsers that derive child metadata from a container file.
- EML headers, attachment hashes, and raw MIME SHA-256 now derive from one stable guarded observation.
- ZIP member hashes and ZIP container SHA-256 now derive from one stable guarded observation.
- Added regression tests for the EML and ZIP single-stream invariants.
- Mutation authority remains unchanged: no DELETE, overwrite, permission change, source-byte alteration, or uncontrolled corpus write is released.
