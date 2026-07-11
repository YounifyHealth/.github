#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python scripts/build_drive_package.py

COMMON=(
  --from=markdown+yaml_metadata_block+pipe_tables+task_lists+raw_tex
  --standalone
  --pdf-engine=/usr/local/bin/lualatex
  --toc
  --toc-depth=2
  --number-sections
  --lua-filter=scripts/table-widths.lua
  --include-in-header=scripts/aws-plan-header.tex
  --include-before-body=scripts/after-toc.tex
  -V papersize=letter
  -V geometry:margin=0.9in
  -V fontsize=11pt
  -V colorlinks=true
  -V linkcolor=linkblue
  -V urlcolor=linkblue
)

quarto pandoc \
  "output/source/Natalyx MVP Fixes - Consolidated Plan Overview.md" \
  "${COMMON[@]}" \
  -o "output/drive/MVP Fixes/Natalyx MVP Fixes - Consolidated Plan Overview.pdf"

for source in "output/drive/MVP Fixes/MD Work Packages"/*.md; do
  name="$(basename "${source%.md}")"
  quarto pandoc "$source" "${COMMON[@]}" \
    -o "output/drive/MVP Fixes/PDF Work Packages/$name.pdf"
done
