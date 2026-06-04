#!/usr/bin/env python3
"""Validate and render Bento PPT SVG slides."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image, ImageStat

from ppt_master_bridge import PptMasterBridgeError, load_native_converter


SVG_NS = "http://www.w3.org/2000/svg"
ALLOWED_TAGS = {
    "svg",
    "g",
    "defs",
    "linearGradient",
    "radialGradient",
    "stop",
    "filter",
    "feDropShadow",
    "feGaussianBlur",
    "feOffset",
    "feBlend",
    "feColorMatrix",
    "clipPath",
    "mask",
    "rect",
    "circle",
    "ellipse",
    "line",
    "polyline",
    "polygon",
    "path",
    "text",
    "tspan",
    "image",
    "style",
    "title",
    "desc",
}
FORBIDDEN_TAGS = {"script", "foreignObject", "animate", "animateTransform", "set"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def parse_viewbox(value: str | None) -> list[float] | None:
    if not value:
        return None
    parts = re.split(r"[\s,]+", value.strip())
    if len(parts) != 4:
        return None
    try:
        return [float(part) for part in parts]
    except ValueError:
        return None


def is_nonblank_png(path: Path) -> bool:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        extrema = rgb.getextrema()
        max_channel_range = max(high - low for low, high in extrema)
        mean_sum = sum(stat.mean)
        return max_channel_range > 8 and mean_sum > 15


def validate_one(
    svg_path: Path,
    render_dir: Path | None,
    native_converter=None,
    merge_paragraphs: bool = False,
) -> dict:
    result = {
        "path": str(svg_path),
        "status": "pass",
        "errors": [],
        "warnings": [],
        "preview": None,
        "native_editable": None,
    }

    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError as exc:
        result["status"] = "fail"
        result["errors"].append(f"XML parse error: {exc}")
        return result

    if local_name(root.tag) != "svg":
        result["errors"].append("Root element is not svg")

    viewbox = parse_viewbox(root.attrib.get("viewBox"))
    if viewbox != [0.0, 0.0, 1280.0, 720.0]:
        result["errors"].append('Root viewBox must be "0 0 1280 720"')

    width = root.attrib.get("width")
    height = root.attrib.get("height")
    if width not in (None, "1280", "1280px"):
        result["warnings"].append("Root width should be 1280")
    if height not in (None, "720", "720px"):
        result["warnings"].append("Root height should be 720")

    card_count = 0
    text_count = 0
    for element in root.iter():
        tag = local_name(element.tag)
        if tag in FORBIDDEN_TAGS:
            result["errors"].append(f"Forbidden SVG tag: {tag}")
        elif tag not in ALLOWED_TAGS:
            result["warnings"].append(f"Unusual SVG tag: {tag}")
        if tag == "rect" and element.attrib.get("data-role") == "card":
            card_count += 1
        if tag == "text":
            text_count += 1
        href = element.attrib.get("href") or element.attrib.get("{http://www.w3.org/1999/xlink}href")
        if href and href.startswith(("http://", "https://")):
            result["errors"].append("Remote image/link reference is not package-safe")

    if card_count == 0:
        result["warnings"].append('No rect with data-role="card" found')
    if text_count == 0:
        result["warnings"].append("No text elements found")

    if render_dir is not None:
        render_dir.mkdir(parents=True, exist_ok=True)
        preview_path = render_dir / f"{svg_path.stem}.png"
        try:
            cairosvg.svg2png(
                url=str(svg_path),
                write_to=str(preview_path),
                output_width=1280,
                output_height=720,
            )
            result["preview"] = str(preview_path)
            if not is_nonblank_png(preview_path):
                result["errors"].append("Rendered preview is blank or nearly blank")
        except Exception as exc:  # noqa: BLE001
            result["errors"].append(f"Render error: {exc}")

    if native_converter is not None:
        trace: list[dict] = []
        try:
            native_converter(
                svg_path,
                slide_num=1,
                verbose=False,
                merge_paragraphs=merge_paragraphs,
                trace_out=trace,
            )
            summary = trace[-1].get("summary", {}) if trace else {}
            events = trace[-1].get("events", []) if trace else []
            native_events = [event for event in events if event.get("decision") == "native"]
            result["native_editable"] = {
                "status": "pass",
                "converted_top_level": summary.get("converted", 0),
                "native_event_count": len(native_events),
                "media_files": summary.get("media_files", 0),
                "animation_targets": summary.get("animation_targets", 0),
            }
            if len(native_events) < 2:
                result["warnings"].append("Native conversion produced fewer than two editable events")
        except Exception as exc:  # noqa: BLE001
            result["native_editable"] = {"status": "fail", "error": str(exc)}
            result["errors"].append(f"Native editable conversion error: {exc}")

    if result["errors"]:
        result["status"] = "fail"
    elif result["warnings"]:
        result["status"] = "warn"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Bento PPT SVG slides.")
    parser.add_argument("svg_files", nargs="+", help="SVG files to validate")
    parser.add_argument("--render-dir", help="Directory for PNG previews")
    parser.add_argument("--json-out", help="Write validation report JSON")
    parser.add_argument("--native-editable", action="store_true", help="Dry-run ppt-master native DrawingML conversion")
    parser.add_argument("--merge-paragraphs", action="store_true", help="Use paragraph merge mode during native dry-run")
    parser.add_argument("--ppt-master-skill-dir", help="Path to the ppt-master skill directory")
    args = parser.parse_args()

    render_dir = Path(args.render_dir).expanduser().resolve() if args.render_dir else None
    native_converter = None
    if args.native_editable:
        try:
            native_converter = load_native_converter(args.ppt_master_skill_dir)
        except PptMasterBridgeError as exc:
            raise SystemExit(str(exc)) from exc

    results = [
        validate_one(
            Path(path).expanduser().resolve(),
            render_dir,
            native_converter=native_converter,
            merge_paragraphs=args.merge_paragraphs,
        )
        for path in args.svg_files
    ]
    report = {
        "total": len(results),
        "passed": sum(1 for item in results if item["status"] == "pass"),
        "warnings": sum(1 for item in results if item["status"] == "warn"),
        "failed": sum(1 for item in results if item["status"] == "fail"),
        "slides": results,
    }

    if args.json_out:
        Path(args.json_out).expanduser().resolve().write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
