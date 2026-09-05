#!/usr/bin/env bash
# ==============================================================================
# 🍎 Joy-Con Mouse 1-Click Installer for macOS
# Location: install.sh (macos branch)
# Remote 1-Liner:
#   curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/macos/install.sh | bash
# ==============================================================================
set -e

# ANSI Styling
BOLD="\033[1m"
CYAN="\033[96m"
PURPLE="\033[95m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
DIM="\033[2m"
RESET="\033[0m"

echo -e "\n================================================================================"
echo -e "  ${BOLD}${PURPLE}🍎 JOY-CON MOUSE 1-CLICK INSTALLER FOR MACOS${RESET}"
echo -e "  ${DIM}Transform Switch Joy-Cons into a wireless Mac pointer & media remote.${RESET}"
echo -e "================================================================================\n"

# Check OS
if [ "$(uname -s)" != "Darwin" ]; then
    echo -e "  ${YELLOW}⚠️  Notice: This branch is specifically tailored for Apple macOS.${RESET}"
    echo -e "  If you are running Linux, switch to the 'main' branch:"
    echo -e "  ${BOLD}curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.sh | bash${RESET}\n"
fi

# Step 1: Check Python 3
echo -e "${BOLD}${CYAN}[Step 1/3] Checking Python environment...${RESET}"
if ! command -v python3 &>/dev/null; then
    echo -e "  ${RED}❌ Python 3 was not found on your Mac.${RESET}"
    echo -e "  Please install Python 3 via Homebrew: ${BOLD}brew install python${RESET}"
    echo -e "  or download from: ${BOLD}https://www.python.org/downloads/${RESET}\n"
    exit 1
fi
echo -e "  ${GREEN}✓ Python 3 detected ($(python3 --version))${RESET}\n"

# Step 2: Deploy Application Files
echo -e "${BOLD}${CYAN}[Step 2/3] Setting up Joy-Con Mouse files...${RESET}"
TARGET_DIR="$HOME/.local/share/joycon-mouse"
mkdir -p "$TARGET_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
if [ -f "$SCRIPT_DIR/joycon-mouse-macos.py" ]; then
    echo -e "  Copying files from local directory to $TARGET_DIR..."
    cp -r "$SCRIPT_DIR"/* "$TARGET_DIR/"
else
    echo -e "  ${PURPLE}📦 Fetching latest macOS release from GitHub...${RESET}"
    curl -fsSL https://github.com/ImNotMrReaper/joycon-mouse/archive/refs/heads/macos.tar.gz | tar -xz -C "$TARGET_DIR" --strip-components=1
fi
chmod +x "$TARGET_DIR"/*.command "$TARGET_DIR"/*.py "$TARGET_DIR"/*.sh 2>/dev/null || true
echo -e "  ${GREEN}✓ Application files ready in $TARGET_DIR${RESET}\n"

# Step 3: Desktop Launcher & Terminal Command
echo -e "${BOLD}${CYAN}[Step 3/3] Creating launchers & shortcuts...${RESET}"

# Desktop Launcher
DESKTOP_LAUNCHER="$HOME/Desktop/Joy-Con Mouse.command"
cat > "$DESKTOP_LAUNCHER" << 'EOF_LAUNCHER'
#!/usr/bin/env bash
DIR="$HOME/.local/share/joycon-mouse"
cd "$DIR" || exit 1
exec python3 "$DIR/joycon-mouse-macos.py" "$@"
EOF_LAUNCHER
chmod +x "$DESKTOP_LAUNCHER"
echo -e "  ${GREEN}✓ Created Desktop launcher: 'Joy-Con Mouse.command'${RESET}"

# Global CLI command in ~/.local/bin
mkdir -p "$HOME/.local/bin"
CLI_CMD="$HOME/.local/bin/joycon-mouse"
cat > "$CLI_CMD" << 'EOF_CLI'
#!/usr/bin/env bash
exec python3 "$HOME/.local/share/joycon-mouse/joycon-mouse-macos.py" "$@"
EOF_CLI
chmod +x "$CLI_CMD"
echo -e "  ${GREEN}✓ Created terminal command: joycon-mouse${RESET}"

# Check and add ~/.local/bin to PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    for rc in "$HOME/.zshrc" "$HOME/.bash_profile" "$HOME/.bashrc"; do
        if [ -f "$rc" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
        fi
    done
    export PATH="$HOME/.local/bin:$PATH"
fi

# Configuration Setup
CONFIG_DIR="$HOME/.config/joycon-mouse"
mkdir -p "$CONFIG_DIR"
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cat > "$CONFIG_DIR/config.json" << 'EOF_CFG'
{
  "sensitivity": 1.0,
  "deadzone": 0.10,
  "rumble": true,
  "disabled_modes": []
}
EOF_CFG
fi

# Final Success Banner
echo -e "\n================================================================================"
echo -e "  ${BOLD}${GREEN}🎉 JOY-CON MOUSE IS INSTALLED ON MACOS!${RESET}"
echo -e "================================================================================"
echo -e "  • Installed Folder:  ${CYAN}$TARGET_DIR${RESET}"
echo -e "  • Desktop Shortcut:  ${CYAN}Joy-Con Mouse.command${RESET} (on your Desktop)"
echo -e "  • Terminal Command:  ${CYAN}joycon-mouse${RESET}"
echo -e "--------------------------------------------------------------------------------"
echo -e "  ⚠️  ${BOLD}${YELLOW}CRITICAL MACOS ACCESSIBILITY PERMISSION:${RESET}"
echo -e "  macOS requires granting Accessibility access so Joy-Con Mouse can move the pointer:"
echo -e "  1. Open ${BOLD}System Settings > Privacy & Security > Accessibility${RESET}."
echo -e "  2. Toggle ${BOLD}ON${RESET} for ${BOLD}Terminal${RESET} (or iTerm2 / your terminal app)."
echo -e "--------------------------------------------------------------------------------"
echo -e "  🎮 ${BOLD}Getting Started:${RESET}"
echo -e "  1. Pair your Joy-Con: System Settings > Bluetooth (Hold Sync button on rail)."
echo -e "  2. Double-click ${BOLD}Joy-Con Mouse.command${RESET} on your Desktop!"
echo -e "================================================================================"
echo ""
