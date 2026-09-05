#!/usr/bin/env python3
"""
Joy-Con Mouse & Universal Remote - Windows Entry Point.
Directly executes the native Windows driver using standard library winmm.dll and user32.dll.
"""
import runpy
import sys
from pathlib import Path


def main():
    target = Path(__file__).parent / "joycon-mouse-windows.py"
    if target.exists():
        runpy.run_path(str(target), run_name="__main__")
    else:
        sys.exit("Error: joycon-mouse-windows.py not found.")


if __name__ == "__main__":
    main()
