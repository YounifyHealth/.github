---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 04: Node 0 workspace and paid-case separation"
author: "L. Rhodes (plan owner) - A. Zhao (technical review requested)"
date: "2026-07-10"
---
# Work Package 04: Node 0 workspace and paid-case separation

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP04 |
| Plan file | `WP04 - Node 0 workspace and paid-case separation.md` |
| Proposed PRs | P04-01, P04-02, P04-03 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

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

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P04-01 | Separate Node 0 workspace storage from paid cases | app | P02-03 | A1 | Exceptional | Dependencies unmet |
| 2 | P04-02 | Add attributable workspace revision and projection contracts | app | P04-01 | A1 | Large | Dependencies unmet |
| 3 | P04-03 | Adapt legacy Node 0 case-shaped data without semantic promotion | app | P04-02 | A1 | Large | Dependencies unmet |

### P04-01 - Separate Node 0 workspace storage from paid cases

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A1 / Exceptional / Dependencies unmet |
| Dependencies | P02-03 |
| Blocking decisions/checkpoints | CHECK-ALAN-122-124 |
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

Hard dependencies: P02-03. Parallel opportunities: P04-03

#### Objective acceptance criteria

- [ ] Introduce workspace, workspace membership, candidate, and selection entities so opening Node 0 never creates a canonical paid case.
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
| Required expertise | domain modelling, PostgreSQL, authorization |
| Higher-capability review | Mandatory before merge |

### P04-02 - Add attributable workspace revision and projection contracts

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
| Dependencies | P04-01 |
| Blocking decisions/checkpoints | D-DATA-01, D-DATA-02, CHECK-ALAN-122-124 |
| Source / salvage | Current facts/memory models, GC authorship audit |

#### Objective

Represent IP assertions, GC confirmations, private notes, and reviewer/provider confirmations as attributable append-only revisions with purpose-limited projections.

#### Scope

- Authorship classes and supersedes links
- Verification/visibility/purpose metadata
- Projection allowlists for IP, GC, case, intelligence, provider

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

Hard dependencies: P04-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Represent IP assertions, GC confirmations, private notes, and reviewer/provider confirmations as attributable append-only revisions with purpose-limited projections.
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
| Required expertise | data provenance, privacy, authorization |
| Higher-capability review | Mandatory before merge |

### P04-03 - Adapt legacy Node 0 case-shaped data without semantic promotion

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
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

| Type | ID / risk | Owner | Affected PRs / latest point | Treatment |
| --- | --- | --- | --- | --- |
| Blocking/product/compliance decision | D-DATA-01 - Which provisional IP assertions may the GC see, which GC answers may the IP see, and which fields survive promotion/provider projection? | Luke | P04-02, P06-02, P06-03, P07-03, P07-04, P09-05, P10-01, P10-02; Before P04-02 | D-DATA-01 - Default deny; expose only explicit purpose-limited projections. Class 1/2 and class 4 never automatically cross roles. |
| Blocking/product/compliance decision | D-DATA-02 - How long to retain unselected candidate assertions and how are GC corrections, conflicting relationship answers, and private IP notes represented? | Luke | P04-02, P04-03, P06-02; Before P04-02 | D-DATA-02 - Append revisions with supersedes/derived-from; never silently erase source; shortest justified retention for unselected candidates. |
| Implementation risk | Semantic data corruption during backfill | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Duplicate cases | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Private candidate leakage | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Older app revision writes legacy shape | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#117 | 5ac09f0cdd92 | Deterministic candidate questionnaire, scoring/status calculation, conversation-guide resource, routes and extensive Node 0 tests. | P04-01, P04-02 | Selective port and rewrite | Unextracted; algorithm/test review required after Alan checkpoint and Luke field/score decision. |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P04-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P04-02 | Retain pending Alan reconciliation; selective port or rebase only after architecture approval | Reinspected at latest head. It is exactly e853821 (no newer delta); retention strengthened, but final extraction waits for Alan checkpoint. |
| app#124 | 84a5a847fea7 | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. | P04-01, P04-02, P04-03 | Retain unchanged as evidence; selective port/rewrite after checkpoint | Unextracted; Alan review explicitly incomplete and unresolved. |
| detached candidate rewrite | 9605d88 | substantial uncommitted Node 0 quiz rewrite | P04-02/P05-02 | Selective port from protected worktree | Preserve; compare with predecessor and #117/#124 before any discard. |
| detached predecessor candidate model | dc6a2f0 | substantial uncommitted predecessor model | P04-02/P05-02 if unique | Selective port from protected worktree | Preserve until rewrite diff/extraction ledger is complete. |

Package source inventory:

- PR #124 candidate/outreach behavior and tests by selective port
- PR #122 case projection primitives after reconciliation
- Older candidate-model and rewrite worktrees

## Ownership recommendation

Alan owns domain/schema implementation; Luke approves entity boundaries and promotion contract. Joint high-capability review is mandatory.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P04-01 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P04-02 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P04-03 | Alan | Alan (proposed) | Luke | Luke | Mandatory |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
