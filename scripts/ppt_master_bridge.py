#!/usr/bin/env python3
"""Load ppt-master's native SVG-to-PPTX converter from a sibling skill."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Callable


class PptMasterBridgeError(RuntimeError):
    """Raised when the ppt-master converter cannot be located or imported."""


def _candidate_skill_dirs(explicit: str | Path | None = None) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env_path = os.environ.get("PPT_MASTER_SKILL_DIR")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    this_skill_dir = Path(__file__).resolve().parents[1]
    candidates.extend(
        [
            this_skill_dir.parent / "ppt-master",
            Path.home() / ".agents" / "skills" / "ppt-master",
            Path.home() / ".codex" / "skills" / "ppt-master",
        ]
    )

    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen:
            unique.append(resolved)
            seen.add(resolved)
    return unique


def resolve_ppt_master_skill_dir(explicit: str | Path | None = None) -> Path:
    """Return the first usable ppt-master skill directory."""
    attempted: list[str] = []
    for skill_dir in _candidate_skill_dirs(explicit):
        attempted.append(str(skill_dir))
        package_dir = skill_dir / "scripts" / "svg_to_pptx"
        if (package_dir / "__init__.py").exists():
            return skill_dir
    raise PptMasterBridgeError(
        "Could not locate ppt-master's svg_to_pptx package. "
        "Set PPT_MASTER_SKILL_DIR or pass --ppt-master-skill-dir. "
        f"Checked: {', '.join(attempted)}"
    )


def import_ppt_master_module(module_name: str, explicit: str | Path | None = None):
    """Import a module from ppt-master/scripts."""
    skill_dir = resolve_ppt_master_skill_dir(explicit)
    scripts_dir = skill_dir / "scripts"
    scripts_dir_str = str(scripts_dir)
    if scripts_dir_str not in sys.path:
        sys.path.insert(0, scripts_dir_str)
    try:
        return importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        raise PptMasterBridgeError(
            f"Failed to import {module_name!r} from {scripts_dir}: {exc}"
        ) from exc


def load_native_builder(explicit: str | Path | None = None) -> Callable:
    module = import_ppt_master_module("svg_to_pptx.pptx_builder", explicit)
    return module.create_pptx_with_native_svg


def load_native_converter(explicit: str | Path | None = None) -> Callable:
    module = import_ppt_master_module("svg_to_pptx.drawingml_converter", explicit)
    return module.convert_svg_to_slide_shapes
