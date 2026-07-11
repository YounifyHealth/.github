# Proposed PR manifest

> Planning-only. Every implementation PR remains a GitHub Project draft item until its plan, decisions and dependencies are ready and implementation actually begins.

Proposed PR count: **50**. Canonical inspection snapshot: **2026-07-10 20:12 America/New_York**.

## Global PR table

| ID | Title | Repository | Work package | DRI | Implementer | Reviewer | Final approver | Dependencies | Gate | Size | Readiness | Blocking decision | Replacement/source PR | Project item |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P00-01 | Approve programme baseline and extraction ledger | .github | WP00 / Preservation, cloud diagnosis, and PR reconciliation | Luke | Luke | Alan | Luke | P00-01 plan sign-off | Pre-A0 | Medium | Needs plan approval | None | All listed draft PRs and protected worktrees | [P00-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P00-01) |
| P01-01 | Establish current-test and PostgreSQL CI evidence | app | WP01 / CI and PostgreSQL evidence gate | Alan | Alan | Luke | Luke | P00-01 | A0 | Medium | Dependencies unmet | None | PR #122 unittest workflow and backend-neutral fixes after reconciliation | [P01-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P01-01) |
| P11-01 | Publish validated Learn artifact and provenance contract | learn | WP11 / Learn release and design-system contract | Alan | Alan | Luke | Luke | P00-01 | A2 | Large | Dependencies unmet | None | Protected feature/learn-resource-rendering-contract, feature/node0-beta-learn-resources | [P11-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-01) |
| P11-03 | Release participant design-system accessibility and interaction contract | design-system | WP11 / Learn release and design-system contract | Alan | Alan | Luke | Luke | P00-01 | A1 | Medium | Dependencies unmet | None | Design-system PRs #7 and #8, dirty local brand assets | [P11-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-03) |
| P02-01 | Decide migration architecture and compatibility contract | app | WP02 / Versioned migrations and readiness | Alan | Alan | Luke | Luke | P01-01 | A0 | Small | Blocked by decision | D-MIG-01 | app/storage/schema.py, app/storage/connection.py | [P02-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-01) |
| P03-01 | Harden auth return-to and participant resume | app | WP03 / Authentication, invitations, and resume | Alan | Alan | Luke | Luke | P01-01 | A1 | Medium | Dependencies unmet | None | PR #122 return_to fixes | [P03-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-01) |
| P13-01 | Expose known-revision health, readiness, and dependency diagnostics | app | WP13 / Deployment, cloud gates, and PHI readiness | Alan | Alan | Luke | Luke | P01-01 | A0 | Large | Dependencies unmet | None | Current /healthz, direct 503 evidence | [P13-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-01) |
| P11-02 | Serve approved Learn catalog versions from intelligence | intelligence | WP11 / Learn release and design-system contract | Alan | Alan | Luke | Luke | P11-01 | A2 | Large | Dependencies unmet | None | Intelligence issue #14, protected dirty learn_resources.py | [P11-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-02) |
| P02-02 | Introduce versioned migration runner and readiness checks | app | WP02 / Versioned migrations and readiness | Alan | Alan | Luke | Luke | P02-01 | A0 | Large | Dependencies unmet | D-MIG-01 | Current init_db startup path | [P02-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-02) |
| P09-01 | Define document lifecycle, authorization, and retention contract | app | WP09 / Documents, active case, and provider handoffs | Alan | Alan | Luke | Luke | P00-01, P02-01 | A2 | Medium | Blocked by decision | D-DOC-01, D-DOC-02, D-PHI-01 | Current metadata-only documents.py, provider branch | [P09-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-01) |
| P13-02 | Harden guarded deployment, rollback, and evidence capture | infra | WP13 / Deployment, cloud gates, and PHI readiness | Alan | Alan | Luke | Luke | P01-01, P13-01 | A0 | Large | Dependencies unmet | D-OPS-01 | Existing guarded app/infra workflows | [P13-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-02) |
| P11-04 | Adopt approved Learn and source-card recipes in app | app | WP11 / Learn release and design-system contract | Alan | Alan | Luke | Luke | P11-02, P11-03 | A2 | Large | Dependencies unmet | None | PR #122 Learn slot, PR #124 dependency note | [P11-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-04) |
| P02-03 | Baseline canonical schema and prove expand-contract repair | app | WP02 / Versioned migrations and readiness | Alan | Alan | Luke | Luke | P02-02 | A1 | Large | Dependencies unmet | None | app/storage/schema.py current definitions, PR #122 forward-migration tests after reconciliation | [P02-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-03) |
| P02-04 | Move intelligence persistence to a revisioned migration namespace | intelligence | WP02 / Versioned migrations and readiness | Alan | Alan | Luke | Luke | P02-01, P02-02 | A1 | Large | Dependencies unmet | D-MIG-01 | src/natalyx_intelligence/shared/persistence.py runtime _ensure_schema | [P02-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-04) |
| P09-02 | Provision private encrypted document and quarantine storage | infra | WP09 / Documents, active case, and provider handoffs | Alan | Alan | Luke | Luke | P09-01, P13-02 | A2 | Large | Dependencies unmet | D-DOC-02, D-PHI-01 | Existing infra platform stack patterns | [P09-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-02) |
| P04-01 | Separate Node 0 workspace storage from paid cases | app | WP04 / Node 0 workspace and paid-case separation | Alan | Alan | Luke | Luke | P02-03 | A1 | Exceptional | Dependencies unmet | CHECK-ALAN-122-124 | PR #124 _ensure_node0_case as behavior to replace, candidate worktrees | [P04-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P04-01) |
| P07-01 | Add versioned commercial configuration and terms acceptance | app | WP07 / Commercial configuration, enrollment, and promotion | Alan | Alan | Luke | Luke | P02-03 | A2 | Large | Dependencies unmet | D-COM-01, D-COM-02, D-COM-03 | Payment/business-model DOCX | [P07-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-01) |
| P09-03 | Implement resilient document upload, scan, and download | app | WP09 / Documents, active case, and provider handoffs | Alan | Alan | Luke | Luke | P09-02, P02-03 | A2 | Exceptional | Dependencies unmet | D-DOC-01, D-DOC-02 | Current metadata scaffold | [P09-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-03) |
| P03-02 | Add low-risk workspace claim lifecycle | app | WP03 / Authentication, invitations, and resume | Alan | Alan | Luke | Luke | P03-01, P04-01 | A1 | Large | Dependencies unmet | D-AUTH-01, CHECK-ALAN-122-124 | PRs #123/#124, dirty onboarding-link worktree | [P03-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-02) |
| P03-03 | Bind paid-case invitations to identity and consent | app | WP03 / Authentication, invitations, and resume | Alan | Alan | Luke | Luke | P03-01, P04-01 | A2 | Large | Dependencies unmet | D-AUTH-01, CHECK-ALAN-122-124 | PR #122 CAS/TTL/self-invite fixes, current invitations.py | [P03-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-03) |
| P04-02 | Add attributable workspace revision and projection contracts | app | WP04 / Node 0 workspace and paid-case separation | Alan | Alan | Luke | Luke | P04-01 | A1 | Large | Dependencies unmet | D-DATA-01, D-DATA-02, CHECK-ALAN-122-124 | Current facts/memory models, GC authorship audit | [P04-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P04-02) |
| P05-01 | Replace Pathfinder routing with deterministic entry decisions | app | WP05 / Node 0 Free, Pathfinder, and resume | Alan | Alan | Luke | Luke | P03-01, P04-01 | A1 | Medium | Dependencies unmet | None | Current pathfinder_destinations.py, PR #119 product-alignment doc | [P05-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-01) |
| P08-01 | Add append-only commercial and money ledgers | app | WP08 / Payments, invoices, credits, and refunds | Alan | Alan | Luke | Luke | P02-03, P07-01 | A2 | Exceptional | Dependencies unmet | D-COM-01, D-COM-02, D-COM-03 | Payment/business-model DOCX | [P08-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-01) |
| P03-04 | Replace shared signup admission with claim-aware Cognito admission | infra | WP03 / Authentication, invitations, and resume | Alan | Alan | Luke | Luke | P03-02, P03-03 | A1 | Large | Blocked by decision | D-AUTH-02 | infra platform-stack.ts current allowlist + shared invite code | [P03-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-04) |
| P04-03 | Adapt legacy Node 0 case-shaped data without semantic promotion | app | WP04 / Node 0 workspace and paid-case separation | Alan | Alan | Luke | Luke | P04-02 | A1 | Large | Dependencies unmet | None | PRs #117/#121/#123/#124 and dirty candidate worktrees | [P04-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P04-03) |
| P10-01 | Version the scoped intelligence context envelope | intelligence | WP10 / Intelligence, memory, proposals, and Ask safety | Alan | Alan | Luke | Luke | P01-01, P04-02 | A2 | Large | Dependencies unmet | D-DATA-01, D-AI-01 | Current case_context advisory stub | [P10-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-01) |
| P05-02 | Rebuild Node 0 Free candidate and outreach domain | app | WP05 / Node 0 Free, Pathfinder, and resume | Alan | Alan | Luke | Luke | P04-02, P05-01 | A1 | Exceptional | Dependencies unmet | CHECK-ALAN-122-124 | PR #117 direct algorithm/test salvage, PR #124, quiz rewrite worktree | [P05-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-02) |
| P06-01 | Add Node 0 Complete entitlement and versioned feature gates | app | WP06 / Node 0 Complete and GC soft onboarding | Alan | Alan | Luke | Luke | P04-01, P07-01, P08-01 | A2 | Large | Dependencies unmet | D-COM-01 | Business-model Node 0 feature table | [P06-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P06-01) |
| P07-02 | Implement commitment and enrollment-pending lifecycle | app | WP07 / Commercial configuration, enrollment, and promotion | Alan | Alan | Luke | Luke | P07-01, P08-01 | A2 | Large | Dependencies unmet | D-COM-04 | Business-model conversion trigger | [P07-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-02) |
| P10-02 | Enforce private/shared memory and evidence-bound proposal approval | app | WP10 / Intelligence, memory, proposals, and Ask safety | Alan | Alan | Luke | Luke | P04-02, P10-01 | A2 | Exceptional | Dependencies unmet | D-DATA-01, D-AI-01 | Current facts/memory/proposals scaffolds, GC authorship audit | [P10-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-02) |
| P10-03 | Harden Ask and Learn grounding and degraded-mode behavior | intelligence | WP10 / Intelligence, memory, proposals, and Ask safety | Alan | Alan | Luke | Luke | P10-01, P11-02 | A2 | Large | Dependencies unmet | D-AI-01 | Current ask_natalyx.py and PR #124 Ask integration | [P10-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-03) |
| P05-03 | Ship resumable Node 0 Free participant surface | app | WP05 / Node 0 Free, Pathfinder, and resume | Alan | Alan | Luke | Luke | P03-01, P05-02, P11-03 | A1 | Large | Dependencies unmet | CHECK-ALAN-122-124 | PRs #121/#124 selective UI port, DS PR #8 | [P05-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-03) |
| P06-02 | Add GC soft onboarding and attributable confirmation | app | WP06 / Node 0 Complete and GC soft onboarding | Alan | Alan | Luke | Luke | P03-02, P04-02, P06-01 | A2 | Exceptional | Dependencies unmet | D-DATA-01, D-DATA-02, CHECK-ALAN-122-124 | PRs #123/#124 UX only, GC authorship audit | [P06-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P06-02) |
| P08-02 | Add processor-neutral payment command and webhook inbox | app | WP08 / Payments, invoices, credits, and refunds | Alan | Alan | Luke | Luke | P08-01, P07-02 | A2 | Exceptional | Blocked by decision | D-PAY-01, D-COM-05 | Business-model processor-neutral requirement | [P08-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-02) |
| P10-04 | Add intelligence safety evaluations and cross-service observability | intelligence | WP10 / Intelligence, memory, proposals, and Ask safety | Alan | Alan | Luke | Luke | P10-02, P10-03 | A2 | Large | Dependencies unmet | None | Current intelligence auth/telemetry tests | [P10-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-04) |
| P13-03 | Automate synthetic A1 core participant journey verification | app | WP13 / Deployment, cloud gates, and PHI readiness | Alan | Alan | Luke | Luke | P03-02, P04-03, P05-03, P11-03, P13-02 | A1 | Large | Dependencies unmet | None | Existing synthetic sandbox/scenario utilities | [P13-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-03) |
| P06-03 | Add readiness report and role-scoped progress surfaces | app | WP06 / Node 0 Complete and GC soft onboarding | Alan | Alan | Luke | Luke | P06-02, P10-02, P11-04 | A2 | Large | Dependencies unmet | D-DATA-01 | PR #124 score/report concepts | [P06-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P06-03) |
| P07-03 | Emit processor-neutral workspace promotion authorization | app | WP07 / Commercial configuration, enrollment, and promotion | Alan | Alan | Luke | Luke | P04-02, P07-02, P08-02 | A2 | Large | Dependencies unmet | D-COM-04, D-DATA-01 | Business-model promotion invariants | [P07-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-03) |
| P07-04 | Promote workspace exactly once from authorization event | app | WP07 / Commercial configuration, enrollment, and promotion | Alan | Alan | Luke | Luke | P03-03, P04-02, P07-03 | A2 | Exceptional | Dependencies unmet | D-COM-04, D-DATA-01, CHECK-ALAN-122-124 | byos.workspace_promotion_authorized.v1 contract, PR #124 source linkage concepts | [P07-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-04) |
| P09-04 | Complete active-case participant document and progress surfaces | app | WP09 / Documents, active case, and provider handoffs | Alan | Alan | Luke | Luke | P03-03, P07-04, P09-03, P11-03 | A2 | Exceptional | Dependencies unmet | D-COM-04, CHECK-ALAN-122-124 | PR #122 selective/direct reuse after checkpoint, PR #124 case UI | [P09-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-04) |
| P08-03 | Implement milestone invoicing, credits, and deterministic refunds | app | WP08 / Payments, invoices, credits, and refunds | Alan | Alan | Luke | Luke | P08-02, P07-04, P09-04 | A2 | Exceptional | Dependencies unmet | D-COM-04, D-COM-06, D-COM-07 | Payment/business-model milestone/refund tables | [P08-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-03) |
| P09-05 | Implement consent-scoped provider handoff snapshots and operations | app | WP09 / Documents, active case, and provider handoffs | Alan | Alan | Luke | Luke | P04-02, P09-03, P09-04, P10-02 | A2 | Exceptional | Dependencies unmet | D-PROV-01, D-PHI-01 | Protected provider-exchange worktree: selective port only after provenance fix | [P09-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-05) |
| P12-01 | Unify Ask and Learn shell with explicit context scopes | app | WP12 / Ask/Learn shell and mobile cutover | Alan | Alan | Luke | Luke | P10-03, P11-04, P09-04 | A2 | Large | Dependencies unmet | D-AI-01 | Current Ask widget/Learn workspace, PR #124 | [P12-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-01) |
| P08-04 | Add payment reconciliation and safe service-pause operations | app | WP08 / Payments, invoices, credits, and refunds | Alan | Alan | Luke | Luke | P08-03 | A2 | Large | Dependencies unmet | D-COM-08 | Business-model failure handling | [P08-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-04) |
| P13-05 | Enforce case RLS and a non-owner PostgreSQL runtime | app | WP13 / Deployment, cloud gates, and PHI readiness | Alan | Alan | Luke | Luke | P02-03, P03-03, P04-03, P09-05, P10-02 | B2 | Exceptional | Dependencies unmet | D-PHI-01 | case-shell.md current app-layer-only/RLS gap | [P13-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-05) |
| P12-02 | Complete mobile participant interaction and accessibility cutover | app | WP12 / Ask/Learn shell and mobile cutover | Alan | Alan | Luke | Luke | P05-03, P06-03, P09-04, P12-01 | A2 | Exceptional | Dependencies unmet | None | PR #122 mobile journey, PR #124 Node 0, DS PR #8 | [P12-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-02) |
| P13-06 | Harden B1/B2 backups, audit, alarms, and cohort controls | infra | WP13 / Deployment, cloud gates, and PHI readiness | Alan | Alan | Luke | Luke | P09-02, P13-02, P13-05 | B2 | Exceptional | Dependencies unmet | D-PHI-01, D-PHI-02 | Existing audit/backup/platform stack constructs | [P13-06](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-06) |
| P13-04 | Automate synthetic A2 commercial and document journey verification | app | WP13 / Deployment, cloud gates, and PHI readiness | Alan | Alan | Luke | Luke | P06-03, P07-04, P08-04, P09-05, P10-04, P12-02, P13-03 | A2 | Exceptional | Dependencies unmet | None | Payment document smoke paths, A1 harness | [P13-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-04) |
| P12-03 | Retire legacy participant routes behind verified redirects | app | WP12 / Ask/Learn shell and mobile cutover | Alan | Alan | Luke | Luke | P12-02, P13-04 | B1 | Large | Dependencies unmet | None | Current route inventory, PRs #112/#119 planning maps | [P12-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P12-03) |
| P13-07 | Publish B1 and B2 privacy, PHI, and operational go-no-go runbooks | .github | WP13 / Deployment, cloud gates, and PHI readiness | Luke | Joint | External/TBD | Luke | P13-04, P13-05, P13-06 | B2 | Large | Blocked by decision | D-PHI-01, D-PHI-02 | Natalyx compliance/company records by reference, all gate evidence | [P13-07](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-07) |

## Execution order

| Order | ID | Title | Repository | Dependencies | Gate |
| --- | --- | --- | --- | --- | --- |
| 1 | P00-01 | Approve programme baseline and extraction ledger | .github | P00-01 | Pre-A0 |
| 2 | P01-01 | Establish current-test and PostgreSQL CI evidence | app | P00-01 | A0 |
| 3 | P11-01 | Publish validated Learn artifact and provenance contract | learn | P00-01 | A2 |
| 4 | P11-03 | Release participant design-system accessibility and interaction contract | design-system | P00-01 | A1 |
| 5 | P02-01 | Decide migration architecture and compatibility contract | app | P01-01 | A0 |
| 6 | P03-01 | Harden auth return-to and participant resume | app | P01-01 | A1 |
| 7 | P13-01 | Expose known-revision health, readiness, and dependency diagnostics | app | P01-01 | A0 |
| 8 | P11-02 | Serve approved Learn catalog versions from intelligence | intelligence | P11-01 | A2 |
| 9 | P02-02 | Introduce versioned migration runner and readiness checks | app | P02-01 | A0 |
| 10 | P09-01 | Define document lifecycle, authorization, and retention contract | app | P00-01, P02-01 | A2 |
| 11 | P13-02 | Harden guarded deployment, rollback, and evidence capture | infra | P01-01, P13-01 | A0 |
| 12 | P11-04 | Adopt approved Learn and source-card recipes in app | app | P11-02, P11-03 | A2 |
| 13 | P02-03 | Baseline canonical schema and prove expand-contract repair | app | P02-02 | A1 |
| 14 | P02-04 | Move intelligence persistence to a revisioned migration namespace | intelligence | P02-01, P02-02 | A1 |
| 15 | P09-02 | Provision private encrypted document and quarantine storage | infra | P09-01, P13-02 | A2 |
| 16 | P04-01 | Separate Node 0 workspace storage from paid cases | app | P02-03 | A1 |
| 17 | P07-01 | Add versioned commercial configuration and terms acceptance | app | P02-03 | A2 |
| 18 | P09-03 | Implement resilient document upload, scan, and download | app | P09-02, P02-03 | A2 |
| 19 | P03-02 | Add low-risk workspace claim lifecycle | app | P03-01, P04-01 | A1 |
| 20 | P03-03 | Bind paid-case invitations to identity and consent | app | P03-01, P04-01 | A2 |
| 21 | P04-02 | Add attributable workspace revision and projection contracts | app | P04-01 | A1 |
| 22 | P05-01 | Replace Pathfinder routing with deterministic entry decisions | app | P03-01, P04-01 | A1 |
| 23 | P08-01 | Add append-only commercial and money ledgers | app | P02-03, P07-01 | A2 |
| 24 | P03-04 | Replace shared signup admission with claim-aware Cognito admission | infra | P03-02, P03-03 | A1 |
| 25 | P04-03 | Adapt legacy Node 0 case-shaped data without semantic promotion | app | P04-02 | A1 |
| 26 | P10-01 | Version the scoped intelligence context envelope | intelligence | P01-01, P04-02 | A2 |
| 27 | P05-02 | Rebuild Node 0 Free candidate and outreach domain | app | P04-02, P05-01 | A1 |
| 28 | P06-01 | Add Node 0 Complete entitlement and versioned feature gates | app | P04-01, P07-01, P08-01 | A2 |
| 29 | P07-02 | Implement commitment and enrollment-pending lifecycle | app | P07-01, P08-01 | A2 |
| 30 | P10-02 | Enforce private/shared memory and evidence-bound proposal approval | app | P04-02, P10-01 | A2 |
| 31 | P10-03 | Harden Ask and Learn grounding and degraded-mode behavior | intelligence | P10-01, P11-02 | A2 |
| 32 | P05-03 | Ship resumable Node 0 Free participant surface | app | P03-01, P05-02, P11-03 | A1 |
| 33 | P06-02 | Add GC soft onboarding and attributable confirmation | app | P03-02, P04-02, P06-01 | A2 |
| 34 | P08-02 | Add processor-neutral payment command and webhook inbox | app | P08-01, P07-02 | A2 |
| 35 | P10-04 | Add intelligence safety evaluations and cross-service observability | intelligence | P10-02, P10-03 | A2 |
| 36 | P13-03 | Automate synthetic A1 core participant journey verification | app | P03-02, P04-03, P05-03, P11-03, P13-02 | A1 |
| 37 | P06-03 | Add readiness report and role-scoped progress surfaces | app | P06-02, P10-02, P11-04 | A2 |
| 38 | P07-03 | Emit processor-neutral workspace promotion authorization | app | P04-02, P07-02, P08-02 | A2 |
| 39 | P07-04 | Promote workspace exactly once from authorization event | app | P03-03, P04-02, P07-03 | A2 |
| 40 | P09-04 | Complete active-case participant document and progress surfaces | app | P03-03, P07-04, P09-03, P11-03 | A2 |
| 41 | P08-03 | Implement milestone invoicing, credits, and deterministic refunds | app | P08-02, P07-04, P09-04 | A2 |
| 42 | P09-05 | Implement consent-scoped provider handoff snapshots and operations | app | P04-02, P09-03, P09-04, P10-02 | A2 |
| 43 | P12-01 | Unify Ask and Learn shell with explicit context scopes | app | P10-03, P11-04, P09-04 | A2 |
| 44 | P08-04 | Add payment reconciliation and safe service-pause operations | app | P08-03 | A2 |
| 45 | P13-05 | Enforce case RLS and a non-owner PostgreSQL runtime | app | P02-03, P03-03, P04-03, P09-05, P10-02 | B2 |
| 46 | P12-02 | Complete mobile participant interaction and accessibility cutover | app | P05-03, P06-03, P09-04, P12-01 | A2 |
| 47 | P13-06 | Harden B1/B2 backups, audit, alarms, and cohort controls | infra | P09-02, P13-02, P13-05 | B2 |
| 48 | P13-04 | Automate synthetic A2 commercial and document journey verification | app | P06-03, P07-04, P08-04, P09-05, P10-04, P12-02, P13-03 | A2 |
| 49 | P12-03 | Retire legacy participant routes behind verified redirects | app | P12-02, P13-04 | B1 |
| 50 | P13-07 | Publish B1 and B2 privacy, PHI, and operational go-no-go runbooks | .github | P13-04, P13-05, P13-06 | B2 |

## Critical path

`P00-01` → `P01-01` → `P02-01` → `P02-02` → `P02-03` → `P07-01` → `P08-01` → `P07-02` → `P08-02` → `P07-03` → `P07-04` → `P09-04` → `P08-03` → `P08-04` → `P13-04` → `P13-07`

Required dependency joins:

- P07-03 additionally waits for P04-02 (workspace/provenance); P07-04 additionally waits for P03-03 (paid-case invitation).
- P09-04 additionally waits for P09-03 and P11-03; P13-04 additionally waits for P06-03, P09-05, P10-04, P12-02 and A1 runner P13-03.
- P13-07 additionally waits for P13-05 RLS/non-owner runtime and P13-06 backup/audit/control evidence before B2.

## Per-PR readiness and acceptance

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

### P01-01 — Establish current-test and PostgreSQL CI evidence

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P01-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P01-01) |
| Gate / size / readiness | A0 / Medium / Dependencies unmet |
| Dependencies | P00-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PR #122 unittest workflow and backend-neutral fixes after reconciliation |

#### Objective

Run the current suite on pull requests/main and prove the existing schema boots and behaves on an ephemeral PostgreSQL service before any migration redesign.

#### Scope

- Python-version/dependency cache and current test suite
- Ephemeral PostgreSQL current-schema evidence
- Sanitized failure artifacts

#### Explicit non-goals

- No migration-version table
- No new-schema tests
- No application behavior

#### Expected files or modules

- `.github/workflows/python-tests.yml`
- `tests/python/test_postgres_current_schema.py`
- `scripts/ci_postgres_evidence.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None; exercise the schema that main owns today. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Add blocking unit and PostgreSQL evidence jobs. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Current Python suite
- init_db twice on PostgreSQL
- representative create/read/authorization path
- intentional failure log-redaction check

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A0** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P00-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Run the current suite on pull requests/main and prove the existing schema boots and behaves on an ephemeral PostgreSQL service before any migration redesign.
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

### P11-01 — Publish validated Learn artifact and provenance contract

| Field | Plan |
| --- | --- |
| Repository / base | `learn` (`main`) |
| Project item | [P11-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-01) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | content pipelines, schema validation, document generation |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P11-03 — Release participant design-system accessibility and interaction contract

| Field | Plan |
| --- | --- |
| Repository / base | `design-system` (`main`) |
| Project item | [P11-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-03) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | design systems, accessibility, Jinja security |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P02-01 — Decide migration architecture and compatibility contract

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P02-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-01) |
| Gate / size / readiness | A0 / Small / Blocked by decision |
| Dependencies | P01-01 |
| Blocking decisions/checkpoints | D-MIG-01 |
| Source / salvage | app/storage/schema.py, app/storage/connection.py |

#### Objective

Record an ADR choosing an established migration framework or justified ordered runner, including PostgreSQL authority, SQLite support, locks, expand/contract, backfills, rollback, and forward repair.

#### Scope

- Compare Alembic and custom runner against current SQL compatibility layer
- Specify old/new revision compatibility and irreversible-change policy

#### Explicit non-goals

- No migration code
- No schema change

#### Expected files or modules

- `docs/adr/ADR-00x-versioned-migrations.md`
- `docs/agents/storage-data-layer.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Decision record only; select framework before P02-02. |

#### Tests and validation

Objective tests:

- ADR decision checklist
- example expand/contract and interrupted-backfill walkthrough

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A0** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P01-01. Parallel opportunities: P02-03

#### Objective acceptance criteria

- [ ] Record an ADR choosing an established migration framework or justified ordered runner, including PostgreSQL authority, SQLite support, locks, expand/contract, backfills, rollback, and forward repair.
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
| Required expertise | PostgreSQL migrations, zero-downtime deployment |
| Higher-capability review | Mandatory before merge |

### P03-01 — Harden auth return-to and participant resume

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-01) |
| Gate / size / readiness | A1 / Medium / Dependencies unmet |
| Dependencies | P01-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | PR #122 return_to fixes |

#### Objective

Make signup/login/confirmation/logout preserve a validated internal destination and restore the correct role-scoped workspace without query parameters becoming authority.

#### Scope

- Central safe_return_to parser
- Resume intent across login/signup/confirm/resend
- Session/cookie security and error states

#### Explicit non-goals

- No invitation issuance
- No case access grant

#### Expected files or modules

- `app/auth/routes.py`
- `app/auth/cloud.py`
- `app/auth/cognito.py`
- `tests/python/test_auth_routes.py`
- `tests/python/test_auth_cloud_integration.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Auth routes accept only allowlisted relative return targets. |
| UI/product surface | Clear expired/failed session recovery. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Open redirect corpus
- logged-out deep link
- signup confirmation
- logout/login resume
- secure/samesite cookie matrix

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

Hard dependencies: P01-01. Parallel opportunities: P03-04

#### Objective acceptance criteria

- [ ] Make signup/login/confirmation/logout preserve a validated internal destination and restore the correct role-scoped workspace without query parameters becoming authority.
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
| Required expertise | Cognito, web session security, FastAPI |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P13-01 — Expose known-revision health, readiness, and dependency diagnostics

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P13-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-01) |
| Gate / size / readiness | A0 / Large / Dependencies unmet |
| Dependencies | P01-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Current /healthz, direct 503 evidence |

#### Objective

Separate liveness, readiness, build revision, migration, database, intelligence, storage, and safe-config status so Gate A0 can identify the actual failing dependency.

#### Scope

- Unauthenticated minimal liveness
- Safe readiness/dependency checks
- Revision/config identifiers without secrets
- Startup failure classification

#### Explicit non-goals

- No PHI/PII in diagnostics
- No dependency mutation

#### Expected files or modules

- `app/health.py`
- `app/main.py`
- `app/dev_diagnostics.py`
- `tests/python/test_health.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Health/readiness endpoints with stable machine-readable reasons. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- DB/migration/intelligence/storage failures
- timeout
- redaction
- known SHA
- ALB contract

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A0** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Structured startup/readiness logs.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P01-01. Parallel opportunities: P13-03, P13-04, P13-05, P13-06, P13-07

#### Objective acceptance criteria

- [ ] Separate liveness, readiness, build revision, migration, database, intelligence, storage, and safe-config status so Gate A0 can identify the actual failing dependency.
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
| Required expertise | runtime operations, FastAPI, observability |
| Higher-capability review | Mandatory before merge |

### P11-02 — Serve approved Learn catalog versions from intelligence

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Project item | [P11-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-02) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Alan |
| Implementer | Alan (proposed; pending consolidated-plan sign-off) |
| Reviewer | Luke |
| Final approver | Luke |
| Required expertise | content serving, FastAPI, provenance |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P02-02 — Introduce versioned migration runner and readiness checks

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P02-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-02) |
| Gate / size / readiness | A0 / Large / Dependencies unmet |
| Dependencies | P02-01 |
| Blocking decisions/checkpoints | D-MIG-01 |
| Source / salvage | Current init_db startup path |

#### Objective

Implement the chosen ordered migration mechanism, checksum ledger, advisory lock, startup mode, and readiness signal without moving product tables yet.

#### Scope

- Version/checksum ledger and PostgreSQL advisory locking
- Separate migrate job/startup fail-closed policy
- Readiness reports pending/failed migration without sensitive detail

#### Explicit non-goals

- No Node 0/commercial tables
- No destructive down migration

#### Expected files or modules

- `migrations/`
- `app/storage/migrations.py`
- `app/readiness.py`
- `app/main.py`
- `tests/python/test_migrations.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Add migration metadata only. |
| API/routes | Add internal readiness detail behind safe health surface. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Bootstrap current database at a verified baseline. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Two concurrent migrators
- Checksum mismatch
- Partial failure and forward repair
- old app during expand window
- SQLite mode per ADR

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A0** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P02-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Implement the chosen ordered migration mechanism, checksum ledger, advisory lock, startup mode, and readiness signal without moving product tables yet.
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
| Required expertise | PostgreSQL, migration framework, runtime operations |
| Higher-capability review | Mandatory before merge |

### P09-01 — Define document lifecycle, authorization, and retention contract

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P09-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-01) |
| Gate / size / readiness | A2 / Medium / Blocked by decision |
| Dependencies | P00-01, P02-01 |
| Blocking decisions/checkpoints | D-DOC-01, D-DOC-02, D-PHI-01 |
| Source / salvage | Current metadata-only documents.py, provider branch |

#### Objective

Record the document state machine, role/purpose authorization matrix, object-key independence, retention/deletion/replacement rules, and failure recovery before storage implementation.

#### Scope

- Upload/scan/available/review/replace/delete states
- Size/type/checksum and filename policy
- Presigned versus proxied download decision
- Orphan/retention jobs

#### Explicit non-goals

- No bucket or application code

#### Expected files or modules

- `docs/adr/ADR-00x-durable-documents.md`
- `docs/agents/documents.md`
- `docs/security/document-threat-model.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Decision and threat model only. |

#### Tests and validation

Objective tests:

- Threat-model abuse cases
- state transition table review
- retention/legal-hold walkthrough

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

Hard dependencies: P00-01, P02-01. Parallel opportunities: P09-03, P09-04, P09-05

#### Objective acceptance criteria

- [ ] Record the document state machine, role/purpose authorization matrix, object-key independence, retention/deletion/replacement rules, and failure recovery before storage implementation.
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
| Required expertise | application security, S3/KMS, privacy |
| Higher-capability review | Mandatory before merge |

### P13-02 — Harden guarded deployment, rollback, and evidence capture

| Field | Plan |
| --- | --- |
| Repository / base | `infra` (`main`) |
| Project item | [P13-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-02) |
| Gate / size / readiness | A0 / Large / Dependencies unmet |
| Dependencies | P01-01, P13-01 |
| Blocking decisions/checkpoints | D-OPS-01 |
| Source / salvage | Existing guarded app/infra workflows |

#### Objective

Make app/intelligence deployment record the image SHA/task definition, wait for health, capture non-secret failure evidence, and roll back or stop safely under explicit guards.

#### Scope

- Known-revision deploy and service stabilization
- Least-privilege one-off migration task identity
- Migration/app compatibility preflight
- Rollback/forward-repair decision
- Evidence artifact

#### Explicit non-goals

- No automatic billable activation
- No planning-task deployment

#### Expected files or modules

- `.github/workflows/cdk.yml`
- `lib/stacks/platform-stack.ts`
- `lib/constructs/migration-task.ts`
- `scripts/verify-service-health.*`
- `docs/runbooks/deploy-rollback.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Guarded workflow/alarms/contracts; default desired counts remain safe. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- CDK/workflow contract
- unhealthy revision
- rollback compatibility
- billable flag false
- missing SSM output

Local validation:

- `npm test`
- `npm run build`
- `Synthesize the affected CDK stack with billable/live changes disabled.`

Cloud validation: run only through Gate **A0** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Synthesize and review first; deploy only through the guarded dev workflow with billable/desired-count defaults unchanged, exact revision recorded, and explicit confirmation outside this planning task.

#### Rollback or forward repair

Return to the prior reviewed stack/task definition when compatible; otherwise keep resources fail-closed and forward-repair under the runbook. Never delete data-bearing resources as an automatic rollback.

#### Dependencies and parallel work

Hard dependencies: P01-01, P13-01. Parallel opportunities: P13-04, P13-05, P13-07

#### Objective acceptance criteria

- [ ] Make app/intelligence deployment record the image SHA/task definition, wait for health, capture non-secret failure evidence, and roll back or stop safely under explicit guards.
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
| Required expertise | AWS ECS/ALB, GitHub Actions, rollback operations |
| Higher-capability review | Mandatory before merge |

### P11-04 — Adopt approved Learn and source-card recipes in app

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P11-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P11-04) |
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

### P02-03 — Baseline canonical schema and prove expand-contract repair

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P02-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-03) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
| Dependencies | P02-02 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | app/storage/schema.py current definitions, PR #122 forward-migration tests after reconciliation |

#### Objective

Move the existing canonical schema under version control, preserve compatible reads/writes, and supply rehearsal/backfill/repair tooling for future packages.

#### Scope

- Baseline existing tables and indexes
- Remove startup DDL only after parity is proved
- Document restore/forward-repair procedure

#### Explicit non-goals

- No semantic Node 0 split
- No commercial schema

#### Expected files or modules

- `migrations/versions/*_canonical_baseline.py`
- `app/storage/schema.py`
- `scripts/rehearse_migrations.py`
- `tests/migrations/`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Existing canonical schema becomes a checksummed baseline. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Expand/contract rehearsal from previous main and representative legacy fixtures. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Fresh install
- Upgrade from captured pre-baseline schema
- previous app compatibility
- large-table backfill rehearsal
- failure injection

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

Hard dependencies: P02-02. Parallel opportunities: P02-01, P02-04

#### Objective acceptance criteria

- [ ] Move the existing canonical schema under version control, preserve compatible reads/writes, and supply rehearsal/backfill/repair tooling for future packages.
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
| Higher-capability review | Mandatory before merge |

### P02-04 — Move intelligence persistence to a revisioned migration namespace

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Project item | [P02-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P02-04) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
| Dependencies | P02-01, P02-02 |
| Blocking decisions/checkpoints | D-MIG-01 |
| Source / salvage | src/natalyx_intelligence/shared/persistence.py runtime _ensure_schema |

#### Objective

Replace intelligence runtime _ensure_schema DDL with the chosen framework, a separate revision namespace/advisory lock, deploy-time migration entrypoint, and cross-service compatibility evidence.

#### Scope

- Fingerprint and baseline intelligence-owned tables
- Separate revision/lock key from app
- Remove runtime DDL authority after adoption
- Shared-Postgres compatibility matrix

#### Explicit non-goals

- No context/product feature
- No app-owned table mutation

#### Expected files or modules

- `migrations/`
- `src/natalyx_intelligence/shared/persistence.py`
- `scripts/migrate.py`
- `tests/test_migrations.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Intelligence-owned tables enter a checksummed revision chain. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Deploy-controlled one-off task; runtime verifies head only. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Fresh/legacy PostgreSQL
- concurrent app/intelligence migrators
- old/new service compatibility
- interrupted migration
- runtime non-owner

Local validation:

- `uv run pytest`
- Run focused contract/migration/safety tests with redacted fixtures.

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P02-01, P02-02. Parallel opportunities: P02-03

#### Objective acceptance criteria

- [ ] Replace intelligence runtime _ensure_schema DDL with the chosen framework, a separate revision namespace/advisory lock, deploy-time migration entrypoint, and cross-service compatibility evidence.
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
| Required expertise | PostgreSQL migrations, FastAPI service operations |
| Higher-capability review | Mandatory before merge |

### P09-02 — Provision private encrypted document and quarantine storage

| Field | Plan |
| --- | --- |
| Repository / base | `infra` (`main`) |
| Project item | [P09-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-02) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P09-01, P13-02 |
| Blocking decisions/checkpoints | D-DOC-02, D-PHI-01 |
| Source / salvage | Existing infra platform stack patterns |

#### Objective

Provision dev/private document buckets, KMS policy, block-public-access, lifecycle/quarantine events, least-privilege task roles, and audit logging behind PHI/billable guardrails.

#### Scope

- Private primary/quarantine storage
- KMS and task-role policy
- Lifecycle/orphan signals
- No public ACL/policy

#### Explicit non-goals

- No production/PHI activation
- No application upload

#### Expected files or modules

- `lib/stacks/platform-stack.ts`
- `lib/constructs/document-storage.ts`
- `test/document-storage.test.ts`
- `docs/agents/platform-stack.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | CDK resources and SSM outputs in dev, desired counts unchanged by default. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- CDK assertions
- IAM negative cases
- public-access-block
- encryption/lifecycle/event contract

Local validation:

- `npm test`
- `npm run build`
- `Synthesize the affected CDK stack with billable/live changes disabled.`

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Synthesize and review first; deploy only through the guarded dev workflow with billable/desired-count defaults unchanged, exact revision recorded, and explicit confirmation outside this planning task.

#### Rollback or forward repair

Return to the prior reviewed stack/task definition when compatible; otherwise keep resources fail-closed and forward-repair under the runbook. Never delete data-bearing resources as an automatic rollback.

#### Dependencies and parallel work

Hard dependencies: P09-01, P13-02. Parallel opportunities: P09-04, P09-05

#### Objective acceptance criteria

- [ ] Provision dev/private document buckets, KMS policy, block-public-access, lifecycle/quarantine events, least-privilege task roles, and audit logging behind PHI/billable guardrails.
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
| Required expertise | AWS S3, KMS/IAM, CDK, security |
| Higher-capability review | Mandatory before merge |

### P04-01 — Separate Node 0 workspace storage from paid cases

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P04-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P04-01) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
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

### P07-01 — Add versioned commercial configuration and terms acceptance

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-01) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P02-03 |
| Blocking decisions/checkpoints | D-COM-01, D-COM-02, D-COM-03 |
| Source / salvage | Payment/business-model DOCX |

#### Objective

Store activated price books, milestone schedules, Node 0 credit rules, and immutable terms/privacy acceptance versions without scattering literals.

#### Scope

- Immutable activated config versions
- JMF/deposit/discount/milestones/credit policy
- Terms and privacy acceptance records

#### Explicit non-goals

- No unresolved Node 0 price value
- No payment provider

#### Expected files or modules

- `migrations/versions/*_commercial_configuration.py`
- `app/domain/commercial_config.py`
- `app/storage/commercial_config.py`
- `tests/python/test_commercial_config.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Commercial configuration and acceptance ledgers. |
| API/routes | Read active config and record acceptance commands. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Activation immutability
- currency/amount validation
- acceptance version
- no retroactive mutation

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P02-03. Parallel opportunities: P07-03, P07-04

#### Objective acceptance criteria

- [ ] Store activated price books, milestone schedules, Node 0 credit rules, and immutable terms/privacy acceptance versions without scattering literals.
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
| Required expertise | commercial systems, PostgreSQL |
| Higher-capability review | Mandatory before merge |

### P09-03 — Implement resilient document upload, scan, and download

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P09-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-03) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P09-02, P02-03 |
| Blocking decisions/checkpoints | D-DOC-01, D-DOC-02 |
| Source / salvage | Current metadata scaffold |

#### Objective

Implement multipart-safe upload intent/finalize, checksum/type/size validation, quarantine/scan transitions, authorized download, replacement, deletion, and task-recovery behavior.

#### Scope

- Opaque object keys and sanitized display names
- Durable upload states
- Malware/quarantine integration
- Presigned/proxy path per ADR
- Audit events

#### Explicit non-goals

- No public object URL
- No provider share by key

#### Expected files or modules

- `app/documents/service.py`
- `app/documents/storage.py`
- `app/routes/documents.py`
- `app/jobs/document_recovery.py`
- `tests/python/test_documents_e2e.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Versioned document/upload/scan/object metadata. |
| API/routes | Intent/finalize/status/download/replace/delete commands. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Oversize/type spoof
- checksum mismatch
- scan fail/timeout
- ECS task replacement
- orphan cleanup
- authorization

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P09-02, P02-03. Parallel opportunities: P09-01

#### Objective acceptance criteria

- [ ] Implement multipart-safe upload intent/finalize, checksum/type/size validation, quarantine/scan transitions, authorized download, replacement, deletion, and task-recovery behavior.
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
| Required expertise | S3, secure uploads, background jobs, authorization |
| Higher-capability review | Mandatory before merge |

### P03-02 — Add low-risk workspace claim lifecycle

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-02) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
| Dependencies | P03-01, P04-01 |
| Blocking decisions/checkpoints | D-AUTH-01, CHECK-ALAN-122-124 |
| Source / salvage | PRs #123/#124, dirty onboarding-link worktree |

#### Objective

Create a pending Node 0 workspace claim that can start from an unaddressed link but requires identity binding, consent, expiry, revocation, and audit before low-risk access.

#### Scope

- Hashed one-time token and claim state machine
- Identity bind/consent/revoke/duplicate/mismatch behavior
- No sensitive case scope

#### Explicit non-goals

- No paid-case membership
- No possession-only private access

#### Expected files or modules

- `app/storage/workspace_claims.py`
- `app/routes/node0_claims.py`
- `app/templates/node0/claim*.html`
- `tests/python/test_workspace_claims.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Workspace claims and audit/idempotency fields. |
| API/routes | Issue, inspect, bind, consent, claim, revoke endpoints. |
| UI/product surface | Low-risk claim and mismatch screens. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Forwarded link
- duplicate/concurrent claim
- expiry/revocation
- identity mismatch
- issuer visibility

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

Hard dependencies: P03-01, P04-01. Parallel opportunities: P03-03

#### Objective acceptance criteria

- [ ] Create a pending Node 0 workspace claim that can start from an unaddressed link but requires identity binding, consent, expiry, revocation, and audit before low-risk access.
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
| Higher-capability review | Mandatory before merge |

### P03-03 — Bind paid-case invitations to identity and consent

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-03) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P03-01, P04-01 |
| Blocking decisions/checkpoints | D-AUTH-01, CHECK-ALAN-122-124 |
| Source / salvage | PR #122 CAS/TTL/self-invite fixes, current invitations.py |

#### Objective

Implement a separate recipient-bound paid-case invitation that grants membership only after authenticated binding, required confirmation, consent, and case/role checks.

#### Scope

- Case invite CAS transitions
- Recipient/issuer mismatch confirmation
- Consent-version capture and membership transaction

#### Explicit non-goals

- No workspace token reuse
- No automatic GC migration from soft onboarding

#### Expected files or modules

- `app/storage/case_invitations.py`
- `app/case_members.py`
- `app/routes/case.py`
- `tests/python/test_case_invitations.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Case-invitation identity, consent, expiry, revocation, idempotency fields. |
| API/routes | Separate paid-case redeem/confirm flow. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Membership grant is a single authorized transaction. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Replay
- self-invite
- active-member duplicate
- mismatch
- expired/revoked
- concurrent redemption rollback

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P03-01, P04-01. Parallel opportunities: P03-02

#### Objective acceptance criteria

- [ ] Implement a separate recipient-bound paid-case invitation that grants membership only after authenticated binding, required confirmation, consent, and case/role checks.
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
| Higher-capability review | Mandatory before merge |

### P04-02 — Add attributable workspace revision and projection contracts

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P04-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P04-02) |
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
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
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

### P05-01 — Replace Pathfinder routing with deterministic entry decisions

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P05-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-01) |
| Gate / size / readiness | A1 / Medium / Dependencies unmet |
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

### P08-01 — Add append-only commercial and money ledgers

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-01) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P02-03, P07-01 |
| Blocking decisions/checkpoints | D-COM-01, D-COM-02, D-COM-03 |
| Source / salvage | Payment/business-model DOCX |

#### Objective

Create immutable commercial-event, invoice, payment, credit, refund, and adjustment entries with deterministic projections and config-version references.

#### Scope

- Ledger invariants and currency precision
- Derived balances/status projections
- Audit/source/idempotency references

#### Explicit non-goals

- No processor
- No mutable balance authority
- No pass-through custody

#### Expected files or modules

- `migrations/versions/*_commercial_ledgers.py`
- `app/storage/ledgers.py`
- `app/domain/money.py`
- `tests/python/test_ledgers.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Append-only financial ledgers and unique idempotency constraints. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Least-privilege write paths and redacted logs. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Double-entry-like conservation checks
- duplicate key
- credit floor
- refund totals
- concurrent append

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P02-03, P07-01. Parallel opportunities: P08-03, P08-04

#### Objective acceptance criteria

- [ ] Create immutable commercial-event, invoice, payment, credit, refund, and adjustment entries with deterministic projections and config-version references.
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
| Required expertise | payments, financial ledgers, PostgreSQL |
| Higher-capability review | Mandatory before merge |

### P03-04 — Replace shared signup admission with claim-aware Cognito admission

| Field | Plan |
| --- | --- |
| Repository / base | `infra` (`main`) |
| Project item | [P03-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-04) |
| Gate / size / readiness | A1 / Large / Blocked by decision |
| Dependencies | P03-02, P03-03 |
| Blocking decisions/checkpoints | D-AUTH-02 |
| Source / salvage | infra platform-stack.ts current allowlist + shared invite code |

#### Objective

Keep internal/dev allowlisting but add a short-lived, recipient-bound admission proof for approved workspace/case claimants so a shared invite code is never the participant trust boundary.

#### Scope

- One-time signed or server-verified admission proof
- Email/purpose/claim/expiry binding
- Replay/revocation/audit
- No membership grant in Cognito

#### Explicit non-goals

- No open self-signup
- No Cognito group as case authority
- No shared user-entered master code

#### Expected files or modules

- `lib/stacks/platform-stack.ts`
- `lib/constructs/auth-admission.ts`
- `test/auth-admission.test.ts`
- `docs/agents/platform-stack.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Client metadata carries opaque admission proof only. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Harden pre-signup Lambda and key/claim verification contract; keep missing config fail closed. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Wrong email/purpose
- expired/replayed proof
- revoked claim
- internal allowlist path
- missing key/config
- membership still denied before app redemption

Local validation:

- `npm test`
- `npm run build`
- `Synthesize the affected CDK stack with billable/live changes disabled.`

Cloud validation: run only through Gate **A1** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Synthesize and review first; deploy only through the guarded dev workflow with billable/desired-count defaults unchanged, exact revision recorded, and explicit confirmation outside this planning task.

#### Rollback or forward repair

Return to the prior reviewed stack/task definition when compatible; otherwise keep resources fail-closed and forward-repair under the runbook. Never delete data-bearing resources as an automatic rollback.

#### Dependencies and parallel work

Hard dependencies: P03-02, P03-03. Parallel opportunities: P03-01

#### Objective acceptance criteria

- [ ] Keep internal/dev allowlisting but add a short-lived, recipient-bound admission proof for approved workspace/case claimants so a shared invite code is never the participant trust boundary.
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
| Required expertise | Cognito, AWS Lambda/KMS, identity security |
| Higher-capability review | Mandatory before merge |

### P04-03 — Adapt legacy Node 0 case-shaped data without semantic promotion

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P04-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P04-03) |
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
| Higher-capability review | Mandatory before merge |

### P10-01 — Version the scoped intelligence context envelope

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Project item | [P10-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-01) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P01-01, P04-02 |
| Blocking decisions/checkpoints | D-DATA-01, D-AI-01 |
| Source / salvage | Current case_context advisory stub |

#### Objective

Define and validate versioned request/response envelopes that keep general Learn, private-user memory, approved shared-case facts, and provider-purpose context distinct.

#### Scope

- Explicit scope and audience
- Source/provenance/verification metadata
- Policy/model/version and redacted trace metadata

#### Explicit non-goals

- No durable app write
- No merged contexts

#### Expected files or modules

- `src/natalyx_intelligence/contracts/context.py`
- `src/natalyx_intelligence/case_context.py`
- `docs/agents/case-context.md`
- `tests/test_context_contract.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Versioned context/advisory contract with strict validation and safe compatibility window. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Cross-scope rejection
- unknown version
- private/shared fixtures
- redaction
- service auth

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

Hard dependencies: P01-01, P04-02. Parallel opportunities: P10-04

#### Objective acceptance criteria

- [ ] Define and validate versioned request/response envelopes that keep general Learn, private-user memory, approved shared-case facts, and provider-purpose context distinct.
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
| Required expertise | FastAPI/Pydantic, AI safety, privacy |
| Higher-capability review | Mandatory before merge |

### P05-02 — Rebuild Node 0 Free candidate and outreach domain

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P05-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-02) |
| Gate / size / readiness | A1 / Exceptional / Dependencies unmet |
| Dependencies | P04-02, P05-01 |
| Blocking decisions/checkpoints | CHECK-ALAN-122-124 |
| Source / salvage | PR #117 direct algorithm/test salvage, PR #124, quiz rewrite worktree |

#### Objective

Port the useful deterministic candidate, preliminary safety, and outreach behavior onto workspace/provenance contracts while preserving the complete-the-match free boundary.

#### Scope

- Unlimited candidates
- Preliminary hard-criteria check with limitations
- Basic outreach sequencing and shareable intro packet

#### Explicit non-goals

- No weighted ranking
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
| Schema/model | Use workspace candidates/assertions from WP04. |
| API/routes | Workspace-scoped candidate and guide commands. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Deterministic metrics
- critical safety blocking
- author attribution
- candidate isolation
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
| Higher-capability review | Mandatory before merge |

### P06-01 — Add Node 0 Complete entitlement and versioned feature gates

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P06-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P06-01) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P04-01, P07-01, P08-01 |
| Blocking decisions/checkpoints | D-COM-01 |
| Source / salvage | Business-model Node 0 feature table |

#### Objective

Model optional Complete access independently from workspace and case, pin the commercial configuration, and expose server-side gates for the approved paid-depth features.

#### Scope

- Grant/suspend/revoke entitlement events
- Commercial-version and payment evidence reference
- Credit accrual link

#### Explicit non-goals

- No hard-coded price
- No paid-case creation

#### Expected files or modules

- `migrations/versions/*_entitlements.py`
- `app/domain/entitlements.py`
- `app/storage/entitlements.py`
- `tests/python/test_entitlements.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Append-only entitlement events plus current projection. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Every Complete feature checks server entitlement. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Grant replay
- suspend/revoke
- config version
- free-feature unaffected
- no case created

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P04-01, P07-01, P08-01. Parallel opportunities: P06-03

#### Objective acceptance criteria

- [ ] Model optional Complete access independently from workspace and case, pin the commercial configuration, and expose server-side gates for the approved paid-depth features.
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
| Higher-capability review | Mandatory before merge |

### P07-02 — Implement commitment and enrollment-pending lifecycle

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-02) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P07-01, P08-01 |
| Blocking decisions/checkpoints | D-COM-04 |
| Source / salvage | Business-model conversion trigger |

#### Objective

Create a deliberate managed-journey commitment with accepted terms, selected payment path, pinned config, and an enrollment invoice request independent from case state.

#### Scope

- Draft/accepted/cancelled/expired commitment transitions
- Payment-path choice
- Enrollment invoice command

#### Explicit non-goals

- No browser-triggered promotion
- No activation

#### Expected files or modules

- `app/domain/commitments.py`
- `app/storage/commitments.py`
- `app/routes/enrollment.py`
- `tests/python/test_commitments.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Commitment events/current projection. |
| API/routes | Create, accept, cancel, inspect enrollment. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Acceptance prerequisites
- duplicate accept
- stale config
- cancel/expire
- resume

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P07-01, P08-01. Parallel opportunities: P07-04

#### Objective acceptance criteria

- [ ] Create a deliberate managed-journey commitment with accepted terms, selected payment path, pinned config, and an enrollment invoice request independent from case state.
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
| Higher-capability review | Mandatory before merge |

### P10-02 — Enforce private/shared memory and evidence-bound proposal approval

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P10-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-02) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P04-02, P10-01 |
| Blocking decisions/checkpoints | D-DATA-01, D-AI-01 |
| Source / salvage | Current facts/memory/proposals scaffolds, GC authorship audit |

#### Objective

Store attributable private/shared memory revisions and require authorized evidence review before an intelligence proposal can affect case truth or provider material.

#### Scope

- Private and shared memory ledgers
- Proposal preview/approve/reject
- Evidence/source and reviewer authority
- Audit/outbox

#### Explicit non-goals

- No automatic AI approval
- No guide notes default shared

#### Expected files or modules

- `app/case_intelligence.py`
- `app/storage/memory.py`
- `app/storage/proposals.py`
- `app/storage/facts.py`
- `tests/python/test_case_intelligence.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Revision/supersedes/provenance/evidence fields under migrations. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Role and purpose authorization on every projection/write. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Private-to-shared denial
- wrong-role approval
- AI provenance remains proposal
- concurrent review
- provider projection

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P04-02, P10-01. Parallel opportunities: P10-03

#### Objective acceptance criteria

- [ ] Store attributable private/shared memory revisions and require authorized evidence review before an intelligence proposal can affect case truth or provider material.
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
| Required expertise | AI safety, authorization, data provenance |
| Higher-capability review | Mandatory before merge |

### P10-03 — Harden Ask and Learn grounding and degraded-mode behavior

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Project item | [P10-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-03) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P10-01, P11-02 |
| Blocking decisions/checkpoints | D-AI-01 |
| Source / salvage | Current ask_natalyx.py and PR #124 Ask integration |

#### Objective

Answer from the declared scope with approved sources/citations and explicit boundary/failure notices; never fabricate case context or silently fall across scope.

#### Scope

- Approved resource resolution
- Scope-specific prompt/context
- Timeout/unavailable/empty-source behavior
- Citation validation

#### Explicit non-goals

- No medical/legal advice
- No unapproved corpus fallback

#### Expected files or modules

- `src/natalyx_intelligence/ask_natalyx.py`
- `src/natalyx_intelligence/learn_resources.py`
- `tests/test_ask_natalyx.py`
- `docs/agents/ask-natalyx.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Responses carry source, scope, policy, safety and degraded-mode metadata. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Empty/unapproved corpus
- service/provider timeout
- case question without case scope
- citation mismatch
- safety escalation

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

Hard dependencies: P10-01, P11-02. Parallel opportunities: P10-02

#### Objective acceptance criteria

- [ ] Answer from the declared scope with approved sources/citations and explicit boundary/failure notices; never fabricate case context or silently fall across scope.
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
| Required expertise | LLM orchestration, retrieval/citations, safety evaluation |
| Higher-capability review | Mandatory before merge |

### P05-03 — Ship resumable Node 0 Free participant surface

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P05-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P05-03) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
| Dependencies | P03-01, P05-02, P11-03 |
| Blocking decisions/checkpoints | CHECK-ALAN-122-124 |
| Source / salvage | PRs #121/#124 selective UI port, DS PR #8 |

#### Objective

Provide a coherent mobile-capable Node 0 Free workspace shell for candidate tracking, outreach, guide use, and resume without paid-case language.

#### Scope

- Workspace home and candidate flow
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
- resume
- authorization
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

### P06-02 — Add GC soft onboarding and attributable confirmation

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P06-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P06-02) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P03-02, P04-02, P06-01 |
| Blocking decisions/checkpoints | D-DATA-01, D-DATA-02, CHECK-ALAN-122-124 |
| Source / salvage | PRs #123/#124 UX only, GC authorship audit |

#### Objective

Let an authenticated GC claim low-risk workspace access, provide GC-owned answers, confirm/replace selected provisional facts, and preserve private boundaries.

#### Scope

- GC-authored profile/intake revisions
- Field-by-field confirmation/replacement
- Purpose-limited IP progress projection

#### Explicit non-goals

- No paid-case membership
- No provider share
- No medical eligibility determination

#### Expected files or modules

- `app/routes/gc_workspace.py`
- `app/storage/gc_onboarding.py`
- `app/templates/node0/gc_onboarding*.html`
- `tests/python/test_gc_soft_onboarding.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Use assertion/revision contract; onboarding progress events. |
| API/routes | No public API/route contract change. |
| UI/product surface | GC consent and privacy explanations. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Paired IP/GC visibility
- private contact/health fields
- revision lineage
- claim replay/mismatch
- mobile resume

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P03-02, P04-02, P06-01. Parallel opportunities: None inside this package beyond review/test preparation.

#### Objective acceptance criteria

- [ ] Let an authenticated GC claim low-risk workspace access, provide GC-owned answers, confirm/replace selected provisional facts, and preserve private boundaries.
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
| Required expertise | privacy, accessible forms, authorization |
| Higher-capability review | Mandatory before merge |

### P08-02 — Add processor-neutral payment command and webhook inbox

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-02) |
| Gate / size / readiness | A2 / Exceptional / Blocked by decision |
| Dependencies | P08-01, P07-02 |
| Blocking decisions/checkpoints | D-PAY-01, D-COM-05 |
| Source / salvage | Business-model processor-neutral requirement |

#### Objective

Define provider ports and a signed, idempotent webhook inbox that emits internal settlement/failure/refund events, including commercial.enrollment_funding_confirmed.v1 when domain conditions hold.

#### Scope

- Provider-neutral intents and event mapping
- Signature/replay/order handling
- Settlement predicate and outbox

#### Explicit non-goals

- No browser redirect settlement
- No financing implementation unless separately approved

#### Expected files or modules

- `app/payments/ports.py`
- `app/payments/webhook_inbox.py`
- `app/routes/payment_webhooks.py`
- `tests/python/test_payment_webhooks.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Processor-event inbox/outbox and mapping records. |
| API/routes | Processor webhook and internal payment commands. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Secrets/endpoints deferred to guarded environment configuration. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Signature failure
- replay/out-of-order
- amount/currency mismatch
- timeout/retry
- settlement event exactly once

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P08-01, P07-02. Parallel opportunities: P08-04

#### Objective acceptance criteria

- [ ] Define provider ports and a signed, idempotent webhook inbox that emits internal settlement/failure/refund events, including commercial.enrollment_funding_confirmed.v1 when domain conditions hold.
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
| Required expertise | payment security, webhooks, event systems |
| Higher-capability review | Mandatory before merge |

### P10-04 — Add intelligence safety evaluations and cross-service observability

| Field | Plan |
| --- | --- |
| Repository / base | `intelligence` (`main`) |
| Project item | [P10-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P10-04) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P10-02, P10-03 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Current intelligence auth/telemetry tests |

#### Objective

Add deterministic safety/grounding evaluations, correlation IDs, latency/failure metrics, and redacted traces across app-intelligence calls.

#### Scope

- Leakage/hallucination/fallback evals
- Correlation and contract version
- Safe logs and alarms

#### Explicit non-goals

- No prompt or participant payload in logs
- No PHI readiness claim

#### Expected files or modules

- `tests/evals/`
- `src/natalyx_intelligence/telemetry.py`
- `docs/runbooks/intelligence.md`
- `app/intelligence_auth.py (consumer follow-up PR if needed)`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- PII/PHI redaction fixtures
- correlation continuity
- failure classification
- model fallback
- eval threshold

Local validation:

- `uv run pytest`
- Run focused contract/migration/safety tests with redacted fixtures.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Metrics and redacted structured events; app-side consumer change must remain a separate coordinated PR if repository boundaries require it.

#### Rollout

Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P10-02, P10-03. Parallel opportunities: P10-01

#### Objective acceptance criteria

- [ ] Add deterministic safety/grounding evaluations, correlation IDs, latency/failure metrics, and redacted traces across app-intelligence calls.
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
| Required expertise | AI evaluation, observability, privacy |
| Higher-capability review | Mandatory before merge |

### P13-03 — Automate synthetic A1 core participant journey verification

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P13-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-03) |
| Gate / size / readiness | A1 / Large / Dependencies unmet |
| Dependencies | P03-02, P04-03, P05-03, P11-03, P13-02 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Existing synthetic sandbox/scenario utilities |

#### Objective

Run the entry, auth, Node 0 Free, low-risk GC claim, role separation, resume, and mobile journey against a known dev revision and publish a redacted A1 evidence bundle.

#### Scope

- A1 core IP/GC workspace journey
- Known SHA and evidence bundle
- Role/authorization negative cases
- Cleanup of synthetic records

#### Explicit non-goals

- No payment/promotion/document journey
- No real user
- No PHI
- No gate auto-approval

#### Expected files or modules

- `tests/cloud/a1/`
- `scripts/run_synthetic_a1.py`
- `.github/workflows/synthetic-cloud-gates.yml`
- `docs/runbooks/synthetic-gates.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Manual/guarded A1 synthetic runner with immutable artifact summary. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Happy path
- authorization denial
- retry/duplicate
- logout/login
- mobile
- dependency outage
- cleanup failure

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

Hard dependencies: P03-02, P04-03, P05-03, P11-03, P13-02. Parallel opportunities: P13-01, P13-05, P13-06, P13-07

#### Objective acceptance criteria

- [ ] Run the entry, auth, Node 0 Free, low-risk GC claim, role separation, resume, and mobile journey against a known dev revision and publish a redacted A1 evidence bundle.
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
| Required expertise | browser automation, AWS dev operations, end-to-end testing |
| Higher-capability review | Mandatory before merge |

### P06-03 — Add readiness report and role-scoped progress surfaces

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P06-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P06-03) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P06-02, P10-02, P11-04 |
| Blocking decisions/checkpoints | D-DATA-01 |
| Source / salvage | PR #124 score/report concepts |

#### Objective

Produce a preliminary, source-labelled Node 0 readiness report and separate IP/GC progress views without overclaiming clearance or exposing private answers.

#### Scope

- Source/verification labels
- IP and GC lenses
- Promotion-ready projection manifest

#### Explicit non-goals

- No provider-confirmed status
- No final case activation

#### Expected files or modules

- `app/domain/node0_readiness.py`
- `app/templates/node0/readiness*.html`
- `app/node0_surface.py`
- `tests/python/test_node0_readiness.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Read-only readiness projection with policy version. |
| UI/product surface | Role-specific report/progress cards. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Provisional labels
- critical missing data
- cross-role redaction
- stale revision
- print/mobile

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

Hard dependencies: P06-02, P10-02, P11-04. Parallel opportunities: P06-01

#### Objective acceptance criteria

- [ ] Produce a preliminary, source-labelled Node 0 readiness report and separate IP/GC progress views without overclaiming clearance or exposing private answers.
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
| Higher-capability review | Mandatory before merge |

### P07-03 — Emit processor-neutral workspace promotion authorization

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-03) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P04-02, P07-02, P08-02 |
| Blocking decisions/checkpoints | D-COM-04, D-DATA-01 |
| Source / salvage | Business-model promotion invariants |

#### Objective

Validate commitment, terms, commercial version, settled funding and credit evidence, then emit exactly one byos.workspace_promotion_authorized.v1 event; processor callbacks and browser redirects cannot emit it.

#### Scope

- Deterministic authorization predicate
- Canonical payload and idempotency key
- Transactional event/outbox
- Funding/credit/config evidence references

#### Explicit non-goals

- No case creation
- No redirect/webhook-as-authority
- No GC membership

#### Expected files or modules

- `app/domain/promotion_authorization.py`
- `app/event_handlers/commercial.py`
- `app/storage/outbox.py`
- `tests/python/test_promotion_authorization.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Internal event producer only. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Only commercial-domain authority can emit the typed event. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Pending/failed/reversed funding
- stale terms/config
- duplicate/replayed inputs
- credit mismatch
- event payload/checksum

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

Hard dependencies: P04-02, P07-02, P08-02. Parallel opportunities: P07-01

#### Objective acceptance criteria

- [ ] Validate commitment, terms, commercial version, settled funding and credit evidence, then emit exactly one byos.workspace_promotion_authorized.v1 event; processor callbacks and browser redirects cannot emit it.
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
| Required expertise | event-driven systems, payments, commercial policy |
| Higher-capability review | Mandatory before merge |

### P07-04 — Promote workspace exactly once from authorization event

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P07-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P07-04) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P03-03, P04-02, P07-03 |
| Blocking decisions/checkpoints | D-COM-04, D-DATA-01, CHECK-ALAN-122-124 |
| Source / salvage | byos.workspace_promotion_authorized.v1 contract, PR #124 source linkage concepts |

#### Objective

Consume byos.workspace_promotion_authorized.v1 to create/find one enrollment_pending paid case, link the source workspace, project allowlisted data, and grant only restricted IP membership.

#### Scope

- Unique promotion idempotency key
- Case/source link and config version
- Purpose-limited data manifest and audit event

#### Explicit non-goals

- No redirect authority
- No GC case membership transfer
- No activation

#### Expected files or modules

- `app/domain/promotion.py`
- `app/storage/promotions.py`
- `app/event_handlers/enrollment.py`
- `tests/python/test_workspace_promotion.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Promotion ledger and source-workspace unique constraint. |
| API/routes | Internal event handler only. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Projection defaults deny and preserves provenance. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Replay/concurrency
- partial transaction
- funding event validation
- private candidate exclusion
- GC invitation required

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P03-03, P04-02, P07-03. Parallel opportunities: P07-01, P07-02

#### Objective acceptance criteria

- [ ] Consume byos.workspace_promotion_authorized.v1 to create/find one enrollment_pending paid case, link the source workspace, project allowlisted data, and grant only restricted IP membership.
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
| Required expertise | event-driven systems, privacy, PostgreSQL |
| Higher-capability review | Mandatory before merge |

### P09-04 — Complete active-case participant document and progress surfaces

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P09-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-04) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P03-03, P07-04, P09-03, P11-03 |
| Blocking decisions/checkpoints | D-COM-04, CHECK-ALAN-122-124 |
| Source / salvage | PR #122 selective/direct reuse after checkpoint, PR #124 case UI |

#### Objective

Expose role-scoped active-case tasks, documents, progress, waiting and safe pause states after activation while keeping the server projection authoritative.

#### Scope

- enrollment_pending versus active surfaces
- IP/GC lenses
- Documents/tasks/timeline/notifications
- Mobile journey orientation

#### Explicit non-goals

- No client-owned state transition
- No operator/provider leakage

#### Expected files or modules

- `app/case_home.py`
- `app/case_journey.py`
- `app/routes/case.py`
- `app/templates/case/`
- `tests/python/test_case_home.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Membership-scoped reads and evidence commands. |
| UI/product surface | Participant control center and journey map backed by case projection. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- IP/GC paired lenses
- pending/active/paused
- no membership
- malformed/stale projection
- mobile/no-JS/reduced-motion

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

Hard dependencies: P03-03, P07-04, P09-03, P11-03. Parallel opportunities: P09-01, P09-02

#### Objective acceptance criteria

- [ ] Expose role-scoped active-case tasks, documents, progress, waiting and safe pause states after activation while keeping the server projection authoritative.
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
| Required expertise | FastAPI/Jinja, accessibility, authorization, state projection |
| Higher-capability review | Mandatory before merge |

### P08-03 — Implement milestone invoicing, credits, and deterministic refunds

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-03) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P08-02, P07-04, P09-04 |
| Blocking decisions/checkpoints | D-COM-04, D-COM-06, D-COM-07 |
| Source / salvage | Payment/business-model milestone/refund tables |

#### Objective

Turn explicit evidence-backed case transitions into one invoice each, apply Node 0 credit, and calculate reproducible earned/uncharged/refunded amounts from immutable state.

#### Scope

- Enrollment/activation/clearance/legal-escrow/pregnancy/birth milestones
- Credit allocation
- Non-clearance and cancellation tables
- Dignity delay for clinical-linked invoices

#### Explicit non-goals

- No unresolved pregnancy-loss automatic disposition
- No promise of reimbursement

#### Expected files or modules

- `app/domain/billing_policy.py`
- `app/domain/refunds.py`
- `app/event_handlers/case_billing.py`
- `tests/python/test_billing_policy.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | Internal evidence-to-invoice commands and explainable refund quote. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Only authorized domain events trigger billing. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- All milestone/refund rows
- duplicate/stale transition
- Node 0 credit
- pay-in-full/deposit math
- clinical notification separation

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

Hard dependencies: P08-02, P07-04, P09-04. Parallel opportunities: P08-01

#### Objective acceptance criteria

- [ ] Turn explicit evidence-backed case transitions into one invoice each, apply Node 0 credit, and calculate reproducible earned/uncharged/refunded amounts from immutable state.
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
| Required expertise | payments, commercial policy, case state |
| Higher-capability review | Mandatory before merge |

### P09-05 — Implement consent-scoped provider handoff snapshots and operations

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P09-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=P09-05) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P04-02, P09-03, P09-04, P10-02 |
| Blocking decisions/checkpoints | D-PROV-01, D-PHI-01 |
| Source / salvage | Protected provider-exchange worktree: selective port only after provenance fix |

#### Objective

Create purpose-bound, reviewed, checksummed provider packets from explicitly allowed facts/documents and operate send/confirm/revoke/reroute without ambient provider access.

#### Scope

- Packet revisions/snapshots/checksums
- Consent, recipient, purpose, expiry
- Operator route review and transmission outcomes
- Inbound evidence becomes proposal

#### Explicit non-goals

- No raw private/provisional bulk projection
- No provider truth without review

#### Expected files or modules

- `app/provider_handoffs.py`
- `app/storage/handoffs.py`
- `app/routes/operator_handoffs.py`
- `app/templates/internal/handoffs/`
- `tests/python/test_provider_handoffs.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Handoff/packet/snapshot/transmission/evidence ledgers under migrations. |
| API/routes | No public API/route contract change. |
| UI/product surface | Case-scoped operator queue and GC review. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Purpose allowlist
- revoked consent
- stale route
- snapshot immutability
- delivery retry
- private/provisional exclusion

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P04-02, P09-03, P09-04, P10-02. Parallel opportunities: P09-01, P09-02

#### Objective acceptance criteria

- [ ] Create purpose-bound, reviewed, checksummed provider packets from explicitly allowed facts/documents and operate send/confirm/revoke/reroute without ambient provider access.
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
| Required expertise | provider workflows, privacy, document security, operations |
| Higher-capability review | Mandatory before merge |

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

### P08-04 — Add payment reconciliation and safe service-pause operations

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P08-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P08-04) |
| Gate / size / readiness | A2 / Large / Dependencies unmet |
| Dependencies | P08-03 |
| Blocking decisions/checkpoints | D-COM-08 |
| Source / salvage | Business-model failure handling |

#### Objective

Expose operator-safe reconciliation, discrepancy, receipt, retry, and non-critical pause controls without blocking safety information or altering clinical truth.

#### Scope

- Ledger-vs-processor reconciliation
- Itemized receipt data
- Grace/reminder/soft-pause policy
- Audited manual adjustments

#### Explicit non-goals

- No organization-wide ambient access
- No critical-service lockout

#### Expected files or modules

- `app/payments/reconciliation.py`
- `app/routes/operator_billing.py`
- `app/templates/internal/billing/`
- `tests/python/test_reconciliation.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | Internal role-gated discrepancy and adjustment surface. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Role denial
- mismatch workflow
- manual adjustment audit
- critical content remains accessible
- provider outage

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **A2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Metrics/alerts for settlement, refund, mismatch and reserve inputs.

#### Rollout

Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate.

#### Rollback or forward repair

Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation.

#### Dependencies and parallel work

Hard dependencies: P08-03. Parallel opportunities: P08-01, P08-02

#### Objective acceptance criteria

- [ ] Expose operator-safe reconciliation, discrepancy, receipt, retry, and non-critical pause controls without blocking safety information or altering clinical truth.
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
| Required expertise | payment operations, authorization, observability |
| Higher-capability review | Mandatory before merge |

### P13-05 — Enforce case RLS and a non-owner PostgreSQL runtime

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P13-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-05) |
| Gate / size / readiness | B2 / Exceptional / Dependencies unmet |
| Dependencies | P02-03, P03-03, P04-03, P09-05, P10-02 |
| Blocking decisions/checkpoints | D-PHI-01 |
| Source / salvage | case-shell.md current app-layer-only/RLS gap |

#### Objective

Move app runtime to a least-privilege non-DDL database role and enforce tenant/case membership policies with RLS/FORCE RLS before any PHI gate can open.

#### Scope

- Runtime/migrator role separation
- RLS/FORCE RLS on case/participant/document/commercial tables
- Transaction-local subject/org/case context
- Policy-negative and pool-reset tests

#### Explicit non-goals

- No PHI gate activation
- No trust in app guards alone
- No runtime DDL

#### Expected files or modules

- `migrations/versions/*_case_rls.py`
- `app/storage/connection.py`
- `app/storage/session_context.py`
- `tests/security/test_case_rls.py`
- `docs/security/rls.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | RLS policies and least-privilege grants under a reviewed migration. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Database denies cross-case/ambient reads even if an app guard is missed. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Cross-case/role denial
- connection-pool context reset
- migrator versus runtime grants
- background worker scope
- previous app compatibility during rollout

Local validation:

- `python -m unittest discover -s tests/python`
- Run the focused test module(s) named above against SQLite and PostgreSQL where applicable.

Cloud validation: run only through Gate **B2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step.

#### Rollback or forward repair

Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence.

#### Dependencies and parallel work

Hard dependencies: P02-03, P03-03, P04-03, P09-05, P10-02. Parallel opportunities: P13-01, P13-02, P13-03, P13-04

#### Objective acceptance criteria

- [ ] Move app runtime to a least-privilege non-DDL database role and enforce tenant/case membership policies with RLS/FORCE RLS before any PHI gate can open.
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
| Required expertise | PostgreSQL RLS, connection pooling, security architecture |
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

### P13-06 — Harden B1/B2 backups, audit, alarms, and cohort controls

| Field | Plan |
| --- | --- |
| Repository / base | `infra` (`main`) |
| Project item | [P13-06](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-06) |
| Gate / size / readiness | B2 / Exceptional / Dependencies unmet |
| Dependencies | P09-02, P13-02, P13-05 |
| Blocking decisions/checkpoints | D-PHI-01, D-PHI-02 |
| Source / salvage | Existing audit/backup/platform stack constructs |

#### Objective

Add the infrastructure evidence and controls required for a named PII beta and later PHI review: backup/restore, data-event audit, least privilege, alarms, log retention, cohort disable, and emergency stop.

#### Scope

- RDS/S3 backup and restore evidence hooks
- CloudTrail S3 data events and access alarms
- Runtime/migrator/task-role least privilege
- Cohort disable and PHI gate kill switch
- Log retention/redaction contracts

#### Explicit non-goals

- No production/PHI activation
- No evidence claim without restore/tabletop

#### Expected files or modules

- `lib/stacks/platform-stack.ts`
- `lib/constructs/audit.ts`
- `lib/constructs/backup.ts`
- `test/security-controls.test.ts`
- `docs/runbooks/security-operations.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Guarded, cost-aware controls with explicit dev defaults and documented operational owners. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- CDK policy assertions
- restore drill
- alarm path
- access-log redaction
- cohort/PHI gate disable
- role boundary

Local validation:

- `npm test`
- `npm run build`
- `Synthesize the affected CDK stack with billable/live changes disabled.`

Cloud validation: run only through Gate **B2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Synthesize and review first; deploy only through the guarded dev workflow with billable/desired-count defaults unchanged, exact revision recorded, and explicit confirmation outside this planning task.

#### Rollback or forward repair

Return to the prior reviewed stack/task definition when compatible; otherwise keep resources fail-closed and forward-repair under the runbook. Never delete data-bearing resources as an automatic rollback.

#### Dependencies and parallel work

Hard dependencies: P09-02, P13-02, P13-05. Parallel opportunities: P13-01, P13-03, P13-04

#### Objective acceptance criteria

- [ ] Add the infrastructure evidence and controls required for a named PII beta and later PHI review: backup/restore, data-event audit, least privilege, alarms, log retention, cohort disable, and emergency stop.
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
| Required expertise | AWS security, backup/restore, CloudTrail/CloudWatch, IAM |
| Higher-capability review | Mandatory before merge |

### P13-04 — Automate synthetic A2 commercial and document journey verification

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P13-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-04) |
| Gate / size / readiness | A2 / Exceptional / Dependencies unmet |
| Dependencies | P06-03, P07-04, P08-04, P09-05, P10-04, P12-02, P13-03 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Payment document smoke paths, A1 harness |

#### Objective

Extend the known-revision cloud harness with commitment, funding, exactly-once promotion, case invite, activation, billing, refund, document, handoff, Ask/Learn, and recovery evidence.

#### Scope

- A2 commercial/promotion/billing/document journey
- Duplicate/retry/refund/failure cases
- Known SHA and evidence bundle
- Synthetic cleanup

#### Explicit non-goals

- No real money
- No real user
- No PHI
- No gate auto-approval

#### Expected files or modules

- `tests/cloud/a2/`
- `scripts/run_synthetic_a2.py`
- `.github/workflows/synthetic-cloud-gates.yml`
- `docs/runbooks/synthetic-gates.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | Guarded A2 synthetic runner; uses processor simulator and synthetic documents only. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Document the contract, version pins and safe partial-merge behavior. |

#### Tests and validation

Objective tests:

- Funding event exactly once
- promotion replay
- case invite
- milestone/refund
- upload/scan failure
- Ask scope
- rollback evidence

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

Hard dependencies: P06-03, P07-04, P08-04, P09-05, P10-04, P12-02, P13-03. Parallel opportunities: P13-01, P13-02, P13-05, P13-06

#### Objective acceptance criteria

- [ ] Extend the known-revision cloud harness with commitment, funding, exactly-once promotion, case invite, activation, billing, refund, document, handoff, Ask/Learn, and recovery evidence.
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
| Required expertise | browser automation, payments testing, AWS dev operations, end-to-end testing |
| Higher-capability review | Mandatory before merge |

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

### P13-07 — Publish B1 and B2 privacy, PHI, and operational go-no-go runbooks

| Field | Plan |
| --- | --- |
| Repository / base | `.github` (`main`) |
| Project item | [P13-07](https://github.com/orgs/NatalyxPlatform/projects/3?query=P13-07) |
| Gate / size / readiness | B2 / Large / Blocked by decision |
| Dependencies | P13-04, P13-05, P13-06 |
| Blocking decisions/checkpoints | D-PHI-01, D-PHI-02 |
| Source / salvage | Natalyx compliance/company records by reference, all gate evidence |

#### Objective

Create the programme evidence index and explicit human approval packets for PII beta (B1) and PHI readiness (B2), linking rather than duplicating controlled company/compliance records.

#### Scope

- Data classification and real-user boundary
- Access/logging/incident/backup/vendor/compliance evidence
- Named approvers and expiry/revalidation
- Rollback/stop response

#### Explicit non-goals

- No legal/compliance self-certification
- No PHI activation by merge

#### Expected files or modules

- `natalyx-repair-program/gates/B1-real-user-pii.md`
- `natalyx-repair-program/gates/B2-phi-go-no-go.md`
- `natalyx-repair-program/evidence-index.md`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | None in this PR; any later schema change stays in its named migration PR. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | No migration or backfill. |
| Security/privacy | Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases. |
| Architecture/docs/config | Controlled go/no-go checklists and evidence links only. |

#### Tests and validation

Objective tests:

- Evidence completeness review
- tabletop incident
- access review
- backup/restore evidence
- external security/privacy sign-off

Local validation:

- `git diff --check`
- `/Users/lukerhodes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/validate_programme.py`

Cloud validation: run only through Gate **B2** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.

#### Diagnostics and observability

Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII.

#### Rollout

Merge only after document/sign-off checks; it changes no runtime. Re-sync the Project from the same canonical data.

#### Rollback or forward repair

Correct the canonical data and regenerate; do not rewrite implementation history.

#### Dependencies and parallel work

Hard dependencies: P13-04, P13-05, P13-06. Parallel opportunities: P13-01, P13-02, P13-03

#### Objective acceptance criteria

- [ ] Create the programme evidence index and explicit human approval packets for PII beta (B1) and PHI readiness (B2), linking rather than duplicating controlled company/compliance records.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The Project item has matching dependency, readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| DRI | Luke |
| Implementer | Joint (proposed; pending consolidated-plan sign-off) |
| Reviewer | External/TBD |
| Final approver | Luke |
| Required expertise | privacy/security governance, operations, compliance |
| Higher-capability review | Mandatory before merge |
