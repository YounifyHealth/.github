#!/usr/bin/env python3
"""Reversibly bench Project 3 and remove local filesystem references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import programme_data as data  # noqa: E402
from scripts.sync_project import inspect_project, item_field_values, run_gh_graphql  # noqa: E402


def chunks(values: list[dict[str, str]], size: int = 12) -> list[list[dict[str, str]]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def clean_body(body: str) -> str:
    replacement = f"[MVP Fixes Drive review package]({data.DRIVE_PACKAGE_URL})"
    body = re.sub(r"`/Users/lukerhodes/[^`]+`", replacement, body)
    body = re.sub(r"/Users/lukerhodes/\S+", data.DRIVE_PACKAGE_URL, body)
    return body


def update_draft_bodies(items: list[dict[str, object]]) -> int:
    changes: list[dict[str, str]] = []
    for item in items:
        content = item.get("content") or {}
        if content.get("url") or not content.get("body") or "/Users/lukerhodes" not in content["body"]:
            continue
        changes.append(
            {
                "id": content["id"],
                "title": content["title"],
                "body": clean_body(content["body"]),
            }
        )
    for batch in chunks(changes):
        clauses = []
        for index, change in enumerate(batch):
            clauses.append(
                f"u{index}:updateProjectV2DraftIssue(input:{{"
                f"draftIssueId:{json.dumps(change['id'])},"
                f"title:{json.dumps(change['title'])},body:{json.dumps(change['body'])}}})"
                "{draftIssue{id}}"
            )
        run_gh_graphql("mutation{" + " ".join(clauses) + "}")
    return len(changes)


def clear_plan_paths(project_id: str, field_id: str, items: list[dict[str, object]]) -> int:
    targets = [
        {"item_id": item["id"]}
        for item in items
        if item_field_values(item).get("Plan document path")
    ]
    for batch in chunks(targets, 20):
        clauses = []
        for index, target in enumerate(batch):
            clauses.append(
                f"c{index}:clearProjectV2ItemFieldValue(input:{{"
                f"projectId:{json.dumps(project_id)},itemId:{json.dumps(target['item_id'])},"
                f"fieldId:{json.dumps(field_id)}}})"
                "{projectV2Item{id}}"
            )
        run_gh_graphql("mutation{" + " ".join(clauses) + "}")
    return len(targets)


def bench_project(project_id: str) -> None:
    mutation = """
    mutation($input: UpdateProjectV2Input!) {
      updateProjectV2(input: $input) {
        projectV2 { id closed shortDescription readme }
      }
    }
    """
    readme = "\n".join(
        [
            "# Benched pending Drive-plan approval",
            "",
            "Do not use this Project for implementation or assignment until Luke and Alan jointly approve the Drive review package.",
            "",
            f"- Consolidated overview: {data.DRIVE_OVERVIEW_URL}",
            f"- Markdown work packages: {data.DRIVE_MD_FOLDER_URL}",
            f"- PDF work packages: {data.DRIVE_PDF_FOLDER_URL}",
            "",
            "All prior local filesystem plan references have been removed. Reactivation requires an explicit review decision and a Drive-link-aware sync.",
        ]
    )
    run_gh_graphql(
        mutation,
        {
            "input": {
                "projectId": project_id,
                "closed": True,
                "shortDescription": "Benched pending Alan review of the Drive-only MVP Fixes plan; not an active implementation tracker.",
                "readme": readme,
            }
        },
    )


def main() -> None:
    project, items = inspect_project()
    field = next((field for field in project["fields"]["nodes"] if field and field["name"] == "Plan document path"), None)
    if not field:
        raise SystemExit("Plan document path field not found")
    updated_bodies = update_draft_bodies(items)
    cleared_paths = clear_plan_paths(project["id"], field["id"], items)
    bench_project(project["id"])

    verified, verified_items = inspect_project()
    remaining_paths = [item["content"]["title"] for item in verified_items if item_field_values(item).get("Plan document path")]
    remaining_local = [
        item["content"]["title"]
        for item in verified_items
        if item.get("content") and "/Users/lukerhodes" in (item["content"].get("body") or "")
    ]
    if not verified.get("closed") or remaining_paths or remaining_local:
        raise SystemExit(
            f"Bench verification failed: closed={verified.get('closed')} paths={remaining_paths} local_bodies={remaining_local}"
        )
    print(
        json.dumps(
            {
                "project": verified["url"],
                "closed": verified["closed"],
                "items_retained": len(verified_items),
                "draft_bodies_cleaned": updated_bodies,
                "plan_path_values_cleared": cleared_paths,
                "remaining_local_paths": 0,
                "drive_package": data.DRIVE_PACKAGE_URL,
                "verification": "passed",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
