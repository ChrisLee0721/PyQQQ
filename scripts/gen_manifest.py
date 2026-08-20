"""Scan docs/ directory and generate manifest.json for the sidebar.

Usage:
    python scripts/gen_manifest.py

Scans docs/ for .md files and generates a manifest.json that the
doc-viewer.html uses to build the sidebar automatically.

Folder structure maps to sections:
- docs/ → Getting Started
- docs/api/ → API Reference
- docs/tutorials/ → Tutorials
- docs/examples/ → Examples
"""

import json
import os
from pathlib import Path


def scan_docs(docs_dir: str = "src/pages/docs") -> dict:
    """Scan docs directory and build manifest."""
    sections = []
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        print(f"Warning: {docs_dir} not found")
        return {"sections": []}

    # Process each subdirectory
    for subdir in sorted(docs_path.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name.startswith(("_", ".")):
            continue

        items = []
        for md_file in sorted(subdir.glob("*.md")):
            # Skip Chinese versions (show as separate items)
            if md_file.stem.endswith("_zh"):
                continue

            title = md_file.stem.replace("_", " ").replace("-", " ").title()
            rel_path = f"docs/{subdir.name}/{md_file.name}"
            items.append({"title": title, "file": rel_path})

        if items:
            section_title = subdir.name.replace("_", " ").replace("-", " ").title()
            sections.append({"title": section_title, "items": items})

    # Add root-level .md files as "Getting Started"
    root_items = []
    for md_file in sorted(docs_path.glob("*.md")):
        if md_file.stem.endswith("_zh"):
            continue
        title = md_file.stem.replace("_", " ").replace("-", " ").title()
        rel_path = f"docs/{md_file.name}"
        root_items.append({"title": title, "file": rel_path})

    if root_items:
        sections.insert(0, {"title": "Getting Started", "items": root_items})

    return {"sections": sections}


def main():
    manifest = scan_docs()

    # Write manifest
    out_path = "src/pages/docs/manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Print summary
    total = sum(len(s["items"]) for s in manifest["sections"])
    print(f"Generated {out_path}")
    print(f"  {len(manifest['sections'])} sections, {total} documents")
    for section in manifest["sections"]:
        print(f"  {section['title']}: {len(section['items'])} docs")


if __name__ == "__main__":
    main()
