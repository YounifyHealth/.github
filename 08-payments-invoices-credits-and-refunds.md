# Work package 08 — Payments, invoices, credits, and refunds

> Planning-only execution contract. Proposed implementers and owners remain recommendations until Alan reviews/signs off the consolidated plan and Luke accepts it. Project: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP08 |
| Plan file | `08-payments-invoices-credits-and-refunds.md` |
| Proposed PRs | P08-01, P08-02, P08-03, P08-04 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

## 1. Purpose and outcome

**Problem.** No append-only commercial ledger or processor-neutral payment boundary currently supports the $8,900 JMF, $750 enrollment, Node 0 credit, milestones, deterministic refunds, or failure recovery.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Immutable commercial ledgers, idempotent provider inbox, milestone engine, reproducible credits/refunds, reconciliation, and safe non-critical pause behavior.

**Explicit non-goals.**

- No custody of pass-through funds
- No financing assumption
- No pregnancy-loss automation before policy
- No accounting-general-ledger replacement

## 2. Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-025 | design authority | business model / Natalyx_Payment_and_Business_Model_BYOS_MVP.docx v1.0 | Sections 3-12 and implementation tables | Node 0 Free must complete the match; Complete is optional/creditable; $8,900 JMF and $750 enrollment anchor the configurable model; promotion follows explicit commitment and funding, not willingness or redirect. |

## 3. Architecture and contracts

- Payments, credits, refunds, adjustments, invoices, and commercial events are append-only; mutable balances are derived projections.
- Processor events enter an idempotent inbox and become internal commands/events only after signature and amount/currency checks.
- Billing follows durable case evidence and never acts as first notification of clinical events.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`; repository-specific PRs remain separate. |
| Entities/state | `journey_commitment`, `payment_obligation + append-only entries`, `workspace_entitlement` |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Processor webhook and internal payment commands. Internal evidence-to-invoice commands and explainable refund quote. |
| Storage | Append-only financial ledgers and unique idempotency constraints. Processor-event inbox/outbox and mapping records. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

### Applicable state machines

### Entitlement (`workspace_entitlement`)

Owner: **natalyx-app commercial domain**. States: `free`, `complete_pending`, `complete_active`, `suspended`, `revoked`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | free | system | active Node 0 workspace | entitlement:{workspace}:free | No workspace | entitlement_granted | Return current | Repair projection from event |
| free | complete_pending | IP/commercial service | accepted Complete offer/config | entitlement:{workspace}:{commitment} | Unknown price/config/terms | complete_requested | Return pending | Cancel/expire commitment |
| complete_pending | complete_active | payment domain | settled Complete ledger entry | entitlement:{payment}:activate | Amount/currency/config mismatch | complete_activated | Replay no-op | Reconcile and retry from inbox |
| complete_active | suspended | authorized commercial policy | refund/reversal or approved pause reason | entitlement:{id}:suspend:{event} | Cannot remove free/safety capability | entitlement_suspended | No-op if same event | Reinstate or revoke through new event |
| complete_active\|suspended | revoked | authorized operator/policy | fraud/refund/terms revocation evidence | entitlement:{id}:revoke:{event} | No silent case cancellation | entitlement_revoked | Idempotent | Manual reviewed regrant creates new entitlement event |

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

### Payment (`payment_obligation + append-only entries`)

Owner: **natalyx-app payment domain**. States: `created`, `processing`, `settled`, `failed`, `partially_refunded`, `refunded`, `reversed`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | created | billing policy | valid invoice/obligation | payment:{invoice}:create | Duplicate or invalid invoice | payment_created | Return current intent | Void/reissue through adjustment |
| created\|failed | processing | processor adapter | signed provider acknowledgement | processor:{provider_event} | Amount/currency/customer mismatch | payment_processing | Inbox replay no-op | Retry same intent or audited replacement |
| processing\|created | settled | payment domain | verified settlement event | processor:{provider_event} | Browser redirect or unverified event | payment_settled | Exactly-once append | Reconcile provider and append repair event |
| created\|processing | failed | payment domain | verified failure/timeout policy | processor:{provider_event} | Cannot overwrite settled | payment_failed | Replay no-op | Retry/new attempt linked to obligation |
| settled\|partially_refunded | partially_refunded\|refunded | authorized refund service | approved refund calculation + processor confirmation | refund:{refund_request} | Exceeds settled less prior refunds | refund_settled | Replay no-op | Reconcile/adjust; never mutate original |
| settled | reversed | payment domain | verified chargeback/reversal | processor:{provider_event} | Unsupported/manual assertion | payment_reversed | Replay no-op | Open discrepancy and apply policy; case is not deleted |

### Append-only commercial contract

Authoritative ledgers:

- `commercial_events`
- `processor_events`
- `invoice_events`
- `payment_ledger_entries`
- `credit_ledger_entries`
- `refund_ledger_entries`
- `adjustment_ledger_entries`
- `performance_obligation_events`
- `promotion_events`

Derived projections:

- payment plan state
- invoice status
- settled cash
- available credit
- recognized/deferred amount
- refundable amount
- delinquency/pause status

Rules:

- Every record carries currency in integer minor units, commercial configuration version, source/idempotency/correlation identifiers and immutable timestamps.
- Mutable balances/statuses are projections only; reversals, chargebacks, credits, refunds and adjustments append entries.
- Processor events are signature-verified, stored once and normalized before domain use.
- Node 0 Complete credit cannot create a negative JMF obligation and stays distinct from cash/refund entries.
- Pass-through clinic/legal/psych/background/escrow/insurance/GC funds never enter Natalyx revenue ledgers.
- Clinical-linked invoices require durable evidence plus dignity-of-timing delay and can never be the first clinical notification.
- Refundable cash = max(0, settled JMF cash - earned JMF - prior cash refunds - chargebacks/reversals), with policy hooks for unresolved cases.

## 4. Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P08-01 | Add append-only commercial and money ledgers | app | P02-03, P07-01 | A2 | Exceptional | Dependencies unmet |
| 2 | P08-02 | Add processor-neutral payment command and webhook inbox | app | P08-01, P07-02 | A2 | Exceptional | Blocked by decision |
| 3 | P08-03 | Implement milestone invoicing, credits, and deterministic refunds | app | P08-02, P07-04, P09-04 | A2 | Exceptional | Dependencies unmet |
| 4 | P08-04 | Add payment reconciliation and safe service-pause operations | app | P08-03 | A2 | Large | Dependencies unmet |

### P08-01 — Add append-only commercial and money ledgers

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-01) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P02-03, P07-01 |
| Blocking decisions/checkpoints | D-COM-01, D-COM-02, D-COM-03 |
| Source / salvage | Payment/business-model DOCX |

#### Objective

Create immutable commercial-event, invoice, payment, credit, refund, and adjustment entries with deterministic projections and config-version references.

#### Scope

- Ledger invariants and currency precision
- Derived balances/status projections
- Audit/source/idempotency references

#### Explicit non-goals

- No processor
- No mutable balance authority
- No pass-through custody

#### Expected files or modules

- `migrations/versions/*_commercial_ledgers.py`
- `app/storage/ledgers.py`
- `app/domain/money.py`
- `tests/python/test_ledgers.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Append-only financial ledgers and unique idempotency constraints. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Least-privilege write paths and redacted logs. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Double-entry-like conservation checks
- duplicate key
- credit floor
- refund totals
- concurrent append

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

Hard dependencies: P02-03, P07-01. Parallel opportunities: P08-03, P08-04

#### Objective acceptance criteria

- [ ] Create immutable commercial-event, invoice, payment, credit, refund, and adjustment entries with deterministic projections and config-version references.
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
| Required expertise | payments, financial ledgers, PostgreSQL |
| Higher-capability review | Mandatory before merge |

### P08-02 — Add processor-neutral payment command and webhook inbox

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-02) |
| Gate / size / readiness | A2 / Exceptional / Blocked by decision |
| Dependencies | P08-01, P07-02 |
| Blocking decisions/checkpoints | D-PAY-01, D-COM-05 |
| Source / salvage | Business-model processor-neutral requirement |

#### Objective

Define provider ports and a signed, idempotent webhook inbox that emits internal settlement/failure/refund events, including commercial.enrollment_funding_confirmed.v1 when domain conditions hold.

#### Scope

- Provider-neutral intents and event mapping
- Signature/replay/order handling
- Settlement predicate and outbox

#### Explicit non-goals

- No browser redirect settlement
- No financing implementation unless separately approved

#### Expected files or modules

- `app/payments/ports.py`
- `app/payments/webhook_inbox.py`
- `app/routes/payment_webhooks.py`
- `tests/python/test_payment_webhooks.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Processor-event inbox/outbox and mapping records. |
| API/routes | Processor webhook and internal payment commands. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Secrets/endpoints deferred to guarded environment configuration. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Signature failure
- replay/out-of-order
- amount/currency mismatch
- timeout/retry
- settlement event exactly once

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

Hard dependencies: P08-01, P07-02. Parallel opportunities: P08-04

#### Objective acceptance criteria

- [ ] Define provider ports and a signed, idempotent webhook inbox that emits internal settlement/failure/refund events, including commercial.enrollment_funding_confirmed.v1 when domain conditions hold.
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
| Required expertise | payment security, webhooks, event systems |
| Higher-capability review | Mandatory before merge |

### P08-03 — Implement milestone invoicing, credits, and deterministic refunds

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-03) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P08-02, P07-04, P09-04 |
| Blocking decisions/checkpoints | D-COM-04, D-COM-06, D-COM-07 |
| Source / salvage | Payment/business-model milestone/refund tables |

#### Objective

Turn explicit evidence-backed case transitions into one invoice each, apply Node 0 credit, and calculate reproducible earned/uncharged/refunded amounts from immutable state.

#### Scope

- Enrollment/activation/clearance/legal-escrow/pregnancy/birth milestones
- Credit allocation
- Non-clearance and cancellation tables
- Dignity delay for clinical-linked invoices

#### Explicit non-goals

- No unresolved pregnancy-loss automatic disposition
- No promise of reimbursement

#### Expected files or modules

- `app/domain/billing_policy.py`
- `app/domain/refunds.py`
- `app/event_handlers/case_billing.py`
- `tests/python/test_billing_policy.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Internal evidence-to-invoice commands and explainable refund quote. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Only authorized domain events trigger billing. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- All milestone/refund rows
- duplicate/stale transition
- Node 0 credit
- pay-in-full/deposit math
- clinical notification separation

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

Hard dependencies: P08-02, P07-04, P09-04. Parallel opportunities: P08-01

#### Objective acceptance criteria

- [ ] Turn explicit evidence-backed case transitions into one invoice each, apply Node 0 credit, and calculate reproducible earned/uncharged/refunded amounts from immutable state.
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
| Required expertise | payments, commercial policy, case state |
| Higher-capability review | Mandatory before merge |

### P08-04 — Add payment reconciliation and safe service-pause operations

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-04) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P08-03 |
| Blocking decisions/checkpoints | D-COM-08 |
| Source / salvage | Business-model failure handling |

#### Objective

Expose operator-safe reconciliation, discrepancy, receipt, retry, and non-critical pause controls without blocking safety information or altering clinical truth.

#### Scope

- Ledger-vs-processor reconciliation
- Itemized receipt data
- Grace/reminder/soft-pause policy
- Audited manual adjustments

#### Explicit non-goals

- No organization-wide ambient access
- No critical-service lockout

#### Expected files or modules

- `app/payments/reconciliation.py`
- `app/routes/operator_billing.py`
- `app/templates/internal/billing/`
- `tests/python/test_reconciliation.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | Internal role-gated discrepancy and adjustment surface. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Role denial
- mismatch workflow
- manual adjustment audit
- critical content remains accessible
- provider outage

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Metrics/alerts for settlement, refund, mismatch and reserve inputs.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P08-03. Parallel opportunities: P08-01, P08-02

#### Objective acceptance criteria

- [ ] Expose operator-safe reconciliation, discrepancy, receipt, retry, and non-critical pause controls without blocking safety information or altering clinical truth.
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
| Required expertise | payment operations, authorization, observability |
| Higher-capability review | Mandatory before merge |

## 5. Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |

Merge order inside this package: `P08-01` → `P08-02` → `P08-03` → `P08-04`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## 6. Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Webhook replay/order; Ledger invariants; Milestone idempotency; Refund table; Node 0 credit floor; Reconciliation mismatch | Expected state/event/UI and named evidence are produced once. |
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
| Blocking/product/compliance decision | D-COM-01 — Set the flat one-time price and tax treatment; it must remain fully creditable against the later JMF. | Luke | P06-01, P07-01, P08-01; Before activation of a Complete configuration | [D-COM-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-01) — Keep no active production value until explicitly approved; test with synthetic configuration. |
| Blocking/product/compliance decision | D-COM-02 — Ratify $8,900 JMF, $7,830 pay-in-full, $750 deposit and 20/30/20/20/10 post-deposit milestones as configuration v1 with effective date/currency. | Luke | P07-01, P08-01, P08-03; Before P07-01 activation data | [D-COM-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-02) — Use the document anchors but require explicit version activation rather than code literals. |
| Blocking/product/compliance decision | D-COM-03 — Approve the actual paid-service terms, privacy/consent disclosure and refundable-to-earned wording. | Luke | P07-01, P07-02, P08-03; Before P07-02 user acceptance | [D-COM-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-03) — External legal/privacy/finance review before any real acceptance. |
| Blocking/product/compliance decision | D-COM-04 — Define evidence for enrollment funding confirmed, promotion authorization, and for onboarding/compatibility complete enough to move case active and earn/issue activation billing. | Luke | P07-02, P07-03, P07-04, P08-03, P09-04; Before P07-02 | [D-COM-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-04) — Funding confirmation is durable ledger evidence; promotion uses the sole typed authorization event; activation requires an explicit evidence checklist, actor and audit event. |
| Blocking/product/compliance decision | D-PAY-01 — Select processor, card/ACH capabilities, webhook/security/settlement semantics and operational ownership. | Luke | P08-02, P08-03, P08-04; Before P08-02 adapter | [D-PAY-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-PAY-01) — Choose only after domain/ledger contract; retain processor-neutral ports. |
| Blocking/product/compliance decision | D-COM-05 — Select financing partner and define when funding is sufficiently authorized/settled; otherwise hide the path. | Luke | P07-02, P08-02; Before financed option is exposed | [D-COM-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-05) — Do not block card/ACH MVP; keep optional and disabled. |
| Blocking/product/compliance decision | D-COM-06 — Decide retained revenue versus future-journey credit after heartbeat loss and contractual support window. | Luke | P08-03; Before automated pregnancy-stage refund logic | [D-COM-06](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-06) — Manual/counsel-reviewed hook until policy is approved; never hard-code. |
| Blocking/product/compliance decision | D-COM-07 — Ratify earned/uncharged/refunded treatment, GC withdrawal/replacement and pay-in-full/financed reconciliation. | Luke | P08-03; Before real billing | [D-COM-07](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-07) — Use document schedule as test anchor; require legal/finance approval for live policy. |
| Blocking/product/compliance decision | D-COM-08 — Define reminder cadence, grace period, pauseable services and safety-critical/document access that can never be blocked. | Luke | P08-04; Before P08-04 | [D-COM-08](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-COM-08) — Default to continued safety and entitled-document access; pause only clearly non-critical future services. |
| Implementation risk | Double charge/refund | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Processor lock-in | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Clinical timing harm | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Pass-through commingling | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Policy gaps | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| No direct source | — | Build from approved contracts/evidence | Package PRs | New implementation | N/A |

Package source inventory:

- Business-model schedules and smoke paths; no current code is authoritative

## 9. Ownership recommendation

Luke owns price/refund/pause policy; Alan implements. Payment, finance, security, and legal review are required before live money movement.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P08-01 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P08-02 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P08-03 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P08-04 | Alan | Alan (proposed) | Luke | Luke | Mandatory |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
