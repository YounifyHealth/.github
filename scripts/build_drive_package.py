#!/usr/bin/env python3
"""Build the clean, Drive-first MVP Fixes review package.

This creates exactly fourteen standalone Markdown work-package plans, a concise
consolidated overview source, and the requested local folder structure.  PDFs
are rendered separately through Quarto's bundled Pandoc + LuaLaTeX so the
result follows the earlier AWS migration-plan convention.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import programme_data as data  # noqa: E402


PACKAGE_ROOT = ROOT / "output" / "drive" / "MVP Fixes"
MD_DIR = PACKAGE_ROOT / "MD Work Packages"
PDF_DIR = PACKAGE_ROOT / "PDF Work Packages"
SOURCE_DIR = ROOT / "output" / "source"
OVERVIEW_SOURCE = SOURCE_DIR / "Natalyx MVP Fixes - Consolidated Plan Overview.md"

LUKE_WPS = {"WP00", "WP05", "WP07", "WP08", "WP11", "WP12"}
ALAN_WPS = {wp["id"] for wp in data.WORK_PACKAGES} - LUKE_WPS


def ascii_dashes(text: str) -> str:
    return text.replace("\u2011", "-").replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-")


def safe_name(wp: dict[str, object], suffix: str) -> str:
    title = str(wp["title"])
    title = title.replace("/", " and ").replace(":", " -")
    title = re.sub(r"[^A-Za-z0-9 ,&()'\-]", "", title)
    return f"{wp['id']} - {title}.{suffix}"


def yaml_header(title: str, subtitle: str) -> str:
    return "\n".join(
        [
            "---",
            f"title: '\\plantitle{{{title}}}'",
            f'title-meta: "{title}"',
            f'subtitle: "{subtitle}"',
            'author: "L. Rhodes (plan owner) - A. Zhao (technical review requested)"',
            'date: "2026-07-10"',
            "---",
            "",
        ]
    )


def replace_project_links(text: str) -> str:
    text = re.sub(
        r"\[([^\]]+)\]\(https://github\.com/orgs/NatalyxPlatform/projects/3\?query=[^)]+\)",
        r"\1",
        text,
    )
    text = re.sub(
        r"\[MVP Product Flow Reshape\]\(https://github\.com/orgs/NatalyxPlatform/projects/3\)",
        "the benched GitHub planning board",
        text,
    )
    return text


def replace_local_paths(text: str) -> str:
    text = text.replace(
        "/Users/lukerhodes/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/validate_programme.py",
        "python scripts/validate_programme.py",
    )
    text = re.sub(
        r"/Users/lukerhodes/\.codex/worktrees/[^/]+/([^`|\n]+)",
        r"protected Codex worktree / \1",
        text,
    )
    text = text.replace("/Users/lukerhodes/Natalyx/", "Natalyx workspace / ")
    return text


def apply_drive_ownership(text: str, wp_id: str) -> str:
    if wp_id in LUKE_WPS:
        text = re.sub(r"^\| DRI \| .* \|$", "| DRI | Luke |", text, flags=re.MULTILINE)
        text = re.sub(
            r"^\| Implementer \| .* \|$",
            "| Implementer | Luke (proposed; pending joint approval) |",
            text,
            flags=re.MULTILINE,
        )
        text = re.sub(r"^\| Reviewer \| .* \|$", "| Reviewer | Alan |", text, flags=re.MULTILINE)
        text = re.sub(r"^\| Final approver \| .* \|$", "| Final approver | Joint |", text, flags=re.MULTILINE)
        text = re.sub(
            r"^\| (P\d{2}-\d{2}) \| .*? \| .*? \| .*? \| .*? \| (.*?) \|$",
            r"| \1 | Luke | Luke (proposed) | Alan | Joint | \2 |",
            text,
            flags=re.MULTILINE,
        )
        text = text.replace("Alan or named PR DRI", "Luke or named PR DRI")
        text = re.sub(
            r"(## Ownership recommendation\n\n).*?(\n\n\| PR \|)",
            r"\1Luke leads this work package, with Alan providing technical review. The split is proposed for review and can be amended before implementation begins.\2",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"Luke decides product/lifecycle/commercial/privacy/PHI/provider policy and accepts gates\. Alan proposes implementation design, decomposition, migrations, code, tests, rollout and repair\. This is a recommendation pending Alan's review/sign-off, not a compulsory assignment\.",
            "Luke leads implementation and product acceptance for this package; Alan reviews architecture, migration, security and failure behavior. This is a recommendation pending joint review, not a compulsory assignment.",
            text,
        )
    return text


def split_pipe_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip())
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return [cell.strip().replace("\\|", "|") for cell in cells]


def expand_state_transition_tables(text: str) -> str:
    """Turn nine-column transition tables into readable Markdown records."""
    expected = [
        "From",
        "To",
        "Actor",
        "Evidence",
        "Idempotency key",
        "Invalid transitions",
        "Audit event",
        "Retry",
        "Recovery",
    ]
    lines = text.splitlines()
    rendered: list[str] = []
    index = 0
    while index < len(lines):
        if split_pipe_row(lines[index]) != expected:
            rendered.append(lines[index])
            index += 1
            continue
        index += 2  # header + Markdown separator
        rows: list[list[str]] = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            cells = split_pipe_row(lines[index])
            if len(cells) == len(expected):
                rows.append(cells)
            index += 1
        for row in rows:
            rendered.extend(
                [
                    f"**Transition: `{row[0]}` -> `{row[1]}`**",
                    "",
                    f"- **Actor:** {row[2]}",
                    f"- **Evidence:** {row[3]}",
                    f"- **Idempotency key:** `{row[4]}`",
                    f"- **Invalid transitions:** {row[5]}",
                    f"- **Audit event:** `{row[6]}`",
                    f"- **Retry:** {row[7]}",
                    f"- **Recovery:** {row[8]}",
                    "",
                ]
            )
    return "\n".join(rendered)


def clean_work_package(wp: dict[str, object]) -> str:
    source = ROOT / data.plan_filename(str(wp["id"]))
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    text = "\n".join(lines).lstrip()
    text = re.sub(
        r"^> Planning-only execution contract\..*$",
        "> Review draft only. Ownership and sequencing remain recommendations until Luke and Alan approve the plan together.",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"^## \d+\.\s+", "## ", text, flags=re.MULTILINE)
    text = re.sub(r"^\| Project item \|.*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\| E-004 \|.*\n", "", text, flags=re.MULTILINE)
    text = re.sub(
        r"^- \[ \] The Project item has matching dependency, readiness, ownership, gate and disposition fields\.\n",
        "",
        text,
        flags=re.MULTILINE,
    )
    text = text.replace("objective acceptance criteria and Project item complete", "objective acceptance criteria and review record complete")
    text = text.replace("Project item / treatment", "Treatment")
    text = text.replace(
        "Use the organisation Project as the programme control plane and this repository-neutral package as the reviewable contract.",
        "Use the Drive review package as the approval surface; reactivate programme tracking only after the package is jointly accepted.",
    )
    text = text.replace("Freeze programme IDs used by the Project", "Freeze programme IDs used across the review package and future tracker")
    text = text.replace("document/project parity validator", "document/package parity validator")
    text = text.replace("Project/document identifier parity", "Drive package/document identifier parity")
    text = text.replace("keep the Project gate blocked", "keep the programme gate blocked")
    text = text.replace(
        "Re-sync the Project from the same canonical data.",
        "Regenerate the Drive review package from the same canonical data; reactivate tracking only after approval.",
    )
    text = text.replace("programme/governance evidence and Project control plane", "programme/governance evidence and future approved tracking")
    text = re.sub(
        r"^\| Plan file \| `[^`]+` \|$",
        f"| Plan file | `{safe_name(wp, 'md')}` |",
        text,
        flags=re.MULTILINE,
    )
    repaired_lines: list[str] = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 10 and re.fullmatch(r"P\d{2}-\d{2}", cells[2]) and cells[5] == cells[2]:
            cells[5] = "None"
            line = "| " + " | ".join(cells[1:-1]) + " |"
        repaired_lines.append(line)
    text = "\n".join(repaired_lines)
    text = expand_state_transition_tables(text)
    text = replace_project_links(text)
    text = replace_local_paths(text)
    text = apply_drive_ownership(text, str(wp["id"]))
    text = ascii_dashes(text)
    subtitle = f"Work Package {wp['number']:02d}: {wp['title']}"
    return yaml_header("Natalyx MVP Fixes", subtitle) + f"# {subtitle}\n\n" + text.strip() + "\n"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    clean_rows = [[ascii_dashes(str(cell)).replace("\n", " ") for cell in row] for row in rows]
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
            *["| " + " | ".join(row) + " |" for row in clean_rows],
        ]
    )


def bullets(values: list[str]) -> str:
    return "\n".join(f"- {ascii_dashes(value)}" for value in values)


def overview_markdown() -> str:
    wp_map = {wp["id"]: wp for wp in data.WORK_PACKAGES}
    pr_by_wp = {wp_id: [pr for pr in data.PROPOSED_PRS if pr["wp"] == wp_id] for wp_id in wp_map}
    ownership = {item["wp"]: item for item in data.WORK_PACKAGE_OWNERSHIP}

    summary_rows: list[list[str]] = []
    for wp in data.WORK_PACKAGES:
        wp_id = wp["id"]
        lead = "Luke" if wp_id in LUKE_WPS else "Alan"
        reviewer = "Alan" if lead == "Luke" else "Luke"
        gates = ", ".join(sorted({pr["gate"] for pr in pr_by_wp[wp_id]}))
        summary_rows.append([wp_id, wp["title"], str(len(pr_by_wp[wp_id])), lead, reviewer, gates])

    parts = [
        yaml_header("Natalyx MVP Fixes", "Consolidated plan overview - fourteen coordinated work packages"),
        "# Purpose and review request",
        "This is a planning document for cleaning up the current Natalyx MVP delivery surface without losing useful work or compounding the present architecture. It consolidates the programme into fourteen bounded work packages and fifty suggested pull requests. The detailed Markdown and PDF plan for each work package is supplied separately in the `MVP Fixes` Drive folder.",
        "The GitHub Project is deliberately benched until this plan is reviewed. Nothing in this document authorizes implementation, PR closure, branch cleanup, cloud changes, schema changes, payment activation, real-user use or PHI processing.",
        "The requested decision is simple: confirm the package boundaries, amend any technical assumptions or PR splits that are wrong, and agree the ownership/review split before implementation begins.",
        "# Current position",
        md_table(
            ["Area", "Current conclusion", "Planning consequence"],
            [
                ["Live dev", "The inspected endpoint returned ALB 503.", "Treat live recovery and known-revision evidence as Gate A0, separate from green CI."],
                ["PR 122", "Materially safer invitation/case-shell behavior, but not the final architecture.", "Selectively salvage tests and hardening after Alan's review is captured."],
                ["PR 124", "Valuable participant work, but it creates a paid-case-shaped record too early and weakens authorship/access boundaries.", "Do not merge unchanged; port behavior into the workspace-first plan."],
                ["Node 0", "Free exploration, Complete entitlement, commitment, payment and paid case are currently too entangled.", "Separate their entities and state machines before expanding UI."],
                ["Commercial", "The business-model document is design authority; no append-only money ledger or promotion authority exists yet.", "Keep prices/terms versioned and processor-neutral; no redirect or raw webhook can promote a case."],
                ["Documents/PHI", "Documents are metadata-only and the provider branch is unreviewed.", "Keep synthetic-only through A2, approved PII at B1, and PHI blocked until formal B2."],
            ],
        ),
        "# Architecture spine",
        bullets(
            [
                "Node 0 begins as a free workspace; opening it never creates a canonical paid case.",
                "Workspace, entitlement, commercial commitment, payment, case, invitation/claim, document and journey-stage lifecycles remain separate.",
                "Only `byos.workspace_promotion_authorized.v1` authorizes exactly one `enrollment_pending` case; browser redirects and raw processor callbacks never do.",
                "IP observations remain IP-attributed and provisional. GC confirmation appends a GC-authored revision; it never silently overwrites or upgrades the source.",
                "The app owns durable case truth, authorization and PHI policy. Intelligence returns advisory proposals only. Learn artifacts and design-system releases remain pinned repository contracts.",
                "PostgreSQL is production authority. Versioned, ordered migrations replace runtime DDL, with locking, checksums, expand/contract compatibility and forward repair.",
                "Real PII/PHI readiness is established by evidence gates and human acceptance, not by merge or deployment success.",
            ]
        ),
        "# Work-package map",
        md_table(["WP", "Work package", "Suggested PRs", "Proposed lead", "Reviewer", "Gate range"], summary_rows),
        "# Suggested ownership and reciprocal review",
        "This is the proposed working split for discussion, chosen to keep product/commercial/content-heavy work with Luke and foundation/security/data/runtime work with Alan while retaining reciprocal review:",
        md_table(
            ["Lead", "Work packages", "Primary responsibility", "Review partner"],
            [
                ["Luke", "WP00, WP05, WP07, WP08, WP11, WP12", "Programme reconciliation; Node 0 Free product boundary; commercial/payment contracts; Learn/design-system release; participant shell/cutover.", "Alan reviews technical architecture, migration, security and failure behavior."],
                ["Alan", "WP01, WP02, WP03, WP04, WP06, WP09, WP10, WP13", "CI/PostgreSQL; migrations; auth/invitations; workspace/case model; GC onboarding; documents/provider handoff; intelligence; deployment/gates.", "Luke reviews product, privacy, commercial, role, truth and release acceptance."],
            ],
        ),
        "External security, privacy, payment, finance, legal, accessibility or provider review remains mandatory where the detailed package names it. The split can be amended before implementation; it is not an assignment imposed by the plan.",
        "# Delivery sequence",
        md_table(
            ["Phase", "Work", "Can run in parallel", "Exit condition"],
            [
                ["Approval", "WP00 plan review and PR 122/124 reconciliation", "No implementation", "Luke and Alan accept or explicitly amend the package boundaries."],
                ["Foundation", "WP01, WP02 and A0 portions of WP13", "Learn/DS source work in WP11", "Current tests run on PostgreSQL; migration ADR/runner and known-revision recovery evidence are accepted."],
                ["Identity and domain", "WP03 and WP04", "Selected WP10 contract work", "Claims/invitations are safe and Node 0 workspace is distinct from paid case."],
                ["Participant core", "WP05 and WP06", "Commercial configuration in WP07", "Free and Complete flows are resumable, attributable and role-scoped."],
                ["Commercial and operations", "WP07, WP08, WP09 and WP10", "Separate repositories can progress behind pinned contracts", "Synthetic A2 covers promotion, money, documents, proposals and failure recovery."],
                ["Release and cutover", "WP11, WP12 and remaining WP13", "Evidence collection across repos", "A1/A2 pass; B1/B2 remain separately controlled human gates."],
            ],
        ),
        "# Programme gates",
        md_table(
            ["Gate", "Purpose", "Owner", "Verifier", "Failure rule"],
            [[gate["id"], gate["title"], gate["owner"], gate["verifier"], gate["failure"]] for gate in data.GATES],
        ),
        "# Work-package details",
    ]

    for wp in data.WORK_PACKAGES:
        wp_id = wp["id"]
        lead = "Luke" if wp_id in LUKE_WPS else "Alan"
        reviewer = "Alan" if lead == "Luke" else "Luke"
        parts.extend(
            [
                f"## {wp_id}: {ascii_dashes(wp['title'])}",
                f"**Problem.** {ascii_dashes(wp['problem'])}",
                f"**Target outcome.** {ascii_dashes(wp['outcome'])}",
                (
                    f"**Proposed lead/review.** {lead} leads; {reviewer} reviews. "
                    + (
                        "The split is proposed for joint review and can be amended before implementation begins."
                        if wp_id in LUKE_WPS
                        else ascii_dashes(ownership[wp_id]["note"])
                    )
                ),
                "**Key boundaries.**\n\n" + bullets([str(value) for value in wp["architecture"]]),
                md_table(
                    ["PR", "Repository", "Suggested change", "Depends on", "Gate"],
                    [[pr["id"], data.REPOSITORIES[pr["repo"]], pr["title"], ", ".join(pr["deps"]) or "None", pr["gate"]] for pr in pr_by_wp[wp_id]],
                ),
                "**Acceptance focus.**\n\n" + bullets([str(value) for value in wp["test_focus"]]),
                "**Primary risks.**\n\n" + bullets([str(value) for value in wp["risks"]]),
                f"Full implementation contract: `{safe_name(wp, 'md')}` in `MD Work Packages`; matching review PDF in `PDF Work Packages`.",
            ]
        )

    parts.extend(
        [
            "# Decisions requiring explicit resolution",
            md_table(
                ["Decision", "Topic", "Owner", "Resolve by", "Recommendation"],
                [[item["id"], item["title"], item["owner"], item["latest"], item["recommendation"]] for item in data.DECISIONS],
            ),
            "# Review checklist",
            bullets(
                [
                    "Are the fourteen work-package boundaries correct, or should any be split, merged or reordered?",
                    "Are the fifty suggested PRs small enough and assigned to the correct repositories?",
                    "Are the workspace/case, invitation, authorship, promotion, payment, document and intelligence contracts technically sound?",
                    "Is the proposed Luke/Alan lead split workable, with reciprocal review as stated?",
                    "Are Alan's outstanding PR 122/124 findings fully represented, and what amendments do they require?",
                    "Do any A0/A1/A2/B1/B2 acceptance criteria or external-review requirements need changing?",
                    "No implementation begins until amendments are incorporated and the plan is jointly accepted.",
                ]
            ),
        ]
    )
    text = ascii_dashes("\n\n".join(parts))
    text = text.replace("Project/document identifier parity", "Drive package/document identifier parity")
    return text.strip() + "\n"


def main() -> None:
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    MD_DIR.mkdir(parents=True)
    PDF_DIR.mkdir(parents=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    for wp in data.WORK_PACKAGES:
        (MD_DIR / safe_name(wp, "md")).write_text(clean_work_package(wp), encoding="utf-8")
    OVERVIEW_SOURCE.write_text(overview_markdown(), encoding="utf-8")

    print(f"Built {len(list(MD_DIR.glob('*.md')))} clean Markdown work packages")
    print(f"Drive package root: {PACKAGE_ROOT}")
    print(f"Overview source: {OVERVIEW_SOURCE}")


if __name__ == "__main__":
    main()
