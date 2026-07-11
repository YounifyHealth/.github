#!/usr/bin/env python3
"""Render a readable PDF directly from consolidated-plan.md.

The parser intentionally supports the Markdown used by this programme: headings,
paragraphs, block quotes, lists/tasks, fenced code, Mermaid flowcharts and tables.
Wide tables become vertical record cards so they remain readable on US Letter.
"""

from __future__ import annotations

import argparse
import html
import math
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


NAVY = colors.HexColor("#243447")
INK = colors.HexColor("#253238")
MUTED = colors.HexColor("#5F6D73")
ORANGE = colors.HexColor("#D96C32")
CREAM = colors.HexColor("#F6F1E7")
PALE = colors.HexColor("#EDF4F5")
LINE = colors.HexColor("#C9D2D5")
GREEN = colors.HexColor("#DDEFE6")


def register_fonts() -> None:
    candidates = {
        "NatalyxSans": [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ],
        "NatalyxMono": [
            "/System/Library/Fonts/Supplemental/Courier New.ttf",
            "/System/Library/Fonts/Menlo.ttc",
        ],
    }
    for name, paths in candidates.items():
        for path in paths:
            try:
                if Path(path).exists() and not path.endswith(".ttc"):
                    pdfmetrics.registerFont(TTFont(name, path))
                    break
            except Exception:
                continue


register_fonts()
SANS = "NatalyxSans" if "NatalyxSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
MONO = "NatalyxMono" if "NatalyxMono" in pdfmetrics.getRegisteredFontNames() else "Courier"


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    styles: dict[str, ParagraphStyle] = {}
    styles["Body"] = ParagraphStyle("Body", parent=base["BodyText"], fontName=SANS, fontSize=8.4, leading=11.1, textColor=INK, spaceAfter=5.5, allowWidows=0, allowOrphans=0)
    styles["Small"] = ParagraphStyle("Small", parent=styles["Body"], fontSize=7.2, leading=9.1, textColor=MUTED)
    styles["Quote"] = ParagraphStyle("Quote", parent=styles["Body"], leftIndent=12, rightIndent=8, borderColor=ORANGE, borderWidth=0, borderPadding=7, backColor=CREAM, textColor=NAVY, spaceBefore=4, spaceAfter=7)
    styles["Code"] = ParagraphStyle("Code", parent=base["Code"], fontName=MONO, fontSize=6.8, leading=8.7, leftIndent=6, rightIndent=6, borderPadding=6, backColor=colors.HexColor("#F2F4F5"), textColor=INK, spaceBefore=4, spaceAfter=7, wordWrap="CJK")
    styles["Table"] = ParagraphStyle("Table", parent=styles["Body"], fontSize=6.8, leading=8.4, spaceAfter=0, wordWrap="CJK")
    styles["TableHead"] = ParagraphStyle("TableHead", parent=styles["Table"], fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_LEFT)
    styles["CardTitle"] = ParagraphStyle("CardTitle", parent=styles["Body"], fontName="Helvetica-Bold", fontSize=8.3, leading=10.2, textColor=NAVY, spaceBefore=5, spaceAfter=3, keepWithNext=True)
    sizes = {1: 20, 2: 16, 3: 12.4, 4: 10.5, 5: 9.4, 6: 8.8}
    leads = {1: 24, 2: 19, 3: 15.5, 4: 13, 5: 11.5, 6: 10.8}
    before = {1: 10, 2: 9, 3: 7, 4: 6, 5: 5, 6: 4}
    after = {1: 8, 2: 7, 3: 5, 4: 4, 5: 3, 6: 3}
    for level in range(1, 7):
        styles[f"H{level}"] = ParagraphStyle(
            f"H{level}", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=sizes[level],
            leading=leads[level], textColor=NAVY if level < 4 else INK, spaceBefore=before[level],
            spaceAfter=after[level], keepWithNext=True,
        )
    styles["Title"] = ParagraphStyle("Title", parent=styles["H1"], alignment=TA_CENTER, fontSize=23, leading=27, textColor=NAVY, spaceBefore=80, spaceAfter=16)
    styles["TOCHeading"] = ParagraphStyle("TOCHeading", parent=styles["H2"], pageBreakBefore=True)
    return styles


STYLES = build_styles()


def inline(text: str) -> str:
    escaped = html.escape(text, quote=True)
    placeholders: dict[str, str] = {}

    def stash(value: str) -> str:
        key = f"@@TOKEN{len(placeholders)}@@"
        placeholders[key] = value
        return key

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: stash(f'<link href="{m.group(2)}" color="#9A4A22">{m.group(1)}</link>'), escaped)
    escaped = re.sub(r"`([^`]+)`", lambda m: stash(f'<font name="{MONO}" color="#7A351A">{m.group(1)}</font>'), escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", escaped)
    escaped = escaped.replace("  ", " &#160;")
    for key, value in placeholders.items():
        escaped = escaped.replace(key, value)
    return escaped


def para(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(inline(text.strip()), STYLES[style])


def split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def is_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(bool(re.fullmatch(r":?-{3,}:?", cell.replace(" ", ""))) for cell in cells)


def table_flowables(headers: list[str], rows: list[list[str]], width: float) -> list[Flowable]:
    count = len(headers)
    if count > 6:
        result: list[Flowable] = []
        for index, row in enumerate(rows, 1):
            label = row[0] if row and row[0] else f"Record {index}"
            result.append(Paragraph(inline(label), STYLES["CardTitle"]))
            data = []
            for key, value in zip(headers, row):
                data.append([Paragraph(inline(key), STYLES["TableHead"]), Paragraph(inline(value), STYLES["Table"])])
            card = Table(data, colWidths=[width * 0.23, width * 0.77], repeatRows=0, splitByRow=1)
            card.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            result += [card, Spacer(1, 5)]
        return result

    data: list[list[Any]] = [[Paragraph(inline(cell), STYLES["TableHead"]) for cell in headers]]
    for row in rows:
        row = row + [""] * (count - len(row))
        data.append([Paragraph(inline(cell), STYLES["Table"]) for cell in row[:count]])
    weights = []
    for column in range(count):
        length = max([len(headers[column])] + [min(len(row[column]) if column < len(row) else 0, 80) for row in rows])
        weights.append(max(8, math.sqrt(length + 1)))
    total = sum(weights)
    col_widths = [width * value / total for value in weights]
    table = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [table, Spacer(1, 6)]


class MermaidFlowable(Flowable):
    def __init__(self, source: str, width: float):
        super().__init__()
        self.source = source
        self.requested_width = width
        self.nodes, self.edges = self._parse(source)
        self.levels = self._levels()
        self.width = width
        self.height = min(620, max(115, len(self.levels) * 70 + 25))

    @staticmethod
    def _parse(source: str) -> tuple[dict[str, str], list[tuple[str, str]]]:
        nodes: dict[str, str] = {}
        edges: list[tuple[str, str]] = []
        for line in source.splitlines():
            for node_id, label in re.findall(r'(\b[A-Za-z0-9_]+)\["([^"]+)"\]', line):
                nodes[node_id] = label
            if "-->" in line:
                parts = line.split("-->")
                left_match = re.search(r"([A-Za-z0-9_]+)(?:\[|\s|$)", parts[0].strip())
                right_match = re.search(r"([A-Za-z0-9_]+)(?:\[|\s|$)", parts[-1].strip())
                if left_match and right_match:
                    left, right = left_match.group(1), right_match.group(1)
                    nodes.setdefault(left, left)
                    nodes.setdefault(right, right)
                    edges.append((left, right))
        return nodes, edges

    def _levels(self) -> list[list[str]]:
        incoming: dict[str, set[str]] = {node: set() for node in self.nodes}
        outgoing: dict[str, set[str]] = {node: set() for node in self.nodes}
        for left, right in self.edges:
            outgoing[left].add(right)
            incoming[right].add(left)
        indegree = {node: len(values) for node, values in incoming.items()}
        queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
        level = {node: 0 for node in queue}
        order: list[str] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in sorted(outgoing[node]):
                level[nxt] = max(level.get(nxt, 0), level[node] + 1)
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        for node in self.nodes:
            if node not in order:
                level[node] = max(level.values(), default=0) + 1
        grouped: dict[int, list[str]] = defaultdict(list)
        for node, value in level.items():
            grouped[value].append(node)
        return [sorted(grouped[key]) for key in sorted(grouped)]

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        self.width = min(self.requested_width, avail_width)
        return self.width, self.height

    def draw(self) -> None:
        c = self.canv
        c.saveState()
        c.setStrokeColor(LINE)
        c.setFillColor(PALE)
        c.roundRect(0, 0, self.width, self.height, 8, fill=1, stroke=1)
        positions: dict[str, tuple[float, float, float, float]] = {}
        level_height = (self.height - 25) / max(1, len(self.levels))
        for level_index, nodes in enumerate(self.levels):
            gap = 8
            box_width = min(175, (self.width - 20 - gap * max(0, len(nodes) - 1)) / max(1, len(nodes)))
            box_height = min(45, level_height - 10)
            row_width = len(nodes) * box_width + max(0, len(nodes) - 1) * gap
            start_x = (self.width - row_width) / 2
            y = self.height - 14 - (level_index + 1) * level_height + (level_height - box_height) / 2
            for index, node in enumerate(nodes):
                x = start_x + index * (box_width + gap)
                positions[node] = (x, y, box_width, box_height)
        c.setStrokeColor(colors.HexColor("#8DA1A8"))
        c.setLineWidth(0.8)
        for left, right in self.edges:
            if left not in positions or right not in positions:
                continue
            lx, ly, lw, _lh = positions[left]
            rx, ry, rw, rh = positions[right]
            x1, y1 = lx + lw / 2, ly
            x2, y2 = rx + rw / 2, ry + rh
            middle = (y1 + y2) / 2
            c.line(x1, y1, x1, middle)
            c.line(x1, middle, x2, middle)
            c.line(x2, middle, x2, y2)
            c.line(x2, y2, x2 - 3, y2 + 5)
            c.line(x2, y2, x2 + 3, y2 + 5)
        for node, (x, y, w, h) in positions.items():
            c.setFillColor(colors.white)
            c.setStrokeColor(ORANGE if node in {"WP00", "WP13"} else NAVY)
            c.setLineWidth(1.0)
            c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
            label = self.nodes[node]
            words = label.split()
            lines: list[str] = []
            current = ""
            for word in words:
                test = (current + " " + word).strip()
                if pdfmetrics.stringWidth(test, "Helvetica", 6.5) <= w - 8:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
            lines = lines[:4]
            c.setFillColor(INK)
            c.setFont("Helvetica", 6.5)
            baseline = y + h / 2 + (len(lines) - 1) * 3.7
            for idx, line in enumerate(lines):
                c.drawCentredString(x + w / 2, baseline - idx * 7.4, line)
        c.restoreState()


class ProgrammeDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs: Any):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="programme", frames=[frame], onPage=self._page)])
        self._bookmark_counter = 0

    def _page(self, canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(self.leftMargin, 0.48 * inch, LETTER[0] - self.rightMargin, 0.48 * inch)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, 0.30 * inch, "Natalyx MVP Product Flow Reshape — planning only")
        canvas.drawRightString(LETTER[0] - self.rightMargin, 0.30 * inch, f"Page {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, Paragraph) and (flowable.style.name == "Title" or flowable.style.name.startswith("H")):
            if flowable.style.name == "Title":
                level = 0
            else:
                match = re.fullmatch(r"H([1-6])", flowable.style.name)
                if not match:
                    return
                level = int(match.group(1)) - 1
            text = flowable.getPlainText()
            key = getattr(flowable, "_bookmark_key", "")
            if not key:
                key = f"heading-{self._bookmark_counter}"
                setattr(flowable, "_bookmark_key", key)
                self._bookmark_counter += 1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=level > 1)
            if level <= 1:
                self.notify("TOCEntry", (level, text, self.page, key))


def flush_paragraph(buffer: list[str], story: list[Flowable]) -> None:
    if not buffer:
        return
    text = " ".join(line.strip() for line in buffer).strip()
    if text:
        story.append(para(text))
    buffer.clear()


def parse_markdown(source: str, width: float) -> list[Flowable]:
    lines = source.splitlines()
    story: list[Flowable] = []
    paragraph: list[str] = []
    index = 0
    first_h1 = True
    skip_manual_toc = False

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if skip_manual_toc and heading_match and len(heading_match.group(1)) <= 2 and heading_match.group(2).strip().lower() != "table of contents":
            skip_manual_toc = False
        if skip_manual_toc:
            index += 1
            continue
        if not stripped:
            flush_paragraph(paragraph, story)
            index += 1
            continue
        if stripped.startswith("```"):
            flush_paragraph(paragraph, story)
            language = stripped[3:].strip().lower()
            index += 1
            code: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1
            if language == "mermaid":
                story += [MermaidFlowable("\n".join(code), width), Spacer(1, 7)]
            else:
                wrapped_lines = []
                max_chars = 112
                for code_line in code:
                    if len(code_line) <= max_chars:
                        wrapped_lines.append(code_line)
                    else:
                        wrapped_lines.extend(code_line[pos:pos + max_chars] for pos in range(0, len(code_line), max_chars))
                story.append(Preformatted("\n".join(wrapped_lines), STYLES["Code"], maxLineLength=112))
            continue
        if heading_match:
            flush_paragraph(paragraph, story)
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            style = "Title" if first_h1 and level == 1 else f"H{level}"
            heading = Paragraph(inline(text), STYLES[style])
            if first_h1 and level == 1:
                story += [heading, HRFlowable(width="65%", thickness=1.5, color=ORANGE, spaceBefore=4, spaceAfter=18)]
                first_h1 = False
            else:
                story.append(heading)
            if text.lower() == "table of contents":
                toc = TableOfContents()
                toc.levelStyles = [
                    ParagraphStyle(f"TOC{n}", fontName=SANS, fontSize=max(7, 10 - n), leading=max(9, 12 - n), leftIndent=n * 14, firstLineIndent=0, textColor=INK, spaceBefore=2)
                    for n in range(6)
                ]
                story += [toc, PageBreak()]
                skip_manual_toc = True
            index += 1
            continue
        if stripped.startswith(">"):
            flush_paragraph(paragraph, story)
            quote_lines = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            story.append(Paragraph(inline(" ".join(quote_lines)), STYLES["Quote"]))
            continue
        if stripped.startswith("|") and index + 1 < len(lines) and is_separator(lines[index + 1]):
            flush_paragraph(paragraph, story)
            headers = split_table_row(lines[index])
            index += 2
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(split_table_row(lines[index]))
                index += 1
            story.extend(table_flowables(headers, rows, width))
            continue
        list_match = re.match(r"^\s*[-*]\s+(?:\[([ xX])\]\s+)?(.*)$", line)
        ordered_match = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if list_match or ordered_match:
            flush_paragraph(paragraph, story)
            items = []
            ordered = bool(ordered_match)
            while index < len(lines):
                current = lines[index]
                match = re.match(r"^\s*[-*]\s+(?:\[([ xX])\]\s+)?(.*)$", current) if not ordered else re.match(r"^\s*\d+\.\s+(.*)$", current)
                if not match:
                    break
                if ordered:
                    text = match.group(1)
                else:
                    checked, text = match.group(1), match.group(2)
                    if checked is not None:
                        text = ("☒ " if checked.lower() == "x" else "☐ ") + text
                items.append(ListItem(Paragraph(inline(text), STYLES["Body"]), leftIndent=12))
                index += 1
            story.append(ListFlowable(items, bulletType="1" if ordered else "bullet", start="1" if ordered else "•", leftIndent=18, bulletFontName=SANS, bulletFontSize=7.5, spaceAfter=5))
            continue
        if re.fullmatch(r"-{3,}", stripped):
            flush_paragraph(paragraph, story)
            story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=4, spaceAfter=4))
            index += 1
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph(paragraph, story)
    return story


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="consolidated-plan.md")
    parser.add_argument("output", nargs="?", default="consolidated-plan.pdf")
    args = parser.parse_args()
    source_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    source = source_path.read_text(encoding="utf-8")
    doc = ProgrammeDocTemplate(
        str(output_path), pagesize=LETTER, rightMargin=0.55 * inch, leftMargin=0.55 * inch,
        topMargin=0.58 * inch, bottomMargin=0.62 * inch, title="Natalyx MVP Product Flow Reshape",
        author="Natalyx", subject=f"Rendered from {source_path.name}", creator="Natalyx planning package render_pdf.py",
    )
    story = parse_markdown(source, doc.width)
    doc.multiBuild(story)
    print(f"Rendered {source_path.name} -> {output_path.name}")


if __name__ == "__main__":
    main()
