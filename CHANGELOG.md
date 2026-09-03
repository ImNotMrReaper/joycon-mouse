# 📜 Changelog

All notable changes to **Joy-Con Mouse & Universal Remote** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
