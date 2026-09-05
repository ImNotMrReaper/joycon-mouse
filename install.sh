#!/usr/bin/env bash
# ==============================================================================
# 🎮 Joy-Con Mouse & Universal Remote Universal 1-Click Installer
# Supports: Linux (Ubuntu, Debian, Fedora, Arch) & macOS (auto-delegation)
# Remote 1-Liner:
#   curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.sh | bash
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

NONINTERACTIVE="${NONINTERACTIVE:-0}"
for arg in "$@"; do
    case "$arg" in
        -y|--yes|--non-interactive)
            NONINTERACTIVE=1
            ;;
    esac
done

# Pipe-safe and non-interactive input helper
prompt_read() {
    local prompt_msg="$1"
    local out_var="$2"
    local default_val="$3"
    if [ "$NONINTERACTIVE" = "1" ] || [ -n "$CI" ]; then
        eval "$out_var=\"$default_val\""
    elif [ -t 0 ]; then
        read -rp "$prompt_msg" "$out_var"
    elif [ -r /dev/tty ]; then
        read -rp "$prompt_msg" "$out_var" < /dev/tty
    else
        eval "$out_var=\"$default_val\""
    fi
}

# --- Operating System Safety Check ---
if [ "$(uname -s)" = "Darwin" ]; then
    echo -e "\n  ${PURPLE}🍎 macOS detected!${RESET}"
    echo -e "  This installer on the main branch is optimized specifically for Linux."
    echo -e "  To install Joy-Con Mouse for macOS, run the macOS branch 1-liner:"
    echo -e "  ${BOLD}curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/macos/install.sh | bash${RESET}\n"
    exit 0
fi

# --- Linux Platform Flow ---
echo -e "\n================================================================================"
echo -e "  ${BOLD}${PURPLE}🎮 JOY-CON MOUSE INTERACTIVE INSTALLER FOR LINUX${RESET}"
echo -e "  ${DIM}Transform Joy-Cons & Gamepads into a precision mouse & media remote.${RESET}"
echo -e "================================================================================\n"

# WSL Notice
if [ -f /proc/version ] && grep -qi "microsoft" /proc/version; then
    echo -e "  ${YELLOW}ℹ️  Notice: Running inside Windows Subsystem for Linux (WSL).${RESET}"
    echo -e "  ${DIM}For native Windows desktop control without VM setup, we recommend running${RESET}"
    echo -e "  ${BOLD}irm https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.ps1 | iex${RESET}"
    echo -e "  ${DIM}directly inside Windows PowerShell!${RESET}\n"
fi

# 1. Dependency Resolution
check_and_install_dependencies() {
    echo -e "${BOLD}${CYAN}[Step 1/6] Checking system dependencies...${RESET}"

    local MISSING=()
    if ! command -v python3 &>/dev/null; then MISSING+=("python3"); fi
    if ! command -v git &>/dev/null; then MISSING+=("git"); fi
    if ! command -v bluetoothctl &>/dev/null; then MISSING+=("bluez"); fi
    if ! command -v modprobe &>/dev/null; then MISSING+=("kmod"); fi

    if [ ${#MISSING[@]} -eq 0 ]; then
        echo -e "  ${GREEN}✓ All core dependencies are installed (python3, git, bluez, kmod).${RESET}\n"
        return 0
    fi

    echo -e "  ${YELLOW}⚠️  The following required system tools are missing:${RESET} ${BOLD}${MISSING[*]}${RESET}"
    echo -e "  Attempting to install automatically using your system package manager...\n"

    if command -v apt-get &>/dev/null; then
        echo -e "  Detected APT package manager (Ubuntu/Debian/Mint/Pop!_OS)."
        sudo apt-get update -qq || true
        sudo apt-get install -y "${MISSING[@]}"
    elif command -v dnf &>/dev/null; then
        echo -e "  Detected DNF package manager (Fedora/RHEL)."
        sudo dnf install -y "${MISSING[@]}"
    elif command -v pacman &>/dev/null; then
        echo -e "  Detected Pacman package manager (Arch Linux/Manjaro/SteamOS)."
        local ARCH_PKGS=()
        for p in "${MISSING[@]}"; do
            if [ "$p" = "python3" ]; then ARCH_PKGS+=("python");
            elif [ "$p" = "bluez" ]; then ARCH_PKGS+=("bluez" "bluez-utils");
            else ARCH_PKGS+=("$p"); fi
        done
        sudo pacman -S --noconfirm "${ARCH_PKGS[@]}"
    elif command -v zypper &>/dev/null; then
        echo -e "  Detected Zypper package manager (openSUSE)."
        sudo zypper install -y "${MISSING[@]}"
    else
        echo -e "  ${RED}Could not auto-detect package manager.${RESET}"
        echo -e "  Please manually install: ${BOLD}${MISSING[*]}${RESET}\n"
        exit 1
    fi

    echo -e "  ${GREEN}✓ Missing dependencies successfully installed.${RESET}\n"
}

check_and_install_dependencies

# 2. Remote Bootstrap or Local Source Detection
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
BOOTSTRAP_DIR=""
IS_GIT_REPO=false

if [ -f "$SCRIPT_DIR/joycon-mouse.py" ]; then
    SOURCE_DIR="$SCRIPT_DIR"
    if [ -d "$SOURCE_DIR/.git" ]; then
        IS_GIT_REPO=true
    fi
else
    echo -e "  ${PURPLE}📦 Fetching latest Joy-Con Mouse repository from GitHub...${RESET}"
    BOOTSTRAP_DIR="$(mktemp -d -t joycon-mouse-install-XXXXXX)"
    trap 'rm -rf "$BOOTSTRAP_DIR"' EXIT
    if command -v git &>/dev/null; then
        git clone --depth 1 https://github.com/ImNotMrReaper/joycon-mouse.git "$BOOTSTRAP_DIR" --quiet
    else
        curl -fsSL https://github.com/ImNotMrReaper/joycon-mouse/archive/refs/heads/main.tar.gz | tar -xz -C "$BOOTSTRAP_DIR" --strip-components=1
    fi
    SOURCE_DIR="$BOOTSTRAP_DIR"
    IS_GIT_REPO=false
fi

# 3. Installation Location Selection
echo -e "${BOLD}${CYAN}[Step 2/6] Choose Installation Location${RESET}"
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

    prompt_read "  Select option [1-4] [${GREEN}1${RESET}]: " LOC_CHOICE "1"
    LOC_CHOICE="${LOC_CHOICE:-1}"

    case "$LOC_CHOICE" in
        1) TARGET_DIR="$DEFAULT_USER_DIR" ;;
        2) TARGET_DIR="$SOURCE_DIR" ;;
        3) TARGET_DIR="$DEFAULT_SYS_DIR" ;;
        4)
            prompt_read "  Enter custom installation directory path: " CUSTOM_PATH ""
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

    prompt_read "  Select option [1-3] [${GREEN}1${RESET}]: " LOC_CHOICE "1"
    LOC_CHOICE="${LOC_CHOICE:-1}"

    case "$LOC_CHOICE" in
        1) TARGET_DIR="$DEFAULT_USER_DIR" ;;
        2) TARGET_DIR="$DEFAULT_SYS_DIR" ;;
        3)
            prompt_read "  Enter custom installation directory path: " CUSTOM_PATH ""
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

# 4. Copy Application Files (if not linking in-place)
echo -e "${BOLD}${CYAN}[Step 3/6] Setting up program files...${RESET}"
if [ "$TARGET_DIR" != "$SOURCE_DIR" ]; then
    echo -e "  Deploying files to $TARGET_DIR..."
    if [[ "$TARGET_DIR" =~ ^/opt/ ]] || [[ "$TARGET_DIR" =~ ^/usr/ ]]; then
        sudo mkdir -p "$TARGET_DIR"
        sudo cp -r "$SOURCE_DIR/joycon-mouse.py" "$SOURCE_DIR/setup_wizard.py" "$SOURCE_DIR/setup.sh" "$SOURCE_DIR/uninstall.sh" "$SOURCE_DIR/test_buttons.py" "$SOURCE_DIR/modes" "$SOURCE_DIR/custom_modes" "$SOURCE_DIR/completions" "$SOURCE_DIR/CUSTOM_MODES.md" "$SOURCE_DIR/README.md" "$SOURCE_DIR/LICENSE" "$TARGET_DIR/"
        sudo chmod +x "$TARGET_DIR"/*.py "$TARGET_DIR"/*.sh 2>/dev/null || true
    else
        mkdir -p "$TARGET_DIR"
        cp -r "$SOURCE_DIR/joycon-mouse.py" "$SOURCE_DIR/setup_wizard.py" "$SOURCE_DIR/setup.sh" "$SOURCE_DIR/uninstall.sh" "$SOURCE_DIR/test_buttons.py" "$SOURCE_DIR/modes" "$SOURCE_DIR/custom_modes" "$SOURCE_DIR/completions" "$SOURCE_DIR/CUSTOM_MODES.md" "$SOURCE_DIR/README.md" "$SOURCE_DIR/LICENSE" "$TARGET_DIR/"
        chmod +x "$TARGET_DIR"/*.py "$TARGET_DIR"/*.sh 2>/dev/null || true
    fi
    echo -e "  ${GREEN}✓ Files successfully deployed.${RESET}"
else
    chmod +x "$SOURCE_DIR"/*.py "$SOURCE_DIR"/*.sh 2>/dev/null || true
    echo -e "  ${GREEN}✓ Using existing directory in-place.${RESET}"
fi

# 5. Global Command Setup (PATH) & Shell Completion
echo -e "\n${BOLD}${CYAN}[Step 4/6] Configuring global terminal command & completions...${RESET}"
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

    # Install system-wide bash completion
    if [ -f "$SOURCE_DIR/completions/joycon-mouse" ]; then
        sudo mkdir -p "/usr/share/bash-completion/completions"
        sudo cp "$SOURCE_DIR/completions/joycon-mouse" "/usr/share/bash-completion/completions/joycon-mouse"
        echo -e "  ${GREEN}✓ Shell completion & auto-suggestions installed.${RESET}"
    fi
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

    # Install user bash completion
    if [ -f "$SOURCE_DIR/completions/joycon-mouse" ]; then
        mkdir -p "$HOME/.local/share/bash-completion/completions"
        cp "$SOURCE_DIR/completions/joycon-mouse" "$HOME/.local/share/bash-completion/completions/joycon-mouse"
        echo -e "  ${GREEN}✓ Shell completion & auto-suggestions installed.${RESET}"
    fi

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "  ${YELLOW}Notice: '$HOME/.local/bin' is not currently in your system PATH.${RESET}"
        prompt_read "  Add it to your ~/.bashrc automatically? [${GREEN}Y${RESET}/n]: " ADD_PATH "y"
        ADD_PATH="${ADD_PATH:-y}"
        if [[ "$ADD_PATH" =~ ^[yY] ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            [ -f "$HOME/.zshrc" ] && echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" || true
            export PATH="$HOME/.local/bin:$PATH"
            echo -e "  ${GREEN}✓ Added to ~/.bashrc.${RESET}"
        fi
    fi
fi

# 6. Linux Permissions & Hardware Configuration
echo -e "\n${BOLD}${CYAN}[Step 5/6] Checking Linux hardware permissions...${RESET}"

# A. Input group check
if ! groups "$USER" | grep -q '\binput\b'; then
    echo -e "  ${YELLOW}⚠️  Permission notice:${RESET} Linux requires your user to be in the 'input' group to create virtual mouse events."
    prompt_read "  Add '$USER' to the 'input' group now? [${GREEN}Y${RESET}/n]: " GRANT_INPUT "y"
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
    prompt_read "     Apply the BlueZ auto-reconnect optimization now? [${GREEN}Y${RESET}/n]: " FIX_BT "y"
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

# 7. Interactive Setup Wizard
echo -e "\n${BOLD}${CYAN}[Step 6/6] Controller Setup & Customization Wizard${RESET}"
echo -e "${DIM}Configure your preferred modes, pointer sensitivity, rumble, and autostart.${RESET}\n"

if [ -t 0 ] || [ -r /dev/tty ]; then
    prompt_read "  Launch interactive setup wizard now? [${GREEN}Y${RESET}/n]: " RUN_SETUP "y"
    RUN_SETUP="${RUN_SETUP:-y}"

    if [[ "$RUN_SETUP" =~ ^[yY] ]]; then
        python3 "$TARGET_DIR/setup_wizard.py"
    fi
else
    echo -e "  ${DIM}Skipping interactive setup wizard (non-interactive session).${RESET}"
    echo -e "  Run ${BOLD}joycon-mouse --setup${RESET} anytime to configure!"
fi

# 8. Final Success Banner
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
echo -e "================================================================================"
echo ""
