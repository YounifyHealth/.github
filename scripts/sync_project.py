#!/usr/bin/env python3
"""Idempotently synchronize the Natalyx MVP reshape planning Project.

Dry-run is the default.  ``--apply`` creates/updates only Project metadata,
draft planning items, and links to the already-existing PRs/issues declared in
``programme_data.py``.  It never creates implementation issues or PRs and it
never edits repository content, branches, workflows, or cloud resources.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import programme_data as data  # noqa: E402


ORG = "NatalyxPlatform"
PROJECT_NUMBER = 3
EXPECTED_PROJECT_ID = "PVT_kwDOEAWZDM4BYbai"
COLORS = ["BLUE", "GREEN", "PURPLE", "YELLOW", "ORANGE", "RED", "PINK", "GRAY"]


def run_gh_graphql(
    query: str,
    variables: dict[str, Any] | None = None,
    *,
    attempts: int = 4,
) -> dict[str, Any]:
    """Run GraphQL through the authenticated GitHub CLI with bounded retries."""
    payload: dict[str, Any] = {"query": query}
    if variables:
        payload["variables"] = variables
    last_error = ""
    for attempt in range(1, attempts + 1):
        proc = subprocess.run(
            ["gh", "api", "graphql", "--input", "-"],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        if proc.returncode == 0:
            response = json.loads(proc.stdout)
            if not response.get("errors"):
                return response["data"]
            last_error = json.dumps(response["errors"], sort_keys=True)
        else:
            last_error = proc.stderr.strip() or proc.stdout.strip()
        if attempt < attempts:
            time.sleep(attempt)
    raise RuntimeError(f"GitHub GraphQL failed after {attempts} attempt(s): {last_error}")


def run_gh_rest(path: str) -> dict[str, Any]:
    last_error = ""
    for attempt in range(1, 5):
        proc = subprocess.run(
            ["gh", "api", path],
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        if proc.returncode == 0:
            return json.loads(proc.stdout)
        last_error = proc.stderr.strip() or proc.stdout.strip()
        if attempt < 4:
            time.sleep(attempt)
    raise RuntimeError(f"GitHub REST failed after 4 attempts for {path}: {last_error}")


PROJECT_QUERY = """
query($org: String!, $number: Int!, $after: String) {
  organization(login: $org) {
    projectV2(number: $number) {
      id title url shortDescription readme closed
      fields(first: 100) {
        nodes {
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { options { id name } }
        }
      }
      items(first: 100, after: $after) {
        totalCount
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          fieldValues(first: 30) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
          content {
            ... on DraftIssue { id title body }
            ... on PullRequest { id title url repository { nameWithOwner } }
            ... on Issue { id title url repository { nameWithOwner } }
          }
        }
      }
    }
  }
}
"""


def inspect_project() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    after: str | None = None
    project: dict[str, Any] | None = None
    while True:
        result = run_gh_graphql(
            PROJECT_QUERY,
            {"org": ORG, "number": PROJECT_NUMBER, "after": after},
        )
        current = result["organization"]["projectV2"]
        if current is None:
            raise RuntimeError(f"Project {ORG} #{PROJECT_NUMBER} not found")
        project = current
        items.extend(current["items"]["nodes"])
        page = current["items"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        after = page["endCursor"]
    assert project is not None
    project["items"]["nodes"] = items
    return project, items


def text_list(values: list[str] | tuple[str, ...], empty: str = "None") -> str:
    return ", ".join(values) if values else empty


def bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def clipped(value: str, limit: int = 1000) -> str:
    value = value.strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def draft_key(title: str) -> str:
    """Return the immutable bracketed programme identifier for a draft."""
    if not title.startswith("[") or "]" not in title:
        raise RuntimeError(f"Draft title lacks a stable bracketed identifier: {title!r}")
    return title.split("]", 1)[0] + "]"


def item_field_values(item: dict[str, Any]) -> dict[str, str]:
    values: dict[str, str] = {}
    for node in item.get("fieldValues", {}).get("nodes", []):
        if not node or not node.get("field"):
            continue
        value = node.get("name") if node.get("name") is not None else node.get("text")
        if value is not None:
            values[node["field"]["name"]] = value
    return values


def owner(value: str | None) -> str:
    value = (value or "").strip()
    if value.startswith("Luke"):
        return "Luke"
    if value.startswith("Alan"):
        return "Alan"
    if value == "Joint" or ("Luke" in value and "Alan" in value):
        return "Joint"
    if not value or value == "N/A":
        return "N/A"
    return "External / TBD"


def repo_option(value: str) -> str:
    mapping = {
        ".github": ".github",
        "app": "natalyx-app",
        "infra": "natalyx-infra",
        "intelligence": "natalyx-intelligence",
        "learn": "natalyx-learn-resources",
        "design-system": "natalyx-design-system",
        "NatalyxPlatform/.github": ".github",
        "NatalyxPlatform/natalyx-app": "natalyx-app",
        "NatalyxPlatform/natalyx-infra": "natalyx-infra",
        "NatalyxPlatform/natalyx-intelligence": "natalyx-intelligence",
        "NatalyxPlatform/natalyx-learn-resources": "natalyx-learn-resources",
        "NatalyxPlatform/natalyx-design-system": "natalyx-design-system",
    }
    return mapping.get(value, "Multiple / external")


def plan_path(filename: str) -> str:
    return str(data.PLAN_ROOT + "/" + filename)


def wp_filename(wp_id: str) -> str:
    return data.plan_filename(wp_id)


def wp_dependencies(wp_id: str) -> list[str]:
    pr_by_id = {pr["id"]: pr for pr in data.PROPOSED_PRS}
    dependencies: set[str] = set()
    for pr in data.PROPOSED_PRS:
        if pr["wp"] != wp_id:
            continue
        for dep in pr["deps"]:
            dep_wp = pr_by_id[dep]["wp"]
            if dep_wp != wp_id:
                dependencies.add(dep_wp)
    return sorted(dependencies)


def wp_gate(wp_id: str) -> str:
    order = {"Pre-A0": 0, "A0": 1, "A1": 2, "A2": 3, "B1": 4, "B2": 5, "Post-B2": 6}
    gates = {pr["gate"] for pr in data.PROPOSED_PRS if pr["wp"] == wp_id}
    return min(gates, key=lambda gate: order[gate])


def item_record(
    title: str,
    body: str,
    fields: dict[str, str],
    *,
    content_url: str | None = None,
    content_api: str | None = None,
) -> dict[str, Any]:
    return {
        "title": title,
        "body": body,
        "fields": {key: clipped(value) for key, value in fields.items() if value},
        "content_url": content_url,
        "content_api": content_api,
    }


def build_items() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    pr_by_id = {pr["id"]: pr for pr in data.PROPOSED_PRS}

    for wp in data.WORK_PACKAGES:
        children = [pr["id"] for pr in data.PROPOSED_PRS if pr["wp"] == wp["id"]]
        decision_ids = sorted({d["id"] for d in data.DECISIONS if set(d["affected"]) & set(children)})
        body = "\n\n".join(
            [
                f"# {wp['id']} — {wp['title']}",
                f"**Outcome:** {wp['outcome']}",
                f"**Problem:** {wp['problem']}",
                f"**Child PRs:** {text_list(children)}",
                f"**Blocking decisions/checkpoints:** {text_list(decision_ids)}",
                f"**Plan:** `{plan_path(wp_filename(wp['id']))}`",
                "**Sign-off:** Alan's implementation/review ownership remains proposed until he reviews this consolidated programme; Luke is final product/architecture approver.",
            ]
        )
        records.append(
            item_record(
                f"[{wp['id']}] {wp['title']}",
                body,
                {
                    "Item type": "Work package",
                    "Work package": wp["id"],
                    "Target repository": "Multiple / external",
                    "DRI": "Joint",
                    "Implementer": "N/A",
                    "Programme reviewer": "Joint",
                    "Final approver": "Luke",
                    "Dependencies": text_list(wp_dependencies(wp["id"])),
                    "Programme gate": wp_gate(wp["id"]),
                    "Size": "N/A",
                    "Blocking decision": text_list(decision_ids),
                    "Source / salvage PR": text_list(wp["salvage"]),
                    "Plan document path": plan_path(wp_filename(wp["id"])),
                    "Readiness": "Needs plan approval",
                    "Disposition": "Programme baseline",
                },
            )
        )

    for pr in data.PROPOSED_PRS:
        body = "\n\n".join(
            [
                f"# {pr['id']} — {pr['title']}",
                f"**Objective:** {pr['objective']}",
                "**Scope**\n" + bullets(pr["scope"]),
                f"**Dependencies:** {text_list(pr['deps'])}",
                f"**Blocking decisions/checkpoints:** {text_list(pr['blocked_by'])}",
                f"**Gate / size:** {pr['gate']} / {pr['size']}",
                "**Acceptance / test plan**\n" + bullets(pr["tests"]),
                f"**Plan:** `{plan_path(wp_filename(pr['wp']))}`",
                "**Ownership note:** Proposed only until Alan reviews/signs off the consolidated programme. No implementation is authorized by this draft item.",
            ]
        )
        records.append(
            item_record(
                f"[{pr['id']}] {pr['title']}",
                body,
                {
                    "Item type": "Proposed PR",
                    "Work package": pr["wp"],
                    "Target repository": repo_option(pr["repo"]),
                    "Proposed PR ID": pr["id"],
                    "DRI": owner(pr["dri"]),
                    "Implementer": owner(pr["implementer"]),
                    "Programme reviewer": owner(pr["reviewer"]),
                    "Final approver": owner(pr["approver"]),
                    "Dependencies": text_list(pr["deps"]),
                    "Programme gate": pr["gate"],
                    "Size": pr["size"],
                    "Blocking decision": text_list(pr["blocked_by"]),
                    "Source / salvage PR": text_list(pr["sources"]),
                    "Plan document path": plan_path(wp_filename(pr["wp"])),
                    "Readiness": pr["readiness"],
                    "Disposition": "Proposed",
                },
            )
        )

    for existing in data.EXISTING_PRS:
        repo_name = existing["repo"].split("/", 1)[1]
        api = f"repos/{existing['repo']}/pulls/{existing['number']}"
        disposition_text = existing["disposition"].lower()
        if "prefer direct" in disposition_text or "retain for direct" in disposition_text:
            disposition = "Direct reuse"
        elif "retain" in disposition_text and "selective port" not in disposition_text:
            disposition = "Retain pending review"
        else:
            disposition = "Selective port"
        body = "\n\n".join(
            [
                f"**Programme extraction record:** `{existing['key']}` at `{existing['sha']}`.",
                f"**Useful:** {existing['useful']}",
                f"**Reusable:** {existing['reusable']}",
                f"**Unsafe unchanged:** {existing['unsafe']}",
                f"**Destination PRs:** {text_list(existing['destinations'])}",
                f"**Review state:** {existing['review']}",
                f"**Disposition:** {existing['disposition']}",
                f"**Close only when:** {existing['close_when']}",
                f"**Extraction ledger:** `{plan_path('existing-pr-extraction-ledger.md')}`",
            ]
        )
        records.append(
            item_record(
                existing["title"],
                body,
                {
                    "Item type": "Existing PR",
                    "Work package": "Programme",
                    "Target repository": repo_name,
                    "DRI": "Joint",
                    "Implementer": "N/A",
                    "Programme reviewer": "Joint",
                    "Final approver": "Luke",
                    "Dependencies": "Extraction destinations: " + text_list(existing["destinations"]),
                    "Programme gate": "Pre-A0",
                    "Size": "N/A",
                    "Blocking decision": "CHECK-ALAN-122-124" if existing["number"] in {122, 124} and repo_name == "natalyx-app" else "None",
                    "Source / salvage PR": f"{existing['url']} @ {existing['sha']}",
                    "Plan document path": plan_path("existing-pr-extraction-ledger.md"),
                    "Readiness": "Awaiting reconciliation" if existing["number"] in {122, 124} and repo_name == "natalyx-app" else "Retained for salvage",
                    "Disposition": disposition,
                },
                content_url=existing["url"],
                content_api=api,
            )
        )

    for issue in data.RELATED_ISSUES:
        api = f"repos/{issue['repo']}/issues/{issue['number']}"
        body = "\n\n".join(
            [
                f"**Existing dependency issue:** {issue['note']}",
                f"**Destination:** {issue['destination']}",
                f"**Plan:** `{plan_path(wp_filename(issue['wp']))}`",
            ]
        )
        records.append(
            item_record(
                issue["title"],
                body,
                {
                    "Item type": "Existing issue",
                    "Work package": issue["wp"],
                    "Target repository": repo_option(issue["repo"]),
                    "DRI": "Joint",
                    "Implementer": "N/A",
                    "Programme reviewer": "Joint",
                    "Final approver": "Luke",
                    "Dependencies": issue["destination"],
                    "Programme gate": pr_by_id[issue["destination"].split("/")[0]]["gate"],
                    "Size": "N/A",
                    "Source / salvage PR": issue["url"],
                    "Plan document path": plan_path(wp_filename(issue["wp"])),
                    "Blocking decision": "None",
                    "Readiness": "Retained for salvage",
                    "Disposition": "Retain pending review",
                },
                content_url=issue["url"],
                content_api=api,
            )
        )

    for decision in data.DECISIONS:
        affected_wps = {pr_by_id[pr_id]["wp"] for pr_id in decision["affected"]}
        affected_repos = {repo_option(pr_by_id[pr_id]["repo"]) for pr_id in decision["affected"]}
        wp_value = next(iter(affected_wps)) if len(affected_wps) == 1 else "Programme"
        repo_value = next(iter(affected_repos)) if len(affected_repos) == 1 else "Multiple / external"
        body = "\n\n".join(
            [
                f"# {decision['id']} — {decision['title']}",
                f"**Question:** {decision['question']}",
                f"**Recommendation:** {decision['recommendation']}",
                f"**Affected PRs:** {text_list(decision['affected'])}",
                f"**Resolve by:** {decision['latest']}",
                f"**Owner / proposer:** {decision['owner']} / {decision['proposer']}",
                f"**Decision register:** `{plan_path('consolidated-plan.md')}`",
            ]
        )
        records.append(
            item_record(
                f"[DECISION {decision['id']}] {decision['title']}",
                body,
                {
                    "Item type": "Decision",
                    "Work package": wp_value,
                    "Target repository": repo_value,
                    "DRI": owner(decision["owner"]),
                    "Implementer": "N/A",
                    "Programme reviewer": owner(decision["proposer"]),
                    "Final approver": owner(decision["owner"]),
                    "Dependencies": "Blocks: " + text_list(decision["affected"]),
                    "Programme gate": "N/A",
                    "Size": "N/A",
                    "Blocking decision": decision["id"],
                    "Source / salvage PR": "Decision register; affected PRs: " + text_list(decision["affected"]),
                    "Plan document path": plan_path("consolidated-plan.md"),
                    "Readiness": "Blocked by decision",
                    "Disposition": "Decision needed",
                },
            )
        )

    checkpoint = data.RECONCILIATION_CHECKPOINT
    body = "\n\n".join(
        [
            f"# {checkpoint['id']} — {checkpoint['title']}",
            f"**State:** {checkpoint['status']}",
            f"**Blocks:** {text_list(checkpoint['blocks'])}",
            "**Recording contract**\n" + bullets(checkpoint["recording"]),
            "**Complete only when**\n" + bullets(checkpoint["complete_when"]),
            f"**Efficiency rule:** {checkpoint['efficiency']}",
            f"**Ledger:** `{plan_path('existing-pr-extraction-ledger.md')}`",
        ]
    )
    records.append(
        item_record(
            f"[CHECKPOINT] {checkpoint['title']}",
            body,
            {
                "Item type": "Review checkpoint",
                "Work package": "Programme",
                "Target repository": "natalyx-app",
                "DRI": owner(checkpoint["owner"]),
                "Implementer": "N/A",
                "Programme reviewer": "Joint",
                "Final approver": owner(checkpoint["approver"]),
                "Dependencies": "PRs app#122 and app#124",
                "Programme gate": "Pre-A0",
                "Size": "N/A",
                "Blocking decision": checkpoint["id"],
                "Source / salvage PR": "app#122, app#124",
                "Plan document path": plan_path("existing-pr-extraction-ledger.md"),
                "Readiness": "Awaiting reconciliation",
                "Disposition": "Checkpoint",
            },
        )
    )

    for gate in data.GATES:
        body = "\n\n".join(
            [
                f"# Gate {gate['id']} — {gate['title']}",
                f"**Prerequisites:** {text_list(gate['prerequisites'])}",
                f"**Blocking decisions:** {text_list(gate['decisions'])}",
                "**Acceptance**\n" + bullets(gate["acceptance"]),
                "**Required evidence**\n" + bullets(gate["evidence"]),
                f"**Failure behavior:** {gate['failure']}",
                f"**Owner / verifier:** {gate['owner']} / {gate['verifier']}",
                f"**Gate contract:** `{plan_path('consolidated-plan.md')}`",
            ]
        )
        records.append(
            item_record(
                f"[GATE {gate['id']}] {gate['title']}",
                body,
                {
                    "Item type": "Programme gate",
                    "Work package": "Programme",
                    "Target repository": "Multiple / external",
                    "DRI": owner(gate["owner"]),
                    "Implementer": "N/A",
                    "Programme reviewer": owner(gate["verifier"]),
                    "Final approver": owner(gate["verifier"]),
                    "Dependencies": text_list(gate["prerequisites"]),
                    "Programme gate": gate["id"],
                    "Size": "N/A",
                    "Blocking decision": text_list(gate["decisions"]),
                    "Source / salvage PR": "Programme gate contract; prerequisites: " + text_list(gate["prerequisites"]),
                    "Plan document path": plan_path("consolidated-plan.md"),
                    "Readiness": "Dependencies unmet",
                    "Disposition": "Gate criterion",
                },
            )
        )

    for cleanup in data.CLEANUP_TASKS:
        body = "\n\n".join(
            [
                f"# {cleanup['id']} — {cleanup['title']}",
                f"**Dependencies:** {text_list(cleanup['deps'])}",
                "**Safety:** No PR, branch or worktree may be closed/deleted until its extraction conditions and explicit team confirmation are complete.",
                f"**Ledger:** `{plan_path('existing-pr-extraction-ledger.md')}`",
            ]
        )
        records.append(
            item_record(
                f"[CLEANUP {cleanup['id']}] {cleanup['title']}",
                body,
                {
                    "Item type": "Cleanup task",
                    "Work package": "Programme",
                    "Target repository": "Multiple / external",
                    "DRI": owner(cleanup["owner"]),
                    "Implementer": "N/A",
                    "Programme reviewer": "Joint",
                    "Final approver": "Luke",
                    "Dependencies": text_list(cleanup["deps"]),
                    "Programme gate": "Post-B2",
                    "Size": "N/A",
                    "Source / salvage PR": "Existing PR extraction ledger",
                    "Blocking decision": "None",
                    "Plan document path": plan_path("existing-pr-extraction-ledger.md"),
                    "Readiness": "Dependencies unmet",
                    "Disposition": "Cleanup only",
                },
            )
        )

    titles = [draft_key(record["title"]) for record in records if not record["content_url"]]
    duplicates = [title for title, count in Counter(titles).items() if count > 1]
    if duplicates:
        raise RuntimeError(f"Duplicate draft titles: {duplicates}")
    if len(records) != 106:
        raise RuntimeError(f"Expected 106 Project records, built {len(records)}")
    return records


def create_field(project_id: str, spec: dict[str, Any]) -> None:
    field_type = "SINGLE_SELECT" if spec["type"] == "single" else "TEXT"
    input_value: dict[str, Any] = {
        "projectId": project_id,
        "dataType": field_type,
        "name": spec["name"],
    }
    if spec["type"] == "single":
        input_value["singleSelectOptions"] = [
            {
                "name": name,
                "color": COLORS[index % len(COLORS)],
                "description": f"Programme value: {name}",
            }
            for index, name in enumerate(spec["options"])
        ]
    mutation = """
    mutation($input: CreateProjectV2FieldInput!) {
      createProjectV2Field(input: $input) {
        projectV2Field {
          ... on ProjectV2FieldCommon { id name dataType }
        }
      }
    }
    """
    # Creation mutations are deliberately single-shot.  If a response is lost,
    # the next whole-script run re-inspects by stable field name before trying
    # again, avoiding blind duplicate creation.
    run_gh_graphql(mutation, {"input": input_value}, attempts=1)


def update_project_metadata(project_id: str) -> None:
    mutation = """
    mutation($input: UpdateProjectV2Input!) {
      updateProjectV2(input: $input) { projectV2 { id } }
    }
    """
    readme = "\n".join(
        [
            "Planning control plane for the Natalyx MVP Product Flow Reshape.",
            "",
            "Canonical package: `.github` branch `plan/mvp-product-flow-reshape`.",
            "No implementation is authorized until Alan reviews the consolidated plan and Luke accepts it.",
            "Readiness is separate from Status; all new items begin in Todo.",
        ]
    )
    run_gh_graphql(
        mutation,
        {
            "input": {
                "projectId": project_id,
                "shortDescription": "Planning-only control plane for the MVP Product Flow Reshape; implementation awaits Alan review and Luke approval.",
                "readme": readme,
            }
        },
    )


def create_draft(project_id: str, record: dict[str, Any]) -> dict[str, str]:
    mutation = """
    mutation($project: ID!, $title: String!, $body: String!) {
      addProjectV2DraftIssue(input: {projectId: $project, title: $title, body: $body}) {
        projectItem { id content { ... on DraftIssue { id title } } }
      }
    }
    """
    result = run_gh_graphql(
        mutation,
        {"project": project_id, "title": record["title"], "body": record["body"]},
        attempts=1,
    )
    item = result["addProjectV2DraftIssue"]["projectItem"]
    return {"item_id": item["id"], "content_id": item["content"]["id"]}


def update_draft(content_id: str, record: dict[str, Any]) -> None:
    mutation = """
    mutation($input: UpdateProjectV2DraftIssueInput!) {
      updateProjectV2DraftIssue(input: $input) { draftIssue { id } }
    }
    """
    run_gh_graphql(
        mutation,
        {"input": {"draftIssueId": content_id, "title": record["title"], "body": record["body"]}},
    )


def add_content(project_id: str, content_id: str) -> str:
    mutation = """
    mutation($project: ID!, $content: ID!) {
      addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
        item { id }
      }
    }
    """
    # As with draft creation, never blindly retry an uncertain add mutation;
    # rerunning the script reconciles the real linked URL first.
    result = run_gh_graphql(mutation, {"project": project_id, "content": content_id}, attempts=1)
    return result["addProjectV2ItemById"]["item"]["id"]


def update_item_fields(
    project_id: str,
    item_id: str,
    values: dict[str, str],
    field_map: dict[str, dict[str, Any]],
) -> None:
    requested = {"Status": "Todo", **values}
    clauses: list[str] = []
    for index, (name, value) in enumerate(requested.items()):
        field = field_map.get(name)
        if field is None:
            raise RuntimeError(f"Missing Project field {name!r}")
        if field["dataType"] == "SINGLE_SELECT":
            option_map = {option["name"]: option["id"] for option in field.get("options", [])}
            if value not in option_map:
                raise RuntimeError(f"Missing option {value!r} for Project field {name!r}")
            encoded = f"{{singleSelectOptionId:{json.dumps(option_map[value])}}}"
        else:
            encoded = f"{{text:{json.dumps(clipped(value))}}}"
        clauses.append(
            f"u{index}: updateProjectV2ItemFieldValue(input:{{"
            f"projectId:{json.dumps(project_id)},itemId:{json.dumps(item_id)},"
            f"fieldId:{json.dumps(field['id'])},value:{encoded}}})"
            "{projectV2Item{id}}"
        )
    run_gh_graphql("mutation {" + " ".join(clauses) + "}")


def content_node(record: dict[str, Any]) -> str:
    payload = run_gh_rest(record["content_api"])
    return payload["node_id"]


def sync(apply: bool) -> dict[str, Any]:
    records = build_items()
    project, existing_items = inspect_project()
    if project["id"] != EXPECTED_PROJECT_ID or project["title"] != data.PROJECT_CONVENTIONS["project"]:
        raise RuntimeError(f"Unexpected Project authority: {project['id']} / {project['title']}")

    field_map = {field["name"]: field for field in project["fields"]["nodes"] if field}
    missing_fields = [spec["name"] for spec in data.PROJECT_FIELDS if spec["name"] not in field_map]
    for spec in data.PROJECT_FIELDS:
        field = field_map.get(spec["name"])
        if not field:
            continue
        expected_type = "SINGLE_SELECT" if spec["type"] == "single" else "TEXT"
        if field["dataType"] != expected_type:
            raise RuntimeError(f"Field {spec['name']!r} has {field['dataType']}, expected {expected_type}")
        if spec["type"] == "single":
            actual_options = {option["name"] for option in field.get("options", [])}
            missing_options = set(spec["options"]) - actual_options
            if missing_options:
                raise RuntimeError(f"Field {spec['name']!r} is missing options {sorted(missing_options)}")
    existing_drafts = {
        draft_key(item["content"]["title"]): item
        for item in existing_items
        if item.get("content") and not item["content"].get("url")
    }
    existing_links = {
        item["content"]["url"]: item
        for item in existing_items
        if item.get("content") and item["content"].get("url")
    }
    missing_drafts = [record for record in records if not record["content_url"] and draft_key(record["title"]) not in existing_drafts]
    missing_links = [record for record in records if record["content_url"] and record["content_url"] not in existing_links]

    summary: dict[str, Any] = {
        "mode": "apply" if apply else "dry-run",
        "project": project["url"],
        "project_id": project["id"],
        "planned_items": len(records),
        "existing_items_before": len(existing_items),
        "missing_fields": missing_fields,
        "missing_drafts": len(missing_drafts),
        "missing_links": len(missing_links),
    }
    if not apply:
        return summary

    print(f"Project metadata: updating {project['url']}", flush=True)
    update_project_metadata(project["id"])
    for index, field_name in enumerate(missing_fields, start=1):
        spec = next(spec for spec in data.PROJECT_FIELDS if spec["name"] == field_name)
        print(f"Fields {index}/{len(missing_fields)}: creating {field_name}", flush=True)
        create_field(project["id"], spec)

    project, existing_items = inspect_project()
    field_map = {field["name"]: field for field in project["fields"]["nodes"] if field}
    existing_drafts = {
        draft_key(item["content"]["title"]): item
        for item in existing_items
        if item.get("content") and not item["content"].get("url")
    }
    existing_links = {
        item["content"]["url"]: item
        for item in existing_items
        if item.get("content") and item["content"].get("url")
    }

    synchronized: list[tuple[dict[str, Any], str]] = []
    for index, record in enumerate(records, start=1):
        if record["content_url"]:
            existing = existing_links.get(record["content_url"])
            if existing:
                item_id = existing["id"]
                action = "reuse linked"
            else:
                item_id = add_content(project["id"], content_node(record))
                action = "link"
        else:
            existing = existing_drafts.get(draft_key(record["title"]))
            if existing:
                item_id = existing["id"]
                update_draft(existing["content"]["id"], record)
                action = "update draft"
            else:
                created = create_draft(project["id"], record)
                item_id = created["item_id"]
                action = "create draft"
        synchronized.append((record, item_id))
        print(f"Items {index}/{len(records)}: {action} {record['title']}", flush=True)

    for index, (record, item_id) in enumerate(synchronized, start=1):
        update_item_fields(project["id"], item_id, record["fields"], field_map)
        print(f"Metadata {index}/{len(synchronized)}: {record['title']}", flush=True)

    final_project, final_items = inspect_project()
    final_fields = {field["name"] for field in final_project["fields"]["nodes"] if field}
    final_drafts = Counter(
        draft_key(item["content"]["title"])
        for item in final_items
        if item.get("content") and not item["content"].get("url")
    )
    final_links = Counter(
        item["content"]["url"]
        for item in final_items
        if item.get("content") and item["content"].get("url")
    )
    missing_titles = [record["title"] for record in records if not record["content_url"] and final_drafts[draft_key(record["title"])] != 1]
    missing_urls = [record["content_url"] for record in records if record["content_url"] and final_links[record["content_url"]] != 1]
    missing_final_fields = [spec["name"] for spec in data.PROJECT_FIELDS if spec["name"] not in final_fields]
    if missing_titles or missing_urls or missing_final_fields or len(final_items) != len(records):
        raise RuntimeError(
            "Final Project validation failed: "
            f"items={len(final_items)} expected={len(records)} "
            f"drafts={missing_titles} links={missing_urls} fields={missing_final_fields}"
        )

    required_for_all = {
        "Status",
        "Item type",
        "Work package",
        "Target repository",
        "DRI",
        "Implementer",
        "Programme reviewer",
        "Final approver",
        "Dependencies",
        "Programme gate",
        "Size",
        "Blocking decision",
        "Source / salvage PR",
        "Plan document path",
        "Readiness",
        "Disposition",
    }
    incomplete_items: list[str] = []
    type_counts: Counter[str] = Counter()
    for item in final_items:
        values = item_field_values(item)
        title = item["content"]["title"]
        missing_values = sorted(name for name in required_for_all if not values.get(name))
        if values.get("Item type") == "Proposed PR" and not values.get("Proposed PR ID"):
            missing_values.append("Proposed PR ID")
        if values.get("Status") != "Todo":
            missing_values.append("Status=Todo")
        if missing_values:
            incomplete_items.append(f"{title}: {', '.join(sorted(set(missing_values)))}")
        if values.get("Item type"):
            type_counts[values["Item type"]] += 1
    expected_types = Counter(
        {
            "Work package": 14,
            "Proposed PR": 50,
            "Existing PR": 9,
            "Existing issue": 2,
            "Decision": 22,
            "Review checkpoint": 1,
            "Programme gate": 5,
            "Cleanup task": 3,
        }
    )
    if incomplete_items or type_counts != expected_types:
        raise RuntimeError(
            "Final field-value validation failed: "
            f"incomplete={incomplete_items} type_counts={dict(type_counts)} expected={dict(expected_types)}"
        )

    summary.update(
        {
            "existing_items_after": len(final_items),
            "fields_after": len(final_fields),
            "custom_fields_after": len([name for name in final_fields if name in {spec['name'] for spec in data.PROJECT_FIELDS}]),
            "validated_unique_items": len(records),
            "validated_item_types": dict(sorted(type_counts.items())),
            "all_statuses": "Todo",
            "required_field_values": "complete",
            "validation": "passed",
        }
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply idempotent Project mutations")
    args = parser.parse_args()
    if args.apply and getattr(data, "PROJECT_BENCHED", False):
        raise SystemExit(
            "Project 3 is benched pending Drive-plan approval. Do not apply the active sync until the programme is jointly reactivated."
        )
    print(json.dumps(sync(args.apply), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
