# Work package 12 — Ask/Learn shell and mobile cutover

> Planning-only execution contract. Proposed implementers and owners remain recommendations until Alan reviews/signs off the consolidated plan and Luke accepts it. Project: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP12 |
| Plan file | `12-ask-learn-shell-and-mobile-cutover.md` |
| Proposed PRs | P12-01, P12-02, P12-03 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

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

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P12-01 | Unify Ask and Learn shell with explicit context scopes | app | P10-03, P11-04, P09-04 | A2 | Large | Dependencies unmet |
| 2 | P12-02 | Complete mobile participant interaction and accessibility cutover | app | P05-03, P06-03, P09-04, P12-01 | A2 | Exceptional | Dependencies unmet |
| 3 | P12-03 | Retire legacy participant routes behind verified redirects | app | P12-02, P13-04 | B1 | Large | Dependencies unmet |

### P12-01 — Unify Ask and Learn shell with explicit context scopes

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P12-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-01) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | privacy UX, FastAPI/Jinja, accessibility |
| Higher-capability review | Mandatory before merge |

### P12-02 — Complete mobile participant interaction and accessibility cutover

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P12-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-02) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P05-03, P06-03, P09-04, P12-01 |
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

Hard dependencies: P05-03, P06-03, P09-04, P12-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Run a bounded participant-only mobile/accessibility pass across entry, auth, Node 0, GC claim, case, documents, Ask, and Learn using the released DS contract.
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
| Required expertise | responsive UI, accessibility, browser testing |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P12-03 — Retire legacy participant routes behind verified redirects

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P12-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-03) |
| Gate / size / readiness | B1 / Large / Dependencies unmet |
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

| Type | ID / risk | Owner | Affected PRs / latest point | Project item / treatment |
| --- | --- | --- | --- | --- |
| Blocking/product/compliance decision | D-AI-01 — Approve scopes, allowed sources, model policy, proposal reviewers, class-5 evidence rail and degraded-mode copy. | Luke | P10-01, P10-02, P10-03, P12-01; Before P10-01 | [D-AI-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=D-AI-01) — Generic case members cannot create reviewed/provider truth; intelligence remains advisory and scope explicit. |
| Implementation risk | Context ambiguity | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Mobile-only dead ends | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Premature legacy removal | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Design drift | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#112 | 9605d88e31bd | Source-first 81-node/12-cluster surface map, participant-renderer boundaries, wave plan and cross-repo seams. | P12-03 | Selective port, then supersede after extraction | Catalogued; content remains to be reconciled into replacement PR acceptance tests. |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P12-03 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |
| app#121 | 529d377e2337 | Primary Node 0 participant model/UI, PDF/guide presentation and focused surface tests. | P12-02 | Selective UI/test port, then supersede | Unextracted; #124 may contain later copies but equivalence must be proved by file/commit comparison. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P12-02 | Retain pending Alan reconciliation; selective port or rebase only after architecture approval | Reinspected at latest head. It is exactly e853821 (no newer delta); retention strengthened, but final extraction waits for Alan checkpoint. |
| app#124 | 84a5a847fea7 | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. | P12-02 | Retain unchanged as evidence; selective port/rewrite after checkpoint | Unextracted; Alan review explicitly incomplete and unresolved. |
| ds#8 | 4656426e493e | Consumer parity and bounded app-owned layout guidance for Node 0/case/mobile adoption. | P12-02 | Prefer direct review/merge if still correct | Direct-reuse candidate; local dirty asset delta separately protected. |

Package source inventory:

- PR #122 responsive journey and lens behavior
- PR #124 Node 0 surfaces
- DS PR #8 parity guidance

## 9. Ownership recommendation

Luke owns journey acceptance; Alan implements and verifies. Accessibility review recommended.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P12-01 | Alan | Alan (proposed) | Luke | Luke | Mandatory |
| P12-02 | Alan | Alan (proposed) | Luke | Luke | As risk warrants |
| P12-03 | Alan | Alan (proposed) | Luke | Luke | As risk warrants |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
