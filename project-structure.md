# GitHub Project structure — MVP Product Flow Reshape

Project: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

## Pre-change inspection

Direct GraphQL inspection found Project 3 open with only GitHub's default Title, Assignees, Status, Labels, Linked PRs, Milestone, Repository, Reviewers, Parent issue, Sub-issues progress, Created, Updated and Closed fields, and **zero items**. The programme sync therefore does not duplicate prior programme items.

## Operating model

| Convention | Rule |
| --- | --- |
| Project | MVP Product Flow Reshape |
| Number | 3 |
| Status | Benched and closed after plan reconciliation; do not use for execution until the amended Drive package is jointly accepted and the Project is separately reactivated/resynced. |
| Hierarchy | Draft items cannot be true GitHub sub-issues. Work-package parents are identifiable draft epics; child PR/decision/gate items link by Work package and Dependencies fields and exact IDs. Convert only when real implementation begins. |
| Readiness | Local preparation status is distinct from merge readiness. A PR may permit isolated uncommitted preparation while remaining blocked from commit, PR creation or merge. |
| Assignment | PR ownership inherits the proposed work-package split pending Alan's review; named technical-decision ownership does not transfer implementation ownership across work packages. |
| Reviewer Field | GitHub reserves the literal custom-field name Reviewer, so Programme reviewer holds the requested planning reviewer role without duplicating the built-in Reviewers metadata. |
| Source Of Truth | programme_data.py is the package generator source and Drive is the canonical review surface. The benched Project becomes an operational control plane only after a separately authorized sync; catalogue changes must not be presented as live Project state. |

## Fields

| Field | Type | Options / use |
| --- | --- | --- |
| Item type | single | Work package, Proposed PR, Existing PR, Existing issue, Decision, Review checkpoint, Programme gate, Cleanup task |
| Work package | single | Programme, WP00, WP01, WP02, WP03, WP04, WP05, WP06, WP07, WP08, WP09, WP10, WP11, WP12, WP13 |
| Target repository | single | .github, natalyx-app, natalyx-infra, natalyx-intelligence, natalyx-learn-resources, natalyx-design-system, Multiple / external |
| Proposed PR ID | text | Free text |
| DRI | single | Luke, Alan, Joint, External / TBD, N/A |
| Implementer | single | Luke, Alan, Joint, External / TBD, N/A |
| Programme reviewer | single | Luke, Alan, Joint, External / TBD, N/A |
| Final approver | single | Luke, Alan, Joint, External / TBD, N/A |
| Dependencies | text | Free text |
| Programme gate | single | Pre-A0, A0, A1, A2, B1, B2, Post-B2, N/A |
| Size | single | Small, Medium, Large, Exceptional, N/A |
| Blocking decision | text | Free text |
| Source / salvage PR | text | Free text |
| Plan document path | text | Free text |
| Readiness | single | Needs plan approval, Awaiting reconciliation, Blocked by decision, Dependencies unmet, Ready to implement, In implementation, Verification, Complete, Retained for salvage |
| Disposition | single | Programme baseline, Proposed, Retain pending review, Direct reuse, Selective port, Rewrite, Supersede after extraction, Defer, Gate criterion, Decision needed, Checkpoint, Cleanup only |

GitHub's existing **Status** field is reused; no duplicate status field is created. Custom fields are the minimum set needed to hold the fields explicitly required by the programme brief for draft items as well as real PRs/issues.

## Item catalogue

| Item type | Expected count | Naming convention |
| --- | --- | --- |
| Work packages | 14 | [WPxx] title |
| Proposed PRs | 52 | [Pxx-yy] title |
| Existing PRs | 9 | Actual linked PR |
| Existing issues | 2 | Actual linked issue |
| Decisions | 24 | [DECISION D-*] title |
| Review checkpoints | 1 | [CHECKPOINT] title |
| Programme gates | 5 | [GATE Ax] title |
| Cleanup tasks | 3 | [CLEANUP C-*] title |

## Desired catalogue and last live snapshot

| Check | Recorded result |
| --- | --- |
| Catalogue Generated At | 2026-07-12 19:30 America/New_York |
| Live Snapshot At | 2026-07-10 21:59 America/New_York |
| Project Id | PVT_kwDOEAWZDM4BYbai |
| Items | 110 |
| Draft Items | 99 |
| Linked Items | 11 |
| Live Items | 106 |
| Live Draft Items | 95 |
| Live Linked Items | 11 |
| Total Fields | 29 |
| Custom Fields | 16 |
| Statuses | Desired catalogue: checkpoint and three resolved decisions Done; implementation PRs Todo. Last live snapshot: all 106 items Todo. |
| Required Values | Desired fields complete on 110 items; Proposed PR ID complete on all 52 proposed PR items |
| Type Counts | 14 WP; 52 proposed PR; 9 existing PR; 2 existing issue; 24 decision; 1 checkpoint; 5 gate; 3 cleanup |
| Result | Local desired catalogue validated; remote Project intentionally not resynced because it is benched and the task authorizes only canonical planning sources/generated artifacts. |

The desired 110-item catalogue is validated locally. The last read-back live snapshot remains 106 items and all Todo; this reconciliation did not apply remote Project changes. All implementation items remain planning-only and no proposed PR is marked `Ready to implement`.

## Dependency and hierarchy representation

Draft items cannot be true GitHub sub-issues. Work-package parents are identifiable draft epics; child PR/decision/gate items link by Work package and Dependencies fields and exact IDs. Convert only when real implementation begins.

Each proposed PR carries a Work package value and exact Dependencies text. Work-package draft bodies list child PR IDs, decisions, gates and plan path. Decision/gate/checkpoint bodies list what they block. This provides deterministic hierarchy without creating empty issues/PRs.

## Status, readiness and disposition

| Dimension | Meaning |
| --- | --- |
| Status | Todo / In Progress / Done: execution state only. |
| Local preparation | Whether isolated, uncommitted, synthetic-only work may occur before joint acceptance. |
| Merge readiness | Whether dependencies, decisions, reciprocal review, A0 and applicable external controls permit merge. |
| Disposition | How existing/proposed/decision/gate/cleanup material should be treated. |
| Ownership | Work-package DRI and primary implementer, separate technical-decision owner, reciprocal reviewer and founder approver; all remain proposed pending Alan's review. |

## Project sync and maintenance

Dry-run/read current state:

```bash
/Users/lukerhodes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/sync_project.py
```

Apply idempotent updates only after separate reactivation/authorization (the script blocks apply while benched):

```bash
/Users/lukerhodes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/sync_project.py --apply
```

After any canonical change, regenerate Markdown, validate and re-render the PDF. Validate the desired catalogue locally; remote sync is a separate authorized action after the benched Project is reactivated.

## Final Project validation checklist

- [ ] One identifiable item for every WP00-WP13.
- [ ] One proposed-PR draft item for all 52 PR IDs.
- [ ] Actual linked PRs #112/#117/#119/#121/#122/#123/#124 and DS #7/#8.
- [ ] Actual linked Learn #3 and Intelligence #14 dependency issues.
- [ ] Alan reconciliation checkpoint present and complete; normal dependencies/decisions remain.
- [ ] Every blocking decision and A0/A1/A2/B1/B2 gate present.
- [ ] Ownership, technical-decision responsibility, dependencies, local preparation, merge readiness, plan path, source/salvage and disposition populated.
- [ ] No duplicate titles/IDs and Project/document parity validator passes.
