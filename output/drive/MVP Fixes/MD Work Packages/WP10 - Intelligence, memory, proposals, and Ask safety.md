---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 10: Intelligence, memory, proposals, and Ask safety"
author: "L. Rhodes (plan owner) - A. Zhao (technical feedback reconciled)"
date: "2026-07-12"
---
# Work Package 10: Intelligence, memory, proposals, and Ask safety

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP10 |
| Plan file | `WP10 - Intelligence, memory, proposals, and Ask safety.md` |
| Proposed PRs | P10-01, P10-02, P10-03, P10-04 |
| Inspection snapshot | 2026-07-12 19:30 America/New_York |

## Purpose and outcome

**Problem.** Private memory, shared case truth, Learn context, and AI proposals have partial contracts but current app code can place IP guide notes into shared memory and provider projections lack provenance enforcement.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Versioned scoped context envelopes, separate private/shared memory revisions, evidence-bound proposal approval, grounded Ask behavior, and cross-service safety evaluation/observability.

**Explicit non-goals.**

- No LLM writes to case truth
- No medical/legal advice
- No silent fallback success
- No final Learn corpus authoring

## Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-014 | verified | app / PR #124@84a5a84 | app/storage/node0.py:42-200,509-600; tests/python/test_node0.py:444-490 | IP/co-IP own candidate reads; GC onboarding writes separate shared/private facts and does not revise the IP assertion. The GC cannot see or correct the IP candidate record. |
| E-015 | verified | app / PR #122@e853821 | app/storage/facts.py:19-69,107-127 | Facts have broad provenance and visibility values but no subject-versus-author role, verification state, derived-from, or supersedes link. |
| E-016 | verified | app / PR #122@e853821 | app/storage/proposals.py:117-142 | Generic proposal approval permits any case member and can pass caller-selected provenance to create_fact; a dedicated evidence/role rail is required before reviewed/provider-confirmed truth. |
| E-017 | verified | app / PR #124@84a5a84 | app/routes/node0.py:686-719 | IP Conversation Guide notes are saved as shared memory and sent to intelligence, creating a future cross-role leakage risk. |
| E-019 | verified protected work | app / dirty feature/provider-exchange-layer-v0@84a5a84 | app/provider_handoffs.py:109-133 and uncommitted handoff modules | The protected provider work is not a PR. Its broad GC-owner fact selection can include private/provisional data, so only selective port after provenance/purpose review is safe. |
| E-020 | verified | intelligence / origin/main@56f6c4b | src/natalyx_intelligence/case_context.py:8-147; docs/agents/case-context.md | The service returns advisory-only proposals and says durable writes are app-owned; this is a useful boundary but the surrounding context provenance remains incomplete. |
| E-021 | verified | intelligence / origin/main@56f6c4b | src/natalyx_intelligence/ask_natalyx.py:34-42,365-378 | Ask accepts known_intake_state without an authorship-class contract and serializes it into model context. |
| E-028 | verified review | app / PR #124 comment 4948149089 | Consolidated review - findings for the WP00 extraction ledger | Alan's completed review classifies #124 as high-value extraction material rather than a merge unit and identifies transaction, privacy, scoring, access, validation, invariant, exposure, retention, performance, CSS and CI findings. |

## Architecture and contracts

- The app owns case truth, authorization, PHI policy, and durable approval; intelligence returns advisory proposals only.
- Every request declares general Learn, private-user, approved-shared-case, or provider-purpose scope; contexts are not merged.
- Failures degrade explicitly with source/boundary notices and no fabricated case answer.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`, `intelligence`; repository-specific PRs remain separate. |
| Entities/state | No new runtime entity; evidence/coordination only. |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Versioned context/advisory contract with strict validation and safe compatibility window. Responses carry source, scope, policy, safety and degraded-mode metadata. |
| Storage | Revision/supersedes/provenance/evidence fields and the private-note remediation under versioned migrations. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

### Data authorship/provenance rules

- Every assertion/revision records subject_ref, semantic_key, author_subject/person/role, authorship_class, provenance, verification_status, visibility, purpose, source_ref, derived_from, supersedes_id, promotion_event_id, policy version and immutable timestamps.
- Class 1 defaults IP-private; class 2 defaults IP-private/internal and visibly says reported by the intended parent, not confirmed by the GC.
- Class 3 is GC-authored and shared only per field/purpose; class 4 is GC-only private; class 5 requires an evidence-linked role-gated reviewer/provider rail.
- GC confirmation appends a class-3 revision referencing the class-2 assertion. Relationship answers can coexist; disagreement is not an overwrite.
- Unselected candidates, raw health assertions, ranking scores and private IP notes do not promote. Derived values inherit the weakest source status.
- Copying, promotion, generic proposal approval, IP assertion or AI inference can never create Natalyx-reviewed, provider-confirmed, medically cleared, legally cleared or insurance-verified truth.

## Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Local preparation | Merge readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P10-01 | Version the scoped intelligence context envelope | intelligence | P01-01, P04-02 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P01-01, P04-02; technical decisions/controls D-AI-01; Gate A0 active and verified; Luke review/final founder approval |
| 2 | P10-02 | Enforce private/shared memory and evidence-bound proposal approval | app | P04-02, P10-01 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P04-02, P10-01; technical decisions/controls D-AI-01; Gate A0 active and verified; Luke review/final founder approval |
| 3 | P10-03 | Harden Ask and Learn grounding and degraded-mode behavior | intelligence | P10-01, P11-02 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P10-01, P11-02; technical decisions/controls D-AI-01; Gate A0 active and verified; Luke review/final founder approval |
| 4 | P10-04 | Add intelligence safety evaluations and cross-service observability | intelligence | P10-02, P10-03 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P10-02, P10-03; Gate A0 active and verified; Luke review/final founder approval |

### P10-01 - Version the scoped intelligence context envelope

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size | A2 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P01-01, P04-02; technical decisions/controls D-AI-01; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Dependencies | P01-01, P04-02 |
| Blocking decisions/checkpoints | D-AI-01 |
| Source / salvage | Current case_context advisory stub |

#### Objective

Define and validate versioned request/response envelopes that keep general Learn, private-user memory, approved shared-case facts, and provider-purpose context distinct.

#### Scope

- Explicit scope and audience
- Source/provenance/verification metadata
- Policy/model/version and redacted trace metadata

#### Explicit non-goals

- No durable app write
- No merged contexts

#### Expected files or modules

- `src/natalyx_intelligence/contracts/context.py`
- `src/natalyx_intelligence/case_context.py`
- `docs/agents/case-context.md`
- `tests/test_context_contract.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Versioned context/advisory contract with strict validation and safe compatibility window. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Cross-scope rejection
- unknown version
- private/shared fixtures
- redaction
- service auth

Local validation:

- `uv run pytest`
- Run focused contract/migration/safety tests with redacted fixtures.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P01-01, P04-02. Parallel opportunities: P10-04

#### Objective acceptance criteria

- [ ] Define and validate versioned request/response envelopes that keep general Learn, private-user memory, approved shared-case facts, and provider-purpose context distinct.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | FastAPI/Pydantic, AI safety, privacy |
| Higher-capability review | Mandatory before merge |

### P10-02 - Enforce private/shared memory and evidence-bound proposal approval

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size | A2 / Exceptional |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P04-02, P10-01; technical decisions/controls D-AI-01; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Dependencies | P04-02, P10-01 |
| Blocking decisions/checkpoints | D-AI-01 |
| Source / salvage | Current facts/memory/proposals scaffolds, GC authorship audit |

#### Objective

Store attributable private/shared memory revisions and require authorized evidence review before an intelligence proposal can affect case truth or provider material.

#### Scope

- Private and shared memory ledgers
- Affected-row inventory for source=node0_conversation_guide_note
- Immediate shared/intelligence exclusion plus idempotent person-owner quarantine/private remediation when rows exist
- Proposal preview/approve/reject
- Evidence/source and reviewer authority
- Audit/outbox

#### Explicit non-goals

- No automatic AI approval
- No guide notes default shared

#### Expected files or modules

- `app/case_intelligence.py`
- `app/storage/memory.py`
- `app/storage/proposals.py`
- `app/storage/facts.py`
- `tests/python/test_case_intelligence.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Revision/supersedes/provenance/evidence fields and the private-note remediation under versioned migrations. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Role and purpose authorization on every projection/write; ambiguous legacy ownership quarantines rather than broadens access. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Zero-row inventory evidence
- affected rows disappear from shared/Ask reads before remediation
- idempotent owner-safe migration
- ambiguous-owner quarantine
- no note content in logs
- private-to-shared denial
- wrong-role approval
- AI provenance remains proposal
- concurrent review
- provider projection

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P04-02, P10-01. Parallel opportunities: P10-03

#### Objective acceptance criteria

- [ ] Store attributable private/shared memory revisions and require authorized evidence review before an intelligence proposal can affect case truth or provider material.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | AI safety, authorization, data provenance |
| Higher-capability review | Mandatory before merge |

### P10-03 - Harden Ask and Learn grounding and degraded-mode behavior

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size | A2 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P10-01, P11-02; technical decisions/controls D-AI-01; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Dependencies | P10-01, P11-02 |
| Blocking decisions/checkpoints | D-AI-01 |
| Source / salvage | Current ask_natalyx.py and PR #124 Ask integration |

#### Objective

Answer from the declared scope with approved sources/citations and explicit boundary/failure notices; never fabricate case context or silently fall across scope.

#### Scope

- Approved resource resolution
- Scope-specific prompt/context
- Timeout/unavailable/empty-source behavior
- Citation validation

#### Explicit non-goals

- No medical/legal advice
- No unapproved corpus fallback

#### Expected files or modules

- `src/natalyx_intelligence/ask_natalyx.py`
- `src/natalyx_intelligence/learn_resources.py`
- `tests/test_ask_natalyx.py`
- `docs/agents/ask-natalyx.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Responses carry source, scope, policy, safety and degraded-mode metadata. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Empty/unapproved corpus
- service/provider timeout
- case question without case scope
- citation mismatch
- safety escalation

Local validation:

- `uv run pytest`
- Run focused contract/migration/safety tests with redacted fixtures.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P10-01, P11-02. Parallel opportunities: P10-02

#### Objective acceptance criteria

- [ ] Answer from the declared scope with approved sources/citations and explicit boundary/failure notices; never fabricate case context or silently fall across scope.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | LLM orchestration, retrieval/citations, safety evaluation |
| Higher-capability review | Mandatory before merge |

### P10-04 - Add intelligence safety evaluations and cross-service observability

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size | A2 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P10-02, P10-03; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P10-02, P10-03 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Current intelligence auth/telemetry tests |

#### Objective

Add deterministic safety/grounding evaluations, correlation IDs, latency/failure metrics, and redacted traces across app-intelligence calls.

#### Scope

- Leakage/hallucination/fallback evals
- Correlation and contract version
- Safe logs and alarms

#### Explicit non-goals

- No prompt or participant payload in logs
- No PHI readiness claim

#### Expected files or modules

- `tests/evals/`
- `src/natalyx_intelligence/telemetry.py`
- `docs/runbooks/intelligence.md`
- `app/intelligence_auth.py (consumer follow-up PR if needed)`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- PII/PHI redaction fixtures
- correlation continuity
- failure classification
- model fallback
- eval threshold

Local validation:

- `uv run pytest`
- Run focused contract/migration/safety tests with redacted fixtures.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Metrics and redacted structured events; app-side consumer change must remain a separate coordinated PR if repository boundaries require it.

#### Rollout

Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P10-02, P10-03. Parallel opportunities: P10-01

#### Objective acceptance criteria

- [ ] Add deterministic safety/grounding evaluations, correlation IDs, latency/failure metrics, and redacted traces across app-intelligence calls.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | AI evaluation, observability, privacy |
| Higher-capability review | Mandatory before merge |

## Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |
| `intelligence` | advisory inference, scoped response/citation contract; no case truth |

Merge order inside this package: `P10-01` → `P10-02` → `P10-03` → `P10-04`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Scope isolation; Proposal approval/rejection; Citation/source validity; Unavailable service; Prompt/context leakage; Trace redaction | Expected state/event/UI and named evidence are produced once. |
| Authorization failure | Wrong/no subject, role, membership, purpose or consent | 403/404 as appropriate; no write or data leak; audit safe failure. |
| Role differences | Separate IP, GC, operator, provider/service identities | Only the approved lens/projection/actions appear. |
| Retries/duplicates | Repeat same canonical request/event | Original result returned; no duplicate membership/case/invoice/document/event. |
| Concurrency | Two writers/claimants/migrators/workers | One valid transition; loser receives deterministic stale/conflict response. |
| Stale state | Old revision/config/terms/token/artifact | Fail closed or approved compatibility behavior; never silent coercion. |
| Malformed input | Boundary, encoding, size, enum, redirect and identifier corpus | Validation before side effects; safe error. |
| Unavailable dependency | Database, intelligence, processor, S3/scanner or auth unavailable | Explicit degraded/blocked behavior; no hallucinated success. |
| Partial failure | Crash between external effect, DB transaction and outbox | Retry/forward repair converges from durable evidence. |
| Logout/login/resume | Session expires/restarts mid-flow | Return to authorized current state; no query/link authority. |
| Mobile/accessibility | 320/375/768 widths, keyboard, focus, reduced motion | Core task completes with truthful state and no clipped controls. |
| Synthetic cloud | Known dev revision and synthetic identities/data | Gate artifact records SHA, dependency status, audit and cleanup. |
| Audit/observability | Inspect events/metrics/logs | Versions, actor/authority, correlation and reason present; no sensitive payload. |

## Risks and decisions

Founder outcomes, Alan's remaining technical ownership and external activation dependencies are recorded separately so a final policy is never mistaken for an active control.

| ID | Status | Classification | Remaining owner | Affected / latest | Programme effect |
| --- | --- | --- | --- | --- | --- |
| D-DATA-01 | Founder decision final; implementation evidence pending | Luke decides product/privacy outcome | Alan - implementation | P04-02, P06-02, P06-03, P07-03, P07-04, P09-05, P10-01, P10-02; Before P04-02 | Founder ambiguity is removed across WP04, WP06, WP07, WP09 and WP10; A1 still requires the technical denial evidence. |
| D-AI-01 | Founder scope/cost final; Alan later; PHI externally gated | Luke sets scope and cost; Alan decides implementation later | Alan - later before P10-01 | P10-01, P10-02, P10-03, P12-01; Before P10-01 | P10/P12 synthetic planning may proceed; implementation completion waits for Alan's technical decision and PHI remains blocked through B2. |

### D-DATA-01 - IP-GC field projection allowlist

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final |
| Founder outcome | Use need-to-know sharing. Shared journey status and agreed relationship/outreach/logistics may cross roles; private IP notes, unconfirmed assertions and GC medical, reproductive, insurance, identity or wellbeing answers do not cross automatically. Provider packets require preview, consent and appropriate verification. |
| Founder constraints | Default-deny field-and-purpose allowlists; Source-labelled corrections; Named-purpose provider projection only |
| What remains for Alan | Define explicit field/purpose allowlists in code and projection contracts; Implement cross-role and provider negative tests |
| Evidence required | Cross-role denial matrix; Provider projection allowlist tests; Correction/source-label evidence |
| Approval rule | Luke approval is required for a broader sharing policy, not for compliant implementation detail. |
| External dependencies | None |
| Affected PRs / latest point | P04-02, P06-02, P06-03, P07-03, P07-04, P09-05, P10-01, P10-02; Before P04-02 |
| Programme effect | Founder ambiguity is removed across WP04, WP06, WP07, WP09 and WP10; A1 still requires the technical denial evidence. |
| Independent recommendation | Default deny; expose only explicit purpose-limited projections. Class 1/2 and class 4 never automatically cross roles. |

### D-AI-01 - Intelligence context and approval authority matrix

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final founder policy; PHI externally dependent |
| Founder outcome | AI is bounded and advisory: role-scoped education, retrieval, summaries, question drafts, next steps and provider preparation using approved Learn and authorized source-labelled context. It never diagnoses, ranks, approves, clears or writes durable truth; authorized human approval precedes memory, case or provider material. |
| Founder constraints | Deterministic or curated fallback; $10 per active case/month and $100 total beta/month ceilings with alerts and graceful fallback; No PHI before B2 |
| What remains for Alan | Choose Bedrock model, prompts, retrieval, schemas, fallback, human-review rails and cost controls |
| Evidence required | Scope/authority negative tests; Fallback and malformed-response tests; Safety and cost evidence |
| Approval rule | Luke approves broader AI authority, higher cost or any PHI use; B2 external approval is mandatory for PHI. |
| External dependencies | B2 external security/privacy/compliance approval before PHI |
| Affected PRs / latest point | P10-01, P10-02, P10-03, P12-01; Before P10-01 |
| Programme effect | P10/P12 synthetic planning may proceed; implementation completion waits for Alan's technical decision and PHI remains blocked through B2. |
| Independent recommendation | Generic case members cannot create reviewed/provider truth; intelligence remains advisory and scope explicit. |

| Implementation risk | Owner | Treatment |
| --- | --- | --- |
| Private-to-shared leakage | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Hallucinated truth | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Sensitive logs | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Contract version drift | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P10-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P10-02 | Selective-port behavior and tests; supersede as programme architecture | Complete at e853821: authoritative behavior/tests and selectively portable implementation are classified; superseded architecture and evidence-only claims are named. |
| app#124 | 84a5a847fea7 | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. | P10-02 | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. |
| main (behind origin/main) | 9d824e8 | dirty Learn registry/corpus plus uv.lock | P11-02/P10-03 as appropriate | Selective port from protected worktree | Do not pull/reset/stash; extract in isolated worktree later. |

Package source inventory:

- Intelligence case_context advisory stub
- App proposal/fact/memory scaffolds
- Protected intelligence Learn corpus changes

## Ownership recommendation

Alan implements service/app contracts; Luke approves truth/privacy policy. Higher-capability, security/privacy, and clinical/legal safety review required.

| PR | WP DRI | Primary implementer | Technical-decision owner | Reviewer | Final approver | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| P10-01 | Alan | Alan (proposed) | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism | Luke | Luke | None |
| P10-02 | Alan | Alan (proposed) | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism | Luke | Luke | None |
| P10-03 | Alan | Alan (proposed) | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism | Luke | Luke | None |
| P10-04 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |

PR ownership inherits the proposed work-package split pending Alan's review. Named technical-decision ownership remains separate and never transfers implementation ownership across work packages; reciprocal and external review requirements remain intact.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
