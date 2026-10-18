---
name: pdf
description: Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout
  matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`,
  `pdfplumber`, and `pypdf` for generation and extraction.
license: Apache-2.0
metadata:
  category: files-documents
  categories_secondary: ''
  tags: pdf, reportlab, pypdf, poppler
  mode: adapt
  upstream_repo: openai/skills
  upstream_path: skills/.curated/pdf
  upstream_sha: 49f948faa9258a0c61caceaf225e179651397431
  upstream_license: Apache-2.0
  changes: 'frontmatter (license SPDX, metadata, stage, topic); body: the privileged apt-get install line
    replaced by asking the user to install poppler-utils; pip/uv installs pinned to reportlab==5.0.1,
    pdfplumber==0.11.10, pypdf==6.21.1 (current on 2026-10-17); executable/non-markdown files omitted:
    agents/openai.yaml'
stage: build
topic: productivity
---


# PDF Skill

## When to use
- Read or review PDF content where layout and visuals matter.
- Create PDFs programmatically with reliable formatting.
- Validate final rendering before delivery.

## Workflow
1. Prefer visual review: render PDF pages to PNGs and inspect them.
   - Use `pdftoppm` if available.
   - If unavailable, install Poppler or ask the user to review the output locally.
2. Use `reportlab` to generate PDFs when creating new documents.
3. Use `pdfplumber` (or `pypdf`) for text extraction and quick checks; do not rely on it for layout fidelity.
4. After each meaningful update, re-render pages and verify alignment, spacing, and legibility.

## Temp and output conventions
- Use `tmp/pdfs/` for intermediate files; delete when done.
- Write final artifacts under `output/pdf/` when working in this repo.
- Keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install reportlab==5.0.1 pdfplumber==0.11.10 pypdf==6.21.1
```
If `uv` is unavailable:
```
python3 -m pip install reportlab==5.0.1 pdfplumber==0.11.10 pypdf==6.21.1
```
System tools (for rendering):
```
# macOS (Homebrew)
brew install poppler

# Ubuntu/Debian: ask the user to install the `poppler-utils` package with the
# system package manager. It needs administrator rights; do not escalate them yourself.
```

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.

## Environment
No required environment variables.

## Rendering command
```
pdftoppm -png $INPUT_PDF $OUTPUT_PREFIX
```

## Quality expectations
- Maintain polished visual design: consistent typography, spacing, margins, and section hierarchy.
- Avoid rendering issues: clipped text, overlapping elements, broken tables, black squares, or unreadable glyphs.
- Charts, tables, and images must be sharp, aligned, and clearly labeled.
- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.
- Citations and references must be human-readable; never leave tool tokens or placeholder strings.

## Final checks
- Do not deliver until the latest PNG inspection shows zero visual or formatting defects.
- Confirm headers/footers, page numbering, and section transitions look polished.
- Keep intermediate files organized or remove them after final approval.
