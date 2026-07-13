---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 04: Node 0 workspace and paid-case separation"
author: "L. Rhodes (plan owner) - A. Zhao (technical feedback reconciled)"
date: "2026-07-12"
---
# Work Package 04: Node 0 workspace and paid-case separation

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP04 |
| Plan file | `WP04 - Node 0 workspace and paid-case separation.md` |
| Proposed PRs | P04-01, P04-02, P04-03 |
| Inspection snapshot | 2026-07-12 19:30 America/New_York |

## Purpose and outcome

**Problem.** PR #124 creates a synthetic canonical case as soon as Node 0 is opened, collapsing free exploration, workspace membership, commercial commitment, and paid-case truth.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** A distinct Node 0 workspace aggregate with attributable revisions and an idempotent, purpose-limited projection into one paid case only after the authorized commercial event.

**Explicit non-goals.**

- No payment processor
- No full Node 0 UI
- No clinical or legal truth promotion
- No deletion of legacy rows during compatibility window

## Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-010 | verified | app / PR #124@84a5a84 | app/routes/node0.py:63-90 | Opening Node 0 calls create_byos_case_for_ip with is_synthetic=True; there is no separate free workspace or authorized promotion. |
| E-011 | verified | app / PR #124@84a5a84 | app/storage/node0.py:400-462; app/routes/node0.py:605-652 | Node 0 can issue an unaddressed GC invitation and redemption ultimately creates case membership, conflating low-risk onboarding possession with case access. |
| E-013 | verified | app / PR #124@84a5a84 | app/node0.py:252-482,622-878,975-1001 | Nineteen IP-entered candidate answers about relationship and third-party circumstances/health derive a 0-100 score, readiness/status, ordering, guide route and evidence packet without per-field provenance or verification. |
| E-014 | verified | app / PR #124@84a5a84 | app/storage/node0.py:42-200,509-600; tests/python/test_node0.py:444-490 | IP/co-IP own candidate reads; GC onboarding writes separate shared/private facts and does not revise the IP assertion. The GC cannot see or correct the IP candidate record. |
| E-015 | verified | app / PR #122@e853821 | app/storage/facts.py:19-69,107-127 | Facts have broad provenance and visibility values but no subject-versus-author role, verification state, derived-from, or supersedes link. |
| E-028 | verified review | app / PR #124 comment 4948149089 | Consolidated review - findings for the WP00 extraction ledger | Alan's completed review classifies #124 as high-value extraction material rather than a merge unit and identifies transaction, privacy, scoring, access, validation, invariant, exposure, retention, performance, CSS and CI findings. |

## Architecture and contracts

- Workspace, entitlement, commercial, payment, and case lifecycles are separate entities and state machines.
- Promotion copies only allowlisted projections with provenance, visibility, and verification intact.
- Compatibility adapters read old case-shaped Node 0 records while new writes target the workspace model.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`; repository-specific PRs remain separate. |
| Entities/state | `node0_workspace` |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | No broad public contract; use the focused commands/events in each PR. |
| Storage | Add node0_workspaces, workspace_memberships, candidate assertion linkage and constraints. Append-only assertion/revision and projection-audit records. Idempotent backfill with source identifiers and exception report. |
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
| 1 | P04-01 | Separate Node 0 workspace storage from paid cases | app | P02-03, P03-05 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P02-03, P03-05; Gate A0 active and verified; Luke review/final founder approval |
| 2 | P04-02 | Add attributable workspace revision and projection contracts | app | P04-01, P03-05 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P04-01, P03-05; Gate A0 active and verified; Luke review/final founder approval |
| 3 | P04-03 | Adapt legacy Node 0 case-shaped data without semantic promotion | app | P04-02 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P04-02; Gate A0 active and verified; Luke review/final founder approval |

### P04-01 - Separate Node 0 workspace storage from paid cases

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size | A1 / Exceptional |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P02-03, P03-05; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P02-03, P03-05 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PR #124 _ensure_node0_case as behavior to replace, candidate worktrees |

#### Objective

Introduce workspace, workspace membership, candidate, and selection entities so opening Node 0 never creates a canonical paid case.

#### Scope

- Workspace aggregate and memberships
- Candidate rows linked to workspace
- Case tables remain paid/manageable aggregate

#### Explicit non-goals

- No UI rewrite
- No promotion
- No legacy deletion

#### Expected files or modules

- `migrations/versions/*_node0_workspaces.py`
- `app/storage/workspaces.py`
- `app/storage/workspace_memberships.py`
- `app/storage/node0.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Add node0_workspaces, workspace_memberships, candidate assertion linkage and constraints. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Expand only; old records remain readable. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Opening Node 0 creates no case
- workspace authorization
- candidate isolation
- concurrent workspace creation
- old app compatibility

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P02-03, P03-05. Parallel opportunities: P04-03

#### Objective acceptance criteria

- [ ] Introduce workspace, workspace membership, candidate, and selection entities so opening Node 0 never creates a canonical paid case.
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
| Required expertise | domain modelling, PostgreSQL, authorization |
| Higher-capability review | Mandatory before merge |

### P04-02 - Add attributable workspace revision and projection contracts

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size | A1 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P04-01, P03-05; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P04-01, P03-05 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Current facts/memory models, GC authorship audit |

#### Objective

Represent IP assertions, GC confirmations, private notes, and reviewer/provider confirmations as attributable append-only revisions with purpose-limited projections.

#### Scope

- Authorship classes and supersedes links
- Verification/visibility/purpose metadata
- Projection allowlists for IP, GC, case, intelligence, provider
- Person-owned private-note contract and explicit-share projection

#### Explicit non-goals

- No provider transmission
- No silent in-place overwrite

#### Expected files or modules

- `migrations/versions/*_authored_assertions.py`
- `app/storage/assertions.py`
- `app/domain/projections.py`
- `tests/python/test_authorship_projections.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Append-only assertion/revision and projection-audit records. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Default deny between roles; explicit purpose projection. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- IP provisional remains attributed
- GC revision does not erase source
- private cross-role denial
- AI cannot upgrade verification
- provider projection allowlist

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P04-01, P03-05. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Represent IP assertions, GC confirmations, private notes, and reviewer/provider confirmations as attributable append-only revisions with purpose-limited projections.
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
| Required expertise | data provenance, privacy, authorization |
| Higher-capability review | Mandatory before merge |

### P04-03 - Adapt legacy Node 0 case-shaped data without semantic promotion

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size | A1 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P04-02; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P04-02 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PRs #117/#121/#123/#124 and dirty candidate worktrees |

#### Objective

Provide a compatibility reader and controlled backfill that maps existing Node 0 rows to workspaces while preserving provenance and never treating legacy scores as verified truth.

#### Scope

- Dry-run audit and deterministic mapping
- Dual-read compatibility window
- Forward repair and per-row exception ledger

#### Explicit non-goals

- No destructive legacy cleanup
- No case creation

#### Expected files or modules

- `migrations/versions/*_node0_legacy_backfill.py`
- `app/storage/node0_compat.py`
- `scripts/audit_node0_backfill.py`
- `tests/fixtures/node0_legacy/`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Idempotent backfill with source identifiers and exception report. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Legacy fixtures
- retry after interruption
- duplicate prevention
- mixed old/new writes
- privacy/provenance preservation

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Counts/checksums and unmapped-row alerts.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P04-02. Parallel opportunities: P04-01

#### Objective acceptance criteria

- [ ] Provide a compatibility reader and controlled backfill that maps existing Node 0 rows to workspaces while preserving provenance and never treating legacy scores as verified truth.
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
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

## Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |

Merge order inside this package: `P04-01` → `P04-02` → `P04-03`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | One workspace/one promotion; Retry/concurrency; No implicit fact upgrade; Private candidate isolation; Old/new revision coexistence | Expected state/event/UI and named evidence are produced once. |
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
| D-AUTH-03 | Resolved by reconciliation | Reconciliation settled | Alan - implementation | P03-02, P03-03, P03-05, P04-01, P04-02, P09-04, P13-05; Resolved 2026-07-12 | No longer blocks the reconciled access/workspace PR sequence. |
| D-DATA-01 | Founder decision final; implementation evidence pending | Luke decides product/privacy outcome | Alan - implementation | P04-02, P06-02, P06-03, P07-03, P07-04, P09-05, P10-01, P10-02; Before P04-02 | Founder ambiguity is removed across WP04, WP06, WP07, WP09 and WP10; A1 still requires the technical denial evidence. |
| D-DATA-02 | Founder default final; external validation before B1 | Luke decides default; external specialist validates | Alan - implementation; privacy/legal - validation | P04-02, P04-03, P06-02; Before P04-02 | Synthetic implementation may proceed; real-user B1 activation remains externally dependent. |

### D-AUTH-03 - Identity, participation and access authorization contract

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final |
| Founder outcome | Identity, participation, access grants, ownership and operation authorization remain separate; participation or lens alone never authorizes. |
| Founder constraints | Subject-derived authorization context; Application and RLS policy parity; Default-deny cross-resource access |
| What remains for Alan | Encode the settled contract in application services and RLS |
| Evidence required | Participation-without-grant and grant-without-capability denials; Application/RLS parity tests |
| Approval rule | No further founder decision unless the boundary changes. |
| External dependencies | None |
| Affected PRs / latest point | P03-02, P03-03, P03-05, P04-01, P04-02, P09-04, P13-05; Resolved 2026-07-12 |
| Programme effect | No longer blocks the reconciled access/workspace PR sequence. |
| Independent recommendation | Identity binds principal to person; participation records domain relationship; grants carry resource-scoped capabilities; application and RLS consume a subject-derived context plus ownership and purpose. Participation/lens alone never authorizes. |

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

### D-DATA-02 - Correction, supersession and unselected-candidate retention

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final founder default; externally dependent activation |
| Founder outcome | Retain candidate/workspace material for a 90-day minimum after explicit rejection, withdrawal or last legitimate outreach, honor earlier valid deletion, retain only non-identifying funnel metrics and a minimal audit tombstone, and preserve legal holds. Corrections append source-labelled revisions and private IP notes remain author-only. |
| Founder constraints | No silent overwrite; Deletion and anonymization are auditable; Legal holds override ordinary deletion |
| What remains for Alan | Implement lifecycle, deletion, anonymization, correction and legal-hold behavior |
| Evidence required | Retention/deletion tests; Anonymization and tombstone evidence; Privacy/legal approval before B1 |
| Approval rule | Luke accepts the live policy after privacy/legal review. |
| External dependencies | Privacy/legal validation before B1 |
| Affected PRs / latest point | P04-02, P04-03, P06-02; Before P04-02 |
| Programme effect | Synthetic implementation may proceed; real-user B1 activation remains externally dependent. |
| Independent recommendation | Append revisions with supersedes/derived-from; never silently erase source; shortest justified retention for unselected candidates. |

| Implementation risk | Owner | Treatment |
| --- | --- | --- |
| Semantic data corruption during backfill | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Duplicate cases | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Private candidate leakage | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Older app revision writes legacy shape | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#117 | 5ac09f0cdd92 | Deterministic candidate questionnaire, scoring/status calculation, conversation-guide resource, routes and extensive Node 0 tests. | P04-01, P04-02 | Selective port and rewrite | Unextracted; algorithm/test review required after Alan checkpoint and Luke field/score decision. |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P04-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P04-02 | Selective-port behavior and tests; supersede as programme architecture | Complete at e853821: authoritative behavior/tests and selectively portable implementation are classified; superseded architecture and evidence-only claims are named. |
| app#124 | 84a5a847fea7 | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. | P04-01, P04-02, P04-03 | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. |
| detached candidate rewrite | 9605d88 | substantial uncommitted Node 0 quiz rewrite | P04-02/P05-02 | Selective port from protected worktree | Preserve; compare with predecessor and #117/#124 before any discard. |
| detached predecessor candidate model | dc6a2f0 | substantial uncommitted predecessor model | P04-02/P05-02 if unique | Selective port from protected worktree | Preserve until rewrite diff/extraction ledger is complete. |

Package source inventory:

- PR #124 candidate/outreach behavior and tests by selective port
- PR #122 case projection primitives after reconciliation
- Older candidate-model and rewrite worktrees

## Ownership recommendation

Alan owns domain/schema implementation; Luke approves entity boundaries and promotion contract. Joint high-capability review is mandatory.

| PR | WP DRI | Primary implementer | Technical-decision owner | Reviewer | Final approver | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| P04-01 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |
| P04-02 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |
| P04-03 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |

PR ownership inherits the proposed work-package split pending Alan's review. Named technical-decision ownership remains separate and never transfers implementation ownership across work packages; reciprocal and external review requirements remain intact.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
