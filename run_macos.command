#!/usr/bin/env bash
# ==============================================================================
# 🍎 Joy-Con Mouse for macOS Double-Click Launcher
# ==============================================================================
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR" || exit 1

clear
echo "================================================================================"
echo "  🎮 JOY-CON MOUSE FOR MACOS (Beta Preview)"
echo "================================================================================"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 was not found on your Mac!"
    echo "Please install Python 3 from https://www.python.org/downloads/ or via Homebrew."
    read -rp "Press Enter to exit..."
    exit 1
fi

echo "[OK] Launching Joy-Con Mouse driver..."
python3 "$DIR/joycon-mouse-macos.py" "$@"

read -rp "Press Enter to close this terminal window..."
