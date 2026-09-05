#!/usr/bin/env bash
# ==============================================================================
# 🍎 Joy-Con Mouse Uninstaller for macOS
# ==============================================================================
set -e

BOLD="\033[1m"
CYAN="\033[96m"
GREEN="\033[92m"
YELLOW="\033[93m"
RESET="\033[0m"

echo -e "\n================================================================================"
echo -e "  ${BOLD}🗑️  JOY-CON MOUSE UNINSTALLER FOR MACOS${RESET}"
echo -e "================================================================================\n"

# Remove application files
if [ -d "$HOME/.local/share/joycon-mouse" ]; then
    rm -rf "$HOME/.local/share/joycon-mouse"
    echo -e "  ${GREEN}✓ Removed application files from ~/.local/share/joycon-mouse${RESET}"
fi

# Remove Desktop shortcut
if [ -f "$HOME/Desktop/Joy-Con Mouse.command" ]; then
    rm -f "$HOME/Desktop/Joy-Con Mouse.command"
    echo -e "  ${GREEN}✓ Removed Desktop shortcut${RESET}"
fi

# Remove CLI command
if [ -f "$HOME/.local/bin/joycon-mouse" ]; then
    rm -f "$HOME/.local/bin/joycon-mouse"
    echo -e "  ${GREEN}✓ Removed ~/.local/bin/joycon-mouse${RESET}"
fi

# Prompt config removal
if [ -d "$HOME/.config/joycon-mouse" ]; then
    read -rp "  Remove user settings in ~/.config/joycon-mouse? [y/N]: " REMOVE_CFG
    if [[ "$REMOVE_CFG" =~ ^[yY] ]]; then
        rm -rf "$HOME/.config/joycon-mouse"
        echo -e "  ${GREEN}✓ Removed user configuration.${RESET}"
    else
        echo -e "  ${YELLOW}Preserved user configuration in ~/.config/joycon-mouse.${RESET}"
    fi
fi

echo -e "\n================================================================================"
echo -e "  ${BOLD}${GREEN}✓ Joy-Con Mouse was cleanly uninstalled from your Mac.${RESET}"
echo -e "================================================================================\n"
