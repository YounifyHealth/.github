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

    overview_pages = int(pdf_info(OVERVIEW)["Pages"])
    if not 15 <= overview_pages <= 40:
        fail(f"overview page count {overview_pages} is outside the concise review range")

    print(
        "Drive package validation passed: "
        f"14 Markdown plans, 14 matching PDFs, one {overview_pages}-page overview, "
        "no local paths, Letter sizing and AWS-plan metadata/style source."
    )


if __name__ == "__main__":
    main()
