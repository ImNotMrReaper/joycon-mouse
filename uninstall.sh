#!/usr/bin/env bash
# ==============================================================================
# 🗑️ Joy-Con Mouse Interactive Uninstaller for Linux
# Location: uninstall.sh
# ==============================================================================
set -e

# ANSI Color Codes
BOLD="\033[1m"
CYAN="\033[96m"
PURPLE="\033[95m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
DIM="\033[2m"
RESET="\033[0m"

echo -e "\n================================================================================"
echo -e "  ${BOLD}${RED}🗑️  JOY-CON MOUSE INTERACTIVE UNINSTALLER${RESET}"
echo -e "  ${DIM}Easily and cleanly remove Joy-Con Mouse from your Linux system.${RESET}"
echo -e "================================================================================\n"

# 1. Safety Confirmation
read -rp "$(echo -e "${BOLD}Are you sure you want to uninstall Joy-Con Mouse?${RESET} [y/${GREEN}N${RESET}]: ")" CONFIRM_UNINSTALL
CONFIRM_UNINSTALL="${CONFIRM_UNINSTALL:-n}"
case "$CONFIRM_UNINSTALL" in
    [yY]|[yY][eE][sS])
        ;;
    *)
        echo -e "\n${GREEN}Uninstallation cancelled.${RESET} Joy-Con Mouse remains installed.\n"
        exit 0
        ;;
esac

echo ""

# 2. Stop and Remove Background Systemd Service
echo -e "${BOLD}${CYAN}[1/4] Checking background services...${RESET}"
SERVICE_FILE="$HOME/.config/systemd/user/joycon-mouse.service"
if systemctl --user is-active --quiet joycon-mouse.service 2>/dev/null; then
    echo -e "  Stopping active background service..."
    systemctl --user stop joycon-mouse.service 2>/dev/null || true
fi

if systemctl --user is-enabled --quiet joycon-mouse.service 2>/dev/null; then
    echo -e "  Disabling systemd background service..."
    systemctl --user disable joycon-mouse.service 2>/dev/null || true
fi

if [ -f "$SERVICE_FILE" ]; then
    rm -f "$SERVICE_FILE"
    systemctl --user daemon-reload 2>/dev/null || true
    echo -e "  ${GREEN}✓ Removed systemd service file:${RESET} $SERVICE_FILE"
else
    echo -e "  ${DIM}No background systemd service was installed.${RESET}"
fi

# 3. Remove Global Executable Commands
echo -e "\n${BOLD}${CYAN}[2/4] Removing global command shortcuts...${RESET}"
REMOVED_CMD=false

if [ -f "$HOME/.local/bin/joycon-mouse" ] || [ -L "$HOME/.local/bin/joycon-mouse" ]; then
    rm -f "$HOME/.local/bin/joycon-mouse"
    echo -e "  ${GREEN}✓ Removed command:${RESET} $HOME/.local/bin/joycon-mouse"
    REMOVED_CMD=true
fi

if [ -f "/usr/local/bin/joycon-mouse" ] || [ -L "/usr/local/bin/joycon-mouse" ]; then
    echo -e "  Removing system-wide command in /usr/local/bin (may request sudo password)..."
    sudo rm -f "/usr/local/bin/joycon-mouse" 2>/dev/null || true
    echo -e "  ${GREEN}✓ Removed command:${RESET} /usr/local/bin/joycon-mouse"
    REMOVED_CMD=true
fi

if [ "$REMOVED_CMD" = false ]; then
    echo -e "  ${DIM}No global command links found.${RESET}"
fi

# 4. Remove Application Files
echo -e "\n${BOLD}${CYAN}[3/4] Checking installed application files...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if script is running in standard user share directory
if [ "$SCRIPT_DIR" = "$HOME/.local/share/joycon-mouse" ]; then
    read -rp "$(echo -e "  Remove installed files from ${BOLD}$SCRIPT_DIR${RESET}? [${GREEN}Y${RESET}/n]: ")" REMOVE_FILES
    REMOVE_FILES="${REMOVE_FILES:-y}"
    if [[ "$REMOVE_FILES" =~ ^[yY] ]]; then
        cd "$HOME" || exit 1
        rm -rf "$SCRIPT_DIR"
        echo -e "  ${GREEN}✓ Removed application folder:${RESET} $SCRIPT_DIR"
    else
        echo -e "  ${DIM}Kept application folder:${RESET} $SCRIPT_DIR"
    fi
elif [ "$SCRIPT_DIR" = "/opt/joycon-mouse" ]; then
    read -rp "$(echo -e "  Remove installed files from ${BOLD}$SCRIPT_DIR${RESET}? (requires sudo) [${GREEN}Y${RESET}/n]: ")" REMOVE_FILES
    REMOVE_FILES="${REMOVE_FILES:-y}"
    if [[ "$REMOVE_FILES" =~ ^[yY] ]]; then
        cd "$HOME" || exit 1
        sudo rm -rf "$SCRIPT_DIR"
        echo -e "  ${GREEN}✓ Removed system application folder:${RESET} $SCRIPT_DIR"
    else
        echo -e "  ${DIM}Kept system application folder:${RESET} $SCRIPT_DIR"
    fi
elif [ -d "$SCRIPT_DIR/.git" ]; then
    echo -e "  ${DIM}Current directory ($SCRIPT_DIR) is a Git development repository.${RESET}"
    echo -e "  ${GREEN}✓ Development source files were preserved.${RESET}"
else
    # Non-standard directory
    read -rp "$(echo -e "  Remove files in current directory ${BOLD}$SCRIPT_DIR${RESET}? [y/${GREEN}N${RESET}]: ")" REMOVE_FILES
    REMOVE_FILES="${REMOVE_FILES:-n}"
    if [[ "$REMOVE_FILES" =~ ^[yY] ]]; then
        cd "$HOME" || exit 1
        rm -rf "$SCRIPT_DIR"
        echo -e "  ${GREEN}✓ Removed folder:${RESET} $SCRIPT_DIR"
    fi
fi

# 5. User Configuration & Custom Modes
echo -e "\n${BOLD}${CYAN}[4/4] Checking user settings and custom modes...${RESET}"
CONFIG_DIR="$HOME/.config/joycon-mouse"

if [ -d "$CONFIG_DIR" ]; then
    echo -e "  Found user configuration directory at: ${BOLD}$CONFIG_DIR${RESET}"
    echo -e "  ${DIM}(Contains your saved sensitivity, rumble settings, and any personal custom modes)${RESET}"
    read -rp "$(echo -e "  Do you want to delete this configuration folder too? [y/${GREEN}N${RESET}]: ")" REMOVE_CONFIG
    REMOVE_CONFIG="${REMOVE_CONFIG:-n}"
    if [[ "$REMOVE_CONFIG" =~ ^[yY] ]]; then
        rm -rf "$CONFIG_DIR"
        echo -e "  ${YELLOW}✓ Removed user configuration:${RESET} $CONFIG_DIR"
    else
        echo -e "  ${GREEN}✓ Kept user settings safe at:${RESET} $CONFIG_DIR"
    fi
else
    echo -e "  ${DIM}No user configuration folder found.${RESET}"
fi

# Completion Banner
echo -e "\n================================================================================"
echo -e "  ${GREEN}${BOLD}✓ JOY-CON MOUSE HAS BEEN CLEANLY UNINSTALLED!${RESET}"
echo -e "================================================================================\n"
