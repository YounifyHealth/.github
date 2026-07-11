---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 06: Node 0 Complete and GC soft onboarding"
author: "L. Rhodes (plan owner) - A. Zhao (technical review requested)"
date: "2026-07-10"
---
# Work Package 06: Node 0 Complete and GC soft onboarding

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP06 |
| Plan file | `WP06 - Node 0 Complete and GC soft onboarding.md` |
| Proposed PRs | P06-01, P06-02, P06-03 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

## Purpose and outcome

**Problem.** Optional paid depth, GC soft onboarding, and readiness reporting need clear entitlement gates without creating a managed case or treating IP assertions as GC answers.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Versioned Node 0 Complete entitlement, authenticated low-risk GC onboarding, attributable GC confirmation/replacement, and a readiness report that remains preliminary.

**Explicit non-goals.**

- No managed case activation
- No provider access
- No medical/legal clearance
- No hard-coded price

## Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-010 | verified | app / PR #124@84a5a84 | app/routes/node0.py:63-90 | Opening Node 0 calls create_byos_case_for_ip with is_synthetic=True; there is no separate free workspace or authorized promotion. |
| E-011 | verified | app / PR #124@84a5a84 | app/storage/node0.py:400-462; app/routes/node0.py:605-652 | Node 0 can issue an unaddressed GC invitation and redemption ultimately creates case membership, conflating low-risk onboarding possession with case access. |
| E-013 | verified | app / PR #124@84a5a84 | app/node0.py:252-482,622-878,975-1001 | Nineteen IP-entered candidate answers about relationship and third-party circumstances/health derive a 0-100 score, readiness/status, ordering, guide route and evidence packet without per-field provenance or verification. |
| E-014 | verified | app / PR #124@84a5a84 | app/storage/node0.py:42-200,509-600; tests/python/test_node0.py:444-490 | IP/co-IP own candidate reads; GC onboarding writes separate shared/private facts and does not revise the IP assertion. The GC cannot see or correct the IP candidate record. |

## Architecture and contracts

- Node 0 Complete is a flat configurable entitlement fully creditable against the JMF.
- GC confirmation appends an attributable revision; it never silently overwrites the IP source.
- GC-private answers stay private; only explicit purpose-limited projections reach the IP.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`; repository-specific PRs remain separate. |
| Entities/state | `node0_workspace`, `workspace_claim`, `workspace_entitlement` |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Read-only readiness projection with policy version. |
| Storage | Append-only entitlement events plus current projection. Use assertion/revision contract; onboarding progress events. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

### Applicable state machines

### Node 0 workspace (`node0_workspace`)

Owner: **natalyx-app**. States: `draft`, `active`, `match_ready`, `promotion_pending`, `promoted`, `archived`.

**Transition: `none` -> `draft`**

- **Actor:** authenticated IP
- **Evidence:** first explicit Node 0 start
- **Idempotency key:** `workspace:{owner}:create`
- **Invalid transitions:** Existing active workspace returns existing
- **Audit event:** `workspace_created`
- **Retry:** Unique owner/idempotency key
- **Recovery:** Forward repair orphan membership

**Transition: `draft` -> `active`**

- **Actor:** IP
- **Evidence:** minimum workspace consent/profile
- **Idempotency key:** `workspace:{id}:activate:{revision}`
- **Invalid transitions:** Missing consent/owner
- **Audit event:** `workspace_activated`
- **Retry:** Return current active revision
- **Recovery:** Correct inputs and retry

**Transition: `active` -> `match_ready`**

- **Actor:** IP + selected GC evidence policy
- **Evidence:** selected candidate + required provisional/GC-authored fields
- **Idempotency key:** `workspace:{id}:ready:{revision}`
- **Invalid transitions:** Critical unknown/decline/revoked claim
- **Audit event:** `workspace_match_ready`
- **Retry:** No duplicate event
- **Recovery:** Reopen active with reason revision

**Transition: `match_ready` -> `promotion_pending`**

- **Actor:** promotion event consumer
- **Evidence:** valid byos.workspace_promotion_authorized.v1
- **Idempotency key:** `promotion:{commitment}:v1`
- **Invalid transitions:** No authorization; already promoted; stale config
- **Audit event:** `workspace_promotion_requested`
- **Retry:** Replay resumes/finds same promotion
- **Recovery:** Forward-repair incomplete transaction

**Transition: `promotion_pending` -> `promoted`**

- **Actor:** promotion service
- **Evidence:** paid case + manifest committed
- **Idempotency key:** `promotion:{commitment}:v1`
- **Invalid transitions:** Projection invariant/privacy failure
- **Audit event:** `workspace_promoted`
- **Retry:** Return same case ID
- **Recovery:** Repair from immutable manifest; never duplicate

**Transition: `draft|active|match_ready` -> `archived`**

- **Actor:** IP/operator per policy
- **Evidence:** explicit archive + retention policy
- **Idempotency key:** `workspace:{id}:archive:{request}`
- **Invalid transitions:** Promotion pending/promoted
- **Audit event:** `workspace_archived`
- **Retry:** Idempotent
- **Recovery:** Restore only through new audited revision if policy permits


### Entitlement (`workspace_entitlement`)

Owner: **natalyx-app commercial domain**. States: `free`, `complete_pending`, `complete_active`, `suspended`, `revoked`.

**Transition: `none` -> `free`**

- **Actor:** system
- **Evidence:** active Node 0 workspace
- **Idempotency key:** `entitlement:{workspace}:free`
- **Invalid transitions:** No workspace
- **Audit event:** `entitlement_granted`
- **Retry:** Return current
- **Recovery:** Repair projection from event

**Transition: `free` -> `complete_pending`**

- **Actor:** IP/commercial service
- **Evidence:** accepted Complete offer/config
- **Idempotency key:** `entitlement:{workspace}:{commitment}`
- **Invalid transitions:** Unknown price/config/terms
- **Audit event:** `complete_requested`
- **Retry:** Return pending
- **Recovery:** Cancel/expire commitment

**Transition: `complete_pending` -> `complete_active`**

- **Actor:** payment domain
- **Evidence:** settled Complete ledger entry
- **Idempotency key:** `entitlement:{payment}:activate`
- **Invalid transitions:** Amount/currency/config mismatch
- **Audit event:** `complete_activated`
- **Retry:** Replay no-op
- **Recovery:** Reconcile and retry from inbox

**Transition: `complete_active` -> `suspended`**

- **Actor:** authorized commercial policy
- **Evidence:** refund/reversal or approved pause reason
- **Idempotency key:** `entitlement:{id}:suspend:{event}`
- **Invalid transitions:** Cannot remove free/safety capability
- **Audit event:** `entitlement_suspended`
- **Retry:** No-op if same event
- **Recovery:** Reinstate or revoke through new event

**Transition: `complete_active|suspended` -> `revoked`**

- **Actor:** authorized operator/policy
- **Evidence:** fraud/refund/terms revocation evidence
- **Idempotency key:** `entitlement:{id}:revoke:{event}`
- **Invalid transitions:** No silent case cancellation
- **Audit event:** `entitlement_revoked`
- **Retry:** Idempotent
- **Recovery:** Manual reviewed regrant creates new entitlement event


### Low-risk workspace identity claim (`workspace_claim`)

Owner: **natalyx-app**. States: `issued`, `pending_identity`, `identity_bound`, `consented`, `claimed`, `mismatch_pending`, `revoked`, `expired`.

**Transition: `none` -> `issued`**

- **Actor:** workspace IP
- **Evidence:** selected candidate + allowed claim scope
- **Idempotency key:** `claim:{workspace}:{candidate}:{generation}`
- **Invalid transitions:** Existing live claim superseded
- **Audit event:** `workspace_claim_issued`
- **Retry:** Return current token only at issuance
- **Recovery:** Issue new generation; old revoked

**Transition: `issued` -> `pending_identity`**

- **Actor:** link holder
- **Evidence:** valid token landing
- **Idempotency key:** `claim:{id}:land`
- **Invalid transitions:** Expired/revoked token
- **Audit event:** `claim_opened`
- **Retry:** Safe repeat
- **Recovery:** Authenticate or exit; no data grant

**Transition: `pending_identity` -> `identity_bound|mismatch_pending`**

- **Actor:** auth provider
- **Evidence:** verified subject/email and binding policy
- **Idempotency key:** `claim:{id}:bind:{subject}`
- **Invalid transitions:** Already claimed/different subject
- **Audit event:** `claim_identity_bound|claim_mismatch`
- **Retry:** CAS no-op or mismatch state
- **Recovery:** Issuer review/new claim

**Transition: `identity_bound` -> `consented`**

- **Actor:** GC claimant
- **Evidence:** workspace consent version
- **Idempotency key:** `claim:{id}:consent:{version}`
- **Invalid transitions:** Stale/missing consent
- **Audit event:** `claim_consented`
- **Retry:** Idempotent
- **Recovery:** Display current consent

**Transition: `consented` -> `claimed`**

- **Actor:** claim service
- **Evidence:** authorized low-risk workspace membership transaction
- **Idempotency key:** `claim:{id}:complete`
- **Invalid transitions:** Case membership requested or conflicting claimant
- **Audit event:** `workspace_claimed`
- **Retry:** Return same membership
- **Recovery:** Transaction rollback/forward repair

**Transition: `issued|pending_identity|identity_bound|consented|mismatch_pending` -> `revoked|expired`**

- **Actor:** issuer/system
- **Evidence:** revocation or TTL
- **Idempotency key:** `claim:{id}:terminal:{event}`
- **Invalid transitions:** No terminal overwrite
- **Audit event:** `claim_revoked|claim_expired`
- **Retry:** Idempotent
- **Recovery:** Fresh claim only


### Invitation and identity safety

Retain from updated PR #122:

- hashed tokens
- purpose-specific TTL with a 14-day ceiling
- CAS terminal transitions
- atomic membership creation
- one-live-GC constraint
- self/existing-member refusal
- safe return_to
- portable integrity/concurrency tests

Required replacement contract:

- Exactly one target: workspace_id or case_id; include purpose, role, access_class, recipient_binding_mode and policy version.
- Email-less possession may only open pending low-risk workspace claim; it cannot reveal sensitive data or grant paid-case membership.
- Paid-case invitation is addressed, authenticated, consented and atomically redeemed; mismatch requires explicit policy/issuer handling and preferably fresh bound token.
- Cognito admission and app membership are separate decisions; account creation never equals workspace/case access.
- Verified identity comes from auth claims, not form-entered email; duplicate claims return the original result.
- Never put raw token/email/PHI in general participant timeline payloads; revoke/expire/supersede fail closed.
- Remove generic unconditional status mutation; expose authorized transition commands only.

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
| 1 | P06-01 | Add Node 0 Complete entitlement and versioned feature gates | app | P04-01, P07-01, P08-01 | A2 | Large | Dependencies unmet |
| 2 | P06-02 | Add GC soft onboarding and attributable confirmation | app | P03-02, P04-02, P06-01 | A2 | Exceptional | Dependencies unmet |
| 3 | P06-03 | Add readiness report and role-scoped progress surfaces | app | P06-02, P10-02, P11-04 | A2 | Large | Dependencies unmet |

### P06-01 - Add Node 0 Complete entitlement and versioned feature gates

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P04-01, P07-01, P08-01 |
| Blocking decisions/checkpoints | D-COM-01 |
| Source / salvage | Business-model Node 0 feature table |

#### Objective

Model optional Complete access independently from workspace and case, pin the commercial configuration, and expose server-side gates for the approved paid-depth features.

#### Scope

- Grant/suspend/revoke entitlement events
- Commercial-version and payment evidence reference
- Credit accrual link

#### Explicit non-goals

- No hard-coded price
- No paid-case creation

#### Expected files or modules

- `migrations/versions/*_entitlements.py`
- `app/domain/entitlements.py`
- `app/storage/entitlements.py`
- `tests/python/test_entitlements.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Append-only entitlement events plus current projection. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Every Complete feature checks server entitlement. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Grant replay
- suspend/revoke
- config version
- free-feature unaffected
- no case created

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

Hard dependencies: P04-01, P07-01, P08-01. Parallel opportunities: P06-03

#### Objective acceptance criteria

- [ ] Model optional Complete access independently from workspace and case, pin the commercial configuration, and expose server-side gates for the approved paid-depth features.
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
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

### P06-02 - Add GC soft onboarding and attributable confirmation

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P03-02, P04-02, P06-01 |
| Blocking decisions/checkpoints | D-DATA-01, D-DATA-02, CHECK-ALAN-122-124 |
| Source / salvage | PRs #123/#124 UX only, GC authorship audit |

#### Objective

Let an authenticated GC claim low-risk workspace access, provide GC-owned answers, confirm/replace selected provisional facts, and preserve private boundaries.

#### Scope

- GC-authored profile/intake revisions
- Field-by-field confirmation/replacement
- Purpose-limited IP progress projection

#### Explicit non-goals

- No paid-case membership
- No provider share
- No medical eligibility determination

#### Expected files or modules

- `app/routes/gc_workspace.py`
- `app/storage/gc_onboarding.py`
- `app/templates/node0/gc_onboarding*.html`
- `tests/python/test_gc_soft_onboarding.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Use assertion/revision contract; onboarding progress events. |
| API/routes | No public API/route contract change. |
| UI/product surface | GC consent and privacy explanations. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Paired IP/GC visibility
- private contact/health fields
- revision lineage
- claim replay/mismatch
- mobile resume

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

Hard dependencies: P03-02, P04-02, P06-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Let an authenticated GC claim low-risk workspace access, provide GC-owned answers, confirm/replace selected provisional facts, and preserve private boundaries.
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
| Required expertise | privacy, accessible forms, authorization |
| Higher-capability review | Mandatory before merge |

### P06-03 - Add readiness report and role-scoped progress surfaces

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P06-02, P10-02, P11-04 |
| Blocking decisions/checkpoints | D-DATA-01 |
| Source / salvage | PR #124 score/report concepts |

#### Objective

Produce a preliminary, source-labelled Node 0 readiness report and separate IP/GC progress views without overclaiming clearance or exposing private answers.

#### Scope

- Source/verification labels
- IP and GC lenses
- Promotion-ready projection manifest

#### Explicit non-goals

- No provider-confirmed status
- No final case activation

#### Expected files or modules

- `app/domain/node0_readiness.py`
- `app/templates/node0/readiness*.html`
- `app/node0_surface.py`
- `tests/python/test_node0_readiness.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Read-only readiness projection with policy version. |
| UI/product surface | Role-specific report/progress cards. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Provisional labels
- critical missing data
- cross-role redaction
- stale revision
- print/mobile

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P06-02, P10-02, P11-04. Parallel opportunities: P06-01

#### Objective acceptance criteria

- [ ] Produce a preliminary, source-labelled Node 0 readiness report and separate IP/GC progress views without overclaiming clearance or exposing private answers.
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
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

## Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |

Merge order inside this package: `P06-01` → `P06-02` → `P06-03`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Entitlement versioning; GC-authored revisions; IP/GC visibility pairs; Revoked/expired claims; No paid-case creation | Expected state/event/UI and named evidence are produced once. |
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
| Blocking/product/compliance decision | D-DATA-02 - How long to retain unselected candidate assertions and how are GC corrections, conflicting relationship answers, and private IP notes represented? | Luke | P04-02, P04-03, P06-02; Before P04-02 | D-DATA-02 - Append revisions with supersedes/derived-from; never silently erase source; shortest justified retention for unselected candidates. |
| Blocking/product/compliance decision | D-DATA-03 - Does any 0-100 candidate ranking or race-based preference survive, and what may provisional third-party answers gate? | Luke | P05-02, P06-03; Before P05-02 | D-DATA-03 - Remove candidate ranking and race preference; use source-labelled questions-to-clarify. Unverified IP answers cannot gate claim/onboarding/eligibility. |
| Blocking/product/compliance decision | D-COM-01 - Set the flat one-time price and tax treatment; it must remain fully creditable against the later JMF. | Luke | P06-01, P07-01, P08-01; Before activation of a Complete configuration | D-COM-01 - Keep no active production value until explicitly approved; test with synthetic configuration. |
| Implementation risk | Entitlement mistaken for case access | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | GC answers exposed to IP | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | IP assertions silently converted | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Price hard-coded | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P06-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#123 | 34078f810b63 | GC onboarding form/copy, hosted auth return, invite handoff and role-specific surface work. | P06-02, P06-03 | Selective UX/test port and rewrite | Unextracted; likely partially copied into #124 but not proven complete. |
| app#124 | 84a5a847fea7 | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. | P06-02, P06-03 | Retain unchanged as evidence; selective port/rewrite after checkpoint | Unextracted; Alan review explicitly incomplete and unresolved. |
| feature/node0-surrogate-onboarding-link | 529d377 | substantial uncommitted onboarding/invitation work | P03-02/P03-03/P06-02 | Selective port from protected worktree | Preserve until file/test extraction is signed off. |

Package source inventory:

- PRs #123/#124 onboarding screens
- Dirty onboarding-link branch
- PR #122 paired-lens tests

## Ownership recommendation

Luke decides product visibility and entitlement boundaries; Alan implements. External privacy review is recommended for field-level projections.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P06-01 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P06-02 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P06-03 | Alan | Alan (proposed) | Luke | Luke | Mandatory |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
