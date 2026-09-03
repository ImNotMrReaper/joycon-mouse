#!/usr/bin/env bash
# ==============================================================================
# 🎮 Joy-Con Mouse & Universal Remote Interactive Installer for Linux
# Location: install.sh
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
echo -e "  ${BOLD}${PURPLE}🎮 JOY-CON MOUSE INTERACTIVE INSTALLER FOR LINUX${RESET}"
echo -e "  ${DIM}Transform Joy-Cons & Gamepads into a precision mouse & media remote.${RESET}"
echo -e "================================================================================\n"

# 1. Verify Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ Error: Python 3 is required but was not found on your system.${RESET}"
    echo -e "   Please install Python 3 with your package manager (e.g. 'sudo apt install python3') and rerun this installer.\n"
    exit 1
fi

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IS_GIT_REPO=false
if [ -d "$SOURCE_DIR/.git" ]; then
    IS_GIT_REPO=true
fi

# 2. Installation Location Selection
echo -e "${BOLD}${CYAN}[Step 1/5] Choose Installation Location${RESET}"
echo -e "${DIM}Where would you like Joy-Con Mouse files to be installed?${RESET}\n"

DEFAULT_USER_DIR="$HOME/.local/share/joycon-mouse"
DEFAULT_SYS_DIR="/opt/joycon-mouse"

if [ "$IS_GIT_REPO" = true ]; then
    echo -e "  ${BOLD}[1] Standard User Directory:${RESET}  $DEFAULT_USER_DIR ${GREEN}(Recommended)${RESET}"
    echo -e "      Clean, isolated user directory. No root password needed."
    echo -e "  ${BOLD}[2] Keep in Current Directory:${RESET} $SOURCE_DIR"
    echo -e "      Links the global command directly to this Git clone without copying files."
    echo -e "  ${BOLD}[3] System-wide Directory:${RESET}    $DEFAULT_SYS_DIR"
    echo -e "      Installs system-wide for all users on this computer (requires sudo)."
    echo -e "  ${BOLD}[4] Custom Directory:${RESET}         Enter your own custom file path.\n"

    read -rp "$(echo -e "  Select option [1-4] [${GREEN}1${RESET}]: ")" LOC_CHOICE
    LOC_CHOICE="${LOC_CHOICE:-1}"

    case "$LOC_CHOICE" in
        1) TARGET_DIR="$DEFAULT_USER_DIR" ;;
        2) TARGET_DIR="$SOURCE_DIR" ;;
        3) TARGET_DIR="$DEFAULT_SYS_DIR" ;;
        4)
            read -rp "$(echo -e "  Enter custom installation directory path: ")" CUSTOM_PATH
            # Expand tilde
            CUSTOM_PATH="${CUSTOM_PATH/#\~/$HOME}"
            if [ -z "$CUSTOM_PATH" ]; then
                TARGET_DIR="$DEFAULT_USER_DIR"
            else
                TARGET_DIR="$CUSTOM_PATH"
            fi
            ;;
        *) TARGET_DIR="$DEFAULT_USER_DIR" ;;
    esac
else
    echo -e "  ${BOLD}[1] Standard User Directory:${RESET}  $DEFAULT_USER_DIR ${GREEN}(Recommended)${RESET}"
    echo -e "      Clean, isolated user directory. No root password needed."
    echo -e "  ${BOLD}[2] System-wide Directory:${RESET}    $DEFAULT_SYS_DIR"
    echo -e "      Installs system-wide for all users on this computer (requires sudo)."
    echo -e "  ${BOLD}[3] Custom Directory:${RESET}         Enter your own custom file path.\n"

    read -rp "$(echo -e "  Select option [1-3] [${GREEN}1${RESET}]: ")" LOC_CHOICE
    LOC_CHOICE="${LOC_CHOICE:-1}"

    case "$LOC_CHOICE" in
        1) TARGET_DIR="$DEFAULT_USER_DIR" ;;
        2) TARGET_DIR="$DEFAULT_SYS_DIR" ;;
        3)
            read -rp "$(echo -e "  Enter custom installation directory path: ")" CUSTOM_PATH
            CUSTOM_PATH="${CUSTOM_PATH/#\~/$HOME}"
            if [ -z "$CUSTOM_PATH" ]; then
                TARGET_DIR="$DEFAULT_USER_DIR"
            else
                TARGET_DIR="$CUSTOM_PATH"
            fi
            ;;
        *) TARGET_DIR="$DEFAULT_USER_DIR" ;;
    esac
fi

echo -e "  ${GREEN}✓ Selected destination:${RESET} $TARGET_DIR\n"

# 3. Copy Application Files (if not linking in-place)
echo -e "${BOLD}${CYAN}[Step 2/5] Setting up program files...${RESET}"
if [ "$TARGET_DIR" != "$SOURCE_DIR" ]; then
    echo -e "  Copying files to $TARGET_DIR..."
    if [[ "$TARGET_DIR" =~ ^/opt/ ]] || [[ "$TARGET_DIR" =~ ^/usr/ ]]; then
        sudo mkdir -p "$TARGET_DIR"
        sudo cp -r "$SOURCE_DIR/joycon-mouse.py" "$SOURCE_DIR/setup_wizard.py" "$SOURCE_DIR/setup.sh" "$SOURCE_DIR/uninstall.sh" "$SOURCE_DIR/test_buttons.py" "$SOURCE_DIR/modes" "$SOURCE_DIR/custom_modes" "$SOURCE_DIR/CUSTOM_MODES.md" "$SOURCE_DIR/README.md" "$SOURCE_DIR/LICENSE" "$TARGET_DIR/"
        sudo chmod +x "$TARGET_DIR"/*.py "$TARGET_DIR"/*.sh 2>/dev/null || true
    else
        mkdir -p "$TARGET_DIR"
        cp -r "$SOURCE_DIR/joycon-mouse.py" "$SOURCE_DIR/setup_wizard.py" "$SOURCE_DIR/setup.sh" "$SOURCE_DIR/uninstall.sh" "$SOURCE_DIR/test_buttons.py" "$SOURCE_DIR/modes" "$SOURCE_DIR/custom_modes" "$SOURCE_DIR/CUSTOM_MODES.md" "$SOURCE_DIR/README.md" "$SOURCE_DIR/LICENSE" "$TARGET_DIR/"
        chmod +x "$TARGET_DIR"/*.py "$TARGET_DIR"/*.sh 2>/dev/null || true
    fi
    echo -e "  ${GREEN}✓ Files successfully deployed.${RESET}"
else
    chmod +x "$SOURCE_DIR"/*.py "$SOURCE_DIR"/*.sh 2>/dev/null || true
    echo -e "  ${GREEN}✓ Using existing directory in-place.${RESET}"
fi

# 4. Global Command Setup (PATH)
echo -e "\n${BOLD}${CYAN}[Step 3/5] Configuring global terminal command...${RESET}"
if [[ "$TARGET_DIR" =~ ^/opt/ ]] || [[ "$TARGET_DIR" =~ ^/usr/ ]]; then
    BIN_PATH="/usr/local/bin/joycon-mouse"
    echo -e "  Creating system executable launcher at $BIN_PATH (requires sudo)..."
    sudo tee "$BIN_PATH" > /dev/null << EOF
#!/usr/bin/env bash
cd "$TARGET_DIR" || exit 1
exec python3 "$TARGET_DIR/joycon-mouse.py" "\$@"
EOF
    sudo chmod +x "$BIN_PATH"
    echo -e "  ${GREEN}✓ Global command '$BIN_PATH' installed.${RESET}"
else
    BIN_DIR="$HOME/.local/bin"
    BIN_PATH="$BIN_DIR/joycon-mouse"
    mkdir -p "$BIN_DIR"
    cat > "$BIN_PATH" << EOF
#!/usr/bin/env bash
cd "$TARGET_DIR" || exit 1
exec python3 "$TARGET_DIR/joycon-mouse.py" "\$@"
EOF
    chmod +x "$BIN_PATH"
    echo -e "  ${GREEN}✓ User command '$BIN_PATH' installed.${RESET}"

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "  ${YELLOW}Notice: '$HOME/.local/bin' is not currently in your system PATH.${RESET}"
        read -rp "$(echo -e "  Add it to your ~/.bashrc automatically? [${GREEN}Y${RESET}/n]: ")" ADD_PATH
        ADD_PATH="${ADD_PATH:-y}"
        if [[ "$ADD_PATH" =~ ^[yY] ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            [ -f "$HOME/.zshrc" ] && echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" || true
            export PATH="$HOME/.local/bin:$PATH"
            echo -e "  ${GREEN}✓ Added to ~/.bashrc.${RESET}"
        fi
    fi
fi

# 5. Linux Permissions & Hardware Configuration
echo -e "\n${BOLD}${CYAN}[Step 4/5] Checking Linux hardware permissions...${RESET}"

# A. Input group check
if ! groups "$USER" | grep -q '\binput\b'; then
    echo -e "  ${YELLOW}⚠️  Permission notice:${RESET} Linux requires your user to be in the 'input' group to create virtual mouse events."
    read -rp "$(echo -e "  Add '$USER' to the 'input' group now? [${GREEN}Y${RESET}/n]: ")" GRANT_INPUT
    GRANT_INPUT="${GRANT_INPUT:-y}"
    if [[ "$GRANT_INPUT" =~ ^[yY] ]]; then
        sudo usermod -aG input "$USER" || echo -e "  ${RED}Could not add user automatically. Run manually: sudo usermod -aG input \$USER${RESET}"
        echo -e "  ${GREEN}✓ Added '$USER' to 'input' group.${RESET} ${DIM}(Note: May require logging out once to take effect)${RESET}"
    fi
else
    echo -e "  ${GREEN}✓ User '$USER' is already in the 'input' group.${RESET}"
fi

# B. uinput kernel module
if ! lsmod | grep -q '\buinput\b'; then
    echo -e "  Loading Linux uinput kernel module..."
    sudo modprobe uinput 2>/dev/null || true
fi

# Ensure persistent uinput loading across reboots
if [ ! -f /etc/modules-load.d/uinput.conf ]; then
    echo "uinput" | sudo tee /etc/modules-load.d/uinput.conf > /dev/null 2>&1 || true
fi
echo -e "  ${GREEN}✓ Linux uinput module verified active.${RESET}"

# C. BlueZ Bluetooth Reconnect Optimization
BLUETOOTH_INPUT_CONF="/etc/bluetooth/input.conf"
NEEDS_BT_FIX=false
if [ -f "$BLUETOOTH_INPUT_CONF" ]; then
    if grep -qE "ClassicBondedOnly\s*=\s*true" "$BLUETOOTH_INPUT_CONF" 2>/dev/null; then
        NEEDS_BT_FIX=true
    elif ! grep -q "ClassicBondedOnly" "$BLUETOOTH_INPUT_CONF" 2>/dev/null; then
        NEEDS_BT_FIX=true
    fi
fi

if [ "$NEEDS_BT_FIX" = true ]; then
    echo -e "\n  ${PURPLE}💡 Bluetooth Reconnection Optimization:${RESET}"
    echo -e "     By default, Ubuntu/BlueZ rejects automatic reconnects from Nintendo Switch controllers on wake."
    read -rp "$(echo -e "     Apply the BlueZ auto-reconnect optimization now? [${GREEN}Y${RESET}/n]: ")" FIX_BT
    FIX_BT="${FIX_BT:-y}"
    if [[ "$FIX_BT" =~ ^[yY] ]]; then
        sudo sed -i 's/.*ClassicBondedOnly=.*/ClassicBondedOnly=false/' "$BLUETOOTH_INPUT_CONF" 2>/dev/null || true
        sudo sed -i 's/.*FastConnectable=.*/FastConnectable=true/' /etc/bluetooth/main.conf 2>/dev/null || true
        sudo systemctl restart bluetooth 2>/dev/null || true
        echo -e "  ${GREEN}✓ Applied Bluetooth auto-reconnect optimization.${RESET}"
    fi
else
    echo -e "  ${GREEN}✓ Bluetooth auto-reconnect optimization is already active.${RESET}"
fi

# 6. Interactive Setup Wizard
echo -e "\n${BOLD}${CYAN}[Step 5/5] Controller Setup & Customization Wizard${RESET}"
echo -e "${DIM}Configure your preferred modes, pointer sensitivity, rumble, and autostart.${RESET}\n"

read -rp "$(echo -e "  Launch interactive setup wizard now? [${GREEN}Y${RESET}/n]: ")" RUN_SETUP
RUN_SETUP="${RUN_SETUP:-y}"

if [[ "$RUN_SETUP" =~ ^[yY] ]]; then
    python3 "$TARGET_DIR/setup_wizard.py"
fi

# 7. Final Success Banner
echo -e "\n================================================================================"
echo -e "  ${BOLD}${GREEN}🎉 JOY-CON MOUSE INSTALLATION COMPLETE!${RESET}"
echo -e "================================================================================"
echo -e "  • Installed Folder:  ${CYAN}$TARGET_DIR${RESET}"
echo -e "  • Global Command:    ${CYAN}joycon-mouse${RESET}"
echo -e "  • Reconfigure:       ${CYAN}joycon-mouse --setup${RESET}  ${DIM}(or run $TARGET_DIR/setup.sh)${RESET}"
echo -e "  • Uninstall:         ${CYAN}joycon-mouse --uninstall${RESET}  ${DIM}(or run $TARGET_DIR/uninstall.sh)${RESET}"
echo -e "--------------------------------------------------------------------------------"
echo -e "  🎮 ${BOLD}Getting Started:${RESET}"
echo -e "  1. Pair your Joy-Con via Bluetooth (Hold small round pairing button until LEDs cycle)."
echo -e "  2. List detected controllers:  ${BOLD}joycon-mouse -l${RESET}"
echo -e "  3. Start desktop controller:   ${BOLD}joycon-mouse${RESET}"
echo -e "================================================================================\n"
