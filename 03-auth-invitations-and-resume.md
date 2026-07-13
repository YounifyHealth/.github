# Work package 03 — Authentication, invitations, and resume

> Planning-only execution contract. The corrected work-package split remains proposed pending Alan's review. Local preparation and merge readiness are separate; the benched Project catalogue is not resynced. Project reference: [MVP Product Flow Reshape](https://github.com/orgs/NatalyxPlatform/projects/3).

| Plan | Value |
| --- | --- |
| Work package | WP03 |
| Plan file | `03-auth-invitations-and-resume.md` |
| Proposed PRs | P03-01, P03-02, P03-03, P03-04, P03-05 |
| Inspection snapshot | 2026-07-12 19:30 America/New_York |

## 1. Purpose and outcome

**Problem.** Current invitation code mixes low-risk onboarding links with case membership, and existing flows need explicit recipient binding, return-to safety, consent, expiry, revocation, duplicate-claim, and mismatch semantics.

**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.

**Completed outcome.** Separate workspace-claim and paid-case invitation lifecycles with safe authentication/resume behavior and no link-possession path to sensitive case access.

**Explicit non-goals.**

- No automatic paid-case membership
- No email deliverability product
- No commercial promotion
- No PHI enablement

## 2. Verified current-state evidence

Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.

| ID | Class | Repository / ref | File, construct or location | Finding |
| --- | --- | --- | --- | --- |
| E-006 | verified | app / PR #122@e853821 | PR comment Review round 2 addressed and changed workflow/tests | Updated PR #122 reports 499 tests plus return_to, TTL, CAS, self-invite, lens and Learn fail-closed fixes; green checks were observed. These are salvage candidates, not blanket merge approval. |
| E-011 | verified | app / PR #124@84a5a84 | app/storage/node0.py:400-462; app/routes/node0.py:605-652 | Node 0 can issue an unaddressed GC invitation and redemption ultimately creates case membership, conflating low-risk onboarding possession with case access. |
| E-012 | verified | app / PR #122@e853821 | app/storage/invitations.py and PR review-round comment | The updated case invitation work adds 14-day ceiling, CAS transitions, mismatch confirmation, self-invite refusal, return_to preservation and paired lens tests; it has no Node 0 workspace target. |
| E-028 | verified review | app / PR #124 comment 4948149089 | Consolidated review — findings for the WP00 extraction ledger | Alan's completed review classifies #124 as high-value extraction material rather than a merge unit and identifies transaction, privacy, scoring, access, validation, invariant, exposure, retention, performance, CSS and CI findings. |
| E-029 | verified preserved branch | app / feat/byos-journey-wave-2@5b63e3a7 | exact three-commit stack on e853821 | Wave 2 contains phase-1 cluster pages, metadata-only request/review, case anchoring and role/owner fixes. Controlled local evidence passed 535 tests with 9 skipped and 36/36 focused tests, but no branch checks, PostgreSQL, browser/accessibility or visual run exists. |
| E-031 | verified | app / feat/byos-journey-wave-2@5b63e3a7 | case_members.py, case_documents.py, storage/documents.py, routes/agency.py | Membership roles still conflate participation, lens and access; document/reviewer loaders are broad or global; participant role/lens can be caller-supplied; operator actions lack a canonical organization-scoped staff capability; no RLS/non-owner runtime enforces denial. |

## 3. Architecture and contracts

- An email-less link may create a pending low-risk workspace claim only.
- Identity binds an authenticated principal to a person; participation records the person's domain relationship; access grants carry resource-scoped capabilities; authorization consumes all three plus ownership and purpose.
- Paid-case membership requires authenticated identity binding, recipient or issuer confirmation as appropriate, explicit consent, and auditable redemption.
- Return targets are internal allowlisted paths and survive login/signup/confirmation without becoming redirect authority.

| Contract area | Package rule |
| --- | --- |
| Ownership boundary | `app`, `infra`; repository-specific PRs remain separate. |
| Entities/state | `case_invitation`, `entry_session`, `workspace_claim` |
| Authorization | Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority. |
| API/service | Auth routes accept only allowlisted relative return targets. Issue, inspect, bind, consent, claim, revoke endpoints. Separate paid-case redeem/confirm flow. Client metadata carries opaque admission proof only. |
| Storage | Workspace claims and audit/idempotency fields. Case-invitation identity, consent, expiry, revocation, idempotency fields. Unique identity binding, participation and access-grant tables with lifecycle and scope constraints. |
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

### Low-risk workspace identity claim (`workspace_claim`)

Owner: **natalyx-app**. States: `issued`, `pending_identity`, `identity_bound`, `consented`, `claimed`, `mismatch_pending`, `revoked`, `expired`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | issued | workspace IP | selected candidate + allowed claim scope | claim:{workspace}:{candidate}:{generation} | Existing live claim superseded | workspace_claim_issued | Return current token only at issuance | Issue new generation; old revoked |
| issued | pending_identity | link holder | valid token landing | claim:{id}:land | Expired/revoked token | claim_opened | Safe repeat | Authenticate or exit; no data grant |
| pending_identity | identity_bound\|mismatch_pending | auth provider | verified subject/email and binding policy | claim:{id}:bind:{subject} | Already claimed/different subject | claim_identity_bound\|claim_mismatch | CAS no-op or mismatch state | Issuer review/new claim |
| identity_bound | consented | GC claimant | workspace consent version | claim:{id}:consent:{version} | Stale/missing consent | claim_consented | Idempotent | Display current consent |
| consented | claimed | claim service | authorized low-risk workspace membership transaction | claim:{id}:complete | Case membership requested or conflicting claimant | workspace_claimed | Return same membership | Transaction rollback/forward repair |
| issued\|pending_identity\|identity_bound\|consented\|mismatch_pending | revoked\|expired | issuer/system | revocation or TTL | claim:{id}:terminal:{event} | No terminal overwrite | claim_revoked\|claim_expired | Idempotent | Fresh claim only |

### Paid-case membership invitation (`case_invitation`)

Owner: **natalyx-app**. States: `issued`, `pending_identity`, `identity_bound`, `mismatch_pending`, `issuer_confirmed`, `consented`, `redeemed`, `declined`, `revoked`, `expired`, `superseded`.

| From | To | Actor | Evidence | Idempotency key | Invalid transitions | Audit event | Retry | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | issued | authorized IP case member | enrollment_pending/active case + recipient binding | case-invite:{case}:{role}:{generation} | Self/member/active-GC/unauthorized | case_invite_issued | Return current; supersede prior live GC invite | Issue corrected invite |
| issued | pending_identity | recipient | valid addressed token landing | case-invite:{id}:land | Expired/revoked | case_invite_opened | Safe repeat | Authenticate with return_to |
| pending_identity | identity_bound\|mismatch_pending | auth provider | verified subject/email | case-invite:{id}:bind:{subject} | Terminal/duplicate/different subject | case_invite_bound\|mismatch | CAS protects terminal | Issuer confirmation or corrected invite |
| mismatch_pending | issuer_confirmed | authorized issuer | explicit reviewed mismatch confirmation | case-invite:{id}:confirm:{issuer} | Issuer unauthorized/recipient changed | case_invite_mismatch_confirmed | CAS no-op | Revoke and reissue |
| identity_bound\|issuer_confirmed | consented | invitee | paid-case role/privacy consent version | case-invite:{id}:consent:{version} | Stale/missing consent | case_invite_consented | Idempotent | Present current consent |
| consented | redeemed | invitation service | single transaction creates person/party/membership | case-invite:{id}:redeem | Existing member/active GC/expired/revoked | case_invite_redeemed | Return same membership | Rollback entire transaction; forward repair from invite |
| issued\|pending_identity\|identity_bound\|mismatch_pending\|issuer_confirmed\|consented | declined\|revoked\|expired\|superseded | invitee/issuer/system | explicit decline/revoke/TTL/new generation | case-invite:{id}:terminal:{event} | No terminal overwrite | case_invite_terminal | Idempotent CAS | Fresh invitation only |

### Invitation and identity safety

Retain from updated PR #122:

- hashed tokens
- purpose-specific TTL with a 14-day ceiling
- CAS terminal transitions
- atomic membership creation
- one-live-GC constraint
- self/existing-member refusal
- safe return_to
- portable integrity/concurrency tests

Required replacement contract:

- Exactly one target: workspace_id or case_id; include purpose, role, access_class, recipient_binding_mode and policy version.
- Email-less possession may only open pending low-risk workspace claim; it cannot reveal sensitive data or grant paid-case membership.
- Paid-case invitation is addressed, authenticated, consented and atomically redeems invitation plus participation, access grant and audit; mismatch requires explicit policy/issuer handling and preferably a fresh bound token.
- Workspace-claim issuance commits supersession, hashed claim, candidate/workspace linkage and required audit atomically; external identity steps use an explicit idempotent completion state.
- Cognito admission and app membership are separate decisions; account creation never equals workspace/case access.
- Verified identity comes from auth claims, not form-entered email; duplicate claims return the original result.
- Never put raw token/email/PHI in general participant timeline payloads; revoke/expire/supersede fail closed.
- Remove generic unconditional status mutation; expose authorized transition commands only.

## 4. Explicit PR sequence

| Order | ID | Title | Repository | Dependencies | Gate | Local preparation | Merge readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P03-01 | Harden auth return-to and participant resume | app | P01-01 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P01-01; Gate A0 active and verified; Luke review/final founder approval |
| 2 | P03-02 | Add low-risk workspace claim lifecycle | app | P03-01, P03-05, P04-01 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P03-01, P03-05, P04-01; Gate A0 active and verified; Luke review/final founder approval |
| 3 | P03-03 | Bind paid-case invitations to identity and consent | app | P03-01, P03-05 | A2 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P03-01, P03-05; Gate A0 active and verified; Luke review/final founder approval |
| 4 | P03-04 | Replace shared signup admission with claim-aware Cognito admission | infra | P03-02, P03-03 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P03-02, P03-03; technical decisions/controls D-AUTH-02; Gate A0 active and verified; Luke review/final founder approval |
| 5 | P03-05 | Implement canonical identity, participation, access, and authorization contracts | app | P02-03, P03-01 | A1 | Not ready; named PR, decision or programme-acceptance prerequisites remain | Blocked pending PR dependencies P02-03, P03-01; Gate A0 active and verified; Luke review/final founder approval |

### P03-01 — Harden auth return-to and participant resume

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-01](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-01) |
| Gate / size | A1 / Medium |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P01-01; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
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
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Cognito, web session security, FastAPI |
| Higher-capability review | Risk-proportionate; not mandatory by programme default |

### P03-02 — Add low-risk workspace claim lifecycle

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-02](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-02) |
| Gate / size | A1 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P03-01, P03-05, P04-01; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P03-01, P03-05, P04-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
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

Hard dependencies: P03-01, P03-05, P04-01. Parallel opportunities: P03-03

#### Objective acceptance criteria

- [ ] Create a pending Node 0 workspace claim that can start from an unaddressed link but requires identity binding, consent, expiry, revocation, and audit before low-risk access.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

### P03-03 — Bind paid-case invitations to identity and consent

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-03](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-03) |
| Gate / size | A2 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P03-01, P03-05; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P03-01, P03-05 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
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

Hard dependencies: P03-01, P03-05. Parallel opportunities: P03-02

#### Objective acceptance criteria

- [ ] Implement a separate recipient-bound paid-case invitation that grants membership only after authenticated binding, required confirmation, consent, and case/role checks.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Python/FastAPI, PostgreSQL, security-aware product engineering |
| Higher-capability review | Mandatory before merge |

### P03-04 — Replace shared signup admission with claim-aware Cognito admission

| Field | Plan |
| --- | --- |
| Repository / base | `infra` (`main`) |
| Project item | [P03-04](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-04) |
| Gate / size | A1 / Large |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P03-02, P03-03; technical decisions/controls D-AUTH-02; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | D-AUTH-02: Alan - later identity/admission mechanism |
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

Hard dependencies: P03-02, P03-03. Parallel opportunities: P03-01, P03-05

#### Objective acceptance criteria

- [ ] Keep internal/dev allowlisting but add a short-lived, recipient-bound admission proof for approved workspace/case claimants so a shared invite code is never the participant trust boundary.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | D-AUTH-02: Alan - later identity/admission mechanism |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | Cognito, AWS Lambda/KMS, identity security |
| Higher-capability review | Mandatory before merge |

### P03-05 — Implement canonical identity, participation, access, and authorization contracts

| Field | Plan |
| --- | --- |
| Repository / base | `app` (`main`) |
| Project item | [P03-05](https://github.com/orgs/NatalyxPlatform/projects/3?query=P03-05) |
| Gate / size | A1 / Exceptional |
| Local preparation status | Not ready; named PR, decision or programme-acceptance prerequisites remain |
| Merge readiness | Blocked pending PR dependencies P02-03, P03-01; Gate A0 active and verified; Luke review/final founder approval |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Dependencies | P02-03, P03-01 |
| Blocking decisions/checkpoints | None beyond dependencies and plan approval |
| Source / salvage | Alan consolidated #124 review, corrected #122 role/lens behavior, Wave 2 person/case-side ownership tests |

#### Objective

Encode the reconciled separation between authenticated identity, domain participation, resource access grants, operation policy and ownership before workspace/case schemas consume role semantics.

#### Scope

- Subject-to-person identity binding
- Separate workspace/case participation lifecycle
- Explicit resource/capability access grants
- Operation policy consumed by application services and RLS
- Person/case-side/case ownership independent of visibility

#### Explicit non-goals

- No global role grants participant data access
- No lens or participation label as standalone authorization
- No Cognito group as case authority

#### Expected files or modules

- `docs/adr/ADR-00x-participation-access.md`
- `migrations/versions/*_participation_access.py`
- `app/authz/context.py`
- `app/storage/access_grants.py`
- `tests/security/test_participation_access.py`

#### Change map

| Area | Planned change |
| --- | --- |
| Schema/model | Unique identity binding, participation and access-grant tables with lifecycle and scope constraints. |
| API/routes | No public API/route contract change. |
| UI/product surface | No visible participant/operator UI change. |
| Infrastructure/workflow | No cloud/infrastructure resource or workflow change. |
| Migration/backfill | Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope. |
| Security/privacy | Every protected command derives context from the authenticated principal rather than caller-supplied role/lens. |
| Architecture/docs/config | Identity, participation, access, authorization and ownership become separate contracts. |

#### Tests and validation

Objective tests:

- Duplicate identity/participation is unrepresentable
- Participation without grant denies
- Grant without operation capability denies
- ownership and cross-org negative matrix
- application/RLS policy parity

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

Hard dependencies: P02-03, P03-01. Parallel opportunities: P03-04

#### Objective acceptance criteria

- [ ] Encode the reconciled separation between authenticated identity, domain participation, resource access grants, operation policy and ownership before workspace/case schemas consume role semantics.
- [ ] Every listed objective test passes locally and at the required gate where applicable.
- [ ] Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.
- [ ] The planning record has matching dependency, local-preparation, merge-readiness, ownership, gate and disposition fields.
- [ ] Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.

#### Ownership and review

| Role | Recommendation |
| --- | --- |
| Work-package DRI | Alan |
| Primary implementer | Alan (proposed; pending Alan review) |
| Technical-decision owner | None; implement the settled founder constraints and approved contracts |
| Reviewer | Luke |
| Final approver | Luke |
| PR-level ownership exception | None |
| Required expertise | domain modelling, authorization, PostgreSQL RLS, identity security |
| Higher-capability review | Mandatory before merge |

## 5. Cross-repository coordination

| Repository | Authority after merge |
| --- | --- |
| `app` | routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain |
| `infra` | AWS resources, IAM/KMS/network/deployment/backup/audit contracts |

Merge order inside this package: `P03-01` → `P03-05` → `P03-03` → `P03-02` → `P03-04`.

Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.

Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.

## 6. Test and acceptance matrix

| Test dimension | Method | Objective result |
| --- | --- | --- |
| Happy path | Logged-out resume; Token replay/expiry/revocation; Duplicate and concurrent claims; Identity mismatch; Workspace-to-case access escalation | Expected state/event/UI and named evidence are produced once. |
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
| D-AUTH-01 | Resolved by reconciliation | Reconciliation settled | Alan - implementation | P03-02, P03-03; Resolved 2026-07-12 | No longer blocks P03-02 or P03-03. |
| D-AUTH-02 | Founder constraints final; Alan later | Alan decides later within founder constraints | Alan - later at P03-04 | P03-04; Before P03-04 | P03-04 and Gate A1 remain blocked until the technical mechanism and evidence exist. |
| D-AUTH-03 | Resolved by reconciliation | Reconciliation settled | Alan - implementation | P03-02, P03-03, P03-05, P04-01, P04-02, P09-04, P13-05; Resolved 2026-07-12 | No longer blocks the reconciled access/workspace PR sequence. |

### D-AUTH-01 - Workspace claim and paid-case identity policy

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final |
| Founder outcome | A bearer link creates only a pending low-risk workspace claim; paid-case access requires authenticated binding, explicit consent and recipient/issuer confirmation. |
| Founder constraints | Minimum-necessary relationship, outreach and logistics context only; No bearer-link case membership |
| What remains for Alan | Implement the settled claim and paid-case invitation contracts |
| Evidence required | Forwarded-link, expiry, mismatch, consent and membership negative tests |
| Approval rule | No further founder decision unless access is broadened. |
| External dependencies | None |
| Affected PRs / latest point | P03-02, P03-03; Resolved 2026-07-12 |
| Programme effect | No longer blocks P03-02 or P03-03. |
| Independent recommendation | A bearer link creates only a pending free-workspace claim with minimum-necessary relationship/outreach/logistics context; paid-case access always requires authenticated binding, explicit consent and recipient/issuer confirmation. |

### D-AUTH-02 - Claim-aware Cognito admission mechanism

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final founder constraints |
| Founder outcome | Participant admission uses short-lived signed or server-verified proof bound to email, purpose, claim and expiry; it admits account creation only and never grants workspace or case membership. Internal admission remains a separate allowlist path. |
| Founder constraints | Short lived; Replay, mismatch, expiry and revocation fail closed; No membership or resource authorization from admission alone |
| What remains for Alan | Choose the proof format, signer/verifier, key lifecycle and claim lifecycle |
| Evidence required | Expiry, replay, wrong-email, wrong-purpose, mismatch and revocation tests; Separate internal allowlist evidence |
| Approval rule | Luke approval is not required unless Alan proposes broader access or materially weaker identity assurance. |
| External dependencies | None |
| Affected PRs / latest point | P03-04; Before P03-04 |
| Programme effect | P03-04 and Gate A1 remain blocked until the technical mechanism and evidence exist. |
| Independent recommendation | Bind proof to email, purpose, claim ID and expiry; it admits account creation only and never grants workspace/case membership. |

### D-AUTH-03 - Identity, participation and access authorization contract

| Field | Recorded decision or requirement |
| --- | --- |
| Decision state | Final |
| Founder outcome | Identity, participation, access grants, ownership and operation authorization remain separate; participation or lens alone never authorizes. |
| Founder constraints | Subject-derived authorization context; Application and RLS policy parity; Default-deny cross-resource access |
| What remains for Alan | Encode the settled contract in application services and RLS |
| Evidence required | Participation-without-grant and grant-without-capability denials; Application/RLS parity tests |
| Approval rule | No further founder decision unless the boundary changes. |
| External dependencies | None |
| Affected PRs / latest point | P03-02, P03-03, P03-05, P04-01, P04-02, P09-04, P13-05; Resolved 2026-07-12 |
| Programme effect | No longer blocks the reconciled access/workspace PR sequence. |
| Independent recommendation | Identity binds principal to person; participation records domain relationship; grants carry resource-scoped capabilities; application and RLS consume a subject-derived context plus ownership and purpose. Participation/lens alone never authorizes. |

| Implementation risk | Owner | Treatment |
| --- | --- | --- |
| Shared links forwarded | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Account mismatch | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Confused-deputy redirects | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |
| Workspace data exposed during upgrade | Alan | Mitigate through explicit tests, rollout and forward-repair evidence before the associated gate. |

## 8. Existing-work salvage

| Source | Head | Valuable content | Destination | Recommendation | Extraction status/safety |
| --- | --- | --- | --- | --- | --- |
| app#122 | e85382150853 | Case projection/lens surfaces, safe return_to, invitation TTL/CAS/self-member/one-GC constraints, transactional membership, fail-closed Learn, SQL-limited timeline, responsive/a11y tests and Python CI workflow. | P03-01, P03-03, P03-05 | Selective-port behavior and tests; supersede as programme architecture | Complete at e853821: authoritative behavior/tests and selectively portable implementation are classified; superseded architecture and evidence-only claims are named. |
| app#123 | 34078f810b63 | GC onboarding form/copy, hosted auth return, invite handoff and role-specific surface work. | P03-01, P03-02 | Selective UX/test port and rewrite | Unextracted; likely partially copied into #124 but not proven complete. |
| app#124 | 84a5a847fea7 | Consolidated Node 0 questionnaire/guide/surfaces, GC onboarding, participant case shell, invitation delegation, DS assets and large focused test suites as extraction evidence. | P03-02, P03-03 | Fully supersede as a merge unit; preserve selective concepts, copy, assets and tests as evidence | Complete at 84a5a84: all consolidated-review findings are dispositioned and assigned; no mergeable/cherry-pick unit is approved. |
| feat/byos-journey-wave-2 | 5b63e3a7c364 | Projection-driven phase-1 cluster presentation, exact route allowlisting, person-versus-case-side ownership intent, transactional submission/work-item and review/audit patterns, fail-closed item retention, approved Learn status selection and 36 focused tests. | P03-01, P03-03, P03-05 | Preserve paused at the exact head; selectively port semantics/tests only after adaptation. Do not merge, cherry-pick, continue implementation or use its runtime schema directly. | Paused exact-head evidence; no direct merge |
| feature/node0-surrogate-onboarding-link | 529d377 | substantial uncommitted onboarding/invitation work | P03-02/P03-03/P06-02 | Selective port from protected worktree | Preserve until file/test extraction is signed off. |

Package source inventory:

- PR #122 return_to, CAS, TTL, self-invite and mismatch fixes
- PRs #123/#124 hosted GC onboarding UX
- Dirty onboarding-link worktree

## 9. Ownership recommendation

Alan proposes implementation and threat-model details; Luke approves role/privacy policy. The reconciliation checkpoint is complete; replacement work still waits for package acceptance and its own dependencies/decisions.

| PR | WP DRI | Primary implementer | Technical-decision owner | Reviewer | Final approver | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| P03-01 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |
| P03-02 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |
| P03-03 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |
| P03-04 | Alan | Alan (proposed) | D-AUTH-02: Alan - later identity/admission mechanism | Luke | Luke | None |
| P03-05 | Alan | Alan (proposed) | None; implement the settled founder constraints and approved contracts | Luke | Luke | None |

PR ownership inherits the proposed work-package split pending Alan's review. Named technical-decision ownership remains separate and never transfers implementation ownership across work packages; reciprocal and external review requirements remain intact.

## 10. Definition of done

- [ ] Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.
- [ ] All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.
- [ ] Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.
- [ ] Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.
- [ ] Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.
- [ ] Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.
- [ ] The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.
