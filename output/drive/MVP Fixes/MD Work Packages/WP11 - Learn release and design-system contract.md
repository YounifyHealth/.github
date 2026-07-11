---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Work Package 11: Learn release and design-system contract"
author: "L. Rhodes (plan owner) - A. Zhao (technical review requested)"
date: "2026-07-10"
---
# Work Package 11: Learn release and design-system contract

> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.

| Plan | Value |
| --- | --- |
| Work package | WP11 |
| Plan file | `WP11 - Learn release and design-system contract.md` |
| Proposed PRs | P11-01, P11-02, P11-03, P11-04 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

## Purpose and outcome

**Problem.** Learn artifact generation and catalog work is dirty/unreleased, while participant surfaces need governed recipes without making aesthetic purity a universal release gate.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Validated provenance-bearing Learn artifacts, approved-only serving, release-blocking DS accessibility/security/interaction contract, and app adoption of stable recipes/source cards.

**Explicit non-goals.**

- No invented final content
- No universal zero-hex rule
- No internal/operator DS merge
- No full legacy redesign

## Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-022 | verified protected work | learn / dirty feature/learn-resource-rendering-contract@9c9a9c2 | builder/validator/schema/templates/preview additions | A substantial artifact/rendering contract exists only as protected uncommitted work; no open Learn PR contains it. |
| E-023 | verified protected work | intelligence / dirty main@9d824e8, behind origin/main | src/natalyx_intelligence/learn_resources.py; starting_natalyx_journey_v1.md | Catalog/resource edits are uncommitted and must not be overwritten or treated as released. |
| E-024 | verified | design-system / main@43dab986; PR #7@cedfcc4; PR #8@4656426 | components, tokens, Jinja attrs/parity guidance | Participant DS recipes and parity guidance exist; local brand assets are also dirty. Internal/operator DS is a separate repository and boundary. |

## Architecture and contracts

- Learn resources own authored artifacts/provenance; intelligence owns approved catalog delivery; app owns authorized presentation and context.
- Security, accessibility, responsive layout, and interaction defects can block release; token/style purity alone is backlog unless tied to concrete risk.
- Participant and internal/operator design systems remain separate.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`, `design-system`, `intelligence`, `learn`; repository-specific PRs remain separate. |
| Entities/state | No new runtime entity; evidence/coordination only. |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Versioned artifact manifest consumed by intelligence. Catalog response includes manifest/version/source/approval fields. Read-only catalog contract with fail-closed approval checks. |
| Storage | No new storage; preserve current state read-only for this package. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

### Design-system release rubric

| Class | Items |
| --- | --- |
| Release-blocking | XSS/escaping or unsafe raw slots; keyboard/focus/screen-reader failures; unusable responsive layout; misleading or nonfunctional interaction; motion without reduced-motion safety; contrast or error-state defects that block task completion |
| Desirable | token/recipe consistency; visual parity; removal of duplicate spacing/color literals; component naming/adoption |
| Deferred | zero raw hex values; zero inline geometry styles; full legacy strangler cleanup; broad participant redesign; internal/operator DS convergence |

Style purity blocks a release only when tied to a concrete security, accessibility, interaction or material maintainability risk.

## Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P11-01 | Publish validated Learn artifact and provenance contract | learn | P00-01 | A2 | Large | Dependencies unmet |
| 2 | P11-02 | Serve approved Learn catalog versions from intelligence | intelligence | P11-01 | A2 | Large | Dependencies unmet |
| 3 | P11-03 | Release participant design-system accessibility and interaction contract | design-system | P00-01 | A1 | Medium | Dependencies unmet |
| 4 | P11-04 | Adopt approved Learn and source-card recipes in app | app | P11-02, P11-03 | A2 | Large | Dependencies unmet |

### P11-01 - Publish validated Learn artifact and provenance contract

| Field | Plan |
| --- | --- |
| Repository / base | `learn` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P00-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Protected feature/learn-resource-rendering-contract, feature/node0-beta-learn-resources |

#### Objective

Turn the protected rendering-contract work into a small releaseable artifact schema/builder/validator with source provenance and no invented resources.

#### Scope

- Markdown/YAML source schema
- Article/PDF/context-packet artifacts
- Source/revision/audience/approval metadata
- Deterministic build

#### Explicit non-goals

- No final content beyond separately approved resources
- No app UI

#### Expected files or modules

- `schemas/`
- `src/natalyx_learn_resources/builder.py`
- `src/natalyx_learn_resources/validator.py`
- `tests/test_builder.py`
- `tests/test_validator.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Versioned artifact manifest consumed by intelligence. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Provenance and release procedure. |

#### Tests and validation

Objective tests:

- Schema invalid cases
- deterministic output
- missing provenance
- unsafe links/HTML
- artifact checksum

Local validation:

- `uv run pytest`
- Run the builder/validator against approved fixture sources and compare deterministic checksums.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P00-01. Parallel opportunities: P11-03, P11-04

#### Objective acceptance criteria

- [ ] Turn the protected rendering-contract work into a small releaseable artifact schema/builder/validator with source provenance and no invented resources.
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
| Required expertise | content pipelines, schema validation, document generation |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P11-02 - Serve approved Learn catalog versions from intelligence

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P11-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Intelligence issue #14, protected dirty learn_resources.py |

#### Objective

Load a pinned Learn artifact manifest, filter to approved audience/scope, and expose explicit empty/degraded behavior without hard-coded duplicate catalog truth.

#### Scope

- Manifest pin/checksum
- Approval/audience/cluster filters
- Source metadata
- Atomic catalog reload

#### Explicit non-goals

- No unapproved fallback catalog
- No app rendering

#### Expected files or modules

- `src/natalyx_intelligence/learn_resources.py`
- `src/natalyx_intelligence/catalog.py`
- `tests/pathfinder/test_corpus_loading.py`
- `docs/agents/learn-resources.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Catalog response includes manifest/version/source/approval fields. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Missing/bad manifest
- unapproved exclusion
- audience filter
- atomic reload
- stale version

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

Hard dependencies: P11-01. Parallel opportunities: P11-03

#### Objective acceptance criteria

- [ ] Load a pinned Learn artifact manifest, filter to approved audience/scope, and expose explicit empty/degraded behavior without hard-coded duplicate catalog truth.
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
| Required expertise | content serving, FastAPI, provenance |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P11-03 - Release participant design-system accessibility and interaction contract

| Field | Plan |
| --- | --- |
| Repository / base | `design-system` (`main`) |
| Gate / size / readiness | A1 / Medium / Dependencies unmet |
| Dependencies | P00-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Design-system PRs #7 and #8, dirty local brand assets |

#### Objective

Land the participant recipes/tokens/assets and parity guidance needed for secure escaping, accessible controls, responsive layouts, and stable interaction contracts.

#### Scope

- Jinja escaping/attrs contract
- 44px/keyboard/focus/reduced-motion requirements
- Responsive shell/recipe guidance
- Versioned vendoring

#### Explicit non-goals

- No universal raw-hex blocker
- No internal/operator DS
- No legacy app sweep

#### Expected files or modules

- `components/`
- `tokens/`
- `assets/`
- `docs/consumer-parity.md`
- `tests/`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | Participant design-system release only. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Template escaping
- raw-slot registry
- keyboard/focus
- responsive visual fixtures
- asset integrity

Local validation:

- `npm test`
- Run recipe escaping, accessibility and responsive fixture checks.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P00-01. Parallel opportunities: P11-01, P11-02

#### Objective acceptance criteria

- [ ] Land the participant recipes/tokens/assets and parity guidance needed for secure escaping, accessible controls, responsive layouts, and stable interaction contracts.
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
| Required expertise | design systems, accessibility, Jinja security |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P11-04 - Adopt approved Learn and source-card recipes in app

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P11-02, P11-03 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PR #122 Learn slot, PR #124 dependency note |

#### Objective

Consume pinned Learn/catalog and participant-DS versions for source cards, reading views, suggestions, and honest empty/error states.

#### Scope

- Version-pinned catalog client
- Source/citation cards and reading shell
- No-resource/degraded states
- Cluster/context handoff

#### Explicit non-goals

- No final content invention
- No case truth write

#### Expected files or modules

- `app/learn_resources.py`
- `app/templates/learn_workspace.html`
- `app/templates/components/participant/`
- `tests/python/test_learn_workspace.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Read-only catalog contract with fail-closed approval checks. |
| UI/product surface | Governed participant recipes. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Approved resource
- missing/unapproved resource
- service timeout
- source links
- mobile/keyboard

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

Hard dependencies: P11-02, P11-03. Parallel opportunities: P11-01

#### Objective acceptance criteria

- [ ] Consume pinned Learn/catalog and participant-DS versions for source cards, reading views, suggestions, and honest empty/error states.
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
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

## Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |
| `design-system` | participant recipes/tokens/accessibility/interaction contract |
| `intelligence` | advisory inference, scoped response/citation contract; no case truth |
| `learn` | authored Learn artifacts, provenance and release manifest |

Merge order inside this package: `P11-01` → `P11-03` → `P11-02` → `P11-04`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Artifact schema/provenance; Approved-only catalog; Missing-resource empty state; Recipe escaping; Keyboard/reduced-motion/mobile | Expected state/event/UI and named evidence are produced once. |
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
| Implementation risk | Fake/unapproved content | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Cross-repo version drift | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Aesthetic review blocks recovery | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | Internal DS leakage | Luke or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#112 | 9605d88e31bd | Source-first 81-node/12-cluster surface map, participant-renderer boundaries, wave plan and cross-repo seams. | P11-03, P11-04 | Selective port, then supersede after extraction | Catalogued; content remains to be reconciled into replacement PR acceptance tests. |
| app#121 | 529d377e2337 | Primary Node 0 participant model/UI, PDF/guide presentation and focused surface tests. | P11-03 | Selective UI/test port, then supersede | Unextracted; #124 may contain later copies but equivalence must be proved by file/commit comparison. |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P11-03 | Retain pending Alan reconciliation; selective port or rebase only after architecture approval | Reinspected at latest head. It is exactly e853821 (no newer delta); retention strengthened, but final extraction waits for Alan checkpoint. |
| app#124 | 84a5a847fea7 | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. | P11-04 | Retain unchanged as evidence; selective port/rewrite after checkpoint | Unextracted; Alan review explicitly incomplete and unresolved. |
| ds#7 | cedfcc489b1f | Documents an escaping/attrs hardening follow-up relevant to participant recipe security. | P11-03 | Retain for direct review/merge or fold into P11-03 | Direct-reuse candidate; not yet merged. |
| ds#8 | 4656426e493e | Consumer parity and bounded app-owned layout guidance for Node 0/case/mobile adoption. | P11-03 | Prefer direct review/merge if still correct | Direct-reuse candidate; local dirty asset delta separately protected. |
| feature/learn-resource-rendering-contract | 9c9a9c2 | substantial uncommitted builder/schema/templates/resource work | P11-01 | Selective port from protected worktree | Do not update/switch/clean; create a future isolated extraction worktree. |
| feature/node0-beta-learn-resources | e1fb2d6 | uncommitted Node 0 Learn implementation | P11-01 after provenance/no-fake-content review | Selective port from protected worktree | Preserve until compared with rendering-contract branch. |
| main (behind origin/main) | 9d824e8 | dirty Learn registry/corpus plus uv.lock | P11-02/P10-03 as appropriate | Selective port from protected worktree | Do not pull/reset/stash; extract in isolated worktree later. |
| feature/ds-consumer-parity-guidance | 4656426 | dirty brand assets beyond PR #8 | P11-03 after asset review | Selective port from protected worktree | Remote PR and local asset delta are separate evidence; do not overwrite. |

Package source inventory:

- Dirty Learn rendering-contract branch
- Learn issue #3
- Intelligence issue #14 and dirty catalog work
- DS PRs #7/#8

## Ownership recommendation

Luke leads this work package, with Alan providing technical review. The split is proposed for review and can be amended before implementation begins.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P11-01 | Luke | Luke (proposed) | Alan | Joint | As risk warrants |
| P11-02 | Luke | Luke (proposed) | Alan | Joint | As risk warrants |
| P11-03 | Luke | Luke (proposed) | Alan | Joint | As risk warrants |
| P11-04 | Luke | Luke (proposed) | Alan | Joint | As risk warrants |

Luke leads implementation and product acceptance for this package; Alan reviews architecture, migration, security and failure behavior. This is a recommendation pending joint review, not a compulsory assignment.

## Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and review record complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
