# Existing PR extraction ledger

> Read-only reconciliation record. No PR, branch or worktree may be closed, retargeted, rebased, cleaned or deleted from this ledger alone.

Inspection snapshot: **2026-07-12 19:30 America/New_York**.

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
| app#122 | e85382150853cf4774948c55b91e330e7e69617e | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P01-01, P02-03, P03-01, P03-03, P03-05, P04-02, P09-04, P10-02, P11-03, P12-02 | Complete at e853821: authoritative behavior/tests and selectively portable implementation are classified; superseded architecture and evidence-only claims are named. | Selective-port behavior and tests; supersede as programme architecture |
| app#123 | 34078f810b634aa6ddce5954763c03cb46b574d8 | GC onboarding form/copy, hosted auth return, invite handoff and role-specific surface work. | P03-01, P03-02, P06-02, P06-03 | Unextracted; likely partially copied into #124 but not proven complete. | Selective UX/test port and rewrite |
| app#124 | 84a5a847fea71213b6257549e5a620f654836cb1 | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. | P03-02, P03-03, P04-01, P04-02, P04-03, P05-02, P05-03, P06-02, P06-03, P09-04, P10-02, P11-03, P11-04, P12-02 | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence |
| ds#7 | cedfcc489b1f60842aed3a9701348c85964cfd96 | Documents an escaping/attrs hardening follow-up relevant to participant recipe security. | P11-03 | Direct-reuse candidate; not yet merged. | Retain for direct review/merge or fold into P11-03 |
| ds#8 | 4656426e493e243785f8490589bf44fc0e05b8d6 | Consumer parity and bounded app-owned layout guidance for Node 0/case/mobile adoption. | P11-03, P12-02 | Direct-reuse candidate; local dirty asset delta separately protected. | Prefer direct review/merge if still correct |

## Detailed PR records

### app#112 — BYOS journey surface migration: surface map + workplan (spec handoff)

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/112 |
| Latest inspected head | 9605d88e31bd7ea5ccb0ddc524c5f2412efb242e |
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
| Useful capability | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. |
| Reusable commits/files | Invitation behavior/tests; case_journey/case_home presenter and paired-lens/mobile tests; .github/workflows/python-tests.yml after CI hardening; DS escaping contract where still applicable. |
| Tests worth preserving | Reported 499-test suite; green unittest/build/contract checks observed at e853821. Preserve concurrency, logged-out invite, paired IP/GC, Learn timeout and render tests. |
| Obsolete/unsafe assumptions | No Node 0 workspace target, payment/promotion or separate claim model; facts/proposals lack strong authorship/approval authority; generic invitation status setter remains; case lifecycle is not the whole programme state model. |
| Replacement destination | P01-01, P02-03, P03-01, P03-03, P03-05, P04-02, P09-04, P10-02, P11-03, P12-02 |
| Extraction status | Complete at e853821: authoritative behavior/tests and selectively portable implementation are classified; superseded architecture and evidence-only claims are named. |
| Outstanding reviewer input | Alan's 2026-07-10 review-round comment and the completed 2026-07-12 reconciliation are captured. No formal GitHub approval is inferred. |
| Recommended disposition | Selective-port behavior and tests; supersede as programme architecture |
| Exact close condition | Every retained behavior/test is reachable in approved replacements or deliberately rejected; no team member elects a separately narrowed #122 merge. |
| Exact branch/worktree delete condition | Only after closure, retained commits/tests are reachable or archived, no worktree depends on the branch, and Alan/Luke explicitly confirm cleanup. |

### app#123 — Node 0 beta: GC onboarding and hosted handoff

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-app/pull/123 |
| Latest inspected head | 34078f810b634aa6ddce5954763c03cb46b574d8 |
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
| Useful capability | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. |
| Reusable commits/files | Deterministic guide/resource/tests, selected Node 0/GC/case presentation, source-aware Learn dependency notes, subject to file-level extraction. |
| Tests worth preserving | test_node0.py and test_case_home.py contain broad behavior/render coverage; green build/contract-smoke observed, but no main Python/PostgreSQL proof. |
| Obsolete/unsafe assumptions | Node 0 Free creates a synthetic canonical case; unaddressed link can lead to case membership; IP third-party assertions drive score/invite; notes become shared memory; no commercial event, payment ledger or promotion. It contains older #122 equivalents but not the later hardening commits through e853821; its checks omit the unittest workflow. |
| Replacement destination | P03-02, P03-03, P04-01, P04-02, P04-03, P05-02, P05-03, P06-02, P06-03, P09-04, P10-02, P11-03, P11-04, P12-02 |
| Extraction status | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. |
| Outstanding reviewer input | Alan's complete consolidated comment 4948149089 is independently reconciled. Its extraction-only recommendation is accepted; several salvage semantics are modified by the workspace/access/document contracts. |
| Recommended disposition | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence |
| Exact close condition | Every retained behavior/test is reachable in approved replacements or explicitly rejected and Luke/Alan confirm supersession. |
| Exact branch/worktree delete condition | Only after closure, replacement reachability/extraction verification, no protected worktree depends on the branch and explicit team cleanup confirmation. |

### ds#7 — Document Jinja attrs hardening follow-up

| Field | Finding |
| --- | --- |
| URL | https://github.com/NatalyxPlatform/natalyx-design-system/pull/7 |
| Latest inspected head | cedfcc489b1f60842aed3a9701348c85964cfd96 |
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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
| Inspection time | 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York) |
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

Latest inspected head: `e85382150853cf4774948c55b91e330e7e69617e` at 2026-07-12T23:30:00Z (2026-07-12 19:30 America/New_York). The earlier reviewed workflow run/comment baseline was `8df63dd`; Alan's current head is `e853821`.

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

Decomposition impact: retain #122's named invitation, CI and case-surface behavior/tests, but do not collapse WP03/WP04/WP07/WP09. The reconciliation checkpoint is complete; normal dependencies and unresolved decisions now govern readiness.

## Preserved Wave 2 branch

| Field | Finding |
| --- | --- |
| Branch / exact head | feat/byos-journey-wave-2 / 5b63e3a7c3643efcd5f3e74f422d095423b55f59 |
| Corrected #122 base | e85382150853cf4774948c55b91e330e7e69617e |
| Commit ancestry | 3a549baf — phase-1 cluster pages and initial metadata-only request flow; e40eebaa — transactional submission, private rows and canonical case anchoring; 5b63e3a7 — role/owner checks, atomic review audit, fail-closed dispatch and N+1 removal |
| Useful | Projection-driven phase-1 cluster presentation, exact route allowlisting, person-versus-case-side ownership intent, transactional submission/work-item and review/audit patterns, fail-closed item retention, approved Learn status selection and 36 focused tests. |
| Unsafe / superseded | Runtime ensure_column/index DDL; identity/participation/access conflation; caller-supplied role/lens authority; unguarded/global loaders; no RLS or staff capability; metadata readiness represented as an approvable empty document; restart purges case-anchored work items; stale work item can approve a resubmitted row; paused/done actions are not capability-gated. |
| Independent reproductions | Second init_db changed a canonical case-anchored reviewer item from present to absent because participant_id='' matched the orphan cleanup.; After v1 was resolved and v2 resubmitted on the same row, the stale v1 work item approved v2 because review CAS bound only document_id/state, not an immutable submission revision. |
| Validation | Controlled local run: 535 passed, 9 skipped in 12.471s; focused Wave 2 cluster suite 36/36. No branch check runs, PostgreSQL, browser/accessibility or visual evidence was present. |
| Destinations | P01-01, P02-03, P03-01, P03-03, P03-05, P09-01, P09-04, P09-06, P11-03, P11-04, P12-02, P13-05 |
| Disposition | Preserve paused at the exact head; selectively port semantics/tests only after adaptation. Do not merge, cherry-pick, continue implementation or use its runtime schema directly. |

## Alan reconciliation checkpoint

| Field | Contract |
| --- | --- |
| Name | Alan review reconciliation: PRs #122/#124 and preserved Wave 2 |
| Status | Complete — independently reconciled 2026-07-12 |
| Blocks |  |
| May amend | WP01, WP03, WP04, WP05, WP06, WP09, WP10, WP11, WP12, WP13 |
| Avoid wasted review | Do not ask Alan to polish code already known to be architecturally obsolete. Complete the safety/defect review at the contract/test level, identify reusable commits/tests, and stop once findings are captured. Obsolete code can be superseded while its findings become replacement acceptance tests. |

Finding recording:

- Record each finding with PR/head SHA, file/line or diff anchor, severity, reproducible behavior, architecture/product implication, proposed acceptance test and destination PR ID.
- Mark whether the finding concerns reusable behavior, obsolete architecture, security/privacy, accessibility, migration, concurrency, test coverage or product semantics.
- Update the extraction ledger and canonical programme data together; regenerate all plans/manifest. The benched Project catalogue may be dry-run validated but is not remotely mutated by this reconciliation.

Resolution rule:

- Evidence beats plan text: a verified defect or missing contract amends the package.
- Alan proposes technical alternatives and records a concise dissent where needed; Luke resolves product, lifecycle, privacy, commercial and cross-repository architecture decisions.
- Security/privacy/payment/PHI disagreements that exceed internal authority go to the named external reviewer; implementation remains blocked.

Completion evidence:

- Alan's #122 changes, completed #124 findings and preserved Wave 2 branch are fully captured.
- Every finding has a disposition and destination or explicit no-action rationale.
- Luke and Alan accept the workspace/case, invitation, authorship and PR-boundary contract, or an explicit unresolved decision remains blocked.
- The checkpoint is complete; each implementation item remains independently blocked by its unresolved decisions, dependencies and gate evidence.

## Frozen independent recommendation matrix

| ID | Recommendation | Disposition | Rationale | Affected WPs / PRs / gates | Decision |
| --- | --- | --- | --- | --- | --- |
| REC-01 | Treat PR #124 as WP00 extraction material, not a merge/conflict-resolution unit. | Accept | No independently mergeable unit survives the stale base and domain blockers. Preserve concepts/tests through clean replacement work. | WP00; P03-02/03; P04-01/02/03; P05-02/03; P06-02/03; P09-04; P10-02; P11-03/04; P12-02 | No — disposition resolved; closure/deletion still requires later team confirmation. |
| REC-02 | Use corrected PR #122 as the invitation/case-shell baseline. | Accept with modification | #122 is authoritative for named tested behavior and reusable tests, not for final entities, runtime DDL, generic fact/proposal authority or the whole journey model. | WP01; WP02; WP03; WP09; WP10; WP11; WP12 | No. |
| REC-03 | Node 0 must delegate invitations to shared authority and make issuance/redemption transactionally complete. | Accept with modification | One invitation authority serves separate resource targets and lifecycles; optional profile completion is resumable rather than forced into membership redemption. | WP03 P03-02/03; WP06 P06-02; A1/A2 | No; D-AUTH-02 remains for Cognito admission mechanics. |
| REC-04 | Resolve canonical identity, participation, access and authorization before schema encoding. | Accept with modification | Identity binds principal to person; participation records domain relationship; grants carry resource capabilities; authorization uses verified context, ownership and purpose. Lens is presentation only. | P03-02/03/05; P04-01/02; P09-04; P13-05; A1/B1 | Resolved as D-AUTH-03. |
| REC-05 | Restrict IP-entered pre-join GC information and remove unverified suitability ranking/gating. | Accept with modification | Allow minimum-necessary relationship/outreach/logistics context only. Health, mental health, substances, citizenship, race, pregnancy, insurance and eligibility normally wait for authenticated GC entry; no provisional value drives critical decisions. | WP04; WP05 P05-02; WP06; WP10; A1/A2 | Resolved as D-DATA-03; exact cross-role fields remain D-DATA-01. |
| REC-06 | Correct shared-memory private notes and migrate already-written rows. | Accept with modification | Run a metadata-only inventory first; record zero-row evidence if none. If rows exist, deny shared/Ask reads immediately and migrate narrowly without broadening access. | WP04 P04-02; WP10 P10-02; A1/A2 | No; actual affected-row count is execution evidence, not an architecture choice. |
| REC-07 | Preserve Wave 2 work from 5b63e3a rather than reimplementing useful behavior. | Accept with modification | Treat 5b63e3a as the strongest cumulative evidence source, not an implementation baseline. Reuse tests and semantics only after the named contract changes. | WP00; WP03; WP09; WP11; WP12; WP13; A2/B1 | No. |
| REC-08 | Separate metadata-only document requests from the full content pipeline. | Accept with modification | A request/readiness marker is not a document. Content state and review begin only after a version exists, and partial merges fail closed. | WP09 P09-01/03/04/05/06; P12-02; A2 | D-DOC-01/02 and D-PHI-01 remain open for content. |
| REC-09 | Move foundational RLS and non-owner runtime before real-user PII. | Accept | App-only checks are inadequate for real-user PII given current broad readers. No alternative isolation model has equivalent evidence at lower programme cost. | WP13 P13-05/06/07; B1/B2 | D-PHI-01/02 remain for approved scope/controls/approvers, not for whether RLS precedes B1. |
| REC-10 | Make #122 Python CI required, stable and resistant to bypass. | Defer | Accept the workflow recommendation now, but enforcement choice/evidence is unavailable. Until D-CI-01 resolves, do not call it bypass-resistant or open real-user gates. | WP01 P01-01; A0 and every later app PR | Yes — D-CI-01, owner Luke; options and required readback/negative test are recorded. |
| REC-11 | Add an explicit Node 0 IP-owner guard and correct non-IP behavior. | Accept with modification | Use one subject-derived capability policy across commands and pages; return explicit deny/role destination without creating a case. | WP03 P03-05; WP05 P05-03; A1 | No. |
| REC-12 | Bound and type Node 0 inputs and malformed request behavior. | Accept | Use strict enums/max lengths plus body/collection limits and controlled 4xx errors; do not silently truncate. | WP05; WP06; WP09; WP12 | No; exact numerical limits are PR acceptance details and D-DOC-02 for files. |
| REC-13 | Move candidate and invitation invariants from app checks into PostgreSQL migrations. | Accept | Business invariants that can be represented in PostgreSQL must remain true independently of application races. | WP02; WP03; WP04; WP05; A1 | No. |
| REC-14 | Replace broad public/cloud prefixes with explicit exposure. | Accept | Explicit route identity is the simplest fail-closed control for the current app. | WP03; WP05; WP06; WP09; WP13; A1/A2 | No. |
| REC-15 | Project expiry on GET and add token/PDF cache, referrer and indexing protections. | Accept | Read projection and mutation must agree, and sensitive responses must be non-cacheable with restrictive referrer/noindex policy. | WP03; WP05 | No. |
| REC-16 | Bound candidate/invitation and memory queries and remove N+1 behavior. | Accept | Filter/limit at the authoritative storage boundary rather than after loading broad rows. | WP05; WP09; WP10; WP12 | No. |
| REC-17 | Add candidate retention, archive, correction and deletion behavior. | Accept | Implement the lifecycle in the candidate domain; keep the exact duration as the named bounded privacy decision. | WP04; WP05 P05-02; A1 | Yes — D-DATA-02 supplies duration and exception policy before live use. |
| REC-18 | Move #124's large global CSS addition to route-scoped Node 0 styling. | Accept with modification | Port only necessary styles through route scope and released DS contracts; block on interaction/accessibility/security, not cosmetic literal purity. | WP05; WP11; WP12 | No. |
| REC-19 | Retain unaddressed claim semantics and one-time share-link rotation. | Accept with modification | Retain token mechanics and low-risk semantics only for a pending free-workspace claim; never layer bearer access onto a paid case. | WP03 P03-02/03; WP06 | Resolved by D-AUTH-01. |
| REC-20 | Standardize organization handling on NATALYX_ORG_ID. | Reject | Configuration unification is convenient evidence, not the final authorization model. Organization must be verified from the authenticated/granted resource context. | WP03 P03-05; WP13 P13-05 | No. |
| REC-21 | Land the GC at shared /case/home and remove a duplicate GC Node 0 home. | Accept with modification | Keep one shared participant shell pattern, but route by actual resource: free-workspace GC projection before promotion, case home only after paid-case access exists. | WP03; WP06; WP09; WP12 | No. |
| REC-22 | Keep return_to, token-scoped landing, duplicate-home cleanup, symbol cleanup and refreshed DS assets from #124. | Accept with modification | Adopt the behavior and cleanup, but keep redirect validation, resource-specific landing and canonical DS release ownership. | WP03; WP05; WP11; WP12 | No. |

### Assessment detail

#### REC-01 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Treat PR #124 as WP00 extraction material, not a merge/conflict-resolution unit. |
| Supporting evidence | Alan comment 4948149089; #124@84a5a84; merge-tree against #122@e853821 produced about 93 conflict regions across 11 files. |
| Prior plan treatment | Already warned against merge but left final disposition pending. |
| Assumptions | Corrected #122 and replacement PRs remain available as source history. |
| Security, privacy and operational impact | Avoids stale invitation/security behavior and case-shaped Node 0 reaching users; preserves useful tests/copy/assets. |
| Dependency and migration impact | WP00 ledger; P03/P04/P05/P06/P09/P10/P11/P12 destinations; no branch mutation. |
| Alternatives considered | Merge whole branch; cherry-pick mixed commits; file-level extraction. |
| Rationale | No independently mergeable unit survives the stale base and domain blockers. Preserve concepts/tests through clean replacement work. |
| Affected WPs / PRs / gates | WP00; P03-02/03; P04-01/02/03; P05-02/03; P06-02/03; P09-04; P10-02; P11-03/04; P12-02 |
| Explicit decision required | No — disposition resolved; closure/deletion still requires later team confirmation. |

#### REC-02 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Use corrected PR #122 as the invitation/case-shell baseline. |
| Supporting evidence | e853821; 499-test report and green workflow; verified return_to, TTL ceiling, CAS, self/existing-member refusal, one-live-GC invariant, transactional join, paired lenses and fail-closed Learn. |
| Prior plan treatment | Selective salvage, pending reconciliation. |
| Assumptions | Behavioral tests can be ported without retaining startup DDL or the case-only domain model. |
| Security, privacy and operational impact | Retains proven concurrency/auth safety while preventing weak participation/provenance/schema semantics becoming programme authority. |
| Dependency and migration impact | P01-01, P03-01/03/05, P09-04, P11-03/04, P12-02; re-express schema through WP02. |
| Alternatives considered | Treat all #122 code/schema as canonical; discard it; behavior/test baseline only. |
| Rationale | #122 is authoritative for named tested behavior and reusable tests, not for final entities, runtime DDL, generic fact/proposal authority or the whole journey model. |
| Affected WPs / PRs / gates | WP01; WP02; WP03; WP09; WP10; WP11; WP12 |
| Explicit decision required | No. |

#### REC-03 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Node 0 must delegate invitations to shared authority and make issuance/redemption transactionally complete. |
| Supporting evidence | #124 splits supersede/create/link/timeline and redemption/profile facts across commits; corrected #122 supplies CAS/TTL guards. |
| Prior plan treatment | Separate workspace claim and paid-case invitation but transaction boundary was underspecified. |
| Assumptions | Identity-provider interaction may require an idempotent completion workflow around a database transaction/outbox. |
| Security, privacy and operational impact | Prevents valid orphan tokens, partial membership/onboarding and possession-only case access. |
| Dependency and migration impact | P03-02 atomically binds workspace claim/identity/consent; P03-03 atomically redeems invite/participation/access/consent/audit; P06-02 resumes optional onboarding idempotently. |
| Alternatives considered | One huge cross-system transaction; explicit idempotent saga/outbox; current sequential commits. |
| Rationale | One invitation authority serves separate resource targets and lifecycles; optional profile completion is resumable rather than forced into membership redemption. |
| Affected WPs / PRs / gates | WP03 P03-02/03; WP06 P06-02; A1/A2 |
| Explicit decision required | No; D-AUTH-02 remains for Cognito admission mechanics. |

#### REC-04 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Resolve canonical identity, participation, access and authorization before schema encoding. |
| Supporting evidence | #122/Wave 2 account_memberships roles double as party role, lens and authorization; first-active membership selection; no party/person alignment; callers pass viewer role/lens; RLS absent. |
| Prior plan treatment | Roles, membership and projections were present but their ownership was not explicit. |
| Assumptions | A principal can be staff globally without participant-data access and a person can participate without an active grant. |
| Security, privacy and operational impact | Eliminates confused role authority and gives application/RLS one auditable policy input. |
| Dependency and migration impact | P03-05 adds identity binding, participation and access-grant constraints; later domain migrations and P13-05 consume the contract. |
| Alternatives considered | Single membership table/role enum; participation-only authorization; separate grants/capabilities. |
| Rationale | Identity binds principal to person; participation records domain relationship; grants carry resource capabilities; authorization uses verified context, ownership and purpose. Lens is presentation only. |
| Affected WPs / PRs / gates | P03-02/03/05; P04-01/02; P09-04; P13-05; A1/B1 |
| Explicit decision required | Resolved as D-AUTH-03. |

#### REC-05 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Restrict IP-entered pre-join GC information and remove unverified suitability ranking/gating. |
| Supporting evidence | #124 scores mental health, substance, citizenship, pregnancy and support claims into 0-100/high_viability/critical_flag and sorts/gates guidance. |
| Prior plan treatment | Provisional attribution existed but still allowed a preliminary hard-criteria check. |
| Assumptions | Before GC joins, the legitimate purpose is low-pressure outreach preparation, not eligibility or professional assessment. |
| Security, privacy and operational impact | Reduces sensitive third-party processing, discrimination and false clinical/eligibility authority. |
| Dependency and migration impact | P04-02 provenance; P05-02 strict allowlist; P06-02 GC-authored data; P10 scopes; legacy scores retained only as source-labelled evidence or excluded. |
| Alternatives considered | Keep ranking with disclaimer; professional approval later; neutral questions only. |
| Rationale | Allow minimum-necessary relationship/outreach/logistics context only. Health, mental health, substances, citizenship, race, pregnancy, insurance and eligibility normally wait for authenticated GC entry; no provisional value drives critical decisions. |
| Affected WPs / PRs / gates | WP04; WP05 P05-02; WP06; WP10; A1/A2 |
| Explicit decision required | Resolved as D-DATA-03; exact cross-role fields remain D-DATA-01. |

#### REC-06 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Correct shared-memory private notes and migrate already-written rows. |
| Supporting evidence | #124 saves Conversation Guide notes with scope=shared and Ask loads shared memory; local inspected SQLite had zero affected rows; #124 was not deployed; remote database state was not verified. |
| Prior plan treatment | New private/shared ledger planned; explicit legacy remediation was missing. |
| Assumptions | Source kind identifies guide notes and owner can normally be recovered from subject/person provenance. |
| Security, privacy and operational impact | Prevents IP reflection notes reaching GC/provider/intelligence while preserving audit and avoiding content in logs. |
| Dependency and migration impact | P04-02 person-owned contract; P10-02 inventory, immediate exclusion, idempotent private/quarantine migration; ambiguous owner quarantines. |
| Alternatives considered | Behavior-only fix; delete rows; owner-safe migration/quarantine. |
| Rationale | Run a metadata-only inventory first; record zero-row evidence if none. If rows exist, deny shared/Ask reads immediately and migrate narrowly without broadening access. |
| Affected WPs / PRs / gates | WP04 P04-02; WP10 P10-02; A1/A2 |
| Explicit decision required | No; actual affected-row count is execution evidence, not an architecture choice. |

#### REC-07 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Preserve Wave 2 work from 5b63e3a rather than reimplementing useful behavior. |
| Supporting evidence | Exact three-commit stack on e853821; 535 passed/9 skipped and 36 focused tests; two independent defects reproduced; runtime DDL, caller roles, broad loaders and no RLS remain. |
| Prior plan treatment | Wave 2 was previously missing and blocked final mapping. |
| Assumptions | The branch remains paused and available for later extraction. |
| Security, privacy and operational impact | Saves tested presentation/transaction semantics without importing restart loss, stale approval, metadata/content conflation or weak access. |
| Dependency and migration impact | P03-05, P09-01/04/06, P11-03/04, P12-02, P13-05; schema re-expressed as migrations. |
| Alternatives considered | Direct merge/cherry-pick; discard; selective adaptation/test port. |
| Rationale | Treat 5b63e3a as the strongest cumulative evidence source, not an implementation baseline. Reuse tests and semantics only after the named contract changes. |
| Affected WPs / PRs / gates | WP00; WP03; WP09; WP11; WP12; WP13; A2/B1 |
| Explicit decision required | No. |

#### REC-08 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Separate metadata-only document requests from the full content pipeline. |
| Supporting evidence | Wave 2 creates an approvable documents row with storage_uri empty; request labels may contain sensitive data; P09 baseline coupled active-case UI to full upload pipeline. |
| Prior plan treatment | P09-04 depended on P09-03 and mixed progress/documents; no independent requirement/work-item model. |
| Assumptions | Phase-1 readiness coordination can operate synthetically without receiving file bytes. |
| Security, privacy and operational impact | Avoids false artifact approval and permits safe partial delivery while content remains quarantined/disabled. |
| Dependency and migration impact | P09-01 defines both machines; P09-04 owns metadata requirements/work items and phase-1 surfaces without P09-03; P09-06 integrates content versions after P09-03; P09-05 depends P09-06. |
| Alternatives considered | Single documents table; metadata-only workflow first; full pipeline first. |
| Rationale | A request/readiness marker is not a document. Content state and review begin only after a version exists, and partial merges fail closed. |
| Affected WPs / PRs / gates | WP09 P09-01/03/04/05/06; P12-02; A2 |
| Explicit decision required | D-DOC-01/02 and D-PHI-01 remain open for content. |

#### REC-09 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Move foundational RLS and non-owner runtime before real-user PII. |
| Supporting evidence | Runtime uses owner-level startup DDL; app/Wave 2 storage has broad/global loaders; no DB policy enforcement or pool-context proof. |
| Prior plan treatment | P13-05 was a B2 prerequisite only. |
| Assumptions | Synthetic A1/A2 may validate features before B1, but no real subject data is admitted. |
| Security, privacy and operational impact | Database denies cross-org/resource/owner access if an app guard fails; reduces B1 breach blast radius. |
| Dependency and migration impact | P13-05/06/07 move to B1; FORCE RLS, NOBYPASSRLS runtime, transaction-local verified context and pool reset tests; B2 remains separate evidence approval. |
| Alternatives considered | App-only isolation; separate databases per cohort; RLS at B2. |
| Rationale | App-only checks are inadequate for real-user PII given current broad readers. No alternative isolation model has equivalent evidence at lower programme cost. |
| Affected WPs / PRs / gates | WP13 P13-05/06/07; B1/B2 |
| Explicit decision required | D-PHI-01/02 remain for approved scope/controls/approvers, not for whether RLS precedes B1. |

#### REC-10 — Defer

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Make #122 Python CI required, stable and resistant to bypass. |
| Supporting evidence | #122 workflow passed; #124 ran only build/contract checks; main lacks Python/PostgreSQL CI; private-repo protection/ruleset API returned plan-level 403. |
| Prior plan treatment | P01-01 added tests but did not define stable contexts, workflow hardening or enforcement limitation. |
| Assumptions | Repository billing/visibility may change independently of code. |
| Security, privacy and operational impact | Prevents test-path bypass and false governance claims; adds PostgreSQL evidence. |
| Dependency and migration impact | P01-01: no path filters, stable names, pinned action SHAs, supported runtime, constraints, timeouts, PostgreSQL job; D-CI-01 governs repository enforcement/readback. |
| Alternatives considered | Procedural review only; GitHub plan/ruleset upgrade; externally enforced merge queue. |
| Rationale | Accept the workflow recommendation now, but enforcement choice/evidence is unavailable. Until D-CI-01 resolves, do not call it bypass-resistant or open real-user gates. |
| Affected WPs / PRs / gates | WP01 P01-01; A0 and every later app PR |
| Explicit decision required | Yes — D-CI-01, owner Luke; options and required readback/negative test are recorded. |

#### REC-11 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Add an explicit Node 0 IP-owner guard and correct non-IP behavior. |
| Supporting evidence | #124 ensure endpoint lets any authenticated subject mint a primary-IP case; viewer/provider/staff paths can fall into storage errors/500. |
| Prior plan treatment | General workspace authorization existed without a shared participant/API guard acceptance matrix. |
| Assumptions | Staff tools are separate from participant Node 0 routes. |
| Security, privacy and operational impact | Prevents privilege creation, role confusion and avoidable errors. |
| Dependency and migration impact | P03-05 subject-derived capabilities; P05-03 shared IP-owner guard and negative role tests. |
| Alternatives considered | Per-route checks; shared router dependency/service policy; redirect all roles. |
| Rationale | Use one subject-derived capability policy across commands and pages; return explicit deny/role destination without creating a case. |
| Affected WPs / PRs / gates | WP03 P03-05; WP05 P05-03; A1 |
| Explicit decision required | No. |

#### REC-12 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Bound and type Node 0 inputs and malformed request behavior. |
| Supporting evidence | #124 hand-parses unbounded names/notes/questions/JSON/forms/collections/PDF content; Wave 2 silently truncates labels/notes. |
| Prior plan treatment | Validation was implicit and spread across feature PRs. |
| Assumptions | Limits can be product-specific but must reject rather than silently alter user data. |
| Security, privacy and operational impact | Controls denial-of-service, log/storage amplification and ambiguous stored content. |
| Dependency and migration impact | P05-02 typed candidate commands/collections; P05-03 form/PDF/body limits; P06-02 onboarding; P09-04 structured metadata/reviewer note; P12-01 Ask. |
| Alternatives considered | Global proxy limit only; silent slicing; layered strict validation. |
| Rationale | Use strict enums/max lengths plus body/collection limits and controlled 4xx errors; do not silently truncate. |
| Affected WPs / PRs / gates | WP05; WP06; WP09; WP12 |
| Explicit decision required | No; exact numerical limits are PR acceptance details and D-DOC-02 for files. |

#### REC-13 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Move candidate and invitation invariants from app checks into PostgreSQL migrations. |
| Supporting evidence | #124 lacks candidate-case FK, invitation-link uniqueness, one-active-outreach constraint and checks for enums/scores; concurrent writes can violate product rules. |
| Prior plan treatment | WP04/WP05 proposed new schema but did not enumerate all reviewed invariants. |
| Assumptions | Versioned migrations and expand/contract compatibility precede domain tables. |
| Security, privacy and operational impact | Prevents orphan/duplicate/contradictory state under concurrency. |
| Dependency and migration impact | P04-01 FKs/uniqueness; P05-02 outreach constraints and no score bounds because ranking is removed; P03-02/03 claim/invite uniqueness; P02-03 migrations. |
| Alternatives considered | App locks only; advisory locks; database constraints plus commands. |
| Rationale | Business invariants that can be represented in PostgreSQL must remain true independently of application races. |
| Affected WPs / PRs / gates | WP02; WP03; WP04; WP05; A1 |
| Explicit decision required | No. |

#### REC-14 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Replace broad public/cloud prefixes with explicit exposure. |
| Supporting evidence | #124 exposes /node0/onboarding/ publicly and /api/node0/ by prefix; Wave 2 demonstrates exact phase-1 allowlisting. |
| Prior plan treatment | Fail-closed route policy existed but did not assign this finding. |
| Assumptions | New routes require explicit security review before cloud/public reachability. |
| Security, privacy and operational impact | Prevents future routes inheriting token/public or cloud exposure accidentally. |
| Dependency and migration impact | P03-02, P05-03, P06-02 exact registries/dependencies; P09-04 exact cluster paths; P13-03 route-negative inventory. |
| Alternatives considered | Prefix allowlist; per-route registry; separate public app. |
| Rationale | Explicit route identity is the simplest fail-closed control for the current app. |
| Affected WPs / PRs / gates | WP03; WP05; WP06; WP09; WP13; A1/A2 |
| Explicit decision required | No. |

#### REC-15 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Project expiry on GET and add token/PDF cache, referrer and indexing protections. |
| Supporting evidence | #124 expired links look active until POST; token-bearing pages/PDFs lack no-store and restrictive referrer policy. |
| Prior plan treatment | Token transitions were covered, response exposure was not. |
| Assumptions | Tokens remain URL-borne only where unavoidable and never appear in telemetry. |
| Security, privacy and operational impact | Reduces stale-action confusion and token/sensitive-output leakage via browser cache, referrer or indexing. |
| Dependency and migration impact | P03-02/03 GET+command expiry and response headers; P05-03 outreach PDF headers; security tests. |
| Alternatives considered | POST-only check; session exchange; header hardening plus one-time token. |
| Rationale | Read projection and mutation must agree, and sensitive responses must be non-cacheable with restrictive referrer/noindex policy. |
| Affected WPs / PRs / gates | WP03; WP05 |
| Explicit decision required | No. |

#### REC-16 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Bound candidate/invitation and memory queries and remove N+1 behavior. |
| Supporting evidence | #124 looks up invitations per candidate and loads all shared memory before Python filtering; Wave 2 removes one reviewer-inbox N+1 but retains broad loaders. |
| Prior plan treatment | Performance was a general risk rather than explicit acceptance criteria. |
| Assumptions | Pagination and purpose-scoped limits are compatible with Node 0 and Ask UX. |
| Security, privacy and operational impact | Bounds latency/memory, narrows accidental data access and improves tenant isolation. |
| Dependency and migration impact | P05-02 batched query-shaped hydration/indexes; P10-02 scope/subject limits at persistence; P12-01 bounded context; P09-04 owner-scoped query shapes. |
| Alternatives considered | Cache current readers; batch only; purpose-scoped SQL. |
| Rationale | Filter/limit at the authoritative storage boundary rather than after loading broad rows. |
| Affected WPs / PRs / gates | WP05; WP09; WP10; WP12 |
| Explicit decision required | No. |

#### REC-17 — Accept

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Add candidate retention, archive, correction and deletion behavior. |
| Supporting evidence | #124 stores sensitive third-party assessments without a lifecycle; current plan has D-DATA-02 but implementation mapping was weak. |
| Prior plan treatment | Retention decision and legacy backfill existed. |
| Assumptions | Legal/privacy may set the exact period; source/audit may require tombstones rather than raw-content retention. |
| Security, privacy and operational impact | Reduces unnecessary third-party data retention while preserving correction/audit needs. |
| Dependency and migration impact | D-DATA-02; P04-02/03 provenance/tombstones; P05-02 archive/anonymize/delete command/job and evidence. |
| Alternatives considered | Indefinite retention; immediate deletion; shortest justified period with tombstone/audit. |
| Rationale | Implement the lifecycle in the candidate domain; keep the exact duration as the named bounded privacy decision. |
| Affected WPs / PRs / gates | WP04; WP05 P05-02; A1 |
| Explicit decision required | Yes — D-DATA-02 supplies duration and exception policy before live use. |

#### REC-18 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Move #124's large global CSS addition to route-scoped Node 0 styling. |
| Supporting evidence | About 3,030 lines were added to global style.css; participant DS and route-specific recipes exist. |
| Prior plan treatment | P05-03 and P11-03 mentioned DS adoption but not the global-style finding. |
| Assumptions | Participant and internal/operator design systems remain separate. |
| Security, privacy and operational impact | Limits cross-surface regressions and clarifies style ownership without making aesthetic purity a release gate. |
| Dependency and migration impact | P05-03 node0.css; P11-03 released tokens/recipes; P12-02 visual/a11y verification. |
| Alternatives considered | Keep global block; CSS modules/build; route stylesheet plus shared DS. |
| Rationale | Port only necessary styles through route scope and released DS contracts; block on interaction/accessibility/security, not cosmetic literal purity. |
| Affected WPs / PRs / gates | WP05; WP11; WP12 |
| Explicit decision required | No. |

#### REC-19 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Retain unaddressed claim semantics and one-time share-link rotation. |
| Supporting evidence | #124 gates allow_unaddressed to GC intent, stores hash only, rotates/supersedes, and displays plaintext once; corrected #122 supplies case-invite guards. |
| Prior plan treatment | Workspace claim separated conceptually but shared engine/resource-target distinction was incomplete. |
| Assumptions | Bearer possession cannot reveal sensitive data or create paid-case membership. |
| Security, privacy and operational impact | Keeps low-friction outreach while bounding replay, forwarding and privilege escalation. |
| Dependency and migration impact | P03-02 workspace claim target; P03-03 recipient-bound case target; shared token/CAS primitives, distinct state machines and consent. |
| Alternatives considered | Addressed links only; unaddressed case invite; unaddressed low-risk workspace claim. |
| Rationale | Retain token mechanics and low-risk semantics only for a pending free-workspace claim; never layer bearer access onto a paid case. |
| Affected WPs / PRs / gates | WP03 P03-02/03; WP06 |
| Explicit decision required | Resolved by D-AUTH-01. |

#### REC-20 — Reject

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Standardize organization handling on NATALYX_ORG_ID. |
| Supporting evidence | #124 restores a configured organization constant, but the intended product is multi-resource/multi-tenant and Wave 2 reviewers/readers are insufficiently org-scoped. |
| Prior plan treatment | Organization scope is part of case/workspace contracts and RLS. |
| Assumptions | A fixed organization may remain a synthetic/dev bootstrap default only. |
| Security, privacy and operational impact | Prevents a deployment constant becoming tenant/access authority. |
| Dependency and migration impact | P03-05 and P13-05 derive organization from verified identity/grant/resource context; config default permitted only in synthetic bootstrap. |
| Alternatives considered | Global configured org; identity claim; resource/grant-derived org context. |
| Rationale | Configuration unification is convenient evidence, not the final authorization model. Organization must be verified from the authenticated/granted resource context. |
| Affected WPs / PRs / gates | WP03 P03-05; WP13 P13-05 |
| Explicit decision required | No. |

#### REC-21 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Land the GC at shared /case/home and remove a duplicate GC Node 0 home. |
| Supporting evidence | #122 has paired case lenses; #124 routes GC to case home after bearer redemption even though Node 0 should not yet create a case. |
| Prior plan treatment | Free workspace and paid case are separate but landing wording was not explicit. |
| Assumptions | The GC may join a free workspace before any promotion and later receive a paid-case invitation. |
| Security, privacy and operational impact | Avoids duplicate participant shells and prevents pre-promotion users from being shown a canonical-case fiction. |
| Dependency and migration impact | P03-02/P06 workspace lens before promotion; P03-03/P09-04 shared case home only after canonical paid-case grant; P12 cutover removes duplicates. |
| Alternatives considered | Always case home; duplicate GC Node 0 home; shared shell with resource-specific projection. |
| Rationale | Keep one shared participant shell pattern, but route by actual resource: free-workspace GC projection before promotion, case home only after paid-case access exists. |
| Affected WPs / PRs / gates | WP03; WP06; WP09; WP12 |
| Explicit decision required | No. |

#### REC-22 — Accept with modification

| Assessment field | Recorded conclusion |
| --- | --- |
| Recommendation | Keep return_to, token-scoped landing, duplicate-home cleanup, symbol cleanup and refreshed DS assets from #124. |
| Supporting evidence | Corrected #122 validates internal return_to; #124 provides one-time token landing and presentation cleanup; canonical participant DS owns released assets/tokens. |
| Prior plan treatment | Most items were salvage candidates without precise ownership. |
| Assumptions | DS assets are ported from an approved release, not vendored ad hoc. |
| Security, privacy and operational impact | Preserves UX value and resume behavior without weakening redirect, token or repository boundaries. |
| Dependency and migration impact | P03-01 return_to; P03-02 token landing; P11-03 DS release; P05-03/P12-02 selective UI cleanup. |
| Alternatives considered | Copy branch files; discard polish; selective port from approved contracts. |
| Rationale | Adopt the behavior and cleanup, but keep redirect validation, resource-specific landing and canonical DS release ownership. |
| Affected WPs / PRs / gates | WP03; WP05; WP11; WP12 |
| Explicit decision required | No. |

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
