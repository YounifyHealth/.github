# Work package 05 — Node 0 Free, Pathfinder, and resume

> Planning-only execution contract. The corrected work-package split remains proposed pending Alan's review. Local preparation and merge readiness are separate; the benched Project catalogue is not resynced. Project reference: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP05 |
| Plan file | `05-node0-free-pathfinder-and-resume.md` |
| Proposed PRs | P05-01, P05-02, P05-03 |
| Inspection snapshot | 2026-07-12 19:30 America/New_York |

## 1. Purpose and outcome

**Problem.** Pathfinder contains service/LLM-era routing complexity and Node 0 Free must satisfy the complete-the-match boundary without payment while preserving explicit IP authorship.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** A deterministic entry router and resumable Node 0 Free flow for education, candidate tracking, preliminary safety checks, outreach guidance, and a willing candidate without a paid case.

**Explicit non-goals.**

- No weighted ranking
- No GC authenticated soft onboarding
- No paid case
- No final Learn content

## 2. Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-010 | verified | app / PR #124@84a5a84 | app/routes/node0.py:63-90 | Opening Node 0 calls create_byos_case_for_ip with is_synthetic=True; there is no separate free workspace or authorized promotion. |
| E-013 | verified | app / PR #124@84a5a84 | app/node0.py:252-482,622-878,975-1001 | Nineteen IP-entered candidate answers about relationship and third-party circumstances/health derive a 0-100 score, readiness/status, ordering, guide route and evidence packet without per-field provenance or verification. |
| E-028 | verified review | app / PR #124 comment 4948149089 | Consolidated review — findings for the WP00 extraction ledger | Alan's completed review classifies #124 as high-value extraction material rather than a merge unit and identifies transaction, privacy, scoring, access, validation, invariant, exposure, retention, performance, CSS and CI findings. |

## 3. Architecture and contracts

- Routing is deterministic policy, not LLM authority.
- Candidate responses are provisional IP assertions, never GC-authored or medically verified facts.
- Safety-critical information and complete-the-match capability remain free.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`; repository-specific PRs remain separate. |
| Entities/state | `entry_session`, `node0_workspace` |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Deterministic route decision response with policy version. Typed workspace-scoped commands reject malformed/oversize input and return neutral questions to clarify, never eligibility flags. UI calls workspace-scoped commands only. |
| Storage | Use workspace candidates/assertions from WP04 with FKs, uniqueness and one-active-outreach invariants. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

### Applicable state machines

### Participant entry and routing (`entry_session`)

Owner: **natalyx-app**. States: `unstarted`, `education`, `identity_required`, `authenticated`, `routed`, `handed_off`, `expired`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unstarted | education | visitor | GET/explicit entry choice | entry:{session}:start | No participant/case write | entry_started | Return current session | Create fresh anonymous session |
| education | identity_required | visitor/policy | route requires saved workspace | entry:{session}:identity | Cannot grant workspace/case | identity_required | Preserve safe return intent | Restart at public choice |
| identity_required | authenticated | Cognito/auth provider | verified subject/session | auth:{subject}:{nonce} | Invalid/expired token | identity_bound | Replay returns authenticated session | Rechallenge; no partial membership |
| education\|authenticated | routed | participant + deterministic policy | validated route answers + policy version | route:{session}:{answer_hash} | Unknown/unsafe route goes review/education | entry_routed | Same input returns same decision | Allow corrected answers/new decision revision |
| routed | handed_off | participant | accepted destination and authorized target | handoff:{session}:{route_version} | Target not authorized/available | entry_handed_off | Resume same safe destination | Return to route result with explanation |
| any nonterminal | expired | system | TTL elapsed/revoked session | entry:{session}:expire | No transition from handed_off needed | entry_expired | Idempotent | New session; no case/access change |

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

### Data authorship/provenance rules

- Every assertion/revision records subject_ref, semantic_key, author_subject/person/role, authorship_class, provenance, verification_status, visibility, purpose, source_ref, derived_from, supersedes_id, promotion_event_id, policy version and immutable timestamps.
- Class 1 defaults IP-private; class 2 defaults IP-private/internal and visibly says reported by the intended parent, not confirmed by the GC.
- Class 3 is GC-authored and shared only per field/purpose; class 4 is GC-only private; class 5 requires an evidence-linked role-gated reviewer/provider rail.
- GC confirmation appends a class-3 revision referencing the class-2 assertion. Relationship answers can coexist; disagreement is not an overwrite.
- Unselected candidates, raw health assertions, ranking scores and private IP notes do not promote. Derived values inherit the weakest source status.
- Copying, promotion, generic proposal approval, IP assertion or AI inference can never create Natalyx-reviewed, provider-confirmed, medically cleared, legally cleared or insurance-verified truth.

## 4. Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Local preparation | Merge readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P05-01 | Replace Pathfinder routing with deterministic entry decisions | app | P03-01, P04-01 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P03-01, P04-01; Gate A0 active and verified; Alan review |
| 2 | P05-02 | Rebuild Node 0 Free candidate and outreach domain | app | P04-02, P05-01 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P04-02, P05-01; Gate A0 active and verified; Alan review |
| 3 | P05-03 | Ship resumable Node 0 Free participant surface | app | P03-01, P05-02, P11-03 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P03-01, P05-02, P11-03; Gate A0 active and verified; Alan review |

### P05-01 — Replace Pathfinder routing with deterministic entry decisions

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P05-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-01) |
| Gate / size | A1 / Medium |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P03-01, P04-01; Gate A0 active and verified; Alan review |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P03-01, P04-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Current pathfinder_destinations.py, PR #119 product-alignment doc |

#### Objective

Route users predictably to Node 0, full IP setup, GC claim, Learn/Ask education, or provider/partner paths using explicit inputs and policy versioning.

#### Scope

- Small versioned decision table
- Clear reason/next-step output
- No LLM dependency for route selection

#### Explicit non-goals

- No final educational content
- No eligibility clearance

#### Expected files or modules

- `app/pathfinder_destinations.py`
- `app/pathfinder_policy.py`
- `app/routes/participant.py`
- `tests/python/test_pathfinder_policy.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Deterministic route decision response with policy version. |
| UI/product surface | Clear entry choices and safe review states. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Decision table coverage
- ambiguous/malformed inputs
- GC invite deep link
- service unavailable
- mobile entry

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P03-01, P04-01. Parallel opportunities: P05-03

#### Objective acceptance criteria

- [ ] Route users predictably to Node 0, full IP setup, GC claim, Learn/Ask education, or provider/partner paths using explicit inputs and policy versioning.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Luke |
| Primary implementer | Luke (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Alan |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P05-02 — Rebuild Node 0 Free candidate and outreach domain

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P05-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-02) |
| Gate / size | A1 / Exceptional |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P04-02, P05-01; Gate A0 active and verified; Alan review |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P04-02, P05-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PR #117 direct algorithm/test salvage, PR #124, quiz rewrite worktree |

#### Objective

Port the useful deterministic candidate, preliminary safety, and outreach behavior onto workspace/provenance contracts while preserving the complete-the-match free boundary.

#### Scope

- Unlimited candidates under bounded command/collection sizes
- Minimum-necessary relationship, outreach and logistics questions only
- Basic outreach sequencing and shareable intro packet
- Migration-backed case/workspace/candidate/outreach constraints
- Batched hydration plus archive/anonymize/delete behavior under D-DATA-02

#### Explicit non-goals

- No weighted ranking or suitability score
- No IP-entered health, substance, mental-health, citizenship, race or eligibility data
- No medical clearance
- No paid feature

#### Expected files or modules

- `app/domain/node0_candidates.py`
- `app/storage/node0.py`
- `app/node0_conversation_guide.py`
- `app/resources/node0_conversation_guide_v1.json`
- `tests/python/test_node0_domain.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Use workspace candidates/assertions from WP04 with FKs, uniqueness and one-active-outreach invariants. |
| API/routes | Typed workspace-scoped commands reject malformed/oversize input and return neutral questions to clarify, never eligibility flags. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Allowed/blocked field matrix
- no ranking/gating
- strict enum/body/collection limits
- author attribution
- candidate isolation
- concurrent outreach invariant
- retention/deletion
- query-count bound
- free feature contract

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

Hard dependencies: P04-02, P05-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Port the useful deterministic candidate, preliminary safety, and outreach behavior onto workspace/provenance contracts while preserving the complete-the-match free boundary.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Luke |
| Primary implementer | Luke (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Alan |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

### P05-03 — Ship resumable Node 0 Free participant surface

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P05-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-03) |
| Gate / size | A1 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P03-01, P05-02, P11-03; Gate A0 active and verified; Alan review |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P03-01, P05-02, P11-03 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PRs #121/#124 selective UI port, DS PR #8 |

#### Objective

Provide a coherent mobile-capable Node 0 Free workspace shell for candidate tracking, outreach, guide use, and resume without paid-case language.

#### Scope

- Workspace home and candidate flow
- Shared IP-owner guard across participant and API routes
- Exact public/cloud exposure registry
- Expiry-aware token views and no-store/referrer/noindex response policy
- Route-scoped Node 0 stylesheet
- Honest preliminary labels/empty/error states
- Logout/login resume and mobile navigation

#### Explicit non-goals

- No Complete-only features
- No paid case/journey hero

#### Expected files or modules

- `app/routes/node0.py`
- `app/node0_surface.py`
- `app/templates/node0/*.html`
- `app/static/node0.*`
- `tests/python/test_node0_ui.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | UI calls workspace-scoped commands only. |
| UI/product surface | Participant DS recipes with responsive interaction and no fake content. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Clickable Free path
- GC/viewer/staff/nonowner denial without 500
- exact route exposure negatives
- expired-token GET
- cache/referrer headers
- malformed/oversize form/PDF input
- resume
- no-JS/keyboard
- 320/375/768px
- dependency failure

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P03-01, P05-02, P11-03. Parallel opportunities: P05-01

#### Objective acceptance criteria

- [ ] Provide a coherent mobile-capable Node 0 Free workspace shell for candidate tracking, outreach, guide use, and resume without paid-case language.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Luke |
| Primary implementer | Luke (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Alan |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

## 5. Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |

Merge order inside this package: `P05-01` → `P05-02` → `P05-03`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## 6. Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | All deterministic route outcomes; Free candidate/outreach boundary; Resume across sessions; Critical-flag fail-safe; Mobile interaction | Expected state/event/UI and named evidence are produced once. |
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

Founder outcomes, Alan's remaining technical ownership and external activation dependencies are recorded separately so a final policy is never mistaken for an active control.

| ID | Status | Classification | Remaining owner | Affected / latest | Programme effect |
| --- | --- | --- | --- | --- | --- |
| D-DATA-03 | Resolved by reconciliation | Reconciliation settled | Alan - implementation | P05-02, P06-03; Resolved 2026-07-12 | No longer blocks Node 0 implementation planning. |

### D-DATA-03 - Candidate scoring and sensitive preference policy

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final |
| Founder outcome | No candidate ranking, viability/eligibility flag or race preference survives; provisional pre-join input can generate neutral source-labelled questions only. |
| Founder constraints | No sensitive third-party scoring or gating; No provisional assertion becomes GC/provider truth |
| What remains for Alan | Remove legacy ranking/gating and preserve neutral-question behavior |
| Evidence required | Prohibited-field and no-ranking tests |
| Approval rule | No further founder decision unless ranking or eligibility behavior is proposed. |
| External dependencies | None |
| Affected PRs / latest point | P05-02, P06-03; Resolved 2026-07-12 |
| Programme effect | No longer blocks Node 0 implementation planning. |
| Independent recommendation | No ranking, viability/eligibility flag or race preference survives. Pre-join IP input is limited to minimum-necessary relationship/outreach/logistics context and may produce neutral source-labelled questions only; it never gates claim, onboarding, provider use or critical decisions. |

| Implementation risk | Owner | Treatment |
| --- | --- | --- |
| Paid features leak into Free | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Provisional score is overclaimed | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Route drift | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| LLM dependency reintroduced | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#117 | 5ac09f0cdd92 | Deterministic candidate questionnaire, scoring/status calculation, conversation-guide resource, routes and extensive Node 0 tests. | P05-02, P05-03 | Selective port and rewrite | Unextracted; algorithm/test review required after Alan checkpoint and Luke field/score decision. |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P05-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#121 | 529d377e2337 | Primary Node 0 participant model/UI, PDF/guide presentation and focused surface tests. | P05-03 | Selective UI/test port, then supersede | Unextracted; #124 may contain later copies but equivalence must be proved by file/commit comparison. |
| app#124 | 84a5a847fea7 | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. | P05-02, P05-03 | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. |
| detached candidate rewrite | 9605d88 | substantial uncommitted Node 0 quiz rewrite | P04-02/P05-02 | Selective port from protected worktree | Preserve; compare with predecessor and #117/#124 before any discard. |
| detached predecessor candidate model | dc6a2f0 | substantial uncommitted predecessor model | P04-02/P05-02 if unique | Selective port from protected worktree | Preserve until rewrite diff/extraction ledger is complete. |

Package source inventory:

- PR #117 quiz/guide algorithms and tests
- PR #121 primary surface
- PR #124 consolidated UI
- Quiz rewrite worktree

## 9. Ownership recommendation

Luke is the proposed DRI and primary implementer; Alan reviews the technical architecture, security and failure behavior. Reconciliation is complete; replacement work waits for WP03/WP04 contracts, and commit/PR/merge waits for Alan's review and joint package acceptance.

| PR | WP DRI | Primary implementer | Technical-decision owner | Reviewer | Final approver | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| P05-01 | Luke | Luke (proposed) | None; implement the settled founder constraints and approved contracts | Alan | Luke | None |
| P05-02 | Luke | Luke (proposed) | None; implement the settled founder constraints and approved contracts | Alan | Luke | None |
| P05-03 | Luke | Luke (proposed) | None; implement the settled founder constraints and approved contracts | Alan | Luke | None |

PR ownership inherits the proposed work-package split pending Alan's review. Named technical-decision ownership remains separate and never transfers implementation ownership across work packages; reciprocal and external review requirements remain intact.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
