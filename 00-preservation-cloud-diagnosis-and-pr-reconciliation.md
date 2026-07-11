# Work package 00 — Preservation, cloud diagnosis, and PR reconciliation

> Planning-only execution contract. Proposed implementers and owners remain recommendations until Alan reviews/signs off the consolidated plan and Luke accepts it. Project: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP00 |
| Plan file | `00-preservation-cloud-diagnosis-and-pr-reconciliation.md` |
| Proposed PRs | P00-01 |
| Inspection snapshot | 2026-07-10 20:12 America/New_York |

## 1. Purpose and outcome

**Problem.** The live app is returning ALB 503 responses while overlapping draft PRs and protected dirty worktrees contain useful but contradictory implementations.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** A signed-off source-of-truth baseline, complete extraction ledger, Alan-review reconciliation, and explicit no-delete/no-close conditions before replacement work begins.

**Explicit non-goals.**

- No code porting
- No PR closure or retargeting
- No branch/worktree cleanup
- No deployment or AWS mutation

## 2. Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-001 | verified | live dev / 2026-07-10 20:12 America/New_York | https://dev.app.natalyx.health/ and /health | Both requests returned HTTP 503 from awselb/2.0; the deployed participant app is not presently usable. |
| E-002 | verified limitation | AWS dev / 2026-07-10 20:12 America/New_York | aws sts get-caller-identity --profile natalyx-dev | Local AWS SSO was expired, so current ECS desired/running counts and task revision were not independently verified. Gate A0 must refresh access and capture them. |
| E-003 | verified | GitHub / 2026-07-10 20:12 America/New_York | NatalyxPlatform open PR query | App PRs #112, #117, #119, #121, #122, #123 and #124 and design-system PRs #7/#8 are open; all app PRs are drafts. |
| E-004 | verified | .github / main@6072ce9 | GitHub Project 3 GraphQL inspection | MVP Product Flow Reshape existed with only default fields and zero items before this planning update. |

## 3. Architecture and contracts

- Treat every existing branch and worktree as read-only evidence until its valuable files, tests, and reviewer findings have a named destination.
- Use the organisation Project as the programme control plane and this repository-neutral package as the reviewable contract.
- Do not infer live health from GitHub build success; Gate A0 requires a known revision and live evidence.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `.github`; repository-specific PRs remain separate. |
| Entities/state | No new runtime entity; evidence/coordination only. |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | No broad public contract; use the focused commands/events in each PR. |
| Storage | No new storage; preserve current state read-only for this package. |
| Audit | Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads. |
| Failure | Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence. |
| Observability | Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging. |
| Compatibility | Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair. |
| Privacy/PHI | Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2. |

## 4. Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Size | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P00-01 | Approve programme baseline and extraction ledger | .github | P00-01 | Pre-A0 | Medium | Needs plan approval |

### P00-01 — Approve programme baseline and extraction ledger

| Field | Plan |
| --- | --- |
| Repository / base | `.github` (`main`) |
| Project item | [P00-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P00-01) |
| Gate / size / readiness | Pre-A0 / Medium / Needs plan approval |
| Dependencies | P00-01 plan sign-off only |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | All listed draft PRs and protected worktrees |

#### Objective

Land the reviewed planning package and extraction baseline only after Alan has reviewed the consolidated document and Luke has accepted the programme contract.

#### Scope

- Record sign-off, unresolved decisions, source SHAs, and reconciliation procedure
- Freeze programme IDs used by the Project

#### Explicit non-goals

- No implementation code
- No assignment becomes mandatory before Alan sign-off

#### Expected files or modules

- `natalyx-repair-program/*.md`
- `natalyx-repair-program/consolidated-plan.pdf`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Repository-neutral planning and programme-control documents only. |

#### Tests and validation

Objective tests:

- git diff --check
- document/project parity validator
- PDF visual QA

Local validation:

- `git diff --check`
- `/Users/lukerhodes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/validate_programme.py`

Cloud validation: run only through Gate **Pre-A0** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Merge only after document/sign-off checks; it changes no runtime. Re-sync the Project from the same canonical data.

#### Rollback or forward repair

Correct the canonical data and regenerate; do not rewrite implementation history.

#### Dependencies and parallel work

Hard dependencies: approved programme baseline. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Land the reviewed planning package and extraction baseline only after Alan has reviewed the consolidated document and Luke has accepted the programme contract.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Luke |
| Implementer | Luke (proposed; pending consolidated-plan sign-off) |
| Reviewer | Alan |
| Final approver | Luke |
| Required expertise | programme architecture, technical programme management |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

## 5. Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `.github` | programme/governance evidence and Project control plane |

Merge order inside this package: `P00-01`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## 6. Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | SHA and timestamp reproducibility; Project/document identifier parity; No dirty-worktree mutation; HTTP and workflow evidence captured separately | Expected state/event/UI and named evidence are produced once. |
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
| Implementation risk | Review findings arrive after decomposition | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | A protected worktree contains the only copy of useful code | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |
| Implementation risk | A green PR is mistaken for live readiness | Alan or named PR DRI | Package PRs; before associated gate | Mitigate through the explicit tests, rollout and forward-repair plan |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#112 | 9605d88e31bd | Source-first 81-node/12-cluster surface map, participant-renderer boundaries, wave plan and cross-repo seams. | P00-01 | Selective port, then supersede after extraction | Catalogued; content remains to be reconciled into replacement PR acceptance tests. |
| app#119 | a8cd2f428535 | Concise product-leverage framing and boundaries for the MVP flow. | P00-01 | Retain as source or merge separately after plan decision | Catalogued; reconcile terminology into approved programme. |

Package source inventory:

- App PRs #112, #117, #119, #121, #122, #123, #124
- Design-system PRs #7 and #8
- Provider-exchange, Node 0 onboarding/quiz, Learn-rendering, and intelligence dirty worktrees

## 9. Ownership recommendation

Luke owns product/architecture acceptance and the closure decision. Alan owns technical reconciliation recommendations. Both sign the checkpoint before Node 0, invitation/auth, or participant case replacement work starts.

| PR | DRI | Implementer | Reviewer | Final approver | External/high-capability review |
| --- | --- | --- | --- | --- | --- |
| P00-01 | Luke | Luke (proposed) | Alan | Luke | As risk warrants |

Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
