#!/usr/bin/env python3
"""Validate the generated Natalyx programme package and dependency model."""

from __future__ import annotations

import re
import sys
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import programme_data as data  # noqa: E402


errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def topological_ids() -> list[str]:
    ids = {pr["id"] for pr in data.PROPOSED_PRS}
    indegree = {pr_id: 0 for pr_id in ids}
    outgoing = {pr_id: set() for pr_id in ids}
    for pr in data.PROPOSED_PRS:
        for dep in pr["deps"]:
            if dep in ids:
                indegree[pr["id"]] += 1
                outgoing[dep].add(pr["id"])
    queue = deque(sorted(pr_id for pr_id, degree in indegree.items() if degree == 0))
    ordered = []
    while queue:
        current = queue.popleft()
        ordered.append(current)
        for nxt in sorted(outgoing[current]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    require(len(ordered) == len(ids), f"Circular dependencies: {sorted(pr_id for pr_id, degree in indegree.items() if degree)}")
    return ordered


def validate_data() -> None:
    wp_ids = [wp["id"] for wp in data.WORK_PACKAGES]
    require(wp_ids == [f"WP{number:02d}" for number in range(14)], f"Work packages are not exactly WP00-WP13: {wp_ids}")
    require(len(set(wp_ids)) == len(wp_ids), "Duplicate work package IDs")

    pr_ids = [pr["id"] for pr in data.PROPOSED_PRS]
    pr_id_set = set(pr_ids)
    require(len(pr_ids) == 52, f"Expected 52 reconciled proposed PRs, found {len(pr_ids)}")
    require({"P03-05", "P09-06"}.issubset(pr_id_set), "Reconciled access/document PRs are missing")
    require(len(pr_id_set) == len(pr_ids), f"Duplicate PR IDs: {[item for item, count in Counter(pr_ids).items() if count > 1]}")
    for pr in data.PROPOSED_PRS:
        require(bool(re.fullmatch(r"P\d{2}-\d{2}", pr["id"])), f"Bad PR ID: {pr['id']}")
        require(pr["wp"] in wp_ids, f"{pr['id']} unknown work package {pr['wp']}")
        for key in ("title", "repo", "objective", "gate", "size", "wp_dri", "dri", "primary_implementer", "implementer", "technical_decision_owner", "reviewer", "approver", "local_preparation_status", "merge_readiness", "ownership_exception"):
            require(bool(pr.get(key)), f"{pr['id']} missing {key}")
        require(bool(pr["scope"]), f"{pr['id']} missing scope")
        require(bool(pr["non_goals"]), f"{pr['id']} missing non-goals")
        require(bool(pr["tests"]), f"{pr['id']} missing tests")
        for dep in pr["deps"]:
            require(dep in pr_ids, f"{pr['id']} unknown dependency {dep}")
    topological_ids()

    expected_luke_wps = {"WP00", "WP05", "WP07", "WP08", "WP11", "WP12"}
    expected_alan_wps = set(wp_ids) - expected_luke_wps
    ownership_by_wp = {item["wp"]: item for item in data.WORK_PACKAGE_OWNERSHIP}
    require(set(ownership_by_wp) == set(wp_ids), "Work-package ownership table does not cover WP00-WP13 exactly")
    require({wp for wp, item in ownership_by_wp.items() if item["dri"] == "Luke"} == expected_luke_wps, "Luke work-package split is incorrect")
    require({wp for wp, item in ownership_by_wp.items() if item["dri"] == "Alan"} == expected_alan_wps, "Alan work-package split is incorrect")
    require(Counter(pr["dri"] for pr in data.PROPOSED_PRS) == Counter({"Luke": 19, "Alan": 33}), "Expected exactly 19 Luke-owned and 33 Alan-owned PRs")
    require(Counter(pr["primary_implementer"] for pr in data.PROPOSED_PRS) == Counter({"Luke": 19, "Alan": 32, "Joint": 1}), "Primary implementer split or exception count is wrong")
    require(set(data.PR_OWNERSHIP_EXCEPTIONS) == {"P13-07"}, "P13-07 must be the sole PR-level ownership exception")
    for pr in data.PROPOSED_PRS:
        wp_owner = ownership_by_wp[pr["wp"]]
        require(pr["wp_dri"] == pr["dri"] == wp_owner["dri"], f"{pr['id']} does not inherit its work-package DRI")
        if pr["id"] == "P13-07":
            require(pr["primary_implementer"] == pr["implementer"] == "Joint", "P13-07 is not Joint implementation")
            require(pr["dri"] == "Alan" and "External" in pr["reviewer"], "P13-07 DRI/review exception is incomplete")
            require(pr["ownership_exception"] != "None", "P13-07 exception lacks justification")
        else:
            require(pr["primary_implementer"] == pr["implementer"] == wp_owner["implementer"], f"{pr['id']} does not inherit its work-package implementer")
            require(pr["reviewer"] == wp_owner["reviewer"], f"{pr['id']} does not inherit reciprocal review")
            require(pr["ownership_exception"] == "None", f"{pr['id']} has an unapproved ownership exception")

    local_preparation_ids = {pr["id"] for pr in data.PROPOSED_PRS if pr["local_preparation_status"].startswith("Eligible for isolated")}
    require(local_preparation_ids == {"P11-01", "P11-03"}, f"Unexpected isolated local-preparation set: {sorted(local_preparation_ids)}")
    for pr_id in local_preparation_ids:
        pr = next(item for item in data.PROPOSED_PRS if item["id"] == pr_id)
        require(pr["dri"] == pr["primary_implementer"] == "Luke", f"{pr_id} local preparation is not Luke-owned")
        require(all(term in pr["local_preparation_status"] for term in ("uncommitted", "synthetic")), f"{pr_id} local-preparation constraints are incomplete")
        require(all(term in pr["merge_readiness"] for term in ("P00-01", "Gate A0", "Alan review")), f"{pr_id} merge controls are incomplete")
    p00 = next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P00-01")
    require("Ready for Alan review and joint acceptance" in p00["local_preparation_status"], "P00-01 is not review-ready")
    require("Blocked pending Alan review and joint programme acceptance" == p00["merge_readiness"], "P00-01 merge readiness is wrong")

    for decision_id in data.TECHNICAL_DECISION_OWNERS:
        require(decision_id in {item["id"] for item in data.DECISIONS}, f"Unknown technical-decision owner mapping {decision_id}")
        for pr_id in next(item for item in data.DECISIONS if item["id"] == decision_id)["affected"]:
            require(decision_id in next(pr for pr in data.PROPOSED_PRS if pr["id"] == pr_id)["technical_decision_owner"], f"{pr_id} does not preserve {decision_id} technical ownership")

    decision_ids = {item["id"] for item in data.DECISIONS}
    require(len(data.DECISIONS) == 24, f"Expected 24 decisions, found {len(data.DECISIONS)}")
    require(len(decision_ids) == len(data.DECISIONS), "Duplicate decision IDs")
    for decision in data.DECISIONS:
        require(decision["owner"], f"{decision['id']} missing owner")
        require(decision["affected"], f"{decision['id']} affects no PR")
        for key in ("status", "classification", "decision_state", "founder_decision", "constraints", "remaining_owner", "alan_remaining", "evidence_required", "approval_required", "external_dependencies", "programme_effect"):
            require(key in decision and decision[key] not in (None, ""), f"{decision['id']} missing resolution field {key}")
        for pr_id in decision["affected"]:
            require(pr_id in pr_ids, f"{decision['id']} references unknown {pr_id}")

    require(data.IMMEDIATE_ALAN_DECISIONS == ["D-CI-01", "D-MIG-01", "D-OPS-01"], "Immediate Alan decision list changed unexpectedly")
    require(set(data.LATER_ALAN_DECISIONS) == {"D-AUTH-02", "D-PAY-01", "D-DOC-01", "D-DOC-02", "D-PROV-01", "D-AI-01", "D-PHI-01", "D-PHI-02"}, "Later Alan decision list is incomplete")
    require(set(data.EXTERNAL_DEPENDENT_DECISIONS).issubset(decision_ids), "External decision list has an unknown ID")
    require("operationally pending" in next(item for item in data.DECISIONS if item["id"] == "D-CI-01")["status"].lower(), "D-CI-01 is not operationally pending")
    require("Alan immediate" in next(item for item in data.DECISIONS if item["id"] == "D-MIG-01")["status"], "D-MIG-01 does not preserve Alan's immediate decision")
    require("Alan immediate" in next(item for item in data.DECISIONS if item["id"] == "D-OPS-01")["status"], "D-OPS-01 does not preserve Alan's immediate decision")
    require("Externally dependent" in next(item for item in data.DECISIONS if item["id"] == "D-COM-03")["status"], "D-COM-03 is not externally dependent")

    allowed_blocks = decision_ids | {data.RECONCILIATION_CHECKPOINT["id"]}
    actual_decision_blockers: set[str] = set()
    for pr in data.PROPOSED_PRS:
        for blocker in pr["blocked_by"]:
            require(blocker in allowed_blocks, f"{pr['id']} unknown blocker {blocker}")
            decision = next((item for item in data.DECISIONS if item["id"] == blocker), None)
            require(decision is None or not decision.get("status", "Open").startswith("Resolved"), f"{pr['id']} is blocked by resolved {blocker}")
            if decision is not None:
                actual_decision_blockers.add(blocker)
                require(blocker in data.ACTIVE_DECISION_BLOCKERS, f"{pr['id']} is blocked by founder-final policy without a remaining technical mechanism: {blocker}")
    require(actual_decision_blockers == data.ACTIVE_DECISION_BLOCKERS, f"Active blocker registry mismatch: data={sorted(data.ACTIVE_DECISION_BLOCKERS)} actual={sorted(actual_decision_blockers)}")
    require(not any(data.RECONCILIATION_CHECKPOINT["id"] in pr["blocked_by"] for pr in data.PROPOSED_PRS), "Completed reconciliation checkpoint still blocks a PR")
    require("D-MIG-01" not in next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P02-01")["blocked_by"], "P02-01 decision work is incorrectly blocked")
    require("D-MIG-01" in next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P02-02")["blocked_by"], "P02-02 is not blocked on Alan's migration decision")
    require("D-MIG-01" in next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P02-03")["blocked_by"], "P02-03 is not blocked on Alan's migration evidence")

    gate_ids = {gate["id"] for gate in data.GATES}
    require(gate_ids == {"A0", "A1", "A2", "B1", "B2"}, f"Unexpected gate set {gate_ids}")
    for gate in data.GATES:
        require(gate["owner"] and gate["verifier"], f"{gate['id']} missing owner/verifier")
        require(gate["acceptance"] and gate["evidence"] and gate["failure"], f"{gate['id']} incomplete contract")
        for prerequisite in gate["prerequisites"]:
            require(prerequisite in pr_id_set | gate_ids, f"{gate['id']} unknown prerequisite {prerequisite}")
        for decision_id in gate["decisions"]:
            require(decision_id in decision_ids, f"{gate['id']} unknown decision {decision_id}")
    gate_order = {"Pre-A0": 0, "A0": 1, "A1": 2, "A2": 3, "B1": 4, "B2": 5, "Post-B2": 6}
    pr_by_id = {pr["id"]: pr for pr in data.PROPOSED_PRS}
    for gate in data.GATES:
        for prerequisite in gate["prerequisites"]:
            if prerequisite in pr_by_id:
                require(gate_order[pr_by_id[prerequisite]["gate"]] <= gate_order[gate["id"]], f"{gate['id']} depends on later-gate {prerequisite} ({pr_by_id[prerequisite]['gate']})")
    a0_text = " ".join(next(gate for gate in data.GATES if gate["id"] == "A0")["acceptance"] + next(gate for gate in data.GATES if gate["id"] == "A0")["evidence"])
    require(all(term in a0_text for term in ("GitHub Team", "PostgreSQL", "negative-bypass", "recovery")), "A0 does not contain CI, PostgreSQL, bypass and recovery evidence")
    b1_text = " ".join(next(gate for gate in data.GATES if gate["id"] == "B1")["acceptance"])
    require(all(term in b1_text for term in ("five IP/GC pairs", "real document bytes", "real provider packets", "de-identified nonclinical")), "B1 scope is not the approved five-pair nonclinical PII boundary")
    b2_text = " ".join(next(gate for gate in data.GATES if gate["id"] == "B2")["acceptance"])
    require(all(term in b2_text for term in ("Qualified external", "30 days", "12 months", "No critical")), "B2 external-review recency/exception contract is incomplete")

    for item in data.CRITICAL_PATH + data.FIRST_THREE_IMPLEMENTATION_PRS:
        require(item in pr_ids, f"Critical/first item is not a PR: {item}")

    existing_keys = [item["key"] for item in data.EXISTING_PRS]
    for required in ["app#112", "app#117", "app#119", "app#121", "app#122", "app#123", "app#124", "ds#7", "ds#8"]:
        require(required in existing_keys, f"Missing extraction record {required}")
    pr122 = next((item for item in data.EXISTING_PRS if item["key"] == "app#122"), None)
    require(pr122 is not None and pr122["sha"] == "e85382150853cf4774948c55b91e330e7e69617e", "PR #122 latest SHA missing/wrong")
    pr124 = next((item for item in data.EXISTING_PRS if item["key"] == "app#124"), None)
    require(pr124 is not None and "independently reconciled" in pr124["review"].lower(), "PR #124 completed review reconciliation missing")
    require(pr124 is not None and "supersede" in pr124["disposition"].lower(), "PR #124 is not superseded as a merge unit")
    require(data.WAVE2_BRANCH["head"] == "5b63e3a7c3643efcd5f3e74f422d095423b55f59", "Wave 2 head missing/wrong")
    require(data.WAVE2_BRANCH["base"] == "e85382150853cf4774948c55b91e330e7e69617e", "Wave 2 corrected #122 base missing/wrong")
    require(len(data.WAVE2_BRANCH["ancestry"]) == 3, "Wave 2 ancestry is not the expected three commits")

    matrix_fields = {"id", "recommendation", "evidence", "current_plan", "assumptions", "impact", "dependency_migration", "alternatives", "conclusion", "rationale", "affected", "decision_required"}
    require(len(data.RECONCILIATION_MATRIX) >= 22, "Reconciliation matrix is not materially complete")
    require(len({item["id"] for item in data.RECONCILIATION_MATRIX}) == len(data.RECONCILIATION_MATRIX), "Duplicate reconciliation IDs")
    for item in data.RECONCILIATION_MATRIX:
        require(matrix_fields.issubset(item) and all(item[field] for field in matrix_fields), f"Reconciliation row {item.get('id')} is incomplete")
        require(item["conclusion"] in {"Accept", "Accept with modification", "Defer", "Reject"}, f"Bad reconciliation conclusion {item.get('id')}: {item.get('conclusion')}")

    require(data.RECONCILIATION_CHECKPOINT["status"].startswith("Complete"), "Reconciliation checkpoint is not complete")
    require(data.RECONCILIATION_CHECKPOINT["blocks"] == [], "Completed reconciliation checkpoint still lists blocks")
    require(next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P03-02")["deps"] == ["P03-01", "P03-05", "P04-01"], "P03-02 reconciled dependencies wrong")
    require(next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P03-03")["deps"] == ["P03-01", "P03-05"], "P03-03 reconciled dependencies wrong")
    require("P09-03" not in next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P09-04")["deps"], "P09-04 still depends on content pipeline")
    require(next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P09-05")["deps"] == ["P04-02", "P09-06", "P10-02"], "P09-05 reconciled dependencies wrong")
    require(next(pr for pr in data.PROPOSED_PRS if pr["id"] == "P13-05")["gate"] == "B1", "P13-05 is not before real-user PII")
    require({"P13-05", "P13-06", "P13-07"}.issubset(set(next(g for g in data.GATES if g["id"] == "B1")["prerequisites"])), "B1 lacks RLS/control/runbook prerequisites")

    require(len(data.AUTHORSHIP_MATRIX) >= 20, "Authorship matrix is not materially complete")
    for item in data.AUTHORSHIP_MATRIX:
        for key in ("element", "class", "subject", "author", "storage", "provenance", "visibility", "verification", "correction", "gc_sees", "ip_sees_gc", "influence", "promotion", "contract"):
            require(bool(item.get(key)), f"Authorship row {item.get('element')} missing {key}")

    require(data.PROMOTION_EVENT["event_type"] == "byos.workspace_promotion_authorized.v1", "Wrong promotion-authorizing event")
    require("browser" in data.PROMOTION_EVENT["browser_rule"].lower(), "Browser redirect prohibition missing")
    require(len(data.STATE_MACHINES) >= 8, "Required separate state machines missing")

    expected_project_items = (
        len(data.WORK_PACKAGES)
        + len(data.PROPOSED_PRS)
        + len(data.EXISTING_PRS)
        + len(data.RELATED_ISSUES)
        + len(data.DECISIONS)
        + 1
        + len(data.GATES)
        + len(data.CLEANUP_TASKS)
    )
    require(data.PROJECT_SYNC_RESULT["items"] == expected_project_items == 110, "Desired Project catalogue count is not 110")
    require(data.PROJECT_SYNC_RESULT["live_items"] == 106, "Last verified live Project snapshot is not preserved")
    require(data.PROJECT_SYNC_RESULT["custom_fields"] == len(data.PROJECT_FIELDS) == 16, "Project custom field count mismatch")
    require(data.PROJECT_SYNC_RESULT["draft_items"] + data.PROJECT_SYNC_RESULT["linked_items"] == expected_project_items, "Desired Project draft/link counts do not sum to total")
    field_names = [field["name"] for field in data.PROJECT_FIELDS]
    require(len(field_names) == len(set(field_names)), "Duplicate Project custom field names")
    require("Programme reviewer" in field_names and "Reviewer" not in field_names, "Reserved reviewer field convention not applied")


def validate_files() -> None:
    expected_plans = [ROOT / data.plan_filename(wp["id"]) for wp in data.WORK_PACKAGES]
    for path in expected_plans:
        require(path.exists(), f"Missing standalone plan {path.name}")
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for section in range(1, 11):
                require(f"{section}." in text, f"{path.name} missing numbered section {section}")
            wp_id = next(wp["id"] for wp in data.WORK_PACKAGES if data.plan_filename(wp["id"]) == path.name)
            for pr in [pr for pr in data.PROPOSED_PRS if pr["wp"] == wp_id]:
                require(pr["id"] in text, f"{pr['id']} missing from {path.name}")
                require(pr["local_preparation_status"] in text, f"{pr['id']} local preparation missing from {path.name}")
                require(pr["merge_readiness"] in text, f"{pr['id']} merge readiness missing from {path.name}")
                require(pr["technical_decision_owner"] in text, f"{pr['id']} technical-decision owner missing from {path.name}")

    required = ["README.md", "existing-pr-extraction-ledger.md", "project-structure.md", "pr-manifest.md", "consolidated-plan.md", "consolidated-plan.pdf", "scripts/sync_project.py"]
    for name in required:
        require((ROOT / name).exists(), f"Missing {name}")

    manifest = (ROOT / "pr-manifest.md").read_text(encoding="utf-8")
    consolidated = (ROOT / "consolidated-plan.md").read_text(encoding="utf-8")
    project = (ROOT / "project-structure.md").read_text(encoding="utf-8")
    ledger = (ROOT / "existing-pr-extraction-ledger.md").read_text(encoding="utf-8")
    for pr in data.PROPOSED_PRS:
        require(pr["id"] in manifest, f"{pr['id']} missing from manifest")
        require(pr["id"] in consolidated, f"{pr['id']} missing from consolidated plan")
        require(pr["local_preparation_status"] in manifest and pr["local_preparation_status"] in consolidated, f"{pr['id']} local preparation parity missing")
        require(pr["merge_readiness"] in manifest and pr["merge_readiness"] in consolidated, f"{pr['id']} merge readiness parity missing")
        require(pr["technical_decision_owner"] in manifest and pr["technical_decision_owner"] in consolidated, f"{pr['id']} technical-decision ownership parity missing")
    for wp in data.WORK_PACKAGES:
        require(wp["id"] in consolidated, f"{wp['id']} missing from consolidated plan")
    for gate in data.GATES:
        require(f"Gate {gate['id']}" in consolidated, f"Gate {gate['id']} missing from consolidated plan")
        require(gate["id"] in project, f"Gate {gate['id']} missing from project structure")
    for decision in data.DECISIONS:
        require(decision["id"] in consolidated, f"{decision['id']} missing from consolidated plan")
        require(decision["founder_decision"] in consolidated, f"{decision['id']} founder outcome missing from consolidated plan")
        for wp in data.WORK_PACKAGES:
            package_pr_ids = {pr["id"] for pr in data.PROPOSED_PRS if pr["wp"] == wp["id"]}
            if package_pr_ids.intersection(decision["affected"]):
                plan_text = (ROOT / data.plan_filename(wp["id"])).read_text(encoding="utf-8")
                require(decision["founder_decision"] in plan_text, f"{decision['id']} founder outcome missing from affected {wp['id']}")
                require(decision["programme_effect"] in plan_text, f"{decision['id']} programme effect missing from affected {wp['id']}")
    require(data.RECONCILIATION_CHECKPOINT["title"] in ledger, "Alan checkpoint missing from extraction ledger")
    require(data.RECONCILIATION_CHECKPOINT["title"] in consolidated, "Alan checkpoint missing from consolidated plan")
    require("e85382150853cf4774948c55b91e330e7e69617e" in ledger, "Latest PR #122 SHA missing from ledger")
    require("5b63e3a7c3643efcd5f3e74f422d095423b55f59" in ledger, "Wave 2 exact head missing from ledger")
    require("REC-22" in ledger and "REC-22" in consolidated, "Complete reconciliation matrix is not rendered")
    wp00 = (ROOT / data.plan_filename("WP00")).read_text(encoding="utf-8")
    require("Frozen independent recommendation matrix" in wp00 and "REC-22" in wp00, "WP00 lacks the frozen reconciliation matrix")
    require("P03-05" in consolidated and "P09-06" in consolidated, "Reconciled PR additions missing from consolidated plan")
    require("authorship" in consolidated.lower() and "provider packet" in consolidated.lower(), "Authorship matrix/coverage missing")
    require("scripts/render_pdf.py consolidated-plan.md consolidated-plan.pdf" in (ROOT / "README.md").read_text(encoding="utf-8"), "Exact PDF render command missing from README")
    require("Desired catalogue and last live snapshot" in project and "110" in project and "106" in project, "Desired/live Project distinction is not recorded")
    require("incomplete and unresolved" not in consolidated.lower(), "Stale incomplete-review wording remains")
    require("forced rls" in consolidated.lower() and "before b1" in consolidated.lower(), "RLS-before-B1 contract missing")
    require("Immediate Alan decisions" in consolidated and "Later Alan decisions" in consolidated and "External dependencies" in consolidated, "Decision timing lanes missing from consolidated plan")
    require("Founder outcomes, Alan's remaining technical ownership" in consolidated, "Affected WP decision-resolution sections are missing")
    require("P13-07 is the sole Joint-implementation exception" in consolidated, "P13-07 ownership exception narrative missing")
    require("Eligible for isolated, uncommitted, synthetic/no-invented-content preparation only" in consolidated, "Neutral isolated local-preparation contract missing")
    require("Luke-owned PRs that may begin now" not in consolidated, "Unwanted standalone Luke local-start wording leaked into canonical output")
    pdf_path = ROOT / "consolidated-plan.pdf"
    require(pdf_path.exists() and pdf_path.stat().st_size > 500_000, "Consolidated PDF missing or implausibly small")


def main() -> None:
    validate_data()
    validate_files()
    if errors:
        print("Programme validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(
        f"Programme validation passed: {len(data.WORK_PACKAGES)} work packages, "
        f"{len(data.PROPOSED_PRS)} proposed PRs, {len(data.DECISIONS)} decisions, "
        f"{len(data.GATES)} gates, {len(data.AUTHORSHIP_MATRIX)} authorship rows."
    )


if __name__ == "__main__":
    main()
