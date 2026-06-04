#!/usr/bin/env python3
"""Load the native SVG-to-PPTX converter bundled with this skill."""

from __future__ import annotations

import importlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


class PptMasterBridgeError(RuntimeError):
    """Raised when the native converter cannot be located or imported."""


@dataclass(frozen=True)
class NativeConverterLocation:
    """Resolved import location for the native SVG-to-PPTX converter."""

    package_dir: Path
    import_parent: Path
    source: str


def _package_dir_from_path(path: Path) -> Path | None:
    """Accept a package dir, its parent, or a legacy skill dir."""
    candidates = [
        path,
        path / "svg_to_pptx",
        path / "scripts" / "svg_to_pptx",
    ]
    for candidate in candidates:
        if (candidate / "__init__.py").exists():
            return candidate.resolve()
    return None


def _candidate_locations(explicit: str | Path | None = None) -> list[NativeConverterLocation]:
    locations: list[NativeConverterLocation] = []
    if explicit:
        package_dir = _package_dir_from_path(Path(explicit).expanduser())
        if package_dir is not None:
            locations.append(
                NativeConverterLocation(package_dir, package_dir.parent, "external-override")
            )
    env_path = os.environ.get("PPT_MASTER_SKILL_DIR")
    if env_path:
        package_dir = _package_dir_from_path(Path(env_path).expanduser())
        if package_dir is not None:
            locations.append(
                NativeConverterLocation(package_dir, package_dir.parent, "external-override")
            )

    this_skill_dir = Path(__file__).resolve().parents[1]
    bundled_package = this_skill_dir / "vendor" / "svg_to_pptx"
    if (bundled_package / "__init__.py").exists():
        locations.append(
            NativeConverterLocation(
                bundled_package.resolve(),
                bundled_package.resolve().parent,
                "bundled-vendor",
            )
        )

    for legacy_path in [
        this_skill_dir.parent / "ppt-master",
        Path.home() / ".agents" / "skills" / "ppt-master",
        Path.home() / ".claude" / "skills" / "ppt-master",
        Path.home() / ".codex" / "skills" / "ppt-master",
    ]:
        package_dir = _package_dir_from_path(legacy_path)
        if package_dir is not None:
            locations.append(
                NativeConverterLocation(package_dir, package_dir.parent, "legacy-external")
            )

    unique: list[NativeConverterLocation] = []
    seen: set[Path] = set()
    for location in locations:
        if location.package_dir not in seen:
            unique.append(location)
            seen.add(location.package_dir)
    return unique


def resolve_native_converter_location(explicit: str | Path | None = None) -> NativeConverterLocation:
    """Return the first usable native converter import location."""
    if explicit:
        explicit_path = Path(explicit).expanduser()
        package_dir = _package_dir_from_path(explicit_path)
        if package_dir is None:
            raise PptMasterBridgeError(
                "Explicit native converter override is invalid. "
                "Pass a svg_to_pptx package dir, its parent, or a legacy ppt-master skill dir. "
                f"Received: {explicit_path}"
            )
        return NativeConverterLocation(package_dir, package_dir.parent, "external-override")

    env_path = os.environ.get("PPT_MASTER_SKILL_DIR")
    if env_path:
        package_dir = _package_dir_from_path(Path(env_path).expanduser())
        if package_dir is None:
            raise PptMasterBridgeError(
                "PPT_MASTER_SKILL_DIR is set but does not point to a usable native converter. "
                "Unset it to use the bundled vendor package or point it at svg_to_pptx/a legacy ppt-master skill. "
                f"Received: {env_path}"
            )
        return NativeConverterLocation(package_dir, package_dir.parent, "external-override")

    attempted: list[str] = []
    for location in _candidate_locations(explicit):
        attempted.append(f"{location.source}:{location.package_dir}")
        return location
    bundled = Path(__file__).resolve().parents[1] / "vendor" / "svg_to_pptx"
    attempted.append(str(bundled))
    raise PptMasterBridgeError(
        "Could not locate the native svg_to_pptx package. "
        "The bundled vendor package is missing or invalid. "
        "Restore vendor/svg_to_pptx or pass --ppt-master-skill-dir as an external override. "
        f"Checked: {', '.join(attempted)}"
    )


def resolve_ppt_master_skill_dir(explicit: str | Path | None = None) -> Path:
    """Legacy helper returning the resolved converter package directory."""
    return resolve_native_converter_location(explicit).package_dir


def import_native_converter_module(module_name: str, explicit: str | Path | None = None):
    """Import a module from the bundled or explicitly configured converter."""
    location = resolve_native_converter_location(explicit)
    import_parent_str = str(location.import_parent)
    if import_parent_str not in sys.path:
        sys.path.insert(0, import_parent_str)
    try:
        return importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        raise PptMasterBridgeError(
            f"Failed to import {module_name!r} from {location.package_dir} "
            f"({location.source}): {exc}"
        ) from exc


def load_native_builder(explicit: str | Path | None = None) -> Callable:
    module = import_native_converter_module("svg_to_pptx.pptx_builder", explicit)
    return module.create_pptx_with_native_svg


def load_native_converter(explicit: str | Path | None = None) -> Callable:
    module = import_native_converter_module("svg_to_pptx.drawingml_converter", explicit)
    return module.convert_svg_to_slide_shapes
