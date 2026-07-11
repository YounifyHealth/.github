# Work package 07 — Commercial configuration, enrollment, and promotion

> Planning-only execution contract. Proposed implementers and owners remain recommendations until Alan reviews/signs off the consolidated plan and Luke accepts it. Project: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP07 |
| Plan file | `07-commercial-configuration-enrollment-and-promotion.md` |
| Proposed PRs | P07-01, P07-02, P07-03, P07-04 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

## 1. Purpose and outcome

**Problem.** The business model requires versioned price/terms, explicit commitment, and one precise processor-neutral event before workspace-to-case promotion; none is currently authoritative.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Versioned commercial configuration and acceptances, a separate commitment/enrollment lifecycle, one processor-neutral byos.workspace_promotion_authorized.v1 event, and exactly-once paid-case creation by its consumer.

**Explicit non-goals.**

- No processor-specific webhook
- No automated unresolved pricing policy
- No activation before onboarding evidence
- No browser-redirect authority

## 2. Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-025 | design authority | business model / Natalyx_Payment_and_Business_Model_BYOS_MVP.docx v1.0 | Sections 3-12 and implementation tables | Node 0 Free must complete the match; Complete is optional/creditable; $8,900 JMF and $750 enrollment anchor the configurable model; promotion follows explicit commitment and funding, not willingness or redirect. |

## 3. Architecture and contracts

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

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | draft | authenticated IP | first explicit Node 0 start | workspace:{owner}:create | Existing active workspace returns existing | workspace_created | Unique owner/idempotency key | Forward repair orphan membership |
| draft | active | IP | minimum workspace consent/profile | workspace:{id}:activate:{revision} | Missing consent/owner | workspace_activated | Return current active revision | Correct inputs and retry |
| active | match_ready | IP + selected GC evidence policy | selected candidate + required provisional/GC-authored fields | workspace:{id}:ready:{revision} | Critical unknown/decline/revoked claim | workspace_match_ready | No duplicate event | Reopen active with reason revision |
| match_ready | promotion_pending | promotion event consumer | valid byos.workspace_promotion_authorized.v1 | promotion:{commitment}:v1 | No authorization; already promoted; stale config | workspace_promotion_requested | Replay resumes/finds same promotion | Forward-repair incomplete transaction |
| promotion_pending | promoted | promotion service | paid case + manifest committed | promotion:{commitment}:v1 | Projection invariant/privacy failure | workspace_promoted | Return same case ID | Repair from immutable manifest; never duplicate |
| draft\|active\|match_ready | archived | IP/operator per policy | explicit archive + retention policy | workspace:{id}:archive:{request} | Promotion pending/promoted | workspace_archived | Idempotent | Restore only through new audited revision if policy permits |

### Commercial commitment (`journey_commitment`)

Owner: **natalyx-app commercial domain**. States: `draft`, `accepted`, `funding_pending`, `funded`, `cancelled`, `expired`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | draft | IP | active workspace + displayed config/terms | commitment:{workspace}:{config} | No active config/workspace | commitment_drafted | Return existing draft | Create new draft after expiry/version change |
| draft | accepted | IP | terms/privacy consent + payment path | commitment:{id}:accept:{terms_hash} | Stale/missing acceptance | commitment_accepted | Return accepted | New acceptance revision if version changes |
| accepted | funding_pending | commercial service | enrollment invoice/payment intent created | commitment:{id}:funding | No invoice or invalid amount | funding_requested | Resume same invoice | Cancel/reissue under audited adjustment |
| funding_pending | funded | payment domain | net settled enrollment funding meets versioned requirement | enrollment-funding:{id}:v1 | Redirect/pending/failed/reversed evidence | commercial.enrollment_funding_confirmed.v1 | Exactly-once event/outbox replay | Reconcile inbox/ledger; no browser repair |
| draft\|accepted\|funding_pending | cancelled | IP/authorized operator | explicit cancellation and refund policy | commitment:{id}:cancel:{request} | Already funded/promoted uses case cancellation rail | commitment_cancelled | Idempotent | New commitment required |
| draft\|accepted | expired | system | offer/terms TTL or config deactivation | commitment:{id}:expire | No expiry after funding | commitment_expired | Idempotent | Draft new version |

### Paid case lifecycle (`case`)

Owner: **natalyx-app**. States: `enrollment_pending`, `active`, `paused`, `closed`, `cancelled`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | enrollment_pending | promotion service | byos.workspace_promotion_authorized.v1 + projection manifest | promotion:{commitment}:v1 | No authorization/duplicate workspace | paid_case_created | Return same case | Forward-repair same promotion |
| enrollment_pending | active | authorized coordinator/domain service | approved onboarding/compatibility/intake/education evidence | case:{id}:activate:{evidence_hash} | Missing/revoked evidence or GC consent | case_activated | No duplicate activation/invoice | Return pending with unmet checklist |
| active | paused | authorized commercial/operations policy | audited non-critical pause reason | case:{id}:pause:{event} | Safety-critical access cannot be paused | case_paused | Idempotent | Resume after evidence; preserve entitled docs |
| paused | active | authorized operator/domain service | pause reason resolved | case:{id}:resume:{event} | Unresolved safety/authorization block | case_resumed | Idempotent | Escalate manual review |
| active\|paused | closed | authorized coordinator | birth/close or completed termination handoff evidence | case:{id}:close:{evidence_hash} | Open critical obligations | case_closed | No-op if same evidence | Reopen only by exceptional audited event |
| enrollment_pending\|active\|paused | cancelled | authorized operator under policy | withdrawal/non-clearance/cancellation + financial disposition | case:{id}:cancel:{request} | Cannot erase records/refund ledger | case_cancelled | Idempotent | Replacement is a new case/workspace policy event |

### Paid-case membership invitation (`case_invitation`)

Owner: **natalyx-app**. States: `issued`, `pending_identity`, `identity_bound`, `mismatch_pending`, `issuer_confirmed`, `consented`, `redeemed`, `declined`, `revoked`, `expired`, `superseded`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | issued | authorized IP case member | enrollment_pending/active case + recipient binding | case-invite:{case}:{role}:{generation} | Self/member/active-GC/unauthorized | case_invite_issued | Return current; supersede prior live GC invite | Issue corrected invite |
| issued | pending_identity | recipient | valid addressed token landing | case-invite:{id}:land | Expired/revoked | case_invite_opened | Safe repeat | Authenticate with return_to |
| pending_identity | identity_bound\|mismatch_pending | auth provider | verified subject/email | case-invite:{id}:bind:{subject} | Terminal/duplicate/different subject | case_invite_bound\|mismatch | CAS protects terminal | Issuer confirmation or corrected invite |
| mismatch_pending | issuer_confirmed | authorized issuer | explicit reviewed mismatch confirmation | case-invite:{id}:confirm:{issuer} | Issuer unauthorized/recipient changed | case_invite_mismatch_confirmed | CAS no-op | Revoke and reissue |
| identity_bound\|issuer_confirmed | consented | invitee | paid-case role/privacy consent version | case-invite:{id}:consent:{version} | Stale/missing consent | case_invite_consented | Idempotent | Present current consent |
| consented | redeemed | invitation service | single transaction creates person/party/membership | case-invite:{id}:redeem | Existing member/active GC/expired/revoked | case_invite_redeemed | Return same membership | Rollback entire transaction; forward repair from invite |
| issued\|pending_identity\|identity_bound\|mismatch_pending\|issuer_confirmed\|consented | declined\|revoked\|expired\|superseded | invitee/issuer/system | explicit decline/revoke/TTL/new generation | case-invite:{id}:terminal:{event} | No terminal overwrite | case_invite_terminal | Idempotent CAS | Fresh invitation only |

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

## 4. Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P07-01 | Add versioned commercial configuration and terms acceptance | app | P02-03 | A2 | Large | Dependencies unmet |
| 2 | P07-02 | Implement commitment and enrollment-pending lifecycle | app | P07-01, P08-01 | A2 | Large | Dependencies unmet |
| 3 | P07-03 | Emit processor-neutral workspace promotion authorization | app | P04-02, P07-02, P08-02 | A2 | Large | Dependencies unmet |
| 4 | P07-04 | Promote workspace exactly once from authorization event | app | P03-03, P04-02, P07-03 | A2 | Exceptional | Dependencies unmet |

### P07-01 — Add versioned commercial configuration and terms acceptance

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-01) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | commercial systems, PostgreSQL |
| Higher-capability review | Mandatory before merge |

### P07-02 — Implement commitment and enrollment-pending lifecycle

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-02) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
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

### P07-03 — Emit processor-neutral workspace promotion authorization

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-03) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | event-driven systems, payments, commercial policy |
| Higher-capability review | Mandatory before merge |

### P07-04 — Promote workspace exactly once from authorization event

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-04) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | event-driven systems, privacy, PostgreSQL |
| Higher-capability review | Mandatory before merge |

## 5. Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |

Merge order inside this package: `P07-01` → `P07-02` → `P07-03` → `P07-04`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## 6. Test and acceptance matrix

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

## 7. Risks and decisions

| Type | ID / risk | Owner | Affected PRs / latest point | Project item / treatment |
| --- | --- | --- | --- | --- |
| Blocking/product/compliance decision | D-DATA-01 — Which provisional IP assertions may the GC see, which GC answers may the IP see, and which fields survive promotion/provider projection? | Luke | P04-02, P06-02, P06-03, P07-03, P07-04, P09-05, P10-01, P10-02; Before P04-02 | [D-DATA-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-DATA-01) — Default deny; expose only explicit purpose-limited projections. Class 1/2 and class 4 never automatically cross roles. |
| Blocking/product/compliance decision | D-COM-01 — Set the flat one-time price and tax treatment; it must remain fully creditable against the later JMF. | Luke | P06-01, P07-01, P08-01; Before activation of a Complete configuration | [D-COM-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-01) — Keep no active production value until explicitly approved; test with synthetic configuration. |
| Blocking/product/compliance decision | D-COM-02 — Ratify $8,900 JMF, $7,830 pay-in-full, $750 deposit and 20/30/20/20/10 post-deposit milestones as configuration v1 with effective date/currency. | Luke | P07-01, P08-01, P08-03; Before P07-01 activation data | [D-COM-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-02) — Use the document anchors but require explicit version activation rather than code literals. |
| Blocking/product/compliance decision | D-COM-03 — Approve the actual paid-service terms, privacy/consent disclosure and refundable-to-earned wording. | Luke | P07-01, P07-02, P08-03; Before P07-02 user acceptance | [D-COM-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-03) — External legal/privacy/finance review before any real acceptance. |
| Blocking/product/compliance decision | D-COM-04 — Define evidence for enrollment funding confirmed, promotion authorization, and for onboarding/compatibility complete enough to move case active and earn/issue activation billing. | Luke | P07-02, P07-03, P07-04, P08-03, P09-04; Before P07-02 | [D-COM-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-04) — Funding confirmation is durable ledger evidence; promotion uses the sole typed authorization event; activation requires an explicit evidence checklist, actor and audit event. |
| Blocking/product/compliance decision | D-COM-05 — Select financing partner and define when funding is sufficiently authorized/settled; otherwise hide the path. | Luke | P07-02, P08-02; Before financed option is exposed | [D-COM-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-05) — Do not block card/ACH MVP; keep optional and disabled. |
| Implementation risk | Configuration drift | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Duplicate promotion | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Redirect spoofing | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Unresolved policy encoded as default | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| No direct source | — | Build from approved contracts/evidence | Package PRs | New implementation | N/A |

Package source inventory:

- Payment/business-model DOCX as authority
- PR #124 source workspace linkage concepts only

## 9. Ownership recommendation

Luke owns commercial semantics and final contract. Alan proposes/implements the state machine and idempotency. Finance/legal review unresolved policy.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P07-01 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P07-02 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P07-03 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P07-04 | Alan | Alan (proposed) | Luke | Luke | Mandatory |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
