---
title: '\plantitle{Natalyx MVP Fixes}'
title-meta: "Natalyx MVP Fixes"
subtitle: "Consolidated plan overview - fourteen coordinated work packages"
author: "L. Rhodes (plan owner) - A. Zhao (technical feedback reconciled)"
date: "2026-07-12"
---


# Purpose and approved planning update

This is the reconciled planning document for cleaning up the current Natalyx MVP delivery surface without losing useful work or compounding the present architecture. It preserves fourteen bounded work packages and now contains 52 suggested pull requests. The detailed Markdown and PDF plan for each work package is supplied separately in the `MVP Fixes` Drive folder.

The GitHub Project is deliberately benched until this plan is reviewed. Only PRs whose local-preparation field expressly permits isolated, uncommitted, synthetic-only preparation may be touched before joint acceptance; nothing authorizes commit, PR creation, merge, branch cleanup, cloud changes, payment activation, real-user use or PHI processing.

Alan's completed technical feedback, corrected #122 and preserved Wave 2 have been independently reconciled. The founder interview is complete: all 24 decision IDs are classified, founder outcomes are final where recorded, and remaining technical controls and external approvals are explicitly separated from those final policies.

# Current position

| Area | Current conclusion | Planning consequence |
| --- | --- | --- |
| Live dev | The inspected endpoint returned ALB 503. | Treat live recovery and known-revision evidence as Gate A0, separate from green CI. |
| PR 122 | Authoritative baseline for named invitation/resume/lens behavior and tests, but not the final schema/domain architecture. | Selectively port behavior/tests; supersede runtime DDL and conflated access/provenance models. |
| PR 124 | Alan's complete review confirms high extraction value but a stale/conflicted and unsafe merge unit. | Fully supersede as a merge unit; port only approved concepts/tests/copy/assets. |
| Wave 2 | Exact three-commit stack at 5b63e3a; 535 tests passed locally, with restart-loss and stale-review defects independently reproduced. | Preserve paused; adapt phase-1 presentation, transaction patterns and tests under P03/P09/P13. |
| Access / CI | Identity/participation/access were conflated and RLS absent. GitHub Team is commercially approved but not yet activated or configured. | P03-05 resolves the access model; P13-05 precedes B1; D-CI-01 keeps A0 and implementation merges blocked until enforcement is active and verified. |
| Node 0 | Free exploration, Complete entitlement, commitment, payment and paid case are currently too entangled. | Separate their entities and state machines before expanding UI. |
| Commercial | Founder beta pricing, commitment, credit, refund, loss and grace policies are final; no append-only money ledger or promotion authority exists yet. | Implement the settled policies as versioned processor-neutral contracts; external terms/tax review still precedes live acceptance or charging. |
| Documents/PHI | Documents are metadata-only and the provider branch is unreviewed. | Keep synthetic-only through A2, approved PII at B1, and PHI blocked until formal B2. |

# Architecture spine

- Node 0 begins as a free workspace; opening it never creates a canonical paid case.
- Workspace, entitlement, commercial commitment, payment, case, invitation/claim, document and journey-stage lifecycles remain separate.
- Identity binds principal to person; participation records the domain relationship; explicit resource grants carry capabilities; application and RLS authorization also consider ownership and purpose.
- Only `byos.workspace_promotion_authorized.v1` authorizes exactly one `enrollment_pending` case; browser redirects and raw processor callbacks never do.
- IP observations remain IP-attributed and provisional. GC confirmation appends a GC-authored revision; it never silently overwrites or upgrades the source.
- Metadata requirements/readiness/work items are not document content. Content versions have a separate upload, quarantine, scan, review, replacement and download lifecycle.
- The app owns durable case truth, authorization and PHI policy. Intelligence returns advisory proposals only. Learn artifacts and design-system releases remain pinned repository contracts.
- PostgreSQL is production authority. Versioned, ordered migrations replace runtime DDL, with locking, checksums, expand/contract compatibility and forward repair.
- Forced RLS and a non-owner runtime precede B1 real-user PII. PHI remains disabled until B2 evidence and human acceptance; merge or deployment success accepts neither gate.

# Work-package map

| WP | Work package | Suggested PRs | Proposed lead | Reviewer | Gate range |
| --- | --- | --- | --- | --- | --- |
| WP00 | Preservation, cloud diagnosis, and PR reconciliation | 1 | Luke | Alan | Pre-A0 |
| WP01 | CI and PostgreSQL evidence gate | 1 | Alan | Luke | A0 |
| WP02 | Versioned migrations and readiness | 4 | Alan | Luke | A0, A1 |
| WP03 | Authentication, invitations, and resume | 5 | Alan | Luke | A1, A2 |
| WP04 | Node 0 workspace and paid-case separation | 3 | Alan | Luke | A1 |
| WP05 | Node 0 Free, Pathfinder, and resume | 3 | Luke | Alan | A1 |
| WP06 | Node 0 Complete and GC soft onboarding | 3 | Alan | Luke | A2 |
| WP07 | Commercial configuration, enrollment, and promotion | 4 | Luke | Alan | A2 |
| WP08 | Payments, invoices, credits, and refunds | 4 | Luke | Alan | A2 |
| WP09 | Documents, active case, and provider handoffs | 6 | Alan | Luke | A2 |
| WP10 | Intelligence, memory, proposals, and Ask safety | 4 | Alan | Luke | A2 |
| WP11 | Learn release and design-system contract | 4 | Luke | Alan | A1, A2 |
| WP12 | Ask/Learn shell and mobile cutover | 3 | Luke | Alan | A2, B1 |
| WP13 | Deployment, cloud gates, and PHI readiness | 7 | Alan | Luke | A0, A1, A2, B1 |

# Suggested ownership and reciprocal review

This is the proposed working split for discussion, chosen to keep product/commercial/content-heavy work with Luke and foundation/security/data/runtime work with Alan while retaining reciprocal review:

| Lead | Work packages | Primary responsibility | Review partner |
| --- | --- | --- | --- |
| Luke | WP00, WP05, WP07, WP08, WP11, WP12 | Programme reconciliation; Node 0 Free product boundary; commercial/payment contracts; Learn/design-system release; participant shell/cutover. | Alan reviews technical architecture, migration, security and failure behavior. |
| Alan | WP01, WP02, WP03, WP04, WP06, WP09, WP10, WP13 | CI/PostgreSQL; migrations; auth/invitations; workspace/case model; GC onboarding; documents/provider handoff; intelligence; deployment/gates. | Luke reviews product, privacy, commercial, role, truth and release acceptance. |

External security, privacy, payment, finance, legal, accessibility or provider review remains mandatory where the detailed package names it. The split can be amended before implementation; it is not an assignment imposed by the plan.

# Delivery sequence

| Phase | Work | Can run in parallel | Exit condition |
| --- | --- | --- | --- |
| Planning closeout | Founder decisions incorporated; WP00 is ready for Alan review and joint acceptance | Only expressly marked isolated, uncommitted preparation | Canonical Markdown/PDF package is validated and Drive readback succeeds. |
| Foundation | WP01, WP02 and A0 portions of WP13 | Learn/DS source work in WP11 | Current tests run on PostgreSQL; migration ADR/runner and known-revision recovery evidence are accepted. |
| Identity and domain | WP03 and WP04 | Selected WP10 contract work | Claims/invitations are safe and Node 0 workspace is distinct from paid case. |
| Participant core | WP05 and WP06 | Commercial configuration in WP07 | Free and Complete flows are resumable, attributable and role-scoped. |
| Commercial and operations | WP07, WP08, WP09 and WP10 | Separate repositories can progress behind pinned contracts | Synthetic A2 covers promotion, money, documents, proposals and failure recovery. |
| Release and cutover | WP11, WP12 and remaining WP13 | Evidence collection across repos | A1/A2 pass; B1/B2 remain separately controlled human gates. |

# Programme gates

| Gate | Purpose | Owner | Verifier | Failure rule |
| --- | --- | --- | --- | --- |
| A0 | Infrastructure recovery and known-revision health | Alan | Luke | Do not proceed to participant validation. Freeze live updates, retain evidence, restore the known compatible image/schema or forward-repair under the approved runbook, and keep the Project gate blocked. |
| A1 | Synthetic core participant journey | Alan | Luke | Stop before Complete, commercial or paid-case validation. Revert/disable the failing participant feature flag or deploy the known A0 revision; preserve synthetic data only for defect diagnosis, then purge under the runbook. |
| A2 | Synthetic commercial, promotion, billing and document journey | Alan | Luke | Disable commercial/document/provider features, retain free/safety content, prevent live money or real documents, reconcile synthetic ledger inconsistencies, and restore the A1-known revision or forward-repair as approved. |
| B1 | Real-user and PII beta readiness | Luke | External/TBD | No real-user invitation. Continue synthetic-only, close control gaps, invalidate stale evidence and re-run the exact affected reviews/tests before a new go/no-go. |
| B2 | PHI readiness and formal go/no-go | Luke | External security/privacy/compliance reviewers | PHI remains prohibited. Keep B1 PII scope only if still independently valid; disable any PHI-capable upload/context path, remediate, and repeat formal review. |

# Recommendation disposition matrix

The full assessment record, including evidence, assumptions, impacts, alternatives and migration implications, is in WP00. This is the decision view:

| ID | Recommendation | Disposition | Rationale | Affected work | Decision |
| --- | --- | --- | --- | --- | --- |
| REC-01 | Treat PR #124 as WP00 extraction material, not a merge/conflict-resolution unit. | Accept | No independently mergeable unit survives the stale base and domain blockers. Preserve concepts/tests through clean replacement work. | WP00; P03-02/03; P04-01/02/03; P05-02/03; P06-02/03; P09-04; P10-02; P11-03/04; P12-02 | No - disposition resolved; closure/deletion still requires later team confirmation. |
| REC-02 | Use corrected PR #122 as the invitation/case-shell baseline. | Accept with modification | #122 is authoritative for named tested behavior and reusable tests, not for final entities, runtime DDL, generic fact/proposal authority or the whole journey model. | WP01; WP02; WP03; WP09; WP10; WP11; WP12 | No. |
| REC-03 | Node 0 must delegate invitations to shared authority and make issuance/redemption transactionally complete. | Accept with modification | One invitation authority serves separate resource targets and lifecycles; optional profile completion is resumable rather than forced into membership redemption. | WP03 P03-02/03; WP06 P06-02; A1/A2 | No; D-AUTH-02 remains for Cognito admission mechanics. |
| REC-04 | Resolve canonical identity, participation, access and authorization before schema encoding. | Accept with modification | Identity binds principal to person; participation records domain relationship; grants carry resource capabilities; authorization uses verified context, ownership and purpose. Lens is presentation only. | P03-02/03/05; P04-01/02; P09-04; P13-05; A1/B1 | Resolved as D-AUTH-03. |
| REC-05 | Restrict IP-entered pre-join GC information and remove unverified suitability ranking/gating. | Accept with modification | Allow minimum-necessary relationship/outreach/logistics context only. Health, mental health, substances, citizenship, race, pregnancy, insurance and eligibility normally wait for authenticated GC entry; no provisional value drives critical decisions. | WP04; WP05 P05-02; WP06; WP10; A1/A2 | Resolved as D-DATA-03; exact cross-role fields remain D-DATA-01. |
| REC-06 | Correct shared-memory private notes and migrate already-written rows. | Accept with modification | Run a metadata-only inventory first; record zero-row evidence if none. If rows exist, deny shared/Ask reads immediately and migrate narrowly without broadening access. | WP04 P04-02; WP10 P10-02; A1/A2 | No; actual affected-row count is execution evidence, not an architecture choice. |
| REC-07 | Preserve Wave 2 work from 5b63e3a rather than reimplementing useful behavior. | Accept with modification | Treat 5b63e3a as the strongest cumulative evidence source, not an implementation baseline. Reuse tests and semantics only after the named contract changes. | WP00; WP03; WP09; WP11; WP12; WP13; A2/B1 | No. |
| REC-08 | Separate metadata-only document requests from the full content pipeline. | Accept with modification | A request/readiness marker is not a document. Content state and review begin only after a version exists, and partial merges fail closed. | WP09 P09-01/03/04/05/06; P12-02; A2 | D-DOC-01/02 and D-PHI-01 remain open for content. |
| REC-09 | Move foundational RLS and non-owner runtime before real-user PII. | Accept | App-only checks are inadequate for real-user PII given current broad readers. No alternative isolation model has equivalent evidence at lower programme cost. | WP13 P13-05/06/07; B1/B2 | D-PHI-01/02 remain for approved scope/controls/approvers, not for whether RLS precedes B1. |
| REC-10 | Make #122 Python CI required, stable and resistant to bypass. | Defer | Accept the workflow recommendation now, but enforcement choice/evidence is unavailable. Until D-CI-01 resolves, do not call it bypass-resistant or open real-user gates. | WP01 P01-01; A0 and every later app PR | Yes - D-CI-01, owner Luke; options and required readback/negative test are recorded. |
| REC-11 | Add an explicit Node 0 IP-owner guard and correct non-IP behavior. | Accept with modification | Use one subject-derived capability policy across commands and pages; return explicit deny/role destination without creating a case. | WP03 P03-05; WP05 P05-03; A1 | No. |
| REC-12 | Bound and type Node 0 inputs and malformed request behavior. | Accept | Use strict enums/max lengths plus body/collection limits and controlled 4xx errors; do not silently truncate. | WP05; WP06; WP09; WP12 | No; exact numerical limits are PR acceptance details and D-DOC-02 for files. |
| REC-13 | Move candidate and invitation invariants from app checks into PostgreSQL migrations. | Accept | Business invariants that can be represented in PostgreSQL must remain true independently of application races. | WP02; WP03; WP04; WP05; A1 | No. |
| REC-14 | Replace broad public/cloud prefixes with explicit exposure. | Accept | Explicit route identity is the simplest fail-closed control for the current app. | WP03; WP05; WP06; WP09; WP13; A1/A2 | No. |
| REC-15 | Project expiry on GET and add token/PDF cache, referrer and indexing protections. | Accept | Read projection and mutation must agree, and sensitive responses must be non-cacheable with restrictive referrer/noindex policy. | WP03; WP05 | No. |
| REC-16 | Bound candidate/invitation and memory queries and remove N+1 behavior. | Accept | Filter/limit at the authoritative storage boundary rather than after loading broad rows. | WP05; WP09; WP10; WP12 | No. |
| REC-17 | Add candidate retention, archive, correction and deletion behavior. | Accept | Implement the lifecycle in the candidate domain; keep the exact duration as the named bounded privacy decision. | WP04; WP05 P05-02; A1 | Yes - D-DATA-02 supplies duration and exception policy before live use. |
| REC-18 | Move #124's large global CSS addition to route-scoped Node 0 styling. | Accept with modification | Port only necessary styles through route scope and released DS contracts; block on interaction/accessibility/security, not cosmetic literal purity. | WP05; WP11; WP12 | No. |
| REC-19 | Retain unaddressed claim semantics and one-time share-link rotation. | Accept with modification | Retain token mechanics and low-risk semantics only for a pending free-workspace claim; never layer bearer access onto a paid case. | WP03 P03-02/03; WP06 | Resolved by D-AUTH-01. |
| REC-20 | Standardize organization handling on NATALYX_ORG_ID. | Reject | Configuration unification is convenient evidence, not the final authorization model. Organization must be verified from the authenticated/granted resource context. | WP03 P03-05; WP13 P13-05 | No. |
| REC-21 | Land the GC at shared /case/home and remove a duplicate GC Node 0 home. | Accept with modification | Keep one shared participant shell pattern, but route by actual resource: free-workspace GC projection before promotion, case home only after paid-case access exists. | WP03; WP06; WP09; WP12 | No. |
| REC-22 | Keep return_to, token-scoped landing, duplicate-home cleanup, symbol cleanup and refreshed DS assets from #124. | Accept with modification | Adopt the behavior and cleanup, but keep redirect validation, resource-specific landing and canonical DS release ownership. | WP03; WP05; WP11; WP12 | No. |

# Work-package details

## WP00: Preservation, cloud diagnosis, and PR reconciliation

**Problem.** The live app is returning ALB 503 responses while overlapping draft PRs and protected dirty worktrees contain useful but contradictory implementations.

**Target outcome.** A source-of-truth baseline with Alan's completed review independently dispositioned, existing work mapped, and explicit no-delete/no-close conditions before replacement work begins.

**Proposed lead/review.** Luke leads; Alan reviews. Ready for Alan review and joint acceptance; no new implementation is authorized by this review package.

**Key boundaries.**

- Treat every existing branch and worktree as read-only evidence until its valuable files, tests, and reviewer findings have a named destination.
- Use Drive as the canonical review surface; the locally validated Project catalogue remains benched until separately reactivated and synced.
- Do not infer live health from GitHub build success; Gate A0 requires a known revision and live evidence.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P00-01 | NatalyxPlatform/.github | Approve programme baseline and extraction ledger | None | Pre-A0 |

**Acceptance focus.**

- SHA and timestamp reproducibility
- Drive package/document identifier parity
- No dirty-worktree mutation
- HTTP and workflow evidence captured separately

**Primary risks.**

- Review findings arrive after decomposition
- A protected worktree contains the only copy of useful code
- A green PR is mistaken for live readiness

Full implementation contract: `WP00 - Preservation, cloud diagnosis, and PR reconciliation.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP01: CI and PostgreSQL evidence gate

**Problem.** Main builds containers and runs a deploy-contract smoke, but does not run the Python suite or prove current schema behavior against PostgreSQL.

**Target outcome.** A first, deliberately CI-only PR that runs the current tests, exercises the existing schema on PostgreSQL, and publishes diagnosable evidence under stable required-check names without introducing the future migration framework.

**Proposed lead/review.** Alan leads; Luke reviews. Technical evidence foundation.

**Key boundaries.**

- PostgreSQL is production authority; SQLite remains a local compatibility target, not production evidence.
- Separate current-schema evidence from tests that require the future migration mechanism.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P01-01 | NatalyxPlatform/natalyx-app | Establish current-test and PostgreSQL CI evidence | P00-01 | A0 |

**Acceptance focus.**

- Current unit suite
- Fresh PostgreSQL database
- Current init_db idempotency
- Failure artifact and log clarity

**Primary risks.**

- CI exposes existing backend drift
- Tests accidentally depend on protected branch code
- Secrets or DB credentials leak in logs

Full implementation contract: `WP01 - CI and PostgreSQL evidence gate.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP02: Versioned migrations and readiness

**Problem.** Startup calls a monolithic CREATE/ALTER routine without an ordered migration ledger, advisory lock, expand/contract contract, or reliable partial-failure recovery.

**Target outcome.** An approved migration ADR, versioned runner, production-safe locking/readiness behavior, baseline migration, and forward-repair procedure proven on PostgreSQL and compatible with supported SQLite development.

**Proposed lead/review.** Alan leads; Luke reviews. Alan chooses the migration framework/mechanism; Luke approves compatibility and risk.

**Key boundaries.**

- Alan evaluates Alembic versus a custom ordered runner; a custom runner is not the default without ADR evidence.
- Migrations are forward-only by default, transaction-scoped where PostgreSQL permits, advisory-locked, checksum-recorded, and expand/contract compatible with the previous app revision.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P02-01 | NatalyxPlatform/natalyx-app | Decide migration architecture and compatibility contract | P01-01 | A0 |
| P02-02 | NatalyxPlatform/natalyx-app | Introduce versioned migration runner and readiness checks | P02-01 | A0 |
| P02-03 | NatalyxPlatform/natalyx-app | Baseline canonical schema and prove expand-contract repair | P02-02 | A1 |
| P02-04 | NatalyxPlatform/natalyx-intelligence | Move intelligence persistence to a revisioned migration namespace | P02-01, P02-02 | A1 |

**Acceptance focus.**

- Fresh and upgraded PostgreSQL
- Concurrent migrators
- Old/new app compatibility
- Interrupted migration and forward repair
- SQLite support decision

**Primary risks.**

- Irreversible DDL
- Concurrent deploy race
- Long backfill lock
- SQLite semantics hide PostgreSQL failure

Full implementation contract: `WP02 - Versioned migrations and readiness.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP03: Authentication, invitations, and resume

**Problem.** Current invitation code mixes low-risk onboarding links with case membership, and existing flows need explicit recipient binding, return-to safety, consent, expiry, revocation, duplicate-claim, and mismatch semantics.

**Target outcome.** Separate workspace-claim and paid-case invitation lifecycles with safe authentication/resume behavior and no link-possession path to sensitive case access.

**Proposed lead/review.** Alan leads; Luke reviews. Alan implements identity/admission controls; Luke reviews founder access constraints.

**Key boundaries.**

- An email-less link may create a pending low-risk workspace claim only.
- Identity binds an authenticated principal to a person; participation records the person's domain relationship; access grants carry resource-scoped capabilities; authorization consumes all three plus ownership and purpose.
- Paid-case membership requires authenticated identity binding, recipient or issuer confirmation as appropriate, explicit consent, and auditable redemption.
- Return targets are internal allowlisted paths and survive login/signup/confirmation without becoming redirect authority.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P03-01 | NatalyxPlatform/natalyx-app | Harden auth return-to and participant resume | P01-01 | A1 |
| P03-02 | NatalyxPlatform/natalyx-app | Add low-risk workspace claim lifecycle | P03-01, P03-05, P04-01 | A1 |
| P03-03 | NatalyxPlatform/natalyx-app | Bind paid-case invitations to identity and consent | P03-01, P03-05 | A2 |
| P03-04 | NatalyxPlatform/natalyx-infra | Replace shared signup admission with claim-aware Cognito admission | P03-02, P03-03 | A1 |
| P03-05 | NatalyxPlatform/natalyx-app | Implement canonical identity, participation, access, and authorization contracts | P02-03, P03-01 | A1 |

**Acceptance focus.**

- Logged-out resume
- Token replay/expiry/revocation
- Duplicate and concurrent claims
- Identity mismatch
- Workspace-to-case access escalation

**Primary risks.**

- Shared links forwarded
- Account mismatch
- Confused-deputy redirects
- Workspace data exposed during upgrade

Full implementation contract: `WP03 - Authentication, invitations, and resume.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP04: Node 0 workspace and paid-case separation

**Problem.** PR #124 creates a synthetic canonical case as soon as Node 0 is opened, collapsing free exploration, workspace membership, commercial commitment, and paid-case truth.

**Target outcome.** A distinct Node 0 workspace aggregate with attributable revisions and an idempotent, purpose-limited projection into one paid case only after the authorized commercial event.

**Proposed lead/review.** Alan leads; Luke reviews. Alan implements the domain/provenance contracts; Luke reviews product/privacy boundaries.

**Key boundaries.**

- Workspace, entitlement, commercial, payment, and case lifecycles are separate entities and state machines.
- Promotion copies only allowlisted projections with provenance, visibility, and verification intact.
- Compatibility adapters read old case-shaped Node 0 records while new writes target the workspace model.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P04-01 | NatalyxPlatform/natalyx-app | Separate Node 0 workspace storage from paid cases | P02-03, P03-05 | A1 |
| P04-02 | NatalyxPlatform/natalyx-app | Add attributable workspace revision and projection contracts | P04-01, P03-05 | A1 |
| P04-03 | NatalyxPlatform/natalyx-app | Adapt legacy Node 0 case-shaped data without semantic promotion | P04-02 | A1 |

**Acceptance focus.**

- One workspace/one promotion
- Retry/concurrency
- No implicit fact upgrade
- Private candidate isolation
- Old/new revision coexistence

**Primary risks.**

- Semantic data corruption during backfill
- Duplicate cases
- Private candidate leakage
- Older app revision writes legacy shape

Full implementation contract: `WP04 - Node 0 workspace and paid-case separation.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP05: Node 0 Free, Pathfinder, and resume

**Problem.** Pathfinder contains service/LLM-era routing complexity and Node 0 Free must satisfy the complete-the-match boundary without payment while preserving explicit IP authorship.

**Target outcome.** A deterministic entry router and resumable Node 0 Free flow for education, candidate tracking, preliminary safety checks, outreach guidance, and a willing candidate without a paid case.

**Proposed lead/review.** Luke leads; Alan reviews. Luke owns Free implementation; Alan reviews technical architecture, security and failure behavior.

**Key boundaries.**

- Routing is deterministic policy, not LLM authority.
- Candidate responses are provisional IP assertions, never GC-authored or medically verified facts.
- Safety-critical information and complete-the-match capability remain free.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P05-01 | NatalyxPlatform/natalyx-app | Replace Pathfinder routing with deterministic entry decisions | P03-01, P04-01 | A1 |
| P05-02 | NatalyxPlatform/natalyx-app | Rebuild Node 0 Free candidate and outreach domain | P04-02, P05-01 | A1 |
| P05-03 | NatalyxPlatform/natalyx-app | Ship resumable Node 0 Free participant surface | P03-01, P05-02, P11-03 | A1 |

**Acceptance focus.**

- All deterministic route outcomes
- Free candidate/outreach boundary
- Resume across sessions
- Critical-flag fail-safe
- Mobile interaction

**Primary risks.**

- Paid features leak into Free
- Provisional score is overclaimed
- Route drift
- LLM dependency reintroduced

Full implementation contract: `WP05 - Node 0 Free, Pathfinder, and resume.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP06: Node 0 Complete and GC soft onboarding

**Problem.** Optional paid depth, GC soft onboarding, and readiness reporting need clear entitlement gates without creating a managed case or treating IP assertions as GC answers.

**Target outcome.** Versioned Node 0 Complete entitlement, authenticated low-risk GC onboarding, attributable GC confirmation/replacement, and a readiness report that remains preliminary.

**Proposed lead/review.** Alan leads; Luke reviews. Alan implements Complete/GC onboarding; Luke reviews cross-role projection and product boundaries.

**Key boundaries.**

- Node 0 Complete is a flat configurable entitlement fully creditable against the JMF.
- GC confirmation appends an attributable revision; it never silently overwrites the IP source.
- GC-private answers stay private; only explicit purpose-limited projections reach the IP.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P06-01 | NatalyxPlatform/natalyx-app | Add Node 0 Complete entitlement and versioned feature gates | P04-01, P07-01, P08-01 | A2 |
| P06-02 | NatalyxPlatform/natalyx-app | Add GC soft onboarding and attributable confirmation | P03-02, P04-02, P06-01 | A2 |
| P06-03 | NatalyxPlatform/natalyx-app | Add readiness report and role-scoped progress surfaces | P06-02, P10-02, P11-04 | A2 |

**Acceptance focus.**

- Entitlement versioning
- GC-authored revisions
- IP/GC visibility pairs
- Revoked/expired claims
- No paid-case creation

**Primary risks.**

- Entitlement mistaken for case access
- GC answers exposed to IP
- IP assertions silently converted
- Price hard-coded

Full implementation contract: `WP06 - Node 0 Complete and GC soft onboarding.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP07: Commercial configuration, enrollment, and promotion

**Problem.** The business model requires versioned price/terms, explicit commitment, and one precise processor-neutral event before workspace-to-case promotion; none is currently authoritative.

**Target outcome.** Versioned commercial configuration and acceptances, a separate commitment/enrollment lifecycle, one processor-neutral byos.workspace_promotion_authorized.v1 event, and exactly-once paid-case creation by its consumer.

**Proposed lead/review.** Luke leads; Alan reviews. Luke implements settled commercial semantics; Alan reviews technical mechanisms and idempotency.

**Key boundaries.**

- Every commitment, invoice, payment, credit, refund, and promotion records the activated commercial-configuration version.
- Only the app-owned commitment/commercial domain emits byos.workspace_promotion_authorized.v1 after durable funding/terms/credit validation; a processor callback or redirect never emits it.
- The consumer creates/fetches one enrollment_pending case and restricted IP membership; GC case access follows the paid-case invitation contract.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P07-01 | NatalyxPlatform/natalyx-app | Add versioned commercial configuration and terms acceptance | P02-03 | A2 |
| P07-02 | NatalyxPlatform/natalyx-app | Implement commitment and enrollment-pending lifecycle | P07-01, P08-01 | A2 |
| P07-03 | NatalyxPlatform/natalyx-app | Emit processor-neutral workspace promotion authorization | P04-02, P07-02, P08-02 | A2 |
| P07-04 | NatalyxPlatform/natalyx-app | Promote workspace exactly once from authorization event | P03-03, P04-02, P07-03 | A2 |

**Acceptance focus.**

- Terms/config version pinning
- Commitment retries
- Exact-once promotion
- Funding reversal handling
- No GC access escalation

**Primary risks.**

- Configuration drift
- Duplicate promotion
- Redirect spoofing
- Unresolved policy encoded as default

Full implementation contract: `WP07 - Commercial configuration, enrollment, and promotion.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP08: Payments, invoices, credits, and refunds

**Problem.** No append-only commercial ledger or processor-neutral payment boundary currently supports the $8,900 JMF, $750 enrollment, Node 0 credit, milestones, deterministic refunds, or failure recovery.

**Target outcome.** Immutable commercial ledgers, idempotent provider inbox, milestone engine, reproducible credits/refunds, reconciliation, and safe non-critical pause behavior.

**Proposed lead/review.** Luke leads; Alan reviews. Luke implements payment-domain contracts after D-PAY-01; external review remains mandatory before real money.

**Key boundaries.**

- Payments, credits, refunds, adjustments, invoices, and commercial events are append-only; mutable balances are derived projections.
- Processor events enter an idempotent inbox and become internal commands/events only after signature and amount/currency checks.
- Billing follows durable case evidence and never acts as first notification of clinical events.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P08-01 | NatalyxPlatform/natalyx-app | Add append-only commercial and money ledgers | P02-03, P07-01 | A2 |
| P08-02 | NatalyxPlatform/natalyx-app | Add processor-neutral payment command and webhook inbox | P08-01, P07-02 | A2 |
| P08-03 | NatalyxPlatform/natalyx-app | Implement milestone invoicing, credits, and deterministic refunds | P08-02, P07-04, P09-04 | A2 |
| P08-04 | NatalyxPlatform/natalyx-app | Add payment reconciliation and safe service-pause operations | P08-03 | A2 |

**Acceptance focus.**

- Webhook replay/order
- Ledger invariants
- Milestone idempotency
- Refund table
- Node 0 credit floor
- Reconciliation mismatch

**Primary risks.**

- Double charge/refund
- Processor lock-in
- Clinical timing harm
- Pass-through commingling
- Policy gaps

Full implementation contract: `WP08 - Payments, invoices, credits, and refunds.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP09: Documents, active case, and provider handoffs

**Problem.** Current documents are metadata-only; the dirty provider branch is unreviewed and can over-project facts. There is no durable private S3/KMS/quarantine/recovery pipeline.

**Target outcome.** A metadata-only requirement/work-item lifecycle distinct from the secure document-content lifecycle, resilient storage/scan/download, usable active-case surfaces, and consent-scoped immutable provider snapshots with operational review.

**Proposed lead/review.** Alan leads; Luke reviews. Alan implements document/provider controls; Luke reviews retention, purpose and PHI boundaries.

**Key boundaries.**

- A requirement, readiness marker or review work item is not a document and cannot be approved as if content exists.
- Private bucket, block-public-access, KMS, opaque keys, application authorization, size/type/checksum gates, quarantine/scan, audit, retention, and orphan cleanup are mandatory for content.
- Provider handoffs are purpose-bound snapshots with checksum/revision/expiry and consent; provider-visible items are allowlisted, not inferred from broad visibility.
- ECS replacement must not lose upload/task state; recovery resumes from durable metadata and object state.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P09-01 | NatalyxPlatform/natalyx-app | Define document lifecycle, authorization, and retention contract | P00-01, P02-01 | A2 |
| P09-02 | NatalyxPlatform/natalyx-infra | Provision private encrypted document and quarantine storage | P09-01, P13-02 | A2 |
| P09-03 | NatalyxPlatform/natalyx-app | Implement resilient document upload, scan, and download | P09-02, P02-03 | A2 |
| P09-04 | NatalyxPlatform/natalyx-app | Ship phase-1 case progress and metadata-only request/review | P03-03, P03-05, P07-04, P09-01, P11-03 | A2 |
| P09-05 | NatalyxPlatform/natalyx-app | Implement consent-scoped provider handoff snapshots and operations | P04-02, P09-06, P10-02 | A2 |
| P09-06 | NatalyxPlatform/natalyx-app | Integrate content-bearing document versions into participant surfaces | P09-03, P09-04 | A2 |

**Acceptance focus.**

- Unauthorized object access
- Oversize/type/spoof
- Scan failure/quarantine
- Partial upload/task loss
- Snapshot immutability/revocation
- Mobile documents

**Primary risks.**

- PHI exposure
- Malware
- Orphaned objects
- Stale provider packet
- Dirty branch leakage

Full implementation contract: `WP09 - Documents, active case, and provider handoffs.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP10: Intelligence, memory, proposals, and Ask safety

**Problem.** Private memory, shared case truth, Learn context, and AI proposals have partial contracts but current app code can place IP guide notes into shared memory and provider projections lack provenance enforcement.

**Target outcome.** Versioned scoped context envelopes, separate private/shared memory revisions, evidence-bound proposal approval, grounded Ask behavior, and cross-service safety evaluation/observability.

**Proposed lead/review.** Alan leads; Luke reviews. Alan implements intelligence contracts after D-AI-01; Luke reviews truth and privacy policy.

**Key boundaries.**

- The app owns case truth, authorization, PHI policy, and durable approval; intelligence returns advisory proposals only.
- Every request declares general Learn, private-user, approved-shared-case, or provider-purpose scope; contexts are not merged.
- Failures degrade explicitly with source/boundary notices and no fabricated case answer.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P10-01 | NatalyxPlatform/natalyx-intelligence | Version the scoped intelligence context envelope | P01-01, P04-02 | A2 |
| P10-02 | NatalyxPlatform/natalyx-app | Enforce private/shared memory and evidence-bound proposal approval | P04-02, P10-01 | A2 |
| P10-03 | NatalyxPlatform/natalyx-intelligence | Harden Ask and Learn grounding and degraded-mode behavior | P10-01, P11-02 | A2 |
| P10-04 | NatalyxPlatform/natalyx-intelligence | Add intelligence safety evaluations and cross-service observability | P10-02, P10-03 | A2 |

**Acceptance focus.**

- Scope isolation
- Proposal approval/rejection
- Citation/source validity
- Unavailable service
- Prompt/context leakage
- Trace redaction

**Primary risks.**

- Private-to-shared leakage
- Hallucinated truth
- Sensitive logs
- Contract version drift

Full implementation contract: `WP10 - Intelligence, memory, proposals, and Ask safety.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP11: Learn release and design-system contract

**Problem.** Learn artifact generation and catalog work is dirty/unreleased, while participant surfaces need governed recipes without making aesthetic purity a universal release gate.

**Target outcome.** Validated provenance-bearing Learn artifacts, approved-only serving, release-blocking DS accessibility/security/interaction contract, and app adoption of stable recipes/source cards.

**Proposed lead/review.** Luke leads; Alan reviews. Luke implements the separate Learn, intelligence-catalog, participant-DS and app-adoption PRs; Alan reviews technical contracts.

**Key boundaries.**

- Learn resources own authored artifacts/provenance; intelligence owns approved catalog delivery; app owns authorized presentation and context.
- Security, accessibility, responsive layout, and interaction defects can block release; token/style purity alone is backlog unless tied to concrete risk.
- Participant and internal/operator design systems remain separate.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P11-01 | NatalyxPlatform/natalyx-learn-resources | Publish validated Learn artifact and provenance contract | P00-01 | A2 |
| P11-02 | NatalyxPlatform/natalyx-intelligence | Serve approved Learn catalog versions from intelligence | P11-01 | A2 |
| P11-03 | NatalyxPlatform/natalyx-design-system | Release participant design-system accessibility and interaction contract | P00-01 | A1 |
| P11-04 | NatalyxPlatform/natalyx-app | Adopt approved Learn and source-card recipes in app | P11-02, P11-03 | A2 |

**Acceptance focus.**

- Artifact schema/provenance
- Approved-only catalog
- Missing-resource empty state
- Recipe escaping
- Keyboard/reduced-motion/mobile

**Primary risks.**

- Fake/unapproved content
- Cross-repo version drift
- Aesthetic review blocks recovery
- Internal DS leakage

Full implementation contract: `WP11 - Learn release and design-system contract.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP12: Ask/Learn shell and mobile cutover

**Problem.** Participant Ask/Learn entry points, case shell, legacy routes, and mobile interactions are not yet one coherent clickable journey with explicit context boundaries.

**Target outcome.** A unified scope-labelled Ask/Learn shell, accessible mobile participant journey, and verified redirect-based legacy cutover with no broken or misleading controls.

**Proposed lead/review.** Luke leads; Alan reviews. Luke implements participant shell/cutover; Alan reviews integration, authorization and failure behavior.

**Key boundaries.**

- The shell labels general, private, and shared-case context and never implies a source exists when it does not.
- Server owns state and permissions; client code enhances interaction only.
- Legacy routes redirect through allowlisted, telemetry-observed compatibility paths before deletion.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P12-01 | NatalyxPlatform/natalyx-app | Unify Ask and Learn shell with explicit context scopes | P10-03, P11-04, P09-04 | A2 |
| P12-02 | NatalyxPlatform/natalyx-app | Complete mobile participant interaction and accessibility cutover | P05-03, P06-03, P09-04, P09-06, P12-01 | A2 |
| P12-03 | NatalyxPlatform/natalyx-app | Retire legacy participant routes behind verified redirects | P12-02, P13-04 | B1 |

**Acceptance focus.**

- Clickable IP/GC flows
- Context labels
- No-JS/reduced-motion/keyboard
- Mobile widths
- Redirect and stale bookmark
- Logout/login/resume

**Primary risks.**

- Context ambiguity
- Mobile-only dead ends
- Premature legacy removal
- Design drift

Full implementation contract: `WP12 - Ask and Learn shell and mobile cutover.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

## WP13: Deployment, cloud gates, and PHI readiness

**Problem.** The dev endpoint is presently 503, deployments do not prove application readiness, and test/deploy success cannot establish real-user or PHI readiness.

**Target outcome.** Known-revision diagnostics, guarded rollback/evidence capture, automated synthetic A1/A2 journeys, and explicit B1/B2 operational/privacy/PHI go/no-go packets.

**Proposed lead/review.** Alan leads; Luke reviews. Alan owns technical gate evidence; Luke accepts gates and external reviewers retain their required attestations.

**Key boundaries.**

- Health, readiness, revision, dependency, migration, and safe configuration signals are distinct.
- Every cloud gate has prerequisites, evidence, owner, verifier, and failure/rollback response.
- B2 requires formal security/privacy/compliance evidence and human go/no-go; it is not a software test result.

| PR | Repository | Suggested change | Depends on | Gate |
| --- | --- | --- | --- | --- |
| P13-01 | NatalyxPlatform/natalyx-app | Expose known-revision health, readiness, and dependency diagnostics | P01-01 | A0 |
| P13-02 | NatalyxPlatform/natalyx-infra | Harden guarded deployment, rollback, and evidence capture | P01-01, P13-01 | A0 |
| P13-03 | NatalyxPlatform/natalyx-app | Automate synthetic A1 core participant journey verification | P03-02, P04-03, P05-03, P11-03, P13-02 | A1 |
| P13-04 | NatalyxPlatform/natalyx-app | Automate synthetic A2 commercial and document journey verification | P06-03, P07-04, P08-04, P09-05, P10-04, P12-02, P13-03 | A2 |
| P13-05 | NatalyxPlatform/natalyx-app | Enforce case RLS and a non-owner PostgreSQL runtime | P02-03, P03-05, P04-03, P08-04, P09-05, P10-02 | B1 |
| P13-06 | NatalyxPlatform/natalyx-infra | Harden B1/B2 backups, audit, alarms, and cohort controls | P09-02, P13-02, P13-05 | B1 |
| P13-07 | NatalyxPlatform/.github | Publish B1 and B2 privacy, PHI, and operational go-no-go runbooks | P13-04, P13-05, P13-06 | B1 |

**Acceptance focus.**

- Known revision
- ALB/ECS/dependency health
- Rollback
- Synthetic A1/A2
- PII controls
- PHI go/no-go evidence

**Primary risks.**

- Unknown running revision
- Rollback incompatible with schema
- Synthetic success overclaimed
- PHI enabled without organizational controls

Full implementation contract: `WP13 - Deployment, cloud gates, and PHI readiness.md` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.

# Founder decision resolution and remaining controls

Founder-final policy is not the same as an active technical control. The status, remaining owner and programme effect below preserve that distinction.

| Decision | Status | Founder outcome | Remaining owner | Resolve by | Programme effect |
| --- | --- | --- | --- | --- | --- |
| D-MIG-01 | Founder constraints final; Alan immediate; operationally pending | Reliability-first migrations with zero intended data loss; PostgreSQL is authoritative for production and SQLite may remain a convenient synthetic local-development projection without full production parity. | Alan - immediate | Before P02-02 | P02-01 decision work may proceed; P02-02, P02-03 and Gate A0 remain blocked until Alan's mechanism and evidence are accepted. |
| D-AUTH-01 | Resolved by reconciliation | A bearer link creates only a pending low-risk workspace claim; paid-case access requires authenticated binding, explicit consent and recipient/issuer confirmation. | Alan - implementation | Resolved 2026-07-12 | No longer blocks P03-02 or P03-03. |
| D-AUTH-02 | Founder constraints final; Alan later | Participant admission uses short-lived signed or server-verified proof bound to email, purpose, claim and expiry; it admits account creation only and never grants workspace or case membership. Internal admission remains a separate allowlist path. | Alan - later at P03-04 | Before P03-04 | P03-04 and Gate A1 remain blocked until the technical mechanism and evidence exist. |
| D-AUTH-03 | Resolved by reconciliation | Identity, participation, access grants, ownership and operation authorization remain separate; participation or lens alone never authorizes. | Alan - implementation | Resolved 2026-07-12 | No longer blocks the reconciled access/workspace PR sequence. |
| D-CI-01 | Founder final; operationally pending | Option A - GitHub Team approved as the private-repository enforcement control. | Alan - immediate | Founder decision resolved 2026-07-13; control required before P01-01 merge or any later app implementation PR | P01-01 merge, Gate A0 and dependent implementation PRs remain blocked until the live control is active and verified. |
| D-DATA-01 | Founder decision final; implementation evidence pending | Use need-to-know sharing. Shared journey status and agreed relationship/outreach/logistics may cross roles; private IP notes, unconfirmed assertions and GC medical, reproductive, insurance, identity or wellbeing answers do not cross automatically. Provider packets require preview, consent and appropriate verification. | Alan - implementation | Before P04-02 | Founder ambiguity is removed across WP04, WP06, WP07, WP09 and WP10; A1 still requires the technical denial evidence. |
| D-DATA-02 | Founder default final; external validation before B1 | Retain candidate/workspace material for a 90-day minimum after explicit rejection, withdrawal or last legitimate outreach, honor earlier valid deletion, retain only non-identifying funnel metrics and a minimal audit tombstone, and preserve legal holds. Corrections append source-labelled revisions and private IP notes remain author-only. | Alan - implementation; privacy/legal - validation | Before P04-02 | Synthetic implementation may proceed; real-user B1 activation remains externally dependent. |
| D-DATA-03 | Resolved by reconciliation | No candidate ranking, viability/eligibility flag or race preference survives; provisional pre-join input can generate neutral source-labelled questions only. | Alan - implementation | Resolved 2026-07-12 | No longer blocks Node 0 implementation planning. |
| D-COM-01 | Founder decision final for beta; tax externally dependent | Node 0 Complete is a voluntary $495 USD one-time upgrade paid by the IP or authorized IP account holder, never the GC, collected before Complete features and fully credited against the later Phase 1/JMF without gating matching or safety support. | Alan - implementation | Before activation of a Complete configuration | P06-01, P07-01 and P08-01 may proceed synthetically; live activation remains gated. |
| D-COM-02 | Founder decision final for v1; live activation gated | Configuration v1 is $8,900 USD: a $750 deposit followed by $1,630, $2,445, $1,630, $1,630 and $815 milestones. Pay-in-full is $7,830 total, leaving $7,080 after the deposit; the separate $495 Complete credit must not be double-counted. | Alan - implementation | Before P07-01 activation data | Synthetic commercial configuration and ledgers may proceed; real charging remains gated. |
| D-COM-03 | Externally dependent; founder policy inputs settled | No live acceptance or charge may rely on the contradictory current terms draft. D-COM-06 and D-COM-07 supply the approved business policy for a new versioned terms package. | External legal/privacy/finance; Luke final business approval | Before P07-02 user acceptance | Synthetic A2 preparation may proceed; live P07-02/P08 charging and B1 customer acceptance remain blocked. |
| D-COM-04 | Founder decision final; implementation evidence pending | Use two-step commitment: settled $750 plus current accepted terms proves commercial enrollment, but payment alone never promotes. Exactly one enrollment-pending case follows explicit IP promotion and authenticated GC consent. The $1,630 activation tranche is earned only after defined IP/GC onboarding and screening coordination has begun; it never implies medical clearance. | Alan - implementation | Before P07-02 | P07-02 through P09-04 may proceed under the settled semantics. |
| D-PAY-01 | Founder constraints final; Alan later | Offer card and US ACH, encourage but do not require ACH above $1,000, absorb ordinary beta fees without surcharging, and keep processor metadata free of GC, journey, clinical or document detail. | Alan - later before P08-02 | Before P08-02 adapter | P08-01 ledger work may proceed; P08-02 and A2 payment completion wait for Alan's processor decision and evidence. |
| D-COM-05 | Founder decision final for beta | Financing is excluded and hidden from beta; Natalyx does not advertise, recommend or integrate a lender or treat lender status as funding evidence. | None during beta | Before financed option is exposed | Financing no longer blocks P08-02; the feature is deliberately out of scope. |
| D-COM-06 | Founder policy final; legal/accounting externally dependent | After post-heartbeat loss, never charge the $815 birth tranche; retain the delivered $1,630 pregnancy-support tranche and grant an equal $1,630 future credit to the same IP household for 36 months, with compassionate manual extension and defined offboarding support. | Alan - implementation; legal/accounting - wording | Before automated pregnancy-stage refund logic | Synthetic P08-03 implementation may proceed; live policy activation remains gated. |
| D-COM-07 | Founder policy final; legal/accounting externally dependent | Protect delivered work: the $750 is refundable until onboarding is delivered and then earned; activation follows D-COM-04. Non-clearance or pre-clearance GC withdrawal stops later charges. Unearned prepayment is refunded within ten business days, with refund or rollover choice and one replacement within 12 months without a second $750 deposit. | Alan - implementation; legal/accounting - wording | Before real billing | Synthetic P08-03 implementation may proceed; live refund/cancellation terms remain gated. |
| D-COM-08 | Founder decision final; implementation evidence pending | Use a humane 30-day grace period with reminders seven days before due, on the due date, and at 7, 14 and 30 days overdue; no beta late fee and human outreach before pause. Only future non-critical paid work may pause after 30 days. | Alan - implementation | Before P08-04 | P08-04 may proceed under the settled policy. |
| D-DOC-01 | Founder default final; Alan later; external validation before B1/B2 | Retain clean active-case documents while active plus two years after close; signed consents, payment/access audits and deletion tombstones for seven years; failed/quarantine orphans seven days; superseded content 90 days unless required; honor valid deletion within 30 days subject to legal hold. Downloads require fresh authorization and links expire within five minutes. | Alan - later before P09-03; privacy/legal - validation | Before P09-03 | P09-01 ADR work may proceed; P09-03/P09-06 and real-content activation wait for Alan's delivery choice and evidence. |
| D-DOC-02 | Founder constraints final; Alan later | Allow PDF, JPEG, PNG and non-macro DOCX up to 50 MiB. Reject spoofed, macro-enabled and archive-like input; quarantine until clean; treat password-protected, skipped, error and timeout results as unavailable. | Alan - later before P09-02 | Before P09-02 | P09-01 contract work may proceed; P09-02/P09-03/P09-06 wait for Alan's technical selection and evidence. |
| D-PROV-01 | Founder decision final; Alan later | Provider handoff is a purpose-bound immutable snapshot for one verified recipient and named purpose, with participant preview/consent, clean documents and appropriately verified source-labelled facts. Unopened access expires after 14 days and can be revoked before access; downloaded copies cannot be recalled. | Alan - later before P09-05 | Before P09-05 | Synthetic provider-snapshot design may proceed; P09-05 completion and real handoff require Alan's evidence and later external review. |
| D-AI-01 | Founder scope/cost final; Alan later; PHI externally gated | AI is bounded and advisory: role-scoped education, retrieval, summaries, question drafts, next steps and provider preparation using approved Learn and authorized source-labelled context. It never diagnoses, ranks, approves, clears or writes durable truth; authorized human approval precedes memory, case or provider material. | Alan - later before P10-01 | Before P10-01 | P10/P12 synthetic planning may proceed; implementation completion waits for Alan's technical decision and PHI remains blocked through B2. |
| D-OPS-01 | Founder constraints final; Alan immediate; operationally pending | Use fail-closed recovery: protect data integrity over uptime, restore only a reviewed proven-compatible application-image/schema pair, use safe read-only or unavailability when uncertain, and forward-repair when rollback is unsafe. Target 30-minute beta recovery; allow up to two hours emergency downtime and notify Luke when more than one hour is expected. | Alan - immediate | Before Gate A0 recovery action | P13-02 and Gate A0 remain blocked until the runbook and synthetic exercise pass; A1 must exercise the control. |
| D-PHI-01 | Founder beta scope final; externally gated | B1 is an invitation-only US beta of at most five IP/GC pairs using names, verified account/contact data, relationship/outreach/logistics, consent versions, nonclinical progress, feedback and processor references only. Medical, reproductive-health, psychological, insurance-health and clinical-clearance data are prohibited; no real document bytes or provider packets; AI receives de-identified nonclinical context only. | Alan - B1/B2 evidence; external reviewers - approval | Before B1 for PII scope; before B2 for PHI | B1 remains blocked until the limited PII control bundle is accepted; real documents/provider packets and all PHI remain blocked until B2. |
| D-PHI-02 | Founder governance final; external reviewers pending | Luke accepts B1 from Alan's technical evidence plus external privacy/legal advice, without separate independent technical sign-off. B1 evidence is at most 60 days old and reruns after material change or 180 days. B2 requires qualified external security, privacy/compliance and legal/vendor review with release evidence at most 30 days old and assessments at most 12 months old. | Alan - evidence; external reviewers - attestations; Luke - go/no-go | Before B1 | B1 and B2 remain blocked until the corresponding evidence is current and the required humans sign off. |

## Immediate Alan decisions

| Decision | Alan owns | Evidence | Latest safe point |
| --- | --- | --- | --- |
| D-CI-01 | Activate GitHub Team when enforcement is required; Configure required unittest and PostgreSQL checks; Restrict routine bypass; Supply ruleset readback and negative-bypass evidence | GitHub Team activation/readback; Mandatory unittest and PostgreSQL checks; Restricted routine bypass; Negative-bypass evidence | Founder decision resolved 2026-07-13; control required before P01-01 merge or any later app implementation PR |
| D-MIG-01 | Choose the migration framework; Choose sequencing/locking and expand-contract mechanics; Choose the detailed rollback, restore or forward-repair mechanism | Migration ADR; Fresh/current/upgrade compatibility matrix; Tested recovery or rollback evidence; Destructive-change approval path | Before P02-02 |
| D-OPS-01 | Choose exact compatibility, rollback/forward-repair and automation mechanisms; Name the evidence owner and write the runbook | Documented recovery procedure; Successful synthetic recovery exercise; Known-compatible image/schema evidence | Before Gate A0 recovery action |

## Later Alan decisions

| Decision | Alan owns | Evidence | Checkpoint |
| --- | --- | --- | --- |
| D-AUTH-02 | Choose the proof format, signer/verifier, key lifecycle and claim lifecycle | Expiry, replay, wrong-email, wrong-purpose, mismatch and revocation tests; Separate internal allowlist evidence | Before P03-04 |
| D-PAY-01 | Choose the processor/vendor, tokenization, webhook, settlement, return/refund and reconciliation mechanisms | Provider security and cost comparison; Synthetic settlement, return, refund, duplicate and reconciliation tests | Before P08-02 adapter |
| D-DOC-01 | Choose proxy versus presigned delivery by class; Implement hold, deletion, tombstone, retry and authorization behavior | Fresh-authorization and five-minute-link tests; Retention/hold/deletion exercise; Privacy/legal approval before real content | Before P09-03 |
| D-DOC-02 | Choose the AWS-native scanner, queue, retry, timeout, recovery and cost-control mechanisms | Type/sniffing/spoof tests; Quarantine, error, timeout and retry tests; Cost estimate and alerts | Before P09-02 |
| D-PROV-01 | Choose recipient verification, snapshot checksum, expiry, revocation and audit mechanisms | Wrong-recipient, expiry, revoke-before-access, reissue and checksum tests | Before P09-05 |
| D-AI-01 | Choose Bedrock model, prompts, retrieval, schemas, fallback, human-review rails and cost controls | Scope/authority negative tests; Fallback and malformed-response tests; Safety and cost evidence | Before P10-01 |
| D-PHI-01 | Implement inventory, cohort controls, RLS, cross-tenant denials, de-identification and prohibited-data tests | Five-pair cohort configuration; RLS/cross-tenant/de-identification/prohibited-data tests; External privacy/legal approval | Before B1 for PII scope; before B2 for PHI |
| D-PHI-02 | Maintain evidence recency, change-triggered reruns and exception records | B1/B2 evidence index with dates; Named reviewers; Exception register; Signed go/no-go | Before B1 |

## External dependencies

| Decision | External dependency | Activation boundary |
| --- | --- | --- |
| D-DATA-02 | Privacy/legal validation before B1 | Synthetic implementation may proceed; real-user B1 activation remains externally dependent. |
| D-COM-01 | Tax treatment and customer-facing wording before live activation | P06-01, P07-01 and P08-01 may proceed synthetically; live activation remains gated. |
| D-COM-02 | Approved terms and tax treatment before live activation | Synthetic commercial configuration and ledgers may proceed; real charging remains gated. |
| D-COM-03 | Legal, privacy, tax and finance review before real-user acceptance or charging | Synthetic A2 preparation may proceed; live P07-02/P08 charging and B1 customer acceptance remain blocked. |
| D-PAY-01 | Payment/security/finance review before real money | P08-01 ledger work may proceed; P08-02 and A2 payment completion wait for Alan's processor decision and evidence. |
| D-COM-06 | Legal and accounting review before live use | Synthetic P08-03 implementation may proceed; live policy activation remains gated. |
| D-COM-07 | Legal and accounting review before live use | Synthetic P08-03 implementation may proceed; live refund/cancellation terms remain gated. |
| D-DOC-01 | Privacy/legal validation before B1/B2 real-content use | P09-01 ADR work may proceed; P09-03/P09-06 and real-content activation wait for Alan's delivery choice and evidence. |
| D-PROV-01 | Privacy/provider review before real handoff | Synthetic provider-snapshot design may proceed; P09-05 completion and real handoff require Alan's evidence and later external review. |
| D-AI-01 | B2 external security/privacy/compliance approval before PHI | P10/P12 synthetic planning may proceed; implementation completion waits for Alan's technical decision and PHI remains blocked through B2. |
| D-PHI-01 | External privacy/legal approval before B1; Qualified external security/privacy/compliance/legal approval before B2 | B1 remains blocked until the limited PII control bundle is accepted; real documents/provider packets and all PHI remain blocked until B2. |
| D-PHI-02 | Named privacy/legal advisers for B1; Named qualified security/privacy/compliance/legal reviewers for B2 | B1 and B2 remain blocked until the corresponding evidence is current and the required humans sign off. |

# Handoff checklist

- All 24 decision IDs are present and uniquely classified.
- D-CI-01, D-MIG-01 and D-OPS-01 remain immediate Alan controls and keep Gate A0 blocked until evidence is accepted.
- Later Alan decisions are attached to their actual work-package checkpoints rather than forced prematurely.
- External terms, tax, privacy, security, compliance and PHI dependencies remain explicit activation gates.
- A0/A1/A2 remain synthetic; B1 is limited to at most five IP/GC pairs and approved nonclinical PII; real document bytes, provider packets and PHI remain prohibited until their later gates.
- The 52 suggested implementation PRs remain proposals; this planning update creates, merges or deploys none of them.
