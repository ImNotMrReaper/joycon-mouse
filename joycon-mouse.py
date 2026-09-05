#!/usr/bin/env python3
"""
Joy-Con Mouse & Universal Remote - macOS Entry Point.
Directly executes the native macOS driver using Apple CoreGraphics and ApplicationServices.
"""
import runpy
import sys
from pathlib import Path


def main():
    target = Path(__file__).parent / "joycon-mouse-macos.py"
    if target.exists():
        runpy.run_path(str(target), run_name="__main__")
    else:
        sys.exit("Error: joycon-mouse-macos.py not found.")


if __name__ == "__main__":
    main()
