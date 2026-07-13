# Work package 12 — Ask/Learn shell and mobile cutover

> Planning-only execution contract. The corrected work-package split remains proposed pending Alan's review. Local preparation and merge readiness are separate; the benched Project catalogue is not resynced. Project reference: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP12 |
| Plan file | `12-ask-learn-shell-and-mobile-cutover.md` |
| Proposed PRs | P12-01, P12-02, P12-03 |
| Inspection snapshot | 2026-07-12 19:30 America/New_York |

## 1. Purpose and outcome

**Problem.** Participant Ask/Learn entry points, case shell, legacy routes, and mobile interactions are not yet one coherent clickable journey with explicit context boundaries.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** A unified scope-labelled Ask/Learn shell, accessible mobile participant journey, and verified redirect-based legacy cutover with no broken or misleading controls.

**Explicit non-goals.**

- No final content authoring
- No staff/operator redesign
- No broad visual rebrand
- No removal before telemetry proves safe

## 2. Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-006 | verified | app / PR #122@e853821 | PR comment Review round 2 addressed and changed workflow/tests | Updated PR #122 reports 499 tests plus return_to, TTL, CAS, self-invite, lens and Learn fail-closed fixes; green checks were observed. These are salvage candidates, not blanket merge approval. |
| E-012 | verified | app / PR #122@e853821 | app/storage/invitations.py and PR review-round comment | The updated case invitation work adds 14-day ceiling, CAS transitions, mismatch confirmation, self-invite refusal, return_to preservation and paired lens tests; it has no Node 0 workspace target. |
| E-024 | verified | design-system / main@43dab986; PR #7@cedfcc4; PR #8@4656426 | components, tokens, Jinja attrs/parity guidance | Participant DS recipes and parity guidance exist; local brand assets are also dirty. Internal/operator DS is a separate repository and boundary. |
| E-029 | verified preserved branch | app / feat/byos-journey-wave-2@5b63e3a7 | exact three-commit stack on e853821 | Wave 2 contains phase-1 cluster pages, metadata-only request/review, case anchoring and role/owner fixes. Controlled local evidence passed 535 tests with 9 skipped and 36/36 focused tests, but no branch checks, PostgreSQL, browser/accessibility or visual run exists. |

## 3. Architecture and contracts

- The shell labels general, private, and shared-case context and never implies a source exists when it does not.
- Server owns state and permissions; client code enhances interaction only.
- Legacy routes redirect through allowlisted, telemetry-observed compatibility paths before deletion.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`; repository-specific PRs remain separate. |
| Entities/state | No new runtime entity; evidence/coordination only. |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Pass versioned scoped envelopes only. Stable redirects with query sanitization. |
| Storage | No new storage; preserve current state read-only for this package. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

## 4. Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Local preparation | Merge readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P12-01 | Unify Ask and Learn shell with explicit context scopes | app | P10-03, P11-04, P09-04 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P10-03, P11-04, P09-04; technical decisions/controls D-AI-01; Gate A0 active and verified; Alan review |
| 2 | P12-02 | Complete mobile participant interaction and accessibility cutover | app | P05-03, P06-03, P09-04, P09-06, P12-01 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P05-03, P06-03, P09-04, P09-06, P12-01; Gate A0 active and verified; Alan review |
| 3 | P12-03 | Retire legacy participant routes behind verified redirects | app | P12-02, P13-04 | B1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P12-02, P13-04; Gate A0 active and verified; Alan review |

### P12-01 — Unify Ask and Learn shell with explicit context scopes

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P12-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-01) |
| Gate / size | A2 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P10-03, P11-04, P09-04; technical decisions/controls D-AI-01; Gate A0 active and verified; Alan review |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Dependencies | P10-03, P11-04, P09-04 |
| Blocking decisions/checkpoints | D-AI-01 |
| Source / salvage | Current Ask widget/Learn workspace, PR #124 |

#### Objective

Present general Learn, private personalization, and approved shared-case Ask as visibly distinct contexts with source cards and safe switching.

#### Scope

- Context scope badge/selector
- Suggested questions and citations
- Boundary and unavailable states
- Case-aware authorization

#### Explicit non-goals

- No context merge
- No case fact write

#### Expected files or modules

- `app/ask_natalyx.py`
- `app/templates/ask_natalyx*.html`
- `app/templates/learn_workspace.html`
- `app/static/js/learn_chat.js`
- `tests/python/test_ask_learn_shell.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Pass versioned scoped envelopes only. |
| UI/product surface | Unified but scope-explicit shell. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- General/private/shared views
- wrong-case denial
- logout/login
- empty/failure
- mobile/keyboard/screen-reader

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

Hard dependencies: P10-03, P11-04, P09-04. Parallel opportunities: P12-03

#### Objective acceptance criteria

- [ ] Present general Learn, private personalization, and approved shared-case Ask as visibly distinct contexts with source cards and safe switching.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Luke |
| Primary implementer | Luke (proposed; pending Alan review) |
| Technical-decision owner | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism |
| Reviewer | Alan |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | privacy UX, FastAPI/Jinja, accessibility |
| Higher-capability review | Mandatory before merge |

### P12-02 — Complete mobile participant interaction and accessibility cutover

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P12-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-02) |
| Gate / size | A2 / Exceptional |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P05-03, P06-03, P09-04, P09-06, P12-01; Gate A0 active and verified; Alan review |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P05-03, P06-03, P09-04, P09-06, P12-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PR #122 mobile journey, PR #124 Node 0, DS PR #8 |

#### Objective

Run a bounded participant-only mobile/accessibility pass across entry, auth, Node 0, GC claim, case, documents, Ask, and Learn using the released DS contract.

#### Scope

- Navigation/forms/cards/dialogs
- 320/375/768 widths
- Keyboard/focus/reduced motion
- Error/loading/empty states

#### Explicit non-goals

- No internal/operator surface
- No visual rebrand
- No zero-hex purity gate

#### Expected files or modules

- `app/templates/participant*/`
- `app/templates/node0/`
- `app/templates/case/`
- `app/static/participant*/`
- `tests/browser/participant_mobile.spec.*`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | Participant interaction defects and concrete DS adoption only. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- All required clickable journeys
- axe/manual keyboard
- reduced motion
- orientation/zoom
- slow dependency

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

Hard dependencies: P05-03, P06-03, P09-04, P09-06, P12-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Run a bounded participant-only mobile/accessibility pass across entry, auth, Node 0, GC claim, case, documents, Ask, and Learn using the released DS contract.
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
| Required expertise | responsive UI, accessibility, browser testing |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P12-03 — Retire legacy participant routes behind verified redirects

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P12-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-03) |
| Gate / size | B1 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P12-02, P13-04; Gate A0 active and verified; Alan review |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P12-02, P13-04 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Current route inventory, PRs #112/#119 planning maps |

#### Objective

Move legacy participant entry/case/Ask/Learn routes behind allowlisted redirects and telemetry, then remove only after a measured compatibility window.

#### Scope

- Route inventory and redirect map
- Bookmark/return_to compatibility
- Telemetry and rollback flag
- Later dead-code removal

#### Explicit non-goals

- No immediate destructive deletion
- No operator route change

#### Expected files or modules

- `app/routes/participant*.py`
- `app/main.py`
- `tests/python/route_inventory.json`
- `docs/runbooks/legacy-cutover.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Stable redirects with query sanitization. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Every legacy route
- query/open-redirect safety
- stale bookmarks
- rollback flag
- route parity

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **B1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Legacy hit counters and unknown-route alerts.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P12-02, P13-04. Parallel opportunities: P12-01

#### Objective acceptance criteria

- [ ] Move legacy participant entry/case/Ask/Learn routes behind allowlisted redirects and telemetry, then remove only after a measured compatibility window.
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

Merge order inside this package: `P12-01` → `P12-02` → `P12-03`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## 6. Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Clickable IP/GC flows; Context labels; No-JS/reduced-motion/keyboard; Mobile widths; Redirect and stale bookmark; Logout/login/resume | Expected state/event/UI and named evidence are produced once. |
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
| D-AI-01 | Founder scope/cost final; Alan later; PHI externally gated | Luke sets scope and cost; Alan decides implementation later | Alan - later before P10-01 | P10-01, P10-02, P10-03, P12-01; Before P10-01 | P10/P12 synthetic planning may proceed; implementation completion waits for Alan's technical decision and PHI remains blocked through B2. |

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
| Context ambiguity | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Mobile-only dead ends | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Premature legacy removal | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Design drift | Luke | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#112 | 9605d88e31bd | Source-first 81-node/12-cluster surface map, participant-renderer boundaries, wave plan and cross-repo seams. | P12-03 | Selective port, then supersede after extraction | Catalogued; content remains to be reconciled into replacement PR acceptance tests. |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P12-03 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#121 | 529d377e2337 | Primary Node 0 participant model/UI, PDF/guide presentation and focused surface tests. | P12-02 | Selective UI/test port, then supersede | Unextracted; #124 may contain later copies but equivalence must be proved by file/commit comparison. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P12-02 | Selective-port behavior and tests; supersede as programme architecture | Complete at e853821: authoritative behavior/tests and selectively portable implementation are classified; superseded architecture and evidence-only claims are named. |
| app#124 | 84a5a847fea7 | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. | P12-02 | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. |
| ds#8 | 4656426e493e | Consumer parity and bounded app-owned layout guidance for Node 0/case/mobile adoption. | P12-02 | Prefer direct review/merge if still correct | Direct-reuse candidate; local dirty asset delta separately protected. |
| feat/byos-journey-wave-2 | 5b63e3a7c364 | Projection-driven phase-1 cluster presentation, exact route allowlisting, person-versus-case-side ownership intent, transactional submission/work-item and review/audit patterns, fail-closed item retention, approved Learn status selection and 36 focused tests. | P12-02 | Preserve paused at the exact head; selectively port semantics/tests only after adaptation. Do not merge, cherry-pick, continue implementation or use its runtime schema directly. | Paused exact-head evidence; no direct merge |

Package source inventory:

- PR #122 responsive journey and lens behavior
- PR #124 Node 0 surfaces
- DS PR #8 parity guidance

## 9. Ownership recommendation

Luke is the proposed DRI and primary implementer for the participant shell and cutover. Alan reviews technical integration, authorization and failure behavior; accessibility review remains required where named.

| PR | WP DRI | Primary implementer | Technical-decision owner | Reviewer | Final approver | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| P12-01 | Luke | Luke (proposed) | D-AI-01: Alan - later model/retrieval/schema/fallback mechanism | Alan | Luke | None |
| P12-02 | Luke | Luke (proposed) | None; implement the settled founder constraints and approved contracts | Alan | Luke | None |
| P12-03 | Luke | Luke (proposed) | None; implement the settled founder constraints and approved contracts | Alan | Luke | None |

PR ownership inherits the proposed work-package split pending Alan's review. Named technical-decision ownership remains separate and never transfers implementation ownership across work packages; reciprocal and external review requirements remain intact.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
