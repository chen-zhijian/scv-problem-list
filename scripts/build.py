#!/usr/bin/env python3
"""Build the manuscript with an existing latexmk installation."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        print(
            "latexmk was not found. Install or select an existing TeX distribution "
            "with latexmk and pdfLaTeX, then run this script again. "
            "This script does not install software.",
            file=sys.stderr,
        )
        return 1

    build_directory = ROOT / "build"
    build_directory.mkdir(exist_ok=True)
    source = ROOT / "papers/src/scv-problem-list.tex"
    destination = ROOT / "papers/scv-problem-list.pdf"
    command = [
        latexmk,
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={build_directory}",
        str(source),
    ]
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Build failed; the published PDF was not replaced: {error}", file=sys.stderr)
        return 1
    built_pdf = build_directory / destination.name
    if not built_pdf.is_file() or not built_pdf.read_bytes().startswith(b"%PDF-"):
        print("Build produced no valid PDF; the published PDF was not replaced.", file=sys.stderr)
        return 1

    temporary = destination.with_suffix(".pdf.tmp")
    try:
        shutil.copyfile(built_pdf, temporary)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    result = subprocess.run([sys.executable, str(ROOT / "scripts/count_problems.py")], cwd=ROOT)
    if result.returncode:
        print("PDF built successfully, but the statistics refresh failed.", file=sys.stderr)
        return result.returncode
    print(f"Built {destination.relative_to(ROOT)}. Auxiliary files remain in build/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
