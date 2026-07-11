---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 07: Commercial configuration, enrollment, and promotion"
author: "L. Rhodes (plan owner) - A. Zhao (technical review requested)"
date: "2026-07-10"
---
# Work Package 07: Commercial configuration, enrollment, and promotion

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP07 |
| Plan file | `WP07 - Commercial configuration, enrollment, and promotion.md` |
| Proposed PRs | P07-01, P07-02, P07-03, P07-04 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

## Purpose and outcome

**Problem.** The business model requires versioned price/terms, explicit commitment, and one precise processor-neutral event before workspace-to-case promotion; none is currently authoritative.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Versioned commercial configuration and acceptances, a separate commitment/enrollment lifecycle, one processor-neutral byos.workspace_promotion_authorized.v1 event, and exactly-once paid-case creation by its consumer.

**Explicit non-goals.**

- No processor-specific webhook
- No automated unresolved pricing policy
- No activation before onboarding evidence
- No browser-redirect authority

## Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-025 | design authority | business model / Natalyx_Payment_and_Business_Model_BYOS_MVP.docx v1.0 | Sections 3-12 and implementation tables | Node 0 Free must complete the match; Complete is optional/creditable; $8,900 JMF and $750 enrollment anchor the configurable model; promotion follows explicit commitment and funding, not willingness or redirect. |

## Architecture and contracts

- Every commitment, invoice, payment, credit, refund, and promotion records the activated commercial-configuration version.
- Only the app-owned commitment/commercial domain emits byos.workspace_promotion_authorized.v1 after durable funding/terms/credit validation; a processor callback or redirect never emits it.
- The consumer creates/fetches one enrollment_pending case and restricted IP membership; GC case access follows the paid-case invitation contract.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`; repository-specific PRs remain separate. |
| Entities/state | `case`, `case_invitation`, `journey_commitment`, `node0_workspace` |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Read active config and record acceptance commands. Create, accept, cancel, inspect enrollment. Internal event producer only. Internal event handler only. |
| Storage | Commercial configuration and acceptance ledgers. Commitment events/current projection. Promotion ledger and source-workspace unique constraint. |
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


### Commercial commitment (`journey_commitment`)

Owner: **natalyx-app commercial domain**. States: `draft`, `accepted`, `funding_pending`, `funded`, `cancelled`, `expired`.

**Transition: `none` -> `draft`**

- **Actor:** IP
- **Evidence:** active workspace + displayed config/terms
- **Idempotency key:** `commitment:{workspace}:{config}`
- **Invalid transitions:** No active config/workspace
- **Audit event:** `commitment_drafted`
- **Retry:** Return existing draft
- **Recovery:** Create new draft after expiry/version change

**Transition: `draft` -> `accepted`**

- **Actor:** IP
- **Evidence:** terms/privacy consent + payment path
- **Idempotency key:** `commitment:{id}:accept:{terms_hash}`
- **Invalid transitions:** Stale/missing acceptance
- **Audit event:** `commitment_accepted`
- **Retry:** Return accepted
- **Recovery:** New acceptance revision if version changes

**Transition: `accepted` -> `funding_pending`**

- **Actor:** commercial service
- **Evidence:** enrollment invoice/payment intent created
- **Idempotency key:** `commitment:{id}:funding`
- **Invalid transitions:** No invoice or invalid amount
- **Audit event:** `funding_requested`
- **Retry:** Resume same invoice
- **Recovery:** Cancel/reissue under audited adjustment

**Transition: `funding_pending` -> `funded`**

- **Actor:** payment domain
- **Evidence:** net settled enrollment funding meets versioned requirement
- **Idempotency key:** `enrollment-funding:{id}:v1`
- **Invalid transitions:** Redirect/pending/failed/reversed evidence
- **Audit event:** `commercial.enrollment_funding_confirmed.v1`
- **Retry:** Exactly-once event/outbox replay
- **Recovery:** Reconcile inbox/ledger; no browser repair

**Transition: `draft|accepted|funding_pending` -> `cancelled`**

- **Actor:** IP/authorized operator
- **Evidence:** explicit cancellation and refund policy
- **Idempotency key:** `commitment:{id}:cancel:{request}`
- **Invalid transitions:** Already funded/promoted uses case cancellation rail
- **Audit event:** `commitment_cancelled`
- **Retry:** Idempotent
- **Recovery:** New commitment required

**Transition: `draft|accepted` -> `expired`**

- **Actor:** system
- **Evidence:** offer/terms TTL or config deactivation
- **Idempotency key:** `commitment:{id}:expire`
- **Invalid transitions:** No expiry after funding
- **Audit event:** `commitment_expired`
- **Retry:** Idempotent
- **Recovery:** Draft new version


### Paid case lifecycle (`case`)

Owner: **natalyx-app**. States: `enrollment_pending`, `active`, `paused`, `closed`, `cancelled`.

**Transition: `none` -> `enrollment_pending`**

- **Actor:** promotion service
- **Evidence:** byos.workspace_promotion_authorized.v1 + projection manifest
- **Idempotency key:** `promotion:{commitment}:v1`
- **Invalid transitions:** No authorization/duplicate workspace
- **Audit event:** `paid_case_created`
- **Retry:** Return same case
- **Recovery:** Forward-repair same promotion

**Transition: `enrollment_pending` -> `active`**

- **Actor:** authorized coordinator/domain service
- **Evidence:** approved onboarding/compatibility/intake/education evidence
- **Idempotency key:** `case:{id}:activate:{evidence_hash}`
- **Invalid transitions:** Missing/revoked evidence or GC consent
- **Audit event:** `case_activated`
- **Retry:** No duplicate activation/invoice
- **Recovery:** Return pending with unmet checklist

**Transition: `active` -> `paused`**

- **Actor:** authorized commercial/operations policy
- **Evidence:** audited non-critical pause reason
- **Idempotency key:** `case:{id}:pause:{event}`
- **Invalid transitions:** Safety-critical access cannot be paused
- **Audit event:** `case_paused`
- **Retry:** Idempotent
- **Recovery:** Resume after evidence; preserve entitled docs

**Transition: `paused` -> `active`**

- **Actor:** authorized operator/domain service
- **Evidence:** pause reason resolved
- **Idempotency key:** `case:{id}:resume:{event}`
- **Invalid transitions:** Unresolved safety/authorization block
- **Audit event:** `case_resumed`
- **Retry:** Idempotent
- **Recovery:** Escalate manual review

**Transition: `active|paused` -> `closed`**

- **Actor:** authorized coordinator
- **Evidence:** birth/close or completed termination handoff evidence
- **Idempotency key:** `case:{id}:close:{evidence_hash}`
- **Invalid transitions:** Open critical obligations
- **Audit event:** `case_closed`
- **Retry:** No-op if same evidence
- **Recovery:** Reopen only by exceptional audited event

**Transition: `enrollment_pending|active|paused` -> `cancelled`**

- **Actor:** authorized operator under policy
- **Evidence:** withdrawal/non-clearance/cancellation + financial disposition
- **Idempotency key:** `case:{id}:cancel:{request}`
- **Invalid transitions:** Cannot erase records/refund ledger
- **Audit event:** `case_cancelled`
- **Retry:** Idempotent
- **Recovery:** Replacement is a new case/workspace policy event


### Paid-case membership invitation (`case_invitation`)

Owner: **natalyx-app**. States: `issued`, `pending_identity`, `identity_bound`, `mismatch_pending`, `issuer_confirmed`, `consented`, `redeemed`, `declined`, `revoked`, `expired`, `superseded`.

**Transition: `none` -> `issued`**

- **Actor:** authorized IP case member
- **Evidence:** enrollment_pending/active case + recipient binding
- **Idempotency key:** `case-invite:{case}:{role}:{generation}`
- **Invalid transitions:** Self/member/active-GC/unauthorized
- **Audit event:** `case_invite_issued`
- **Retry:** Return current; supersede prior live GC invite
- **Recovery:** Issue corrected invite

**Transition: `issued` -> `pending_identity`**

- **Actor:** recipient
- **Evidence:** valid addressed token landing
- **Idempotency key:** `case-invite:{id}:land`
- **Invalid transitions:** Expired/revoked
- **Audit event:** `case_invite_opened`
- **Retry:** Safe repeat
- **Recovery:** Authenticate with return_to

**Transition: `pending_identity` -> `identity_bound|mismatch_pending`**

- **Actor:** auth provider
- **Evidence:** verified subject/email
- **Idempotency key:** `case-invite:{id}:bind:{subject}`
- **Invalid transitions:** Terminal/duplicate/different subject
- **Audit event:** `case_invite_bound|mismatch`
- **Retry:** CAS protects terminal
- **Recovery:** Issuer confirmation or corrected invite

**Transition: `mismatch_pending` -> `issuer_confirmed`**

- **Actor:** authorized issuer
- **Evidence:** explicit reviewed mismatch confirmation
- **Idempotency key:** `case-invite:{id}:confirm:{issuer}`
- **Invalid transitions:** Issuer unauthorized/recipient changed
- **Audit event:** `case_invite_mismatch_confirmed`
- **Retry:** CAS no-op
- **Recovery:** Revoke and reissue

**Transition: `identity_bound|issuer_confirmed` -> `consented`**

- **Actor:** invitee
- **Evidence:** paid-case role/privacy consent version
- **Idempotency key:** `case-invite:{id}:consent:{version}`
- **Invalid transitions:** Stale/missing consent
- **Audit event:** `case_invite_consented`
- **Retry:** Idempotent
- **Recovery:** Present current consent

**Transition: `consented` -> `redeemed`**

- **Actor:** invitation service
- **Evidence:** single transaction creates person/party/membership
- **Idempotency key:** `case-invite:{id}:redeem`
- **Invalid transitions:** Existing member/active GC/expired/revoked
- **Audit event:** `case_invite_redeemed`
- **Retry:** Return same membership
- **Recovery:** Rollback entire transaction; forward repair from invite

**Transition: `issued|pending_identity|identity_bound|mismatch_pending|issuer_confirmed|consented` -> `declined|revoked|expired|superseded`**

- **Actor:** invitee/issuer/system
- **Evidence:** explicit decline/revoke/TTL/new generation
- **Idempotency key:** `case-invite:{id}:terminal:{event}`
- **Invalid transitions:** No terminal overwrite
- **Audit event:** `case_invite_terminal`
- **Retry:** Idempotent CAS
- **Recovery:** Fresh invitation only


### Data authorship/provenance rules

- Every assertion/revision records subject_ref, semantic_key, author_subject/person/role, authorship_class, provenance, verification_status, visibility, purpose, source_ref, derived_from, supersedes_id, promotion_event_id, policy version and immutable timestamps.
- Class 1 defaults IP-private; class 2 defaults IP-private/internal and visibly says reported by the intended parent, not confirmed by the GC.
- Class 3 is GC-authored and shared only per field/purpose; class 4 is GC-only private; class 5 requires an evidence-linked role-gated reviewer/provider rail.
- GC confirmation appends a class-3 revision referencing the class-2 assertion. Relationship answers can coexist; disagreement is not an overwrite.
- Unselected candidates, raw health assertions, ranking scores and private IP notes do not promote. Derived values inherit the weakest source status.
- Copying, promotion, generic proposal approval, IP assertion or AI inference can never create Natalyx-reviewed, provider-confirmed, medically cleared, legally cleared or insurance-verified truth.

### Sole promotion-authorizing event

`event_type: byos.workspace_promotion_authorized.v1`

Producer: natalyx-app commitment/commercial domain after deterministic validation. Consumer: natalyx-app promotion service.

Payload:

```text
event_id
idempotency_key
workspace_id
commitment_id
owner_person_id
owner_subject
commercial_config_version
terms_acceptance_ids[]
payment_plan_id
funding_evidence.kind
funding_evidence.commercial_event_id
funding_evidence.settled_amount_minor
funding_evidence.currency
credit_allocation_ids[]
initial_case_state=enrollment_pending
occurred_at
correlation_id
causation_id
schema_version
```

Authorization conditions:

- Workspace is active/match-ready, unarchived and not already promoted.
- Commitment references the same workspace, has current terms/privacy acceptances and is in funding_pending/funded per the approved state contract.
- Payment path and activated commercial configuration are pinned.
- Required enrollment funding has a verified settled ledger entry or separately approved financing/manual-funding evidence; a processor webhook is first normalized and cannot itself authorize promotion.
- Credit allocation is non-negative, reproducible and cannot exceed the applicable obligation.
- No cancellation, compliance hold, reversal that invalidates funding, or existing promotion is present.

Unique constraints:

- one promotion per workspace
- one case per promotion event
- one result per idempotency key
- one primary owner membership per created case

No browser success/return route and no raw processor callback can emit or substitute for this event.

## Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P07-01 | Add versioned commercial configuration and terms acceptance | app | P02-03 | A2 | Large | Dependencies unmet |
| 2 | P07-02 | Implement commitment and enrollment-pending lifecycle | app | P07-01, P08-01 | A2 | Large | Dependencies unmet |
| 3 | P07-03 | Emit processor-neutral workspace promotion authorization | app | P04-02, P07-02, P08-02 | A2 | Large | Dependencies unmet |
| 4 | P07-04 | Promote workspace exactly once from authorization event | app | P03-03, P04-02, P07-03 | A2 | Exceptional | Dependencies unmet |

### P07-01 - Add versioned commercial configuration and terms acceptance

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P02-03 |
| Blocking decisions/checkpoints | D-COM-01, D-COM-02, D-COM-03 |
| Source / salvage | Payment/business-model DOCX |

#### Objective

Store activated price books, milestone schedules, Node 0 credit rules, and immutable terms/privacy acceptance versions without scattering literals.

#### Scope

- Immutable activated config versions
- JMF/deposit/discount/milestones/credit policy
- Terms and privacy acceptance records

#### Explicit non-goals

- No unresolved Node 0 price value
- No payment provider

#### Expected files or modules

- `migrations/versions/*_commercial_configuration.py`
- `app/domain/commercial_config.py`
- `app/storage/commercial_config.py`
- `tests/python/test_commercial_config.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Commercial configuration and acceptance ledgers. |
| API/routes | Read active config and record acceptance commands. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Activation immutability
- currency/amount validation
- acceptance version
- no retroactive mutation

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

Hard dependencies: P02-03. Parallel opportunities: P07-03, P07-04

#### Objective acceptance criteria

- [ ] Store activated price books, milestone schedules, Node 0 credit rules, and immutable terms/privacy acceptance versions without scattering literals.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Luke |
| Implementer | Luke (proposed; pending joint approval) |
| Reviewer | Alan |
| Final approver | Joint |
| Required expertise | commercial systems, PostgreSQL |
| Higher-capability review | Mandatory before merge |

### P07-02 - Implement commitment and enrollment-pending lifecycle

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P07-01, P08-01 |
| Blocking decisions/checkpoints | D-COM-04 |
| Source / salvage | Business-model conversion trigger |

#### Objective

Create a deliberate managed-journey commitment with accepted terms, selected payment path, pinned config, and an enrollment invoice request independent from case state.

#### Scope

- Draft/accepted/cancelled/expired commitment transitions
- Payment-path choice
- Enrollment invoice command

#### Explicit non-goals

- No browser-triggered promotion
- No activation

#### Expected files or modules

- `app/domain/commitments.py`
- `app/storage/commitments.py`
- `app/routes/enrollment.py`
- `tests/python/test_commitments.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Commitment events/current projection. |
| API/routes | Create, accept, cancel, inspect enrollment. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Acceptance prerequisites
- duplicate accept
- stale config
- cancel/expire
- resume

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

Hard dependencies: P07-01, P08-01. Parallel opportunities: P07-04

#### Objective acceptance criteria

- [ ] Create a deliberate managed-journey commitment with accepted terms, selected payment path, pinned config, and an enrollment invoice request independent from case state.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Luke |
| Implementer | Luke (proposed; pending joint approval) |
| Reviewer | Alan |
| Final approver | Joint |
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

### P07-03 - Emit processor-neutral workspace promotion authorization

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P04-02, P07-02, P08-02 |
| Blocking decisions/checkpoints | D-COM-04, D-DATA-01 |
| Source / salvage | Business-model promotion invariants |

#### Objective

Validate commitment, terms, commercial version, settled funding and credit evidence, then emit exactly one byos.workspace_promotion_authorized.v1 event; processor callbacks and browser redirects cannot emit it.

#### Scope

- Deterministic authorization predicate
- Canonical payload and idempotency key
- Transactional event/outbox
- Funding/credit/config evidence references

#### Explicit non-goals

- No case creation
- No redirect/webhook-as-authority
- No GC membership

#### Expected files or modules

- `app/domain/promotion_authorization.py`
- `app/event_handlers/commercial.py`
- `app/storage/outbox.py`
- `tests/python/test_promotion_authorization.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Internal event producer only. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Only commercial-domain authority can emit the typed event. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Pending/failed/reversed funding
- stale terms/config
- duplicate/replayed inputs
- credit mismatch
- event payload/checksum

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

Hard dependencies: P04-02, P07-02, P08-02. Parallel opportunities: P07-01

#### Objective acceptance criteria

- [ ] Validate commitment, terms, commercial version, settled funding and credit evidence, then emit exactly one byos.workspace_promotion_authorized.v1 event; processor callbacks and browser redirects cannot emit it.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Luke |
| Implementer | Luke (proposed; pending joint approval) |
| Reviewer | Alan |
| Final approver | Joint |
| Required expertise | event-driven systems, payments, commercial policy |
| Higher-capability review | Mandatory before merge |

### P07-04 - Promote workspace exactly once from authorization event

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P03-03, P04-02, P07-03 |
| Blocking decisions/checkpoints | D-COM-04, D-DATA-01, CHECK-ALAN-122-124 |
| Source / salvage | byos.workspace_promotion_authorized.v1 contract, PR #124 source linkage concepts |

#### Objective

Consume byos.workspace_promotion_authorized.v1 to create/find one enrollment_pending paid case, link the source workspace, project allowlisted data, and grant only restricted IP membership.

#### Scope

- Unique promotion idempotency key
- Case/source link and config version
- Purpose-limited data manifest and audit event

#### Explicit non-goals

- No redirect authority
- No GC case membership transfer
- No activation

#### Expected files or modules

- `app/domain/promotion.py`
- `app/storage/promotions.py`
- `app/event_handlers/enrollment.py`
- `tests/python/test_workspace_promotion.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Promotion ledger and source-workspace unique constraint. |
| API/routes | Internal event handler only. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Projection defaults deny and preserves provenance. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Replay/concurrency
- partial transaction
- funding event validation
- private candidate exclusion
- GC invitation required

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

Hard dependencies: P03-03, P04-02, P07-03. Parallel opportunities: P07-01, P07-02

#### Objective acceptance criteria

- [ ] Consume byos.workspace_promotion_authorized.v1 to create/find one enrollment_pending paid case, link the source workspace, project allowlisted data, and grant only restricted IP membership.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Luke |
| Implementer | Luke (proposed; pending joint approval) |
| Reviewer | Alan |
| Final approver | Joint |
| Required expertise | event-driven systems, privacy, PostgreSQL |
| Higher-capability review | Mandatory before merge |

## Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |

Merge order inside this package: `P07-01` → `P07-02` → `P07-03` → `P07-04`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Terms/config version pinning; Commitment retries; Exact-once promotion; Funding reversal handling; No GC access escalation | Expected state/event/UI and named evidence are produced once. |
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
| Blocking/product/compliance decision | D-COM-01 - Set the flat one-time price and tax treatment; it must remain fully creditable against the later JMF. | Luke | P06-01, P07-01, P08-01; Before activation of a Complete configuration | D-COM-01 - Keep no active production value until explicitly approved; test with synthetic configuration. |
| Blocking/product/compliance decision | D-COM-02 - Ratify $8,900 JMF, $7,830 pay-in-full, $750 deposit and 20/30/20/20/10 post-deposit milestones as configuration v1 with effective date/currency. | Luke | P07-01, P08-01, P08-03; Before P07-01 activation data | D-COM-02 - Use the document anchors but require explicit version activation rather than code literals. |
| Blocking/product/compliance decision | D-COM-03 - Approve the actual paid-service terms, privacy/consent disclosure and refundable-to-earned wording. | Luke | P07-01, P07-02, P08-03; Before P07-02 user acceptance | D-COM-03 - External legal/privacy/finance review before any real acceptance. |
| Blocking/product/compliance decision | D-COM-04 - Define evidence for enrollment funding confirmed, promotion authorization, and for onboarding/compatibility complete enough to move case active and earn/issue activation billing. | Luke | P07-02, P07-03, P07-04, P08-03, P09-04; Before P07-02 | D-COM-04 - Funding confirmation is durable ledger evidence; promotion uses the sole typed authorization event; activation requires an explicit evidence checklist, actor and audit event. |
| Blocking/product/compliance decision | D-COM-05 - Select financing partner and define when funding is sufficiently authorized/settled; otherwise hide the path. | Luke | P07-02, P08-02; Before financed option is exposed | D-COM-05 - Do not block card/ACH MVP; keep optional and disabled. |
| Implementation risk | Configuration drift | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Duplicate promotion | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Redirect spoofing | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Unresolved policy encoded as default | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| No direct source | - | Build from approved contracts/evidence | Package PRs | New implementation | N/A |

Package source inventory:

- Payment/business-model DOCX as authority
- PR #124 source workspace linkage concepts only

## Ownership recommendation

Luke leads this work package, with Alan providing technical review. The split is proposed for review and can be amended before implementation begins.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P07-01 | Luke | Luke (proposed) | Alan | Joint | Mandatory |
| P07-02 | Luke | Luke (proposed) | Alan | Joint | Mandatory |
| P07-03 | Luke | Luke (proposed) | Alan | Joint | Mandatory |
| P07-04 | Luke | Luke (proposed) | Alan | Joint | Mandatory |

Luke leads implementation and product acceptance for this package; Alan reviews architecture, migration, security and failure behavior. This is a recommendation pending joint review, not a compulsory assignment.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
