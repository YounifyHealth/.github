#!/usr/bin/env python3
"""Validate the local Drive upload package against the review contract."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import programme_data as data  # noqa: E402


PACKAGE = ROOT / "output" / "drive" / "MVP Fixes"
MD_DIR = PACKAGE / "MD Work Packages"
PDF_DIR = PACKAGE / "PDF Work Packages"
OVERVIEW = PACKAGE / "Natalyx MVP Fixes - Consolidated Plan Overview.pdf"


def fail(message: str) -> None:
    raise SystemExit(f"Drive package validation failed: {message}")


def pdf_info(path: Path) -> dict[str, str]:
    proc = subprocess.run(["pdfinfo", str(path)], text=True, capture_output=True, check=True)
    values: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def pdf_text(path: Path) -> str:
    proc = subprocess.run(["pdftotext", str(path), "-"], text=True, capture_output=True, check=True)
    return proc.stdout


def parity_tokens(text: str) -> set[str]:
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"https?://\S+", " ", text)
    return set(re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{3,}", text.lower()))


def token_coverage(markdown_text: str, rendered_text: str) -> float:
    source = parity_tokens(markdown_text)
    rendered = parity_tokens(rendered_text)
    return len(source & rendered) / len(source) if source else 1.0


def main() -> None:
    markdown = sorted(MD_DIR.glob("*.md"))
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    root_pdfs = sorted(PACKAGE.glob("*.pdf"))
    if len(markdown) != 14 or len(pdfs) != 14 or root_pdfs != [OVERVIEW]:
        fail(f"expected 14 MD, 14 package PDFs and one overview; found {len(markdown)}, {len(pdfs)}, {len(root_pdfs)}")
    if {path.stem for path in markdown} != {path.stem for path in pdfs}:
        fail("Markdown/PDF filename stems do not match")

    banned = ["/Users/lukerhodes", "github.com/orgs/NatalyxPlatform/projects/3?query=", "| Project item |"]
    for index, (wp, path) in enumerate(zip(data.WORK_PACKAGES, markdown, strict=True)):
        text = path.read_text(encoding="utf-8")
        if not path.name.startswith(wp["id"] + " - ") or wp["id"] not in text:
            fail(f"work-package ordering/name mismatch at {path.name}")
        for value in banned:
            if value in text:
                fail(f"banned review-package value {value!r} in {path.name}")
        for pr in [item for item in data.PROPOSED_PRS if item["wp"] == wp["id"]]:
            if pr["id"] not in text:
                fail(f"{pr['id']} missing from {path.name}")
            for field in ("local_preparation_status", "merge_readiness", "technical_decision_owner"):
                if pr[field] not in text:
                    fail(f"{pr['id']} {field} missing from {path.name}")
        if "Luke-owned PRs that may begin now" in text:
            fail(f"unwanted standalone Luke local-start wording in {path.name}")
        if wp["id"] == "WP00" and ("REC-22" not in text or data.WAVE2_BRANCH["head"] not in text):
            fail("WP00 does not contain the complete reconciliation matrix and Wave 2 exact head")

    for path in [OVERVIEW, *pdfs]:
        info = pdf_info(path)
        if info.get("Title") != "Natalyx MVP Fixes":
            fail(f"wrong title metadata in {path.name}: {info.get('Title')}")
        if info.get("Page size") != "612 x 792 pts (letter)":
            fail(f"wrong page size in {path.name}: {info.get('Page size')}")
        if int(info.get("Pages", "0")) < 3:
            fail(f"implausibly short PDF {path.name}")
        text = pdf_text(path)
        if "/Users/lukerhodes" in text or "\\plantitle" in text:
            fail(f"local path or unrendered title command in {path.name}")
        if not re.search(r"Natalyx MVP Fixes", text):
            fail(f"title text not extractable in {path.name}")

    coverages: list[tuple[str, float]] = []
    pdf_by_stem = {path.stem: path for path in pdfs}
    for path in markdown:
        coverage = token_coverage(path.read_text(encoding="utf-8"), pdf_text(pdf_by_stem[path.stem]))
        coverages.append((path.name, coverage))
        if coverage < 0.97:
            fail(f"Markdown/PDF token parity below 97% for {path.name}: {coverage:.1%}")

    overview_source = ROOT / "output" / "source" / "Natalyx MVP Fixes - Consolidated Plan Overview.md"
    overview_coverage = token_coverage(overview_source.read_text(encoding="utf-8"), pdf_text(OVERVIEW))
    if overview_coverage < 0.97:
        fail(f"overview Markdown/PDF token parity below 97%: {overview_coverage:.1%}")

    overview_text = pdf_text(OVERVIEW)
    for marker in ("REC-22", "P03-05", "P09-06", "P13-07", "5b63e3a", "RLS", "B1", "B2", "Suggested ownership and reciprocal review", "Founder decision resolution", "Immediate Alan decisions", "Later Alan decisions", "External dependencies"):
        if marker not in overview_text:
            fail(f"reconciled overview marker {marker!r} missing")
    stale_overview_phrases = ["technical review requested", "the remaining decision is whether", "decisions requiring explicit resolution", "no implementation begins until amendments"]
    for phrase in stale_overview_phrases:
        if phrase in overview_text.lower():
            fail(f"stale overview wording remains: {phrase!r}")
    if "Luke-owned PRs that may begin now" in overview_text:
        fail("unwanted standalone Luke local-start wording in overview")

    luke_count = sum(pr["dri"] == "Luke" for pr in data.PROPOSED_PRS)
    alan_count = sum(pr["dri"] == "Alan" for pr in data.PROPOSED_PRS)
    if (luke_count, alan_count) != (19, 33):
        fail(f"ownership split is {luke_count} Luke / {alan_count} Alan, expected 19 / 33")

    overview_pages = int(pdf_info(OVERVIEW)["Pages"])
    if not 15 <= overview_pages <= 60:
        fail(f"overview page count {overview_pages} is outside the concise review range")

    print(
        "Drive package validation passed: "
        f"14 Markdown plans, 14 matching PDFs, one {overview_pages}-page overview, "
        f"minimum Markdown/PDF token parity {min(value for _, value in coverages):.1%}, "
        f"overview parity {overview_coverage:.1%}, no local paths, Letter sizing and AWS-plan metadata/style source."
    )


if __name__ == "__main__":
    main()
