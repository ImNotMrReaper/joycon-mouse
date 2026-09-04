# 📜 Changelog

All notable changes to **Joy-Con Mouse & Universal Remote** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0-preview] - 2026-09-04

### 🌐 Multi-Platform Architecture & Preview Branches
- **Multi-OS Branch Infrastructure**:
  - `windows`: Dedicated branch with pure Python WinMM (`winmm.dll` `joyGetPosEx`) and Win32 User32 (`user32.dll` `mouse_event`, `keybd_event`) via standard library `ctypes`.
  - `macos`: Dedicated branch with pure Python Apple CoreGraphics and `ApplicationServices.framework` via standard library `ctypes`.
- **Windows 1-Click Installer & Uninstaller Suite**:
  - `install.bat`: Interactive 1-click Windows installer with automatic Python 3.12 detection/winget installation, `%APPDATA%\joycon-mouse` configuration setup, and automatic Desktop & Start Menu shortcut generation.
  - `uninstall.bat`: Clean 1-click Windows uninstaller that removes shortcuts and prompts for config cleanup.
  - `run_windows.bat`: Double-clickable terminal runner for Windows 10/11.
  - `build_exe.bat`: 1-click standalone executable (`JoyConMouse.exe`) packager via PyInstaller.
- **macOS Double-Click Launcher**:
  - `run_macos.command`: Double-clickable terminal runner for macOS Monterey, Ventura, Sonoma, and Sequoia.

### 🤖 AI Agent Architecture & Scope Governance
- **Repository-Level AI Rules**:
  - `AGENTS.md`: Full architectural specification, project axioms, and non-negotiables for autonomous coding agents and LLM pair programmers.
  - `.cursorrules`: Cursor IDE project scope rules.
  - `CLAUDE.md`: Anthropic Claude Code guidelines.
  - `.github/copilot-instructions.md`: GitHub Copilot instructions.
- Strict enforcement of zero-pip dependency rule, prohibition of bloated GUI wrappers (Electron/Qt/Tkinter), and requirement that all new controller actions subclass `BaseMode` in `custom_modes/`.

### 🐧 WSL (Windows Subsystem for Linux) Compatibility
- Added `is_wsl_environment()` auto-detection in `joycon-mouse.py` and `install.sh`.
- Context-aware guidance for forwarding USB/Bluetooth gamepads via `usbipd-win` and `sudo modprobe uinput`, or switching to the 1-click native `windows` branch for zero VM overhead.

### 👥 Non-Coder Beta Testing Ecosystem
- `TESTING_GUIDE.md`: Comprehensive guide with prerequisites (Python with PATH checkbox, Git, PyCharm Community Edition), hardware pairing instructions, no-code `config.json` customization, and review workflows.
- `.github/ISSUE_TEMPLATE/tester_feedback.md`: 1-click GitHub Issue template with structured hardware checklists and ratings.
- Added "Contributors & Community Testers" section to `README.md`.

---

## [1.1.0] - 2026-09-03

### 🌟 Added
- **Universal Modular Plugin Architecture**: Decoupled all controller modes into independent `BaseMode` modules.
- **Three-Tier Dynamic Discovery Engine**: Automatically scans and loads modes from `modes/` (core built-ins), `custom_modes/` (shared community modes), and `~/.config/joycon-mouse/custom_modes/` (private user modes).
- **Crash Isolation**: Faulty or syntax-broken custom modes produce isolated warnings without crashing the running driver daemon.
- **Standalone Mode Execution**: Every mode script can run independently (`python3 <mode_file>.py`) to render complete visual ASCII cheatsheets without hardware connected.
- **Community Custom Modes**:
  - `custom_modes/presentation.py`: Wireless slideshow clicker for Google Slides, LibreOffice Impress, and PowerPoint.
  - `custom_modes/gaming_hotkeys.py`: Couch gaming companion with Quick Save/Load, Map, Inventory, and F13–F16 macro keys.
- **CLI Mode Management**:
  - `--list-modes`: View structured status table of all active and disabled modes.
  - `--create-mode <name>`: Auto-scaffold new custom mode template.
  - `--enable-mode <name>` / `--disable-mode <name>`: Persistently toggle modes in user configuration.
- **Interactive 1-Click Installer (`install.sh`)**:
  - Automatic multi-distro dependency resolution (APT, DNF, Pacman, Zypper).
  - Smart destination selection (`~/.local/share/joycon-mouse`, in-place git linking, or custom path).
  - Global command launcher generation in `~/.local/bin` or `/usr/local/bin`.
- **Interactive Setup Wizard (`setup_wizard.py` / `setup.sh` / `--setup`)**:
  - Visual terminal wizard to pick modes, sensitivity presets (Casual, Balanced, Fast), controller rumble, and autostart daemon.
  - Multi-select, comma-separated toggles, and natural language input aliases.
- **Interactive Clean Uninstaller (`uninstall.sh` / `--uninstall`)**:
  - Safely stops systemd service, removes binaries, cleans application files, and prompts on user config preservation.
- **Continuous Integration (CI)**: GitHub Actions workflow testing Python 3.8–3.13 compilation, shell syntax, and mode discovery.
- **Repository Documentation**: Added `CUSTOM_MODES.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, PR templates, and custom mode issue templates.

---

## [1.0.0] - 2026-09-02

### 🚀 Initial Public Release
- **Zero External Dependencies**: Pure Python implementation using standard Linux kernel ioctls (`fcntl`, `struct`, `select`).
- **Mode 1: Desktop Mouse**: Smooth analog stick cursor with hybrid acceleration curves ($x^{1.6}$) and zero drift.
- **Mode 2: Universal Media Remote**: Side-rail volume control (`SL`/`SR`), subtitles toggle (`C`), instant rewind (`-10s`), and analog stick continuous seek ($\pm 5\text{s}$).
- **Mode 3: Interactive Terminal Controller**: Hands-free AI pair programming companion (`Enter`, History `Up`/`Down`, `Tab` auto-complete, `Esc`, `Ctrl+C` interrupt, `Ctrl+L` clear, and smooth buffer scrolling).
- **Physical Haptic Feedback**: Joy-Con vibration clicks on mode cycle, screenshots, and authentication.
- **Hardware Device Grabbing (`EVIOCGRAB`)**: Eliminates double-input conflicts with Steam Big Picture and Steam Desktop Configuration.
- **Auto-Dormant Detection**: Automatically yields device grab when games or emulators launch.
- **Dual Joy-Con Pairing**: Detects simultaneously connected Left and Right Joy-Cons and binds them into a unified desktop controller.
- **Smart Dual-Action Buttons**: Tap Home/Capture for Super (Overview); Hold for instant screenshot.
- **Interactive Diagnostic Visualizer**: `joycon-mouse --test-buttons` for real-time button scancode and stick axis testing.
- **Background Autostart**: 1-click systemd user service (`--install-service` / `--uninstall-service`).
- **Bluetooth Reconnection Fix**: Solved BlueZ `ClassicBondedOnly` pairing drops on wake.
