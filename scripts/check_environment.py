#!/usr/bin/env python3
"""Check runtime capabilities for the Bento PPT workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

from ppt_master_bridge import PptMasterBridgeError, resolve_native_converter_location


REQUIRED_PACKAGES = {
    "cairosvg": "SVG rendering",
    "PIL": "image inspection through Pillow",
    "pptx": "PowerPoint package creation through python-pptx",
}

OPTIONAL_PACKAGES = {
    "docx": "DOCX fallback extraction through python-docx",
    "pdfplumber": "PDF text/table fallback extraction",
    "pypdf": "PDF embedded image fallback extraction",
    "pandas": "spreadsheet/CSV fallback extraction",
    "openpyxl": "XLSX fallback engine",
    "tabulate": "Markdown table previews for pandas",
}

CJK_FONT_CANDIDATES = [
    "Noto Sans CJK SC",
    "WenQuanYi Micro Hei",
    "Microsoft YaHei",
    "Source Han Sans SC",
]


def check_import(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def status(ok: bool) -> str:
    return "pass" if ok else "fail"


def warn_status(ok: bool) -> str:
    return "pass" if ok else "warn"


def check_markdown_read(skill_dir: Path) -> dict:
    target = skill_dir / "SKILL.md"
    try:
        target.read_text(encoding="utf-8")
        return {"name": "read_markdown", "required": True, "status": "pass", "detail": str(target)}
    except Exception as exc:  # noqa: BLE001
        return {"name": "read_markdown", "required": True, "status": "fail", "detail": str(exc)}


def check_packages() -> list[dict]:
    results: list[dict] = []
    for module_name, detail in REQUIRED_PACKAGES.items():
        ok = check_import(module_name)
        results.append(
            {
                "name": f"python_package:{module_name}",
                "required": True,
                "status": status(ok),
                "detail": detail,
            }
        )
    for module_name, detail in OPTIONAL_PACKAGES.items():
        ok = check_import(module_name)
        results.append(
            {
                "name": f"python_package:{module_name}",
                "required": False,
                "status": warn_status(ok),
                "detail": detail if ok else f"optional missing: {detail}",
            }
        )
    return results


def check_native_converter(explicit: str | None) -> dict:
    try:
        location = resolve_native_converter_location(explicit)
        return {
            "name": "export_editable_pptx",
            "required": True,
            "status": "pass",
            "source": location.source,
            "detail": f"native svg_to_pptx package found at {location.package_dir}",
        }
    except PptMasterBridgeError as exc:
        return {
            "name": "export_editable_pptx",
            "required": True,
            "status": "fail",
            "source": "missing",
            "detail": f"{exc}. Final delivery requires this capability.",
        }


def check_font() -> dict:
    fc_match = shutil.which("fc-match")
    if not fc_match:
        return {
            "name": "cjk_font",
            "required": False,
            "status": "warn",
            "detail": "fc-match unavailable; cannot verify CJK font support",
        }
    for font_name in CJK_FONT_CANDIDATES:
        completed = subprocess.run(
            [fc_match, font_name],
            check=False,
            capture_output=True,
            text=True,
        )
        output = (completed.stdout or completed.stderr).strip()
        if completed.returncode == 0 and output:
            return {
                "name": "cjk_font",
                "required": False,
                "status": "pass",
                "detail": f"{font_name}: {output}",
            }
    return {
        "name": "cjk_font",
        "required": False,
        "status": "warn",
        "detail": "no preferred CJK font candidate matched",
    }


def build_report(args: argparse.Namespace) -> dict:
    skill_dir = Path(__file__).resolve().parents[1]
    checks = [
        {
            "name": "run_python",
            "required": True,
            "status": "pass",
            "detail": sys.executable,
        },
        check_markdown_read(skill_dir),
        *check_packages(),
        check_native_converter(args.ppt_master_skill_dir),
        check_font(),
    ]
    required_failures = [item for item in checks if item["required"] and item["status"] != "pass"]
    optional_warnings = [item for item in checks if not item["required"] and item["status"] != "pass"]
    return {
        "skill_dir": str(skill_dir),
        "python": sys.version,
        "requirement_file": str(skill_dir / "requirement.txt"),
        "status": "pass" if not required_failures else "fail",
        "required_failures": required_failures,
        "optional_warnings": optional_warnings,
        "checks": checks,
    }


def print_text(report: dict) -> None:
    print(f"Bento PPT environment: {report['status']}")
    print(f"Skill dir: {report['skill_dir']}")
    print(f"Requirement file: {report['requirement_file']}")
    for item in report["checks"]:
        marker = "required" if item["required"] else "optional"
        source = f" [{item['source']}]" if item.get("source") else ""
        print(f"- {item['status']}: {item['name']} ({marker}){source} - {item['detail']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Bento PPT workflow runtime capabilities.")
    parser.add_argument("--json-out", help="Write full capability report to JSON")
    parser.add_argument(
        "--ppt-master-skill-dir",
        help="Optional external override: path to svg_to_pptx, its parent, or a legacy ppt-master skill dir",
    )
    args = parser.parse_args()

    report = build_report(args)
    print_text(report)

    if args.json_out:
        Path(args.json_out).expanduser().resolve().write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
