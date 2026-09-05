<div align="center">

# 🎮 Joy-Cons & Gamepads | Universal Controller Mouse for macOS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20Sonoma%20%7C%20Ventura%20%7C%20Monterey-000000.svg)](#-quick-start-for-macos)
[![CI](https://github.com/ImNotMrReaper/joycon-mouse/actions/workflows/ci.yml/badge.svg?branch=macos)](https://github.com/ImNotMrReaper/joycon-mouse/actions/workflows/ci.yml)
[![Dependencies](https://img.shields.io/badge/dependencies-zero%20external-success.svg)](https://github.com/ImNotMrReaper/joycon-mouse/tree/macos)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Transform Nintendo Switch Joy-Cons and standard gamepads (Xbox, PlayStation DualSense/DualShock, Switch Pro, 8BitDo) into a wireless precision desktop mouse, couch media remote, and presentation clicker on Apple macOS with zero external dependencies.**

<br/>

<img src="assets/joycon_banner.svg" alt="Joy-Con & Gamepad Mouse Banner" width="100%">

</div>

---

> 💡 **Operating System Branches:**  
> This branch (`macos`) is optimized exclusively for **Apple macOS (Monterey, Ventura, Sonoma, Sequoia)**.  
> If you are on Linux, switch to the [**`main` branch**](https://github.com/ImNotMrReaper/joycon-mouse/tree/main).  
> If you are on Windows, switch to the [**`windows` branch**](https://github.com/ImNotMrReaper/joycon-mouse/tree/windows).

---

## 🌟 macOS Features

- **Zero External Dependencies**: Pure Python standard library utilizing native Apple `CoreGraphics` & `ApplicationServices.framework` via standard library `ctypes`:
  - Direct hardware cursor movement using `CGEventCreateMouseEvent` and `CGEventPost`.
  - Zero pip dependencies, zero compilation steps, and zero background daemon bloat.
- **Universal Gamepad & Joy-Con Support**: Plug-and-play support for single Joy-Cons, paired Dual Joy-Cons, and full-sized gamepads (Xbox Series X|S / One, PlayStation DualSense / DualShock, Switch Pro, 8BitDo).
- **Dedicated Screenshot & Mission Control**: Dedicated Share/Capture button triggers instant screenshot and Guide/Home button triggers Mission Control / Launchpad.
- **Ergonomic Volume Orientation**: Natural left = Down, right = Up volume controls across all controllers.
- **⚡ 1-Liner Quick Install**: Run one command in Terminal to install the driver, create a Desktop launcher, and configure global commands.
- **Desktop Double-Click Launcher**: Generates `Joy-Con Mouse.command` on your Desktop so you can start the driver without using a terminal.
- **Terminal CLI Command**: Launch anytime by typing `joycon-mouse` in your Terminal.
- **Modular Controller Modes**:
  - **Desktop Mouse**: Smooth analog stick cursor gliding with acceleration curves and scroll.
  - **Universal Media Remote**: Control Spotify, YouTube, VLC, and browsers with side-rail volume (`SL`/`SR`) and track navigation.
  - **Interactive Terminal Controller**: Hands-free terminal navigation: Enter, History Up/Down, Tab auto-complete, and Ctrl+C.
  - **Wireless Presentation Clicker**: Next/Prev slide and blank screen for Keynote, Google Slides, and PowerPoint.
  - **Gaming & Macro Hotkeys**: Couch gaming hotkeys and action shortcuts.

---

## 📁 macOS Repository Structure

```text
joycon-mouse/ (macos branch)
├── install.sh                 # 1-Click macOS installer (creates Desktop shortcut & PATH)
├── uninstall.sh               # Clean uninstaller (removes files & shortcut)
├── run_macos.command          # Double-clickable macOS runner script
├── joycon-mouse-macos.py      # Native Apple CoreGraphics driver via ctypes
├── joycon-mouse.py            # macOS entry point
├── modes/                     # Built-in controller modes (Air Mouse, Media, Terminal)
├── custom_modes/              # Shared community modes (Gaming Hotkeys, Presentation)
├── TESTING_GUIDE.md           # Tester & collaborator guide
├── AGENTS.md                  # Universal AI assistant guardrails
└── README.md                  # macOS documentation
```

---

## 🚀 Quick Start for macOS

### ⚡ Option A: 1-Liner Terminal Install (Fastest)

Open **Terminal** (Press <kbd>Cmd</kbd> + <kbd>Space</kbd> → type `Terminal`) and paste:

```bash
curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/macos/install.sh | bash
```

* Deploys files to `~/.local/share/joycon-mouse`.
* Creates a double-clickable **`Joy-Con Mouse.command`** shortcut on your **Desktop**.
* Adds the global `joycon-mouse` command to your PATH.

---

### 📦 Option B: Offline / Local Installation

1. **Pair your Joy-Con:**
   * Hold the round **Sync button** on the Joy-Con side-rail until green lights cycle up and down.
   * Open **System Settings > Bluetooth**, find Joy-Con under "Nearby Devices", and click **Connect**.
2. **Grant Accessibility Permission (One-time macOS Requirement):**
   * Go to **System Settings > Privacy & Security > Accessibility**.
   * Toggle **ON** for **Terminal** (or iTerm2 / your terminal app).
3. **Launch Anytime:**
   * Double-click **`run_macos.command`** or run `./install.sh`!

---

## 👥 Contributors & Community Testers

| Contributor | Role | Platform / Hardware Tested | Status |
| :--- | :--- | :--- | :--- |
| [**@ImNotMrReaper**](https://github.com/ImNotMrReaper) | Creator & Lead Maintainer | Linux (Ubuntu 24.04 LTS), Joy-Con (L/R) | Active |
| *Community Testers* | Windows & Mac Testers | Windows 10/11, macOS Sequoia/Sonoma | In Progress |

> 📢 **Are you helping test?** [Submit your feedback here](https://github.com/ImNotMrReaper/joycon-mouse/issues/new?template=tester_feedback.md) to get your name and profile added to the wall!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
