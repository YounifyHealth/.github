#!/usr/bin/env python3
"""Render the planning package from programme_data.py.

This is a mechanical renderer: product/architecture decisions live in the
canonical data module and every Markdown view is regenerated together.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from programme_data import (  # noqa: E402
    AUTHORSHIP_CLASSES,
    AUTHORSHIP_CONTRACT,
    AUTHORSHIP_MATRIX,
    CLEANUP_TASKS,
    COMMERCIAL_LEDGER_CONTRACT,
    CRITICAL_JOINS,
    CRITICAL_PATH,
    DECISIONS,
    DESIGN_SYSTEM_RELEASE_POLICY,
    DOCUMENT_CONTRACT,
    EARLY_PARALLEL_SEQUENCE,
    EVIDENCE,
    EXISTING_PRS,
    FIRST_THREE_IMPLEMENTATION_PRS,
    GATES,
    INSPECTED_AT,
    INVITATION_CONTRACT,
    MIGRATION_DECISION_CONTRACT,
    PARALLEL_LANES,
    PLAN_BRANCH,
    PLAN_ROOT,
    PROJECT_CONVENTIONS,
    PROJECT_FIELDS,
    PROJECT_SYNC_RESULT,
    PROJECT_URL,
    PROMOTION_EVENT,
    PROPOSED_PRS,
    PROTECTED_WORKTREES,
    RECONCILIATION_CHECKPOINT,
    RELATED_ISSUES,
    RELEASE_STRATEGY,
    REVIEW_MODEL,
    RISK_REGISTER,
    STATE_MACHINES,
    TRANSITION_ENVELOPE,
    TRANSITION_RULES,
    WORK_PACKAGE_OWNERSHIP,
    WORK_PACKAGES,
    WP_BY_ID,
    plan_filename,
)


PYTHON = "/Users/lukerhodes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"


def esc(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", "<br>")


def md_table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(esc(cell) for cell in row) + " |")
    return "\n".join(output)


def bullets(items: Iterable[Any], *, checked: bool = False) -> str:
    prefix = "- [ ] " if checked else "- "
    values = [str(item) for item in items]
    return "\n".join(prefix + item for item in values) if values else "- None."


def numbered(items: Iterable[Any]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))


def anchor(text: str) -> str:
    value = re.sub(r"[^a-z0-9 -]", "", text.lower())
    return re.sub(r"[ -]+", "-", value).strip("-")


def prs_for(wp_id: str) -> list[dict[str, Any]]:
    return [pr for pr in PROPOSED_PRS if pr["wp"] == wp_id]


def decisions_for(wp_id: str) -> list[dict[str, Any]]:
    ids = {pr["id"] for pr in prs_for(wp_id)}
    return [decision for decision in DECISIONS if ids.intersection(decision["affected"])]


def evidence_for(wp_id: str) -> list[dict[str, Any]]:
    return [item for item in EVIDENCE if wp_id in item["wps"]]


def machines_for(wp_id: str) -> list[dict[str, Any]]:
    return [machine for machine in STATE_MACHINES if wp_id in machine["wps"]]


def topological_prs() -> list[dict[str, Any]]:
    ids = {pr["id"] for pr in PROPOSED_PRS}
    indegree = {pr_id: 0 for pr_id in ids}
    outgoing: dict[str, set[str]] = {pr_id: set() for pr_id in ids}
    for pr in PROPOSED_PRS:
        for dep in pr["deps"]:
            if dep in ids:
                outgoing[dep].add(pr["id"])
                indegree[pr["id"]] += 1
    queue = deque(sorted((pr_id for pr_id, degree in indegree.items() if degree == 0)))
    ordered: list[str] = []
    while queue:
        current = queue.popleft()
        ordered.append(current)
        for nxt in sorted(outgoing[current]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if len(ordered) != len(ids):
        cyclic = sorted(pr_id for pr_id, degree in indegree.items() if degree)
        raise RuntimeError(f"Circular PR dependency: {cyclic}")
    by_id = {pr["id"]: pr for pr in PROPOSED_PRS}
    return [by_id[pr_id] for pr_id in ordered]


def local_commands(repo: str) -> list[str]:
    return {
        "app": ["python -m unittest discover -s tests/python", "Run the focused test module(s) named above against SQLite and PostgreSQL where applicable."],
        "intelligence": ["uv run pytest", "Run focused contract/migration/safety tests with redacted fixtures."],
        "learn": ["uv run pytest", "Run the builder/validator against approved fixture sources and compare deterministic checksums."],
        "infra": ["npm test", "npm run build", "Synthesize the affected CDK stack with billable/live changes disabled."],
        "design-system": ["npm test", "Run recipe escaping, accessibility and responsive fixture checks."],
        ".github": ["git diff --check", f"{PYTHON} scripts/validate_programme.py"],
    }.get(repo, ["Run the repository's focused and full validation suites."])


def rollout_text(pr: dict[str, Any]) -> str:
    if pr["repo"] == ".github":
        return "Merge only after document/sign-off checks; it changes no runtime. Re-sync the Project from the same canonical data."
    if pr["repo"] == "infra":
        return "Synthesize and review first; deploy only through the guarded dev workflow with billable/desired-count defaults unchanged, exact revision recorded, and explicit confirmation outside this planning task."
    if "schema" in pr["changes"] or "migration" in pr["changes"]:
        return "Ship expand-only and dark by default; run the one-off migrator, verify readiness/old-revision compatibility, then enable writers/readers in a later compatible step."
    if pr["repo"] in {"learn", "design-system", "intelligence"}:
        return "Release a versioned/pinned artifact or API contract first; consumers opt in explicitly and retain fail-closed/previous-version behavior during the compatibility window."
    return "Deploy behind the narrowest practical feature/config gate, verify the named synthetic flow and diagnostics on a known revision, then widen only at the associated programme gate."


def repair_text(pr: dict[str, Any]) -> str:
    if pr["repo"] == ".github":
        return "Correct the canonical data and regenerate; do not rewrite implementation history."
    if pr["repo"] == "infra":
        return "Return to the prior reviewed stack/task definition when compatible; otherwise keep resources fail-closed and forward-repair under the runbook. Never delete data-bearing resources as an automatic rollback."
    if "schema" in pr["changes"] or "migration" in pr["changes"]:
        return "Prefer application rollback within the expand/contract window and a new forward-repair migration. An irreversible schema reversal requires its own approval and backup evidence."
    return "Disable the feature or return to the prior compatible image; retain append-only audit/ledger history and repair with a new event/revision rather than destructive mutation."


def observability_text(pr: dict[str, Any]) -> str:
    explicit = pr["changes"].get("observability")
    if explicit:
        return explicit
    return "Emit correlation/idempotency/policy/version identifiers, transition/result counters and bounded failure reasons; never log tokens, processor payloads, raw documents, prompts, PHI or unnecessary PII."


def parallel_for(pr: dict[str, Any]) -> str:
    peers = []
    for other in prs_for(pr["wp"]):
        if other["id"] == pr["id"]:
            continue
        if other["id"] not in pr["deps"] and pr["id"] not in other["deps"]:
            peers.append(other["id"])
    return ", ".join(peers) if peers else "None inside this package beyond review/test preparation."


def default_change(area: str) -> str:
    return {
        "schema": "None in this PR; any later schema change stays in its named migration PR.",
        "api": "No public API/route contract change.",
        "ui": "No visible participant/operator UI change.",
        "infra": "No cloud/infrastructure resource or workflow change.",
        "migration": "No migration or backfill.",
        "security": "Preserve existing fail-closed boundaries; validate the PR-specific privacy/security cases.",
    }[area]


def render_pr(pr: dict[str, Any], level: int = 3) -> str:
    h = "#" * level
    sections: list[str] = [f"{h} {pr['id']} — {pr['title']}"]
    sections.append(md_table(
        ["Field", "Plan"],
        [
            ["Repository / base", f"`{pr['repo']}` (`{pr['base']}`)"],
            ["Project item", f"[{pr['id']}]({pr['project_item']})"],
            ["Gate / size / readiness", f"{pr['gate']} / {pr['size']} / {pr['readiness']}"],
            ["Dependencies", ", ".join(pr["deps"]) or "P00-01 plan sign-off only"],
            ["Blocking decisions/checkpoints", ", ".join(pr["blocked_by"]) or "None beyond dependencies and plan approval"],
            ["Source / salvage", ", ".join(pr["sources"]) or "None"],
        ],
    ))
    sections += [f"{h}# Objective", pr["objective"], f"{h}# Scope", bullets(pr["scope"]), f"{h}# Explicit non-goals", bullets(pr["non_goals"])]
    sections += [f"{h}# Expected files or modules", bullets(f"`{item}`" for item in pr["files"])]
    changes = pr["changes"]
    sections += [
        f"{h}# Change map",
        md_table(
            ["Area", "Planned change"],
            [
                ["Schema/model", changes.get("schema", default_change("schema"))],
                ["API/routes", changes.get("api", default_change("api"))],
                ["UI/product surface", changes.get("ui", default_change("ui"))],
                ["Infrastructure/workflow", changes.get("infra", changes.get("workflow", default_change("infra")))],
                ["Migration/backfill", changes.get("migration", "Apply through the named versioned migration; no ad-hoc startup DDL. Backfill is none unless explicitly listed in scope." if any("migrations/" in item for item in pr["files"]) else default_change("migration"))],
                ["Security/privacy", changes.get("security", default_change("security"))],
                ["Architecture/docs/config", changes.get("architecture", changes.get("documentation", "Document the contract, version pins and safe partial-merge behavior."))],
            ],
        ),
        f"{h}# Tests and validation",
        "Objective tests:\n\n" + bullets(pr["tests"]),
        "Local validation:\n\n" + bullets(f"`{cmd}`" if " " in cmd and not cmd.startswith("Run") else cmd for cmd in local_commands(pr["repo"])),
        f"Cloud validation: run only through Gate **{pr['gate']}** on a known revision, using synthetic data until B1 and no PHI until B2. A merge or green deployment is not gate acceptance.",
        f"{h}# Diagnostics and observability",
        observability_text(pr),
        f"{h}# Rollout",
        rollout_text(pr),
        f"{h}# Rollback or forward repair",
        repair_text(pr),
        f"{h}# Dependencies and parallel work",
        f"Hard dependencies: {', '.join(pr['deps']) or 'approved programme baseline'}. Parallel opportunities: {parallel_for(pr)}",
        f"{h}# Objective acceptance criteria",
        bullets([
            pr["objective"],
            "Every listed objective test passes locally and at the required gate where applicable.",
            "Every explicit non-goal remains out of the diff and no protected worktree/branch is modified during extraction.",
            "The Project item has matching dependency, readiness, ownership, gate and disposition fields.",
            "Rollout/repair evidence is attached before merge; unresolved decisions remain blocked rather than encoded as guesses.",
        ], checked=True),
        f"{h}# Ownership and review",
        md_table(
            ["Role", "Recommendation"],
            [
                ["DRI", pr["dri"]], ["Implementer", f"{pr['implementer']} (proposed; pending consolidated-plan sign-off)"],
                ["Reviewer", pr["reviewer"]], ["Final approver", pr["approver"]],
                ["Required expertise", ", ".join(pr["expertise"])],
                ["Higher-capability review", "Mandatory before merge" if pr["high_review"] else "Risk-proportionate; not mandatory by programme default"],
            ],
        ),
    ]
    return "\n\n".join(sections)


def render_machine(machine: dict[str, Any], level: int = 3) -> str:
    h = "#" * level
    rows = []
    for item in machine["transitions"]:
        rows.append([item["start"], item["end"], item["actor"], item["evidence"], item["key"], item["invalid"], item["audit"], item["retry"], item["recovery"]])
    return "\n\n".join([
        f"{h} {machine['title']} (`{machine['entity']}`)",
        f"Owner: **{machine['owner']}**. States: " + ", ".join(f"`{state}`" for state in machine["states"]) + ".",
        md_table(["From", "To", "Actor", "Evidence", "Idempotency key", "Invalid transitions", "Audit event", "Retry", "Recovery"], rows),
    ])


def contract_summary(wp: dict[str, Any]) -> str:
    package_prs = prs_for(wp["id"])
    repos = sorted({pr["repo"] for pr in package_prs})
    machines = machines_for(wp["id"])
    entities = sorted({machine["entity"] for machine in machines})
    api_items = [pr["changes"].get("api") for pr in package_prs if pr["changes"].get("api")]
    storage_items = [pr["changes"].get("schema") or pr["changes"].get("migration") for pr in package_prs if pr["changes"].get("schema") or pr["changes"].get("migration")]
    return md_table(
        ["Contract area", "Package rule"],
        [
            ["Ownership boundary", ", ".join(f"`{repo}`" for repo in repos) + "; repository-specific PRs remain separate."],
            ["Entities/state", ", ".join(f"`{entity}`" for entity in entities) or "No new runtime entity; evidence/coordination only."],
            ["Authorization", "Authenticated subject/service plus entity membership, role, purpose, consent and expected revision; query parameters, links and UI state are never authority."],
            ["API/service", " ".join(api_items) or "No broad public contract; use the focused commands/events in each PR."],
            ["Storage", " ".join(storage_items) or "No new storage; preserve current state read-only for this package."],
            ["Audit", "Use the common transition envelope and append-only source/event identifiers; redact tokens, raw documents, prompts and sensitive payloads."],
            ["Failure", "Fail closed for authorization, provenance, money, document and PHI boundaries; expose a bounded actionable error and preserve retry/repair evidence."],
            ["Observability", "Correlation, policy/schema/config version, transition and dependency result metrics without PHI/PII payload logging."],
            ["Compatibility", "Additive/dual-compatible changes, explicit version pins, old/new revision window and named forward repair."],
            ["Privacy/PHI", "Synthetic only through A2; approved PII only at B1; PHI remains blocked until formal B2."],
        ],
    )


def package_coordination(wp: dict[str, Any]) -> str:
    package_prs = prs_for(wp["id"])
    repos = sorted({pr["repo"] for pr in package_prs})
    ordered = [pr["id"] for pr in topological_prs() if pr["wp"] == wp["id"]]
    boundaries = {
        "app": "routing, validation, authorization, participant/case/workflow truth, PHI policy and commercial domain",
        "infra": "AWS resources, IAM/KMS/network/deployment/backup/audit contracts",
        "intelligence": "advisory inference, scoped response/citation contract; no case truth",
        "learn": "authored Learn artifacts, provenance and release manifest",
        "design-system": "participant recipes/tokens/accessibility/interaction contract",
        ".github": "programme/governance evidence and Project control plane",
    }
    rows = [[f"`{repo}`", boundaries.get(repo, "Repository-local contract")] for repo in repos]
    return "\n\n".join([
        md_table(["Repository", "Authority after merge"], rows),
        "Merge order inside this package: " + " → ".join(f"`{item}`" for item in ordered) + ".",
        "Handoff rule: producer contract/version must merge and be pinned before its consumer enables the feature. During a partial merge, consumers fail closed or retain the last approved version; they do not fabricate data or silently broaden access.",
        "Compatibility window: keep prior readers/writers and rollback image usable through the named gate; contract/migration PRs document the exact removal point.",
    ])


def package_test_matrix(wp: dict[str, Any]) -> str:
    focus = "; ".join(wp["test_focus"])
    rows = [
        ["Happy path", focus, "Expected state/event/UI and named evidence are produced once."],
        ["Authorization failure", "Wrong/no subject, role, membership, purpose or consent", "403/404 as appropriate; no write or data leak; audit safe failure."],
        ["Role differences", "Separate IP, GC, operator, provider/service identities", "Only the approved lens/projection/actions appear."],
        ["Retries/duplicates", "Repeat same canonical request/event", "Original result returned; no duplicate membership/case/invoice/document/event."],
        ["Concurrency", "Two writers/claimants/migrators/workers", "One valid transition; loser receives deterministic stale/conflict response."],
        ["Stale state", "Old revision/config/terms/token/artifact", "Fail closed or approved compatibility behavior; never silent coercion."],
        ["Malformed input", "Boundary, encoding, size, enum, redirect and identifier corpus", "Validation before side effects; safe error."],
        ["Unavailable dependency", "Database, intelligence, processor, S3/scanner or auth unavailable", "Explicit degraded/blocked behavior; no hallucinated success."],
        ["Partial failure", "Crash between external effect, DB transaction and outbox", "Retry/forward repair converges from durable evidence."],
        ["Logout/login/resume", "Session expires/restarts mid-flow", "Return to authorized current state; no query/link authority."],
        ["Mobile/accessibility", "320/375/768 widths, keyboard, focus, reduced motion", "Core task completes with truthful state and no clipped controls."],
        ["Synthetic cloud", "Known dev revision and synthetic identities/data", "Gate artifact records SHA, dependency status, audit and cleanup."],
        ["Audit/observability", "Inspect events/metrics/logs", "Versions, actor/authority, correlation and reason present; no sensitive payload."],
    ]
    return md_table(["Test dimension", "Method", "Objective result"], rows)


def package_salvage(wp: dict[str, Any]) -> str:
    ids = {pr["id"] for pr in prs_for(wp["id"])}
    rows: list[list[str]] = []
    for item in EXISTING_PRS:
        destinations = set(item["destinations"])
        if ids.intersection(destinations):
            rows.append([item["key"], item["sha"][:12], item["useful"], ", ".join(sorted(ids.intersection(destinations))), item["disposition"], item["extraction"]])
    for worktree in PROTECTED_WORKTREES:
        if any(pr_id in worktree["destination"] for pr_id in ids):
            rows.append([worktree["branch"], worktree["head"], worktree["status"], worktree["destination"], "Selective port from protected worktree", worktree["rule"]])
    if not rows:
        rows.append(["No direct source", "—", "Build from approved contracts/evidence", "Package PRs", "New implementation", "N/A"])
    return md_table(["Source", "Head", "Valuable content", "Destination", "Recommendation", "Extraction status/safety"], rows)


def render_wp(wp: dict[str, Any], *, top_level: int = 1, include_title: bool = True) -> str:
    h1 = "#" * top_level
    h2 = "#" * (top_level + 1)
    title = f"Work package {wp['number']:02d} — {wp['title']}"
    package_prs = prs_for(wp["id"])
    content: list[str] = []
    if include_title:
        content.append(f"{h1} {title}")
    content.append(
        f"> Planning-only execution contract. Proposed implementers and owners remain recommendations until Alan reviews/signs off the consolidated plan and Luke accepts it. Project: [{PROJECT_CONVENTIONS['project']}]({PROJECT_URL})."
    )
    content.append(md_table(
        ["Plan", "Value"],
        [["Work package", wp["id"]], ["Plan file", f"`{plan_filename(wp['id'])}`"], ["Proposed PRs", ", ".join(pr["id"] for pr in package_prs)], ["Inspection snapshot", INSPECTED_AT]],
    ))
    content += [
        f"{h2} 1. Purpose and outcome",
        f"**Problem.** {wp['problem']}",
        f"**Why this package exists.** It creates a reviewable boundary so the programme can progress without mixing product, data, security, infrastructure and rollout concerns in one oversized change.",
        f"**Completed outcome.** {wp['outcome']}",
        "**Explicit non-goals.**\n\n" + bullets(wp["non_goals"]),
        f"{h2} 2. Verified current-state evidence",
        "Classification is explicit: **verified** is observed code/PR/live behavior; **verified limitation** records an evidence gap; **design authority** is an approved planning source; **design decision** is proposed future behavior. None is silently treated as another.",
        md_table(
            ["ID", "Class", "Repository / ref", "File, construct or location", "Finding"],
            [[item["id"], item["kind"], f"{item['repo']} / {item['ref']}", item["location"], item["claim"]] for item in evidence_for(wp["id"])],
        ),
        f"{h2} 3. Architecture and contracts",
        bullets(wp["architecture"]),
        contract_summary(wp),
    ]
    if machines_for(wp["id"]):
        content.append(f"{h2}# Applicable state machines")
        for machine in machines_for(wp["id"]):
            content.append(render_machine(machine, top_level + 2))
    if wp["id"] == "WP02":
        content += [f"{h2}# Migration ADR contract", "Options:\n\n" + numbered(MIGRATION_DECISION_CONTRACT["options"]), f"**Provisional recommendation.** {MIGRATION_DECISION_CONTRACT['provisional_recommendation']}", bullets(MIGRATION_DECISION_CONTRACT["requirements"])]
    if wp["id"] in {"WP03", "WP06"}:
        content += [f"{h2}# Invitation and identity safety", "Retain from updated PR #122:\n\n" + bullets(INVITATION_CONTRACT["retain_from_122"]), "Required replacement contract:\n\n" + bullets(INVITATION_CONTRACT["required_changes"])]
    if wp["id"] in {"WP04", "WP05", "WP06", "WP07", "WP09", "WP10"}:
        content += [f"{h2}# Data authorship/provenance rules", bullets(AUTHORSHIP_CONTRACT)]
    if wp["id"] == "WP07":
        content += [f"{h2}# Sole promotion-authorizing event", f"`event_type: {PROMOTION_EVENT['event_type']}`", f"Producer: {PROMOTION_EVENT['producer']}. Consumer: {PROMOTION_EVENT['consumer']}.", "Payload:\n\n```text\n" + "\n".join(PROMOTION_EVENT["payload"]) + "\n```", "Authorization conditions:\n\n" + bullets(PROMOTION_EVENT["conditions"]), "Unique constraints:\n\n" + bullets(PROMOTION_EVENT["constraints"]), PROMOTION_EVENT["browser_rule"]]
    if wp["id"] == "WP08":
        content += [f"{h2}# Append-only commercial contract", "Authoritative ledgers:\n\n" + bullets(f"`{item}`" for item in COMMERCIAL_LEDGER_CONTRACT["authoritative"]), "Derived projections:\n\n" + bullets(COMMERCIAL_LEDGER_CONTRACT["projections"]), "Rules:\n\n" + bullets(COMMERCIAL_LEDGER_CONTRACT["rules"])]
    if wp["id"] == "WP09":
        content += [f"{h2}# Durable document and S3 contract"]
        for key in ("storage", "upload", "download", "recovery"):
            content += [f"{h2}## {key.title()}", bullets(DOCUMENT_CONTRACT[key])]
    if wp["id"] == "WP11":
        content += [f"{h2}# Design-system release rubric", md_table(["Class", "Items"], [["Release-blocking", "; ".join(DESIGN_SYSTEM_RELEASE_POLICY["release_blocking"])], ["Desirable", "; ".join(DESIGN_SYSTEM_RELEASE_POLICY["desirable"])], ["Deferred", "; ".join(DESIGN_SYSTEM_RELEASE_POLICY["deferred"])] ]), DESIGN_SYSTEM_RELEASE_POLICY["rule"]]
    if wp["id"] == "WP13":
        content += [f"{h2}# Programme gate summary", render_gate_table(compact=False)]
    content.append(f"{h2} 4. Explicit PR sequence")
    content.append(md_table(["Order", "ID", "Title", "Repository", "Dependencies", "Gate", "Size", "Readiness"], [[i, pr["id"], pr["title"], pr["repo"], ", ".join(pr["deps"]) or "P00-01", pr["gate"], pr["size"], pr["readiness"]] for i, pr in enumerate(package_prs, 1)]))
    for pr in package_prs:
        content.append(render_pr(pr, top_level + 2))
    content += [
        f"{h2} 5. Cross-repository coordination",
        package_coordination(wp),
        f"{h2} 6. Test and acceptance matrix",
        package_test_matrix(wp),
        f"{h2} 7. Risks and decisions",
        md_table(
            ["Type", "ID / risk", "Owner", "Affected PRs / latest point", "Project item / treatment"],
            [["Blocking/product/compliance decision", decision["id"] + " — " + decision["question"], decision["owner"], ", ".join(decision["affected"]) + "; " + decision["latest"], f"[{decision['id']}]({PROJECT_URL}?query={decision['id']}) — {decision['recommendation']}"] for decision in decisions_for(wp["id"])]
            + [["Implementation risk", risk, "Alan or named PR DRI", "Package PRs; before associated gate", "Mitigate through the explicit tests, rollout and forward-repair plan"] for risk in wp["risks"]],
        ),
        f"{h2} 8. Existing-work salvage",
        package_salvage(wp),
        "Package source inventory:\n\n" + bullets(wp["salvage"]),
        f"{h2} 9. Ownership recommendation",
        wp["coordination"],
        md_table(["PR", "DRI", "Implementer", "Reviewer", "Final approver", "External/high-capability review"], [[pr["id"], pr["dri"], pr["implementer"] + " (proposed)", pr["reviewer"], pr["approver"], "Mandatory" if pr["high_review"] else "As risk warrants"] for pr in package_prs]),
        "Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment.",
        f"{h2} 10. Definition of done",
        bullets([
            "Every proposed PR is merged in dependency order or explicitly dispositioned, with its objective acceptance criteria and Project item complete.",
            "All package blocking decisions are resolved by the named owner; no commercial/privacy/security value is guessed in code.",
            "Local, PostgreSQL, role/authorization, retry/concurrency, failure, mobile and synthetic-cloud evidence required by this package is attached.",
            "Cross-repository contracts and artifact/migration versions are pinned; partial-merge behavior is fail-closed or explicitly degraded.",
            "Observability is sufficient to identify revision, transition, dependency and safe failure without sensitive payloads.",
            "Existing PR/worktree value and reviewer findings are extracted before closure; no cleanup occurs without team confirmation.",
            "The associated programme gate is accepted by Luke and any required external reviewer; tests/deploy alone do not establish B1/B2.",
        ], checked=True),
    ]
    return "\n\n".join(content) + "\n"


def render_gate_table(*, compact: bool) -> str:
    if compact:
        return md_table(["Gate", "Owner / verifier", "Prerequisites", "Evidence"], [[gate["id"], f"{gate['owner']} / {gate['verifier']}", ", ".join(gate["prerequisites"]), "; ".join(gate["evidence"])] for gate in GATES])
    parts = []
    for gate in GATES:
        parts += [
            f"### Gate {gate['id']} — {gate['title']}",
            md_table(["Field", "Contract"], [["Prerequisite PRs/gates", ", ".join(gate["prerequisites"])], ["Prerequisite decisions", ", ".join(gate["decisions"])], ["Responsible owner", gate["owner"]], ["Verifier", gate["verifier"]]]),
            "Acceptance matrix:\n\n" + bullets(gate["acceptance"], checked=True),
            "Required evidence:\n\n" + bullets(gate["evidence"]),
            f"**Failure and rollback response.** {gate['failure']}",
        ]
    return "\n\n".join(parts)


def global_pr_table() -> str:
    rows = []
    for pr in topological_prs():
        wp = WP_BY_ID[pr["wp"]]
        rows.append([
            pr["id"], pr["title"], pr["repo"], f"{pr['wp']} / {wp['title']}", pr["dri"], pr["implementer"], pr["reviewer"], pr["approver"],
            ", ".join(pr["deps"]) or "P00-01 plan sign-off", pr["gate"], pr["size"], pr["readiness"], ", ".join(pr["blocked_by"]) or "None", ", ".join(pr["sources"]) or "None", f"[{pr['id']}]({pr['project_item']})",
        ])
    return md_table(["ID", "Title", "Repository", "Work package", "DRI", "Implementer", "Reviewer", "Final approver", "Dependencies", "Gate", "Size", "Readiness", "Blocking decision", "Replacement/source PR", "Project item"], rows)


def dependency_mermaid() -> str:
    labels = {wp["id"]: f"{wp['id']} {wp['title']}" for wp in WORK_PACKAGES}
    edges = [
        ("WP00", "WP01"), ("WP00", "WP11"), ("WP01", "WP02"), ("WP01", "WP13"),
        ("WP02", "WP03"), ("WP02", "WP04"), ("WP03", "WP05"), ("WP04", "WP05"),
        ("WP04", "WP06"), ("WP04", "WP07"), ("WP05", "WP06"), ("WP07", "WP08"),
        ("WP06", "WP07"), ("WP07", "WP09"), ("WP08", "WP09"), ("WP04", "WP10"),
        ("WP11", "WP10"), ("WP10", "WP12"), ("WP11", "WP12"), ("WP09", "WP12"),
        ("WP03", "WP13"), ("WP05", "WP13"), ("WP08", "WP13"), ("WP09", "WP13"), ("WP12", "WP13"),
    ]
    lines = ["flowchart TD"]
    used = set()
    for left, right in edges:
        if left not in used:
            lines.append(f'  {left}["{labels[left]}"] --> {right}["{labels[right]}"]')
            used.update({left, right})
        else:
            lines.append(f"  {left} --> {right}")
    return "```mermaid\n" + "\n".join(lines) + "\n```"


def render_extraction_ledger() -> str:
    parts = [
        "# Existing PR extraction ledger",
        "> Read-only reconciliation record. No PR, branch or worktree may be closed, retargeted, rebased, cleaned or deleted from this ledger alone.",
        f"Inspection snapshot: **{INSPECTED_AT}**.",
        "## Preservation and extraction sequence",
        numbered([
            "Preserve dirty worktrees and identify active branches/PRs.", "Reinspect latest heads.", "Complete this extraction ledger.",
            "Reconcile Alan's findings.", "Approve replacement architecture/PR boundaries.", "Create/ready Project draft items.",
            "Open replacement drafts only when implementation starts.", "Extract/port/rewrite value.", "Close superseded PRs only after accounting.",
            "Delete branches/worktrees only after closure and team confirmation.",
        ]),
        "## Summary",
        md_table(["PR", "Latest head", "Useful capability", "Destination", "Status", "Disposition"], [[item["key"], item["sha"], item["useful"], ", ".join(item["destinations"]), item["extraction"], item["disposition"]] for item in EXISTING_PRS]),
        "## Detailed PR records",
    ]
    for item in EXISTING_PRS:
        parts += [
            f"### {item['key']} — {item['title']}",
            md_table(["Field", "Finding"], [
                ["URL", item["url"]], ["Latest inspected head", item["sha"]], ["Inspection time", item["inspected"]],
                ["Useful capability", item["useful"]], ["Reusable commits/files", item["reusable"]], ["Tests worth preserving", item["tests"]],
                ["Obsolete/unsafe assumptions", item["unsafe"]], ["Replacement destination", ", ".join(item["destinations"])],
                ["Extraction status", item["extraction"]], ["Outstanding reviewer input", item["review"]], ["Recommended disposition", item["disposition"]],
                ["Exact close condition", item["close_when"]], ["Exact branch/worktree delete condition", item["delete_when"]],
            ]),
        ]
    pr122 = next(item for item in EXISTING_PRS if item["number"] == 122 and item["repo"].endswith("natalyx-app"))
    parts += [
        "## Latest PR #122 reinspection",
        f"Latest inspected head: `{pr122['sha']}` at {pr122['inspected']}. The earlier reviewed workflow run/comment baseline was `8df63dd`; Alan's current head is `e853821`.",
        "Fixed or materially improved since the earlier snapshot:\n\n" + bullets([
            "Logged-out invite delivery/resume and validated internal return_to across login/signup/confirm/resend.",
            "Paired IP/GC lens semantics and render-time action labels.",
            "CAS redemption/expiry/mismatch transitions, self-invite refusal and one-live-GC constraints.",
            "14-day expiry ceiling, portable integrity handling and duplicate-live-invite forward migration.",
            "Blocking Python CI workflow, fail-closed Learn approval, bounded Learn timeout, SQL-limited timeline and safer cookie/dead-button behavior.",
        ]),
        "Remaining conflicts/gaps:\n\n" + bullets([
            "No distinct Node 0 workspace or workspace claim target; it cannot be stacked unchanged with #124.",
            "No commercial commitment/funding/promotion or separate entitlement/payment/document lifecycle.",
            "Generic fact/proposal/invitation rails still need explicit author/authority/evidence transition commands.",
            "The case projection is useful case-stage presentation, not a universal programme state machine.",
        ]),
        "Decomposition impact: retain more of #122's CI, invitation and case-surface tests/implementation, but do not collapse WP03/WP04/WP07/WP09. Workspace/case separation and Alan reconciliation remain blocking.",
        "## Alan reconciliation checkpoint",
        md_table(["Field", "Contract"], [["Name", RECONCILIATION_CHECKPOINT["title"]], ["Status", RECONCILIATION_CHECKPOINT["status"]], ["Blocks", ", ".join(RECONCILIATION_CHECKPOINT["blocks"])], ["May amend", ", ".join(RECONCILIATION_CHECKPOINT["may_amend"])], ["Avoid wasted review", RECONCILIATION_CHECKPOINT["efficiency"]]]),
        "Finding recording:\n\n" + bullets(RECONCILIATION_CHECKPOINT["recording"]),
        "Resolution rule:\n\n" + bullets(RECONCILIATION_CHECKPOINT["resolution"]),
        "Complete only when:\n\n" + bullets(RECONCILIATION_CHECKPOINT["complete_when"], checked=True),
        "## Protected local worktrees",
        md_table(["Repository", "Path", "Branch/head", "Protected content", "Destination", "Safety rule"], [[item["repo"], f"`{item['path']}`", f"{item['branch']} / {item['head']}", item["status"], item["destination"], item["rule"]] for item in PROTECTED_WORKTREES]),
        "## Cleanup tasks",
        md_table(["ID", "Task", "Dependencies", "Owner"], [[item["id"], item["title"], ", ".join(item["deps"]), item["owner"]] for item in CLEANUP_TASKS]),
    ]
    return "\n\n".join(parts) + "\n"


def render_pr_manifest() -> str:
    parts = [
        "# Proposed PR manifest",
        "> Planning-only. Every implementation PR remains a GitHub Project draft item until its plan, decisions and dependencies are ready and implementation actually begins.",
        f"Proposed PR count: **{len(PROPOSED_PRS)}**. Canonical inspection snapshot: **{INSPECTED_AT}**.",
        "## Global PR table",
        global_pr_table(),
        "## Execution order",
        md_table(["Order", "ID", "Title", "Repository", "Dependencies", "Gate"], [[idx, pr["id"], pr["title"], pr["repo"], ", ".join(pr["deps"]) or "P00-01", pr["gate"]] for idx, pr in enumerate(topological_prs(), 1)]),
        "## Critical path",
        " → ".join(f"`{item}`" for item in CRITICAL_PATH),
        "Required dependency joins:\n\n" + bullets(CRITICAL_JOINS),
        "## Per-PR readiness and acceptance",
    ]
    for pr in topological_prs():
        parts.append(render_pr(pr, 3))
    return "\n\n".join(parts) + "\n"


def render_project_structure() -> str:
    counts = {
        "Work packages": len(WORK_PACKAGES), "Proposed PRs": len(PROPOSED_PRS), "Existing PRs": len(EXISTING_PRS),
        "Existing issues": len(RELATED_ISSUES), "Decisions": len(DECISIONS), "Review checkpoints": 1,
        "Programme gates": len(GATES), "Cleanup tasks": len(CLEANUP_TASKS),
    }
    parts = [
        "# GitHub Project structure — MVP Product Flow Reshape",
        f"Project: [{PROJECT_CONVENTIONS['project']}]({PROJECT_URL}).",
        "## Pre-change inspection",
        "Direct GraphQL inspection found Project 3 open with only GitHub's default Title, Assignees, Status, Labels, Linked PRs, Milestone, Repository, Reviewers, Parent issue, Sub-issues progress, Created, Updated and Closed fields, and **zero items**. The programme sync therefore does not duplicate prior programme items.",
        "## Operating model",
        md_table(["Convention", "Rule"], [[key.replace("_", " ").title(), value] for key, value in PROJECT_CONVENTIONS.items()]),
        "## Fields",
        md_table(["Field", "Type", "Options / use"], [[field["name"], field["type"], ", ".join(field.get("options", [])) or "Free text"] for field in PROJECT_FIELDS]),
        "GitHub's existing **Status** field is reused; no duplicate status field is created. Custom fields are the minimum set needed to hold the fields explicitly required by the programme brief for draft items as well as real PRs/issues.",
        "## Item catalogue",
        md_table(["Item type", "Expected count", "Naming convention"], [[name, count, {"Work packages": "[WPxx] title", "Proposed PRs": "[Pxx-yy] title", "Existing PRs": "Actual linked PR", "Existing issues": "Actual linked issue", "Decisions": "[DECISION D-*] title", "Review checkpoints": "[CHECKPOINT] title", "Programme gates": "[GATE Ax] title", "Cleanup tasks": "[CLEANUP C-*] title"}[name]] for name, count in counts.items()]),
        "## Live post-sync validation",
        md_table(["Check", "Verified result"], [[key.replace("_", " ").title(), value] for key, value in PROJECT_SYNC_RESULT.items()]),
        "The synchronizer read these values back from Project 3 after the final update; it did not infer them from the local catalogue. All items remain planning-only and no proposed PR is marked `Ready to implement`.",
        "## Dependency and hierarchy representation",
        PROJECT_CONVENTIONS["hierarchy"],
        "Each proposed PR carries a Work package value and exact Dependencies text. Work-package draft bodies list child PR IDs, decisions, gates and plan path. Decision/gate/checkpoint bodies list what they block. This provides deterministic hierarchy without creating empty issues/PRs.",
        "## Status, readiness and disposition",
        md_table(["Dimension", "Meaning"], [["Status", "Todo / In Progress / Done: execution state only."], ["Readiness", "Whether plan/decision/dependency/reconciliation conditions permit implementation."], ["Disposition", "How existing/proposed/decision/gate/cleanup material should be treated."], ["Ownership", "DRI/implementer/reviewer/approver recommendation; Alan remains proposed until sign-off."]]),
        "## Project sync and maintenance",
        f"Dry-run/read current state:\n\n```bash\n{PYTHON} scripts/sync_project.py\n```",
        f"Apply idempotent updates:\n\n```bash\n{PYTHON} scripts/sync_project.py --apply\n```",
        "After any canonical change, regenerate Markdown, validate, re-render the PDF, then re-run the idempotent Project sync. Do not hand-edit IDs/titles/dependencies in only one surface.",
        "## Final Project validation checklist",
        bullets([
            "One identifiable item for every WP00-WP13.", f"One proposed-PR draft item for all {len(PROPOSED_PRS)} PR IDs.",
            "Actual linked PRs #112/#117/#119/#121/#122/#123/#124 and DS #7/#8.",
            "Actual linked Learn #3 and Intelligence #14 dependency issues.", "Alan reconciliation checkpoint present and blocking named replacement work.",
            "Every blocking decision and A0/A1/A2/B1/B2 gate present.", "Ownership, dependencies, readiness, plan path, source/salvage and disposition populated.",
            "No duplicate titles/IDs and Project/document parity validator passes.",
        ], checked=True),
    ]
    return "\n\n".join(parts) + "\n"


def render_authorship_section() -> str:
    rows = []
    headers = ["Element", "Class", "Subject", "Current author", "Storage", "Provenance", "Visibility", "Verification", "Correction/replacement", "GC sees it?", "IP sees GC answer?", "Downstream influence", "Promotion behavior", "Recommended contract"]
    for item in AUTHORSHIP_MATRIX:
        rows.append([item["element"], item["class"], item["subject"], item["author"], item["storage"], item["provenance"], item["visibility"], item["verification"], item["correction"], item["gc_sees"], item["ip_sees_gc"], item["influence"], item["promotion"], item["contract"]])
    return "\n\n".join([
        "Class definitions:\n\n" + md_table(["Class", "Meaning"], [[key, value] for key, value in AUTHORSHIP_CLASSES.items()]),
        md_table(headers, rows),
        "Global contract:\n\n" + bullets(AUTHORSHIP_CONTRACT),
    ])


def render_consolidated() -> str:
    ordered = topological_prs()
    parts = [
        "# Natalyx MVP Product Flow Reshape — consolidated programme plan",
        "> Planning-only. Do not implement, deploy, migrate, change cloud resources, alter existing PRs or clean protected worktrees from this document. Alan should review/sign off this consolidated plan before proposed assignments become expected work.",
        f"Inspection snapshot: **{INSPECTED_AT}**. Planning branch: `{PLAN_BRANCH}`. GitHub Project: [{PROJECT_CONVENTIONS['project']}]({PROJECT_URL}). Proposed PRs: **{len(PROPOSED_PRS)}**.",
        "## Table of contents",
        bullets([
            "[Executive summary](#executive-summary)", "[Current verified verdict](#current-verified-verdict)", "[Architecture principles](#architecture-principles)",
            "[Dependency graph](#dependency-graph)", "[Global PR table and execution order](#global-pr-table-and-execution-order)", "[Parallel lanes and critical path](#parallel-lanes-and-critical-path)",
            "[State transition contract](#state-transition-contract)", "[Programme gates](#programme-gates)", "[GitHub Project operating model](#github-project-operating-model)",
            "[Ownership, delegation and review](#ownership-delegation-and-review)", "[Existing-PR extraction and Alan checkpoint](#existing-pr-extraction-and-alan-checkpoint)",
            "[Data authorship and provenance](#data-authorship-and-provenance)", "[Migration architecture](#migration-architecture)", "[Promotion, commercial and payment contract](#promotion-commercial-and-payment-contract)",
            "[Invitation safety](#invitation-safety)", "[Documents and S3](#documents-and-s3)", "[Design-system release rubric](#design-system-release-rubric)",
            "[Decision register](#decision-register)", "[Risk register](#risk-register)", "[Release strategy and real-user/PHI boundaries](#release-strategy-and-real-userphi-boundaries)",
            "[Document index and maintenance](#document-index-and-maintenance)", "[Detailed work packages](#detailed-work-packages)",
        ]),
        "## Executive summary",
        "The programme is a controlled rebuild around **free Node 0 workspace → explicit entitlement/commitment/payment → typed promotion authorization → enrollment-pending paid case**, not a patch stack on the current case-shaped Node 0 branch. The live dev endpoint is currently 503, so A0 recovery and current CI/PostgreSQL evidence come first. PR #122's update materially improves invitation and case-surface safety and should be salvaged; PR #124 remains valuable but structurally unsafe unchanged. Alan's unfinished review is an explicit blocking checkpoint, not an assumed approval.",
        "The canonical package proposes 50 focused PRs across app, infra, intelligence, Learn, participant design system and organisation planning. It keeps free education/safety capability, payment and truth state separate; uses one processor-neutral promotion authorization; preserves authorship/provenance; and gates real PII/PHI behind independent evidence rather than deploy success.",
        "## Current verified verdict",
        md_table(["Area", "Verdict", "Evidence / consequence"], [
            ["Live cloud", "Not usable now", "dev.app.natalyx.health returned ALB 503 at the inspection snapshot; A0 is open."],
            ["AWS detail", "Partially unverified", "Local natalyx-dev SSO expired; service counts/task revision must be captured during A0."],
            ["CI/Postgres", "Insufficient on main", "Container build + contract smoke exist; no main Python/PostgreSQL evidence job."],
            ["PR #122", "Materially improved, not final architecture", "Latest e853821 fixes return_to/TTL/CAS/lens/CI and should be selectively retained."],
            ["PR #124", "Do not merge unchanged", "Free Node 0 creates a canonical case; unaddressed link can lead to case membership; no commercial promotion/provenance contract."],
            ["Payments/documents/PHI", "Not implemented/ready", "No money ledger; documents metadata-only; app-layer authorization and synthetic-first PHI gate remain."],
        ]),
        "## Architecture principles",
        bullets([
            "natalyx-app owns routing, validation, permissions, participant/workspace/case/commercial truth and PHI policy.",
            "Workspace, entitlement, commitment, payment, case, invitation/claim, document and journey-stage state machines remain separate.",
            "PostgreSQL is production authority; established migrations are preferred pending ADR; runtime identities lose DDL authority.",
            f"Only `{PROMOTION_EVENT['event_type']}` authorizes workspace-to-case promotion; redirects and raw webhooks never do.",
            "Commercial/money events are append-only; balances/statuses are projections.",
            "IP observations/provisional assertions remain attributed; GC/provider confirmation appends revisions and never silently erases/elevates source.",
            "Provider/intelligence/Learn projections are purpose-, role-, consent-, provenance- and version-bound.",
            "Security/accessibility/responsive interaction can block release; aesthetic/token purity alone generally cannot.",
            "Synthetic only through A2, approved PII scope at B1, PHI only after formal B2.",
        ]),
        "## Dependency graph",
        dependency_mermaid(),
        "The graph is package-level; the PR table below is the executable dependency authority.",
        "## Global PR table and execution order",
        global_pr_table(),
        "Topological execution order:\n\n" + md_table(["Order", "ID", "Title", "Repository", "Dependencies", "Gate"], [[idx, pr["id"], pr["title"], pr["repo"], ", ".join(pr["deps"]) or "P00-01", pr["gate"]] for idx, pr in enumerate(ordered, 1)]),
        "## Parallel lanes and critical path",
        "Critical path:\n\n" + " → ".join(f"`{item}`" for item in CRITICAL_PATH),
        "Required dependency joins:\n\n" + bullets(CRITICAL_JOINS),
        "First three implementation PRs:\n\n" + numbered(f"`{item}` — {next(pr['title'] for pr in PROPOSED_PRS if pr['id'] == item)}" for item in FIRST_THREE_IMPLEMENTATION_PRS),
        md_table(["Lane", "Lead", "Items", "Coordination"], [[lane["lane"], lane["lead"], ", ".join(lane["items"]), lane["coordination"]] for lane in PARALLEL_LANES]),
        "Early sequencing:\n\n" + numbered(" + ".join(stage) for stage in EARLY_PARALLEL_SEQUENCE),
        "## State transition contract",
        "Common envelope:\n\n```text\n" + "\n".join(TRANSITION_ENVELOPE) + "\n```",
        bullets(TRANSITION_RULES),
    ]
    for machine in STATE_MACHINES:
        parts.append(render_machine(machine, 3))
    parts += [
        "## Programme gates",
        render_gate_table(compact=False),
        "## GitHub Project operating model",
        render_project_structure().replace("# GitHub Project structure — MVP Product Flow Reshape\n\n", ""),
        "## Ownership, delegation and review",
        md_table(["Work package", "DRI", "Implementer", "Reviewer", "Approver", "Split"], [[item["wp"], item["dri"], item["implementer"] + " (proposed)", item["reviewer"], item["approver"], item["note"]] for item in WORK_PACKAGE_OWNERSHIP]),
        md_table(["Checkpoint", "When", "Owner", "Evidence"], [[item["checkpoint"], item["when"], item["owner"], item["evidence"]] for item in REVIEW_MODEL]),
        "Delegation rule: Luke decides product/lifecycle/commercial/privacy/PHI/provider boundaries and accepts gates; Alan proposes implementation and owns technical delivery/validation after sign-off. Joint planning is mandatory for migration, invitation admission, authorship/projection, promotion, activation, document plane and B1/B2. External review is mandatory for payment/refund, auth security, document/PHI, provider sharing and AI truth boundaries.",
        "## Existing-PR extraction and Alan checkpoint",
        render_extraction_ledger().replace("# Existing PR extraction ledger\n\n", ""),
        "## Data authorship and provenance",
        render_authorship_section(),
        "### Concise answer for Alan",
        "The intended parent answers today because Node 0 was built as a private pre-contact reflection tool: relationship context and observed signals can tailor a low-pressure conversation guide before the prospective GC has an account. That limited use is reasonable. What is not reasonable is treating those answers as if the GC made or confirmed them, especially health, age, citizenship, family status, insurance, consent, preferences or eligibility. Those must be GC-authored, with reviewer/provider confirmation where required. When the GC joins, her answer appends an attributable revision; the earlier IP statement remains labelled as IP-reported/unconfirmed, GC-private data stays private, and only an explicit purpose-limited projection reaches the IP. The current score/invite gating and missing reconciliation should be replaced.",
        "## Migration architecture",
        "Options:\n\n" + numbered(MIGRATION_DECISION_CONTRACT["options"]),
        f"**Provisional recommendation:** {MIGRATION_DECISION_CONTRACT['provisional_recommendation']}",
        bullets(MIGRATION_DECISION_CONTRACT["requirements"]),
        "## Promotion, commercial and payment contract",
        f"Sole authorization: `{PROMOTION_EVENT['event_type']}`. Producer: {PROMOTION_EVENT['producer']}. Consumer: {PROMOTION_EVENT['consumer']}.",
        "Payload:\n\n```text\n" + "\n".join(PROMOTION_EVENT["payload"]) + "\n```",
        "Conditions:\n\n" + bullets(PROMOTION_EVENT["conditions"]),
        "Constraints:\n\n" + bullets(PROMOTION_EVENT["constraints"]),
        PROMOTION_EVENT["browser_rule"],
        "Append-only ledgers:\n\n" + bullets(f"`{item}`" for item in COMMERCIAL_LEDGER_CONTRACT["authoritative"]),
        "Rules:\n\n" + bullets(COMMERCIAL_LEDGER_CONTRACT["rules"]),
        "## Invitation safety",
        "Retain from #122:\n\n" + bullets(INVITATION_CONTRACT["retain_from_122"]),
        "Required changes:\n\n" + bullets(INVITATION_CONTRACT["required_changes"]),
        "## Documents and S3",
    ]
    for key in ("storage", "upload", "download", "recovery"):
        parts += [f"### {key.title()}", bullets(DOCUMENT_CONTRACT[key])]
    parts += [
        "## Design-system release rubric",
        md_table(["Class", "Items"], [["Release-blocking", "; ".join(DESIGN_SYSTEM_RELEASE_POLICY["release_blocking"])], ["Desirable", "; ".join(DESIGN_SYSTEM_RELEASE_POLICY["desirable"])], ["Deferred", "; ".join(DESIGN_SYSTEM_RELEASE_POLICY["deferred"])] ]),
        DESIGN_SYSTEM_RELEASE_POLICY["rule"],
        "## Decision register",
        md_table(["ID", "Decision", "Owner / proposer", "Affected PRs", "Latest point", "Recommendation / treatment", "Project item"], [[d["id"], d["question"], f"{d['owner']} / {d['proposer']}", ", ".join(d["affected"]), d["latest"], d["recommendation"], f"[{d['id']}]({PROJECT_URL}?query={d['id']})"] for d in DECISIONS]),
        "## Risk register",
        md_table(["ID", "Class", "Risk", "Owner", "Mitigation", "Gate"], [[r["id"], r["class"], r["risk"], r["owner"], r["mitigation"], r["gate"]] for r in RISK_REGISTER]),
        "## Release strategy and real-user/PHI boundaries",
        bullets(RELEASE_STRATEGY),
        "A0/A1/A2 remain synthetic. B1 is a named, approved PII-only beta boundary. B2 is a formal PHI go/no-go that requires organizational, contractual, operational and technical evidence; successful tests or deployment alone are insufficient.",
        "## Document index and maintenance",
        render_document_index(),
        f"Regenerate all Markdown:\n\n```bash\n{PYTHON} scripts/render_programme.py\n```",
        f"Validate parity/dependencies:\n\n```bash\n{PYTHON} scripts/validate_programme.py\n```",
        f"Render this exact Markdown to PDF:\n\n```bash\n{PYTHON} scripts/render_pdf.py consolidated-plan.md consolidated-plan.pdf\n```",
        "## Detailed work packages",
    ]
    for wp in WORK_PACKAGES:
        parts.append(render_wp(wp, top_level=2))
    return "\n\n".join(parts) + "\n"


def render_document_index() -> str:
    rows = [["README.md", "Programme entrypoint, index, operating/maintenance/render instructions"], ["existing-pr-extraction-ledger.md", "PR/worktree preservation, extraction and closure/delete conditions"], ["project-structure.md", "GitHub Project fields, items and conventions"], ["pr-manifest.md", "Canonical proposed PR inventory and execution order"], ["consolidated-plan.md", "Full programme source for the PDF"], ["consolidated-plan.pdf", "Rendered review copy generated only from consolidated-plan.md"]]
    rows += [[plan_filename(wp["id"]), f"Standalone execution plan for {wp['id']} — {wp['title']}"] for wp in WORK_PACKAGES]
    rows += [["programme_data.py", "Canonical structured source used to keep IDs/contracts consistent"], ["scripts/render_programme.py", "Mechanical Markdown renderer"], ["scripts/render_pdf.py", "Markdown-to-PDF renderer"], ["scripts/validate_programme.py", "Cross-file/dependency/gate validator"], ["scripts/sync_project.py", "Idempotent GitHub Project inspector/synchronizer"]]
    return md_table(["Document", "Purpose"], rows)


def render_readme() -> str:
    parts = [
        "# Natalyx repair programme planning package",
        "> Planning only. No application, infrastructure, schema, deployment or cloud mutation is authorized by these files. Alan should review/sign off the consolidated plan before proposed assignments become expected work.",
        "## Executive summary",
        f"This clean planning worktree on `{PLAN_BRANCH}` contains 14 standalone work-package plans, a {len(PROPOSED_PRS)}-PR manifest, extraction ledger, Project operating model, consolidated Markdown and a PDF rendered from that Markdown. The organisation Project [{PROJECT_CONVENTIONS['project']}]({PROJECT_URL}) is the operational control plane.",
        "## Current verified verdict",
        "The dev app endpoint returned ALB 503 at the inspection snapshot, and local AWS SSO was expired, so A0 is not passed and the exact running ECS revision still needs capture. Main lacks a Python/PostgreSQL evidence job. Updated PR #122 is stronger and worth selective reuse; PR #124 remains architecturally unsafe unchanged because Node 0 Free creates a canonical case and an unaddressed link can lead to case membership.",
        "## Architecture principles",
        bullets([
            "Separate entry, workspace, entitlement, commitment, payment, case, claim/invitation and document state machines.",
            f"Only `{PROMOTION_EVENT['event_type']}` authorizes paid-case promotion.",
            "PostgreSQL production authority, versioned migrations, append-only commercial/authorship/audit history.",
            "IP provisional information remains attributed; GC/private/provider truth has explicit authorship, visibility, verification and revision.",
            "Synthetic A0-A2, PII-only B1, formal human PHI B2.",
        ]),
        "## Dependency graph",
        dependency_mermaid(),
        "## Critical path and first work",
        "Critical path:\n\n" + " → ".join(f"`{item}`" for item in CRITICAL_PATH),
        "Required dependency joins:\n\n" + bullets(CRITICAL_JOINS),
        "First three implementation PRs:\n\n" + numbered(f"`{item}` — {next(pr['title'] for pr in PROPOSED_PRS if pr['id'] == item)}" for item in FIRST_THREE_IMPLEMENTATION_PRS),
        "CI/A0/migration design can progress after plan sign-off while Alan completes the explicit #122/#124 reconciliation checkpoint. Replacement auth, Node 0 and participant case work waits for that checkpoint.",
        "## Programme gates",
        render_gate_table(compact=True),
        "## GitHub Project operating model",
        f"Use [{PROJECT_CONVENTIONS['project']}]({PROJECT_URL}) as the authoritative tracker. {PROJECT_CONVENTIONS['hierarchy']} {PROJECT_CONVENTIONS['readiness']} {PROJECT_CONVENTIONS['assignment']}",
        "## Ownership and review",
        md_table(["Work package", "DRI", "Implementer", "Reviewer", "Approver", "Note"], [[item["wp"], item["dri"], item["implementer"] + " (proposed)", item["reviewer"], item["approver"], item["note"]] for item in WORK_PACKAGE_OWNERSHIP]),
        "## Document index",
        render_document_index(),
        "## Reproducible generation, validation and PDF render",
        "Regenerate Markdown:\n\n```bash\n" + PYTHON + " scripts/render_programme.py\n```",
        "Validate identifiers/dependencies/gates/cross-file coverage:\n\n```bash\n" + PYTHON + " scripts/validate_programme.py\n```",
        "Render the PDF **from consolidated-plan.md**:\n\n```bash\n" + PYTHON + " scripts/render_pdf.py consolidated-plan.md consolidated-plan.pdf\n```",
        "Inspect PDF metadata/text/pages:\n\n```bash\npdfinfo consolidated-plan.pdf\npdftotext consolidated-plan.pdf /tmp/consolidated-plan.txt\npdftoppm -f 1 -singlefile -png -r 110 consolidated-plan.pdf /tmp/natalyx-plan-first\n```",
        "Synchronize the GitHub Project (dry-run, then apply):\n\n```bash\n" + PYTHON + " scripts/sync_project.py\n" + PYTHON + " scripts/sync_project.py --apply\n```",
        "## Maintenance instructions",
        numbered([
            "Edit programme_data.py, not a single rendered plan, when an ID/title/dependency/owner/gate/decision/disposition changes.",
            "Record new Alan findings in the extraction/checkpoint data with exact head and evidence anchor.",
            "Regenerate Markdown and run validate_programme.py; resolve every circular/missing/mismatch result.",
            "Re-render the PDF, inspect representative first/table/diagram/code/last pages and verify text/headings/page count.",
            "Run git diff --check, then run the idempotent Project sync and verify expected counts/fields.",
            "Never make a proposed item Ready to implement until plan approval, decisions, dependencies and checkpoint requirements are satisfied.",
        ]),
    ]
    return "\n\n".join(parts) + "\n"


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    ordered = topological_prs()
    assert len({pr["id"] for pr in ordered}) == len(PROPOSED_PRS)
    for wp in WORK_PACKAGES:
        write(ROOT / plan_filename(wp["id"]), render_wp(wp))
    write(ROOT / "README.md", render_readme())
    write(ROOT / "existing-pr-extraction-ledger.md", render_extraction_ledger())
    write(ROOT / "project-structure.md", render_project_structure())
    write(ROOT / "pr-manifest.md", render_pr_manifest())
    write(ROOT / "consolidated-plan.md", render_consolidated())
    print(f"Rendered {len(WORK_PACKAGES)} work-package plans and {len(PROPOSED_PRS)} proposed PRs into {ROOT}")


if __name__ == "__main__":
    main()
