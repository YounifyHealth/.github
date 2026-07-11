# Existing PR extraction ledger

> Read-only reconciliation record. No PR, branch or worktree may be closed, retargeted, rebased, cleaned or deleted from this ledger alone.

Inspection snapshot: **2026-07-10 20:12 America/New_York**.

## Preservation and extraction sequence

1. Preserve dirty worktrees and identify active branches/PRs.
2. Reinspect latest heads.
3. Complete this extraction ledger.
4. Reconcile Alan's findings.
5. Approve replacement architecture/PR boundaries.
6. Create/ready Project draft items.
7. Open replacement drafts only when implementation starts.
8. Extract/port/rewrite value.
9. Close superseded PRs only after accounting.
10. Delete branches/worktrees only after closure and team confirmation.

## Summary

| PR | Latest head | Useful capability | Destination | Status | Disposition |
| --- | --- | --- | --- | --- | --- |
| app#112 | 9605d88e31bd7ea5ccb0ddc524c5f2412efb242e | Source-first 81-node/12-cluster surface map, participant-renderer boundaries, wave plan and cross-repo seams. | P00-01, P09-04, P11-03, P11-04, P12-03 | Catalogued; content remains to be reconciled into replacement PR acceptance tests. | Selective port, then supersede after extraction |
| app#117 | 5ac09f0cdd9299667fd70e845e606b1892f98ece | Deterministic candidate questionnaire, scoring/status calculation, conversation-guide resource, routes and extensive Node 0 tests. | P04-01, P04-02, P05-02, P05-03 | Unextracted; algorithm/test review required after Alan checkpoint and Luke field/score decision. | Selective port and rewrite |
| app#119 | a8cd2f4285358077490f02089ac8f9e6f1e8bed3 | Concise product-leverage framing and boundaries for the MVP flow. | P00-01, P04-01, P05-01, P06-01, P10-01, P12-03 | Catalogued; reconcile terminology into approved programme. | Retain as source or merge separately after plan decision |
| app#121 | 529d377e23376268b44c95ba9974aa0cd133275f | Primary Node 0 participant model/UI, PDF/guide presentation and focused surface tests. | P05-03, P11-03, P12-02 | Unextracted; #124 may contain later copies but equivalence must be proved by file/commit comparison. | Selective UI/test port, then supersede |
| app#122 | e85382150853cf4774948c55b91e330e7e69617e | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P01-01, P02-03, P03-01, P03-03, P04-02, P09-04, P10-02, P11-03, P12-02 | Reinspected at latest head. It is exactly e853821 (no newer delta); retention strengthened, but final extraction waits for Alan checkpoint. | Retain pending Alan reconciliation; selective port or rebase only after architecture approval |
| app#123 | 34078f810b634aa6ddce5954763c03cb46b574d8 | GC onboarding form/copy, hosted auth return, invite handoff and role-specific surface work. | P03-01, P03-02, P06-02, P06-03 | Unextracted; likely partially copied into #124 but not proven complete. | Selective UX/test port and rewrite |
| app#124 | 84a5a847fea71213b6257549e5a620f654836cb1 | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. | P04-01, P04-02, P04-03, P05-02, P05-03, P06-02, P06-03, P09-04, P10-02, P11-04, P12-02 | Unextracted; Alan review explicitly incomplete and unresolved. | Retain unchanged as evidence; selective port/rewrite after checkpoint |
| ds#7 | cedfcc489b1f60842aed3a9701348c85964cfd96 | Documents an escaping/attrs hardening follow-up relevant to participant recipe security. | P11-03 | Direct-reuse candidate; not yet merged. | Retain for direct review/merge or fold into P11-03 |
| ds#8 | 4656426e493e243785f8490589bf44fc0e05b8d6 | Consumer parity and bounded app-owned layout guidance for Node 0/case/mobile adoption. | P11-03, P12-02 | Direct-reuse candidate; local dirty asset delta separately protected. | Prefer direct review/merge if still correct |

## Detailed PR records

### app#112 — BYOS journey surface migration: surface map + workplan (spec handoff)

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/112 |
| Latest inspected head | 9605d88e31bd7ea5ccb0ddc524c5f2412efb242e |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Source-first 81-node/12-cluster surface map, participant-renderer boundaries, wave plan and cross-repo seams. |
| Reusable commits/files | docs/plans/byos-journey-surface-map.md; docs/plans/byos-journey-surface-workplan.md; single documentation commit 9605d88. |
| Tests worth preserving | Docs-only; preserve its stated acceptance/test map, not CI results as product evidence. |
| Obsolete/unsafe assumptions | Predates the explicit free-workspace/paid-case/commercial/provenance split and cannot be the implementation sequence by itself. |
| Replacement destination | P00-01, P09-04, P11-03, P11-04, P12-03 |
| Extraction status | Catalogued; content remains to be reconciled into replacement PR acceptance tests. |
| Outstanding reviewer input | No GitHub review recorded. |
| Recommended disposition | Selective port, then supersede after extraction |
| Exact close condition | Every unique architecture/product decision is either adopted in the programme or rejected with rationale; Alan confirms no needed review input remains; replacement plan is approved. |
| Exact branch/worktree delete condition | PR is closed, commit is reachable from retained history or archived reference, no attached dirty worktree/unique commit remains, and Luke/Alan explicitly confirm cleanup. |

### app#117 — Node 0 beta: Outreach Readiness Quiz and deterministic Conversation Guide

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/117 |
| Latest inspected head | 5ac09f0cdd9299667fd70e845e606b1892f98ece |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Deterministic candidate questionnaire, scoring/status calculation, conversation-guide resource, routes and extensive Node 0 tests. |
| Reusable commits/files | app/node0.py; app/node0_conversation_guide.py; resource JSON; focused tests; only the non-ranking/safety-safe algorithms that pass D-DATA-03. |
| Tests worth preserving | tests/python/test_node0.py contains useful deterministic and authorization cases. |
| Obsolete/unsafe assumptions | Large mixed UI/style/schema PR; case-shaped persistence, 0-100 ranking and unverified third-party answers conflict with workspace/provenance contract. |
| Replacement destination | P04-01, P04-02, P05-02, P05-03 |
| Extraction status | Unextracted; algorithm/test review required after Alan checkpoint and Luke field/score decision. |
| Outstanding reviewer input | No GitHub review recorded. |
| Recommended disposition | Selective port and rewrite |
| Exact close condition | Approved questionnaire/guide behavior and every valuable test are mapped to P05-02/P05-03 or deliberately rejected; replacement PRs contain provenance and Free-tier contract. |
| Exact branch/worktree delete condition | Close conditions met, stacked PRs #121/#123 are reconciled, branch has no unique retained worktree content, and team confirms deletion. |

### app#119 — Docs: align MVP app flows to process leverage points

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/119 |
| Latest inspected head | a8cd2f4285358077490f02089ac8f9e6f1e8bed3 |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Concise product-leverage framing and boundaries for the MVP flow. |
| Reusable commits/files | docs/plans/mvp-process-leverage-alignment.md and its two documentation commits. |
| Tests worth preserving | Docs-only; no executable behavior. |
| Obsolete/unsafe assumptions | Does not define implementation state machines, funding, provenance or gate evidence; title similarity must not make it the programme authority. |
| Replacement destination | P00-01, P04-01, P05-01, P06-01, P10-01, P12-03 |
| Extraction status | Catalogued; reconcile terminology into approved programme. |
| Outstanding reviewer input | No GitHub review recorded. |
| Recommended disposition | Retain as source or merge separately after plan decision |
| Exact close condition | Luke decides whether the source document remains useful independently; if superseded, every unique principle is cited/adopted or rejected in the approved programme. |
| Exact branch/worktree delete condition | Only after close/merge, source commit remains reachable, no worktree depends on branch and team confirms. |

### app#121 — Node 0 beta: primary participant surface

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/121 |
| Latest inspected head | 529d377e23376268b44c95ba9974aa0cd133275f |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Primary Node 0 participant model/UI, PDF/guide presentation and focused surface tests. |
| Reusable commits/files | app/node0_surface.py; node0_pdf.py; route/template/asset/test slices after comparison with #124. |
| Tests worth preserving | Node 0 surface/rendering tests worth porting to P05-03. |
| Obsolete/unsafe assumptions | Stacked on #117 rather than main, inherits case-shaped candidate model, and includes broad Wave 0/DS content already landed through #115; only tip 529d377 is genuinely unique. It predates the authorship/workspace split. |
| Replacement destination | P05-03, P11-03, P12-02 |
| Extraction status | Unextracted; #124 may contain later copies but equivalence must be proved by file/commit comparison. |
| Outstanding reviewer input | No GitHub review recorded. |
| Recommended disposition | Selective UI/test port, then supersede |
| Exact close condition | All unique surface/PDF/test value is proven present in an approved replacement or explicitly rejected; stacked dependency is no longer needed. |
| Exact branch/worktree delete condition | After #117/#123/#124 reconciliation, PR closure, no dirty worktree/unique commits, and team confirmation. |

### app#122 — Wave 1 participant case shell surfaces

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/122 |
| Latest inspected head | e85382150853cf4774948c55b91e330e7e69617e |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. |
| Reusable commits/files | Invitation commits/files and tests; case_journey/case_home presenter and paired-lens/mobile tests; .github/workflows/python-tests.yml; DS vendoring/escaping contract where still applicable. |
| Tests worth preserving | Reported 499-test suite; green unittest/build/contract checks observed at e853821. Preserve concurrency, logged-out invite, paired IP/GC, Learn timeout and render tests. |
| Obsolete/unsafe assumptions | No Node 0 workspace target, payment/promotion or separate claim model; facts/proposals lack strong authorship/approval authority; generic invitation status setter remains; case lifecycle is not the whole programme state model. |
| Replacement destination | P01-01, P02-03, P03-01, P03-03, P04-02, P09-04, P10-02, P11-03, P12-02 |
| Extraction status | Reinspected at latest head. It is exactly e853821 (no newer delta); retention strengthened, but final extraction waits for Alan checkpoint. |
| Outstanding reviewer input | Alan's 2026-07-10 review-round comment records fixes from earlier 8df63dd to e853821. No formal GitHub review object; current planning must not imply all architecture is approved. |
| Recommended disposition | Retain pending Alan reconciliation; selective port or rebase only after architecture approval |
| Exact close condition | CHECK-ALAN-122-124 is complete; every fix/finding/test has a destination; replacement contracts cover workspace/case/provenance; the relevant replacements have merged or the team explicitly elects to merge a narrowed #122. |
| Exact branch/worktree delete condition | Only after final disposition/closure, all commits/tests are reachable or intentionally discarded, no worktree depends on branch, and Alan/Luke confirm cleanup. |

### app#123 — Node 0 beta: GC onboarding and hosted handoff

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/123 |
| Latest inspected head | 34078f810b634aa6ddce5954763c03cb46b574d8 |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | GC onboarding form/copy, hosted auth return, invite handoff and role-specific surface work. |
| Reusable commits/files | Onboarding templates/routes/tests after field-level privacy and claim separation review. |
| Tests worth preserving | Preserve hosted-return, invalid/decline and GC lens interaction cases after comparison with #124/dirty onboarding branch. |
| Obsolete/unsafe assumptions | Stacked on #121, predates PR #122 hardening, and conflates soft onboarding with case-shaped data/membership; GC answers do not revise IP assertions. It also mixes participant work with a large internal/operator redesign and vendored internal DS, which must stay out of this participant programme. |
| Replacement destination | P03-01, P03-02, P06-02, P06-03 |
| Extraction status | Unextracted; likely partially copied into #124 but not proven complete. |
| Outstanding reviewer input | No GitHub review recorded. |
| Recommended disposition | Selective UX/test port and rewrite |
| Exact close condition | Hosted return and onboarding value is mapped to claim-aware, attributable GC replacement PRs and no unique behavior remains. |
| Exact branch/worktree delete condition | After stacked PR/worktree reconciliation, closure, retained commits/tests are reachable, and team confirms. |

### app#124 — Consolidate BYOS Node 0 handoff

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/124 |
| Latest inspected head | 84a5a847fea71213b6257549e5a620f654836cb1 |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Current consolidation of Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitations, DS assets and large focused test suites. |
| Reusable commits/files | Deterministic guide/resource/tests, selected Node 0/GC/case presentation, source-aware Learn dependency notes, subject to file-level extraction. |
| Tests worth preserving | test_node0.py and test_case_home.py contain broad behavior/render coverage; green build/contract-smoke observed, but no main Python/PostgreSQL proof. |
| Obsolete/unsafe assumptions | Node 0 Free creates a synthetic canonical case; unaddressed link can lead to case membership; IP third-party assertions drive score/invite; notes become shared memory; no commercial event, payment ledger or promotion. It contains older #122 equivalents but not the later hardening commits through e853821; its checks omit the unittest workflow. |
| Replacement destination | P04-01, P04-02, P04-03, P05-02, P05-03, P06-02, P06-03, P09-04, P10-02, P11-04, P12-02 |
| Extraction status | Unextracted; Alan review explicitly incomplete and unresolved. |
| Outstanding reviewer input | Alan's review is explicitly incomplete and unresolved (halfway through per team update). No completion is assumed; CHECK-ALAN-122-124 blocks final disposition and replacement work. |
| Recommended disposition | Retain unchanged as evidence; selective port/rewrite after checkpoint |
| Exact close condition | Alan completes and reconciles findings; every valuable commit/file/test has a destination; replacement architecture is approved; extracted replacements cover value; Luke and Alan confirm supersession. |
| Exact branch/worktree delete condition | Only after closure, replacement merges/extraction verification, no protected worktree depends on branch and explicit team cleanup confirmation. |

### ds#7 — Document Jinja attrs hardening follow-up

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-design-system/pull/7 |
| Latest inspected head | cedfcc489b1f60842aed3a9701348c85964cfd96 |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Documents an escaping/attrs hardening follow-up relevant to participant recipe security. |
| Reusable commits/files | Documentation commit/contract as direct source for P11-03. |
| Tests worth preserving | Preserve attrs/escaping contract tests in the eventual DS release. |
| Obsolete/unsafe assumptions | Draft guidance alone does not prove consumer safety and should not block cloud recovery for aesthetic reasons. |
| Replacement destination | P11-03 |
| Extraction status | Direct-reuse candidate; not yet merged. |
| Outstanding reviewer input | No recorded review in this inspection. |
| Recommended disposition | Retain for direct review/merge or fold into P11-03 |
| Exact close condition | Merged as-is after review or content/tests are present in an approved DS replacement. |
| Exact branch/worktree delete condition | After merge/closure, no unique dirty asset changes on the branch and team confirmation. |

### ds#8 — Add consumer visual parity guidance

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-design-system/pull/8 |
| Latest inspected head | 4656426e493e243785f8490589bf44fc0e05b8d6 |
| Inspection time | 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York) |
| Useful capability | Consumer parity and bounded app-owned layout guidance for Node 0/case/mobile adoption. |
| Reusable commits/files | Guidance and validation expectations for P11-03/P12-02. |
| Tests worth preserving | Use concrete responsive/a11y/security requirements; do not turn every token mismatch into a blocker. |
| Obsolete/unsafe assumptions | Local worktree contains extra dirty brand assets not represented by remote PR; do not overwrite or assume included. |
| Replacement destination | P11-03, P12-02 |
| Extraction status | Direct-reuse candidate; local dirty asset delta separately protected. |
| Outstanding reviewer input | Open, not draft; no recorded formal review in this inspection. |
| Recommended disposition | Prefer direct review/merge if still correct |
| Exact close condition | Merged or equivalent guidance/tests are released and app pins that release. |
| Exact branch/worktree delete condition | After closure/merge and explicit confirmation that local dirty assets are committed elsewhere or intentionally discarded. |

## Latest PR #122 reinspection

Latest inspected head: `e85382150853cf4774948c55b91e330e7e69617e` at 2026-07-11T00:59:11Z (2026-07-10 20:59:11 America/New_York). The earlier reviewed workflow run/comment baseline was `8df63dd`; Alan's current head is `e853821`.

Fixed or materially improved since the earlier snapshot:

- Logged-out invite delivery/resume and validated internal return_to across login/signup/confirm/resend.
- Paired IP/GC lens semantics and render-time action labels.
- CAS redemption/expiry/mismatch transitions, self-invite refusal and one-live-GC constraints.
- 14-day expiry ceiling, portable integrity handling and duplicate-live-invite forward migration.
- Blocking Python CI workflow, fail-closed Learn approval, bounded Learn timeout, SQL-limited timeline and safer cookie/dead-button behavior.

Remaining conflicts/gaps:

- No distinct Node 0 workspace or workspace claim target; it cannot be stacked unchanged with #124.
- No commercial commitment/funding/promotion or separate entitlement/payment/document lifecycle.
- Generic fact/proposal/invitation rails still need explicit author/authority/evidence transition commands.
- The case projection is useful case-stage presentation, not a universal programme state machine.

Decomposition impact: retain more of #122's CI, invitation and case-surface tests/implementation, but do not collapse WP03/WP04/WP07/WP09. Workspace/case separation and Alan reconciliation remain blocking.

## Alan reconciliation checkpoint

| Field | Contract |
| --- | --- |
| Name | Alan review reconciliation: PRs #122 and #124 |
| Status | Unresolved input |
| Blocks | P03-01, P03-02, P03-03, P03-04, P04-01, P04-02, P04-03, P05-01, P05-02, P05-03, P06-01, P06-02, P06-03, P09-04 |
| May amend | WP01, WP03, WP04, WP05, WP06, WP09, WP10, WP11, WP12, WP13 |
| Avoid wasted review | Do not ask Alan to polish code already known to be architecturally obsolete. Complete the safety/defect review at the contract/test level, identify reusable commits/tests, and stop once findings are captured. Obsolete code can be superseded while its findings become replacement acceptance tests. |

Finding recording:

- Record each finding with PR/head SHA, file/line or diff anchor, severity, reproducible behavior, architecture/product implication, proposed acceptance test and destination PR ID.
- Mark whether the finding concerns reusable behavior, obsolete architecture, security/privacy, accessibility, migration, concurrency, test coverage or product semantics.
- Update this extraction ledger first; then update the canonical programme data, regenerate all plans/manifest and re-sync the Project so no source diverges.

Resolution rule:

- Evidence beats plan text: a verified defect or missing contract amends the package.
- Alan proposes technical alternatives and records a concise dissent where needed; Luke resolves product, lifecycle, privacy, commercial and cross-repository architecture decisions.
- Security/privacy/payment/PHI disagreements that exceed internal authority go to the named external reviewer; implementation remains blocked.

Complete only when:

- [ ] Alan confirms his #122 changes and unfinished #124 findings are fully captured.
- [ ] Every finding has a disposition and destination or explicit no-action rationale.
- [ ] Luke and Alan accept the workspace/case, invitation, authorship and PR-boundary contract, or an explicit unresolved decision remains blocked.
- [ ] No replacement implementation item is marked Ready to implement until both the checkpoint and its own dependencies/decisions are clear.

## Protected local worktrees

| Repository | Path | Branch/head | Protected content | Destination | Safety rule |
| --- | --- | --- | --- | --- | --- |
| app | `/Users/lukerhodes/Natalyx/natalyx-app` | feature/provider-exchange-layer-v0 / 84a5a84 | substantial uncommitted provider handoff/ops/document work | P09-01/P09-03/P09-05 after provenance/security review | Do not stage, reset, stash, switch, commit, clean or overwrite. |
| app | `/Users/lukerhodes/.codex/worktrees/1b3f/natalyx-app` | feature/node0-surrogate-onboarding-link / 529d377 | substantial uncommitted onboarding/invitation work | P03-02/P03-03/P06-02 | Preserve until file/test extraction is signed off. |
| app | `/Users/lukerhodes/.codex/worktrees/39b2/natalyx-app` | detached candidate rewrite / 9605d88 | substantial uncommitted Node 0 quiz rewrite | P04-02/P05-02 | Preserve; compare with predecessor and #117/#124 before any discard. |
| app | `/Users/lukerhodes/.codex/worktrees/6233/natalyx-app` | detached predecessor candidate model / dc6a2f0 | substantial uncommitted predecessor model | P04-02/P05-02 if unique | Preserve until rewrite diff/extraction ledger is complete. |
| learn | `/Users/lukerhodes/Natalyx/natalyx-learn-resources` | feature/learn-resource-rendering-contract / 9c9a9c2 | substantial uncommitted builder/schema/templates/resource work | P11-01 | Do not update/switch/clean; create a future isolated extraction worktree. |
| learn | `/Users/lukerhodes/.codex/worktrees/9dfc/natalyx-learn-resources` | feature/node0-beta-learn-resources / e1fb2d6 | uncommitted Node 0 Learn implementation | P11-01 after provenance/no-fake-content review | Preserve until compared with rendering-contract branch. |
| intelligence | `/Users/lukerhodes/Natalyx/natalyx-intelligence` | main (behind origin/main) / 9d824e8 | dirty Learn registry/corpus plus uv.lock | P11-02/P10-03 as appropriate | Do not pull/reset/stash; extract in isolated worktree later. |
| design-system | `/Users/lukerhodes/Natalyx/Natalyx Design System` | feature/ds-consumer-parity-guidance / 4656426 | dirty brand assets beyond PR #8 | P11-03 after asset review | Remote PR and local asset delta are separate evidence; do not overwrite. |
| internal-design-system | `/Users/lukerhodes/Natalyx/Natalyx Internal View Design System` | main / current local | substantial uncommitted operator shell/design-system work | Not part of participant DS; review only if P09-05 operator UI needs approved internal recipes | Preserve repo boundary and dirty worktree. |

## Cleanup tasks

| ID | Task | Dependencies | Owner |
| --- | --- | --- | --- |
| CLEAN-01 | Verify extraction completeness before any PR closure | CHECK-ALAN-122-124 | Joint |
| CLEAN-02 | Close superseded PRs only after replacement evidence is reachable | CLEAN-01 | Luke |
| CLEAN-03 | Delete remote branches/worktrees only after closure and team confirmation | CLEAN-02 | Alan |
