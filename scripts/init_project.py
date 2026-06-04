#!/usr/bin/env python3
"""Initialize a Codex Bento PPT project directory."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Codex Bento PPT project scaffold.")
    parser.add_argument("project_dir", help="Project directory to create")
    parser.add_argument("--title", default="Untitled Deck", help="Deck title")
    parser.add_argument("--slides", type=int, default=8, help="Target slide count")
    args = parser.parse_args()

    project = Path(args.project_dir).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    for name in ("source_assets", "page_plans", "svg", "previews", "exports"):
        (project / name).mkdir(exist_ok=True)

    manifest = {
        "title": args.title,
        "target_slide_count": args.slides,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workflow": "codex-bento-ppt",
        "canvas": {"width": 1280, "height": 720},
        "artifacts": {
            "source_inventory": "source_inventory.json",
            "source_digest": "source_digest.md",
            "source_assets": "source_assets/",
            "requirements": "requirements.md",
            "research": "research.md",
            "outline": "outline.json",
            "sticky_notes": "sticky_notes.md",
            "page_plans": "page_plans/",
            "svg": "svg/",
            "previews": "previews/",
            "exports": "exports/",
        },
    }
    manifest_path = project / "manifest.json"
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    placeholders = {
        "source_digest.md": "# Source Digest\n\n## Source Coverage\n\n- \n",
        "requirements.md": f"# Requirements\n\n- Deck title: {args.title}\n- Target slide count: {args.slides}\n",
        "research.md": "# Research\n\n## Executive Takeaways\n\n- \n",
        "sticky_notes.md": "# Sticky Notes\n\n",
    }
    for rel_path, content in placeholders.items():
        path = project / rel_path
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    outline_path = project / "outline.json"
    if not outline_path.exists():
        outline_path.write_text(
            json.dumps(
                {
                    "deck": {
                        "title": args.title,
                        "subtitle": "",
                        "audience": "",
                        "objective": "",
                        "slides": [],
                    }
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"Initialized Codex Bento PPT project: {project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
