---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 10: Intelligence, memory, proposals, and Ask safety"
author: "L. Rhodes (plan owner) - A. Zhao (technical review requested)"
date: "2026-07-10"
---
# Work Package 10: Intelligence, memory, proposals, and Ask safety

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP10 |
| Plan file | `WP10 - Intelligence, memory, proposals, and Ask safety.md` |
| Proposed PRs | P10-01, P10-02, P10-03, P10-04 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

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
| Storage | Revision/supersedes/provenance/evidence fields under migrations. |
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

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P10-01 | Version the scoped intelligence context envelope | intelligence | P01-01, P04-02 | A2 | Large | Dependencies unmet |
| 2 | P10-02 | Enforce private/shared memory and evidence-bound proposal approval | app | P04-02, P10-01 | A2 | Exceptional | Dependencies unmet |
| 3 | P10-03 | Harden Ask and Learn grounding and degraded-mode behavior | intelligence | P10-01, P11-02 | A2 | Large | Dependencies unmet |
| 4 | P10-04 | Add intelligence safety evaluations and cross-service observability | intelligence | P10-02, P10-03 | A2 | Large | Dependencies unmet |

### P10-01 - Version the scoped intelligence context envelope

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P01-01, P04-02 |
| Blocking decisions/checkpoints | D-DATA-01, D-AI-01 |
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
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | FastAPI/Pydantic, AI safety, privacy |
| Higher-capability review | Mandatory before merge |

### P10-02 - Enforce private/shared memory and evidence-bound proposal approval

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P04-02, P10-01 |
| Blocking decisions/checkpoints | D-DATA-01, D-AI-01 |
| Source / salvage | Current facts/memory/proposals scaffolds, GC authorship audit |

#### Objective

Store attributable private/shared memory revisions and require authorized evidence review before an intelligence proposal can affect case truth or provider material.

#### Scope

- Private and shared memory ledgers
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
| Schema/model | Revision/supersedes/provenance/evidence fields under migrations. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Role and purpose authorization on every projection/write. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Private-to-shared denial
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
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | AI safety, authorization, data provenance |
| Higher-capability review | Mandatory before merge |

### P10-03 - Harden Ask and Learn grounding and degraded-mode behavior

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
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
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | LLM orchestration, retrieval/citations, safety evaluation |
| Higher-capability review | Mandatory before merge |

### P10-04 - Add intelligence safety evaluations and cross-service observability

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
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
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
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

| Type | ID / risk | Owner | Affected PRs / latest point | Treatment |
| --- | --- | --- | --- | --- |
| Blocking/product/compliance decision | D-DATA-01 - Which provisional IP assertions may the GC see, which GC answers may the IP see, and which fields survive promotion/provider projection? | Luke | P04-02, P06-02, P06-03, P07-03, P07-04, P09-05, P10-01, P10-02; Before P04-02 | D-DATA-01 - Default deny; expose only explicit purpose-limited projections. Class 1/2 and class 4 never automatically cross roles. |
| Blocking/product/compliance decision | D-AI-01 - Approve scopes, allowed sources, model policy, proposal reviewers, class-5 evidence rail and degraded-mode copy. | Luke | P10-01, P10-02, P10-03, P12-01; Before P10-01 | D-AI-01 - Generic case members cannot create reviewed/provider truth; intelligence remains advisory and scope explicit. |
| Implementation risk | Private-to-shared leakage | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Hallucinated truth | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Sensitive logs | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Contract version drift | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P10-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P10-02 | Retain pending Alan reconciliation; selective port or rebase only after architecture approval | Reinspected at latest head. It is exactly e853821 (no newer delta); retention strengthened, but final extraction waits for Alan checkpoint. |
| app#124 | 84a5a847fea7 | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. | P10-02 | Retain unchanged as evidence; selective port/rewrite after checkpoint | Unextracted; Alan review explicitly incomplete and unresolved. |
| main (behind origin/main) | 9d824e8 | dirty Learn registry/corpus plus uv.lock | P11-02/P10-03 as appropriate | Selective port from protected worktree | Do not pull/reset/stash; extract in isolated worktree later. |

Package source inventory:

- Intelligence case_context advisory stub
- App proposal/fact/memory scaffolds
- Protected intelligence Learn corpus changes

## Ownership recommendation

Alan implements service/app contracts; Luke approves truth/privacy policy. Higher-capability, security/privacy, and clinical/legal safety review required.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P10-01 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P10-02 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P10-03 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P10-04 | Alan | Alan (proposed) | Luke | Luke | Mandatory |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
