#!/usr/bin/env bash
# ==============================================================================
# Joy-Con Mouse Interactive Setup & Configuration Script
# Location: setup.sh
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "❌ Error: Python 3 is required but was not found on your system."
    echo "   Please install Python 3 (e.g. 'sudo apt install python3') and try again."
    exit 1
fi

# Execute setup wizard
exec python3 "$SCRIPT_DIR/setup_wizard.py" "$@"
