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
    require(len(pr_id_set) == len(pr_ids), f"Duplicate PR IDs: {[item for item, count in Counter(pr_ids).items() if count > 1]}")
    for pr in data.PROPOSED_PRS:
        require(bool(re.fullmatch(r"P\d{2}-\d{2}", pr["id"])), f"Bad PR ID: {pr['id']}")
        require(pr["wp"] in wp_ids, f"{pr['id']} unknown work package {pr['wp']}")
        for key in ("title", "repo", "objective", "gate", "size", "dri", "implementer", "reviewer", "approver", "readiness"):
            require(bool(pr.get(key)), f"{pr['id']} missing {key}")
        require(bool(pr["scope"]), f"{pr['id']} missing scope")
        require(bool(pr["non_goals"]), f"{pr['id']} missing non-goals")
        require(bool(pr["tests"]), f"{pr['id']} missing tests")
        for dep in pr["deps"]:
            require(dep in pr_ids, f"{pr['id']} unknown dependency {dep}")
    topological_ids()

    decision_ids = {item["id"] for item in data.DECISIONS}
    require(len(decision_ids) == len(data.DECISIONS), "Duplicate decision IDs")
    for decision in data.DECISIONS:
        require(decision["owner"], f"{decision['id']} missing owner")
        require(decision["affected"], f"{decision['id']} affects no PR")
        for pr_id in decision["affected"]:
            require(pr_id in pr_ids, f"{decision['id']} references unknown {pr_id}")

    allowed_blocks = decision_ids | {data.RECONCILIATION_CHECKPOINT["id"]}
    for pr in data.PROPOSED_PRS:
        for blocker in pr["blocked_by"]:
            require(blocker in allowed_blocks, f"{pr['id']} unknown blocker {blocker}")

    gate_ids = {gate["id"] for gate in data.GATES}
    require(gate_ids == {"A0", "A1", "A2", "B1", "B2"}, f"Unexpected gate set {gate_ids}")
    for gate in data.GATES:
        require(gate["owner"] and gate["verifier"], f"{gate['id']} missing owner/verifier")
        require(gate["acceptance"] and gate["evidence"] and gate["failure"], f"{gate['id']} incomplete contract")
        for prerequisite in gate["prerequisites"]:
            require(prerequisite in pr_id_set | gate_ids, f"{gate['id']} unknown prerequisite {prerequisite}")
        for decision_id in gate["decisions"]:
            require(decision_id in decision_ids, f"{gate['id']} unknown decision {decision_id}")

    for item in data.CRITICAL_PATH + data.FIRST_THREE_IMPLEMENTATION_PRS:
        require(item in pr_ids, f"Critical/first item is not a PR: {item}")

    existing_keys = [item["key"] for item in data.EXISTING_PRS]
    for required in ["app#112", "app#117", "app#119", "app#121", "app#122", "app#123", "app#124", "ds#7", "ds#8"]:
        require(required in existing_keys, f"Missing extraction record {required}")
    pr122 = next((item for item in data.EXISTING_PRS if item["key"] == "app#122"), None)
    require(pr122 is not None and pr122["sha"] == "e85382150853cf4774948c55b91e330e7e69617e", "PR #122 latest SHA missing/wrong")
    pr124 = next((item for item in data.EXISTING_PRS if item["key"] == "app#124"), None)
    require(pr124 is not None and "incomplete" in pr124["review"].lower(), "PR #124 unfinished review not explicit")

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
    require(data.PROJECT_SYNC_RESULT["items"] == expected_project_items == 106, "Project sync item count is not 106")
    require(data.PROJECT_SYNC_RESULT["custom_fields"] == len(data.PROJECT_FIELDS) == 16, "Project custom field count mismatch")
    require(data.PROJECT_SYNC_RESULT["draft_items"] + data.PROJECT_SYNC_RESULT["linked_items"] == expected_project_items, "Project draft/link counts do not sum to total")
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
    for wp in data.WORK_PACKAGES:
        require(wp["id"] in consolidated, f"{wp['id']} missing from consolidated plan")
    for gate in data.GATES:
        require(f"Gate {gate['id']}" in consolidated, f"Gate {gate['id']} missing from consolidated plan")
        require(gate["id"] in project, f"Gate {gate['id']} missing from project structure")
    for decision in data.DECISIONS:
        require(decision["id"] in consolidated, f"{decision['id']} missing from consolidated plan")
    require(data.RECONCILIATION_CHECKPOINT["title"] in ledger, "Alan checkpoint missing from extraction ledger")
    require(data.RECONCILIATION_CHECKPOINT["title"] in consolidated, "Alan checkpoint missing from consolidated plan")
    require("e85382150853cf4774948c55b91e330e7e69617e" in ledger, "Latest PR #122 SHA missing from ledger")
    require("authorship" in consolidated.lower() and "provider packet" in consolidated.lower(), "Authorship matrix/coverage missing")
    require("consolidated-plan.md consolidated-plan.pdf" in (ROOT / "README.md").read_text(encoding="utf-8"), "Exact PDF render command missing from README")
    require("Live post-sync validation" in project and "All 106 items are Todo" in project, "Live Project validation is not recorded")
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
