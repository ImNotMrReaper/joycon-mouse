<div align="center">

# 🎮 Joy-Cons & Gamepads | Universal Controller Mouse & Remote

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue.svg)](#-quick-start-by-operating-system)
[![CI](https://github.com/ImNotMrReaper/joycon-mouse/actions/workflows/ci.yml/badge.svg)](https://github.com/ImNotMrReaper/joycon-mouse/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ImNotMrReaper/joycon-mouse?color=blue)](https://github.com/ImNotMrReaper/joycon-mouse/releases/latest)
[![Dependencies](https://img.shields.io/badge/dependencies-zero%20external-success.svg)](https://github.com/ImNotMrReaper/joycon-mouse)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Transform Nintendo Switch Joy-Cons and universal gamepads (Xbox, PlayStation DualSense/DualShock, Switch Pro Controller, 8BitDo) into a wireless precision desktop mouse, couch media remote, and presentation clicker with zero external dependencies.**

<br/>

<img src="assets/joycon_banner.svg" alt="Joy-Con & Gamepad Mouse Banner" width="100%">

</div>

---

> [!TIP]
> **🚀 Tested on a different Linux distro, Steam Deck, or controller?**  
> We'd love your feedback! [Open an issue or testing report](https://github.com/ImNotMrReaper/joycon-mouse/issues) to share your distro and hardware setup, or submit a custom mode PR via [`CUSTOM_MODES.md`](CUSTOM_MODES.md).

---

## 🌟 Key Features

- **Zero External Dependencies**: Pure Python using standard library (`fcntl`, `struct`, `select`, `math`, `os`, `threading`, `importlib`). No pip dependencies or bloated wrappers.
- **Universal Controller & Gamepad Support**: Plug-and-play support for single Joy-Cons, paired Dual Joy-Cons, and full-sized gamepads (Xbox Series X|S / One / 360, PlayStation DualSense / DualShock, Nintendo Switch Pro Controller, 8BitDo).
- **Physical Haptic / Rumble Feedback**: Joy-Con and gamepads provide physical vibration clicks when switching modes, capturing screenshots, or unlocking credentials.
- **Dedicated Screenshot vs. Home Separation**: Instant 0ms screenshot on dedicated Capture/Share buttons and instant Home/Super key on Guide/Home buttons for full controllers, with smart dual-action hold preserved on single Joy-Cons.
- **Ergonomic Volume Orientation**: Natural left = Volume Down, right = Volume Up across Left Joy-Con rail, Right Joy-Con rail, and D-pad.
- **Universal Modular Plugin Engine**: Fully decoupled mode architecture. Every mode is a standalone, hot-discoverable Python plugin.
- **Built-in & Community Modes**:
  1. **Desktop Mouse** ([`modes/air_mouse.py`](modes/air_mouse.py)): Precision analog stick pointer with hybrid acceleration curve ($x^{1.6}$) and zero drift.
  2. **Universal Media Remote** ([`modes/media_remote.py`](modes/media_remote.py)): Dedicated side-rail volume (`SL`/`SR`), subtitles (`C`), instant rewind (`-10s`), and analog stick continuous seek ($\pm 5\text{s}$).
  3. **Interactive Terminal Controller** ([`modes/terminal.py`](modes/terminal.py)): Hands-free AI pair programming & shell companion (`Enter`, History `Up`/`Down`, `Tab` auto-complete, `Esc`, `Ctrl+C` interrupt, `Ctrl+L` clear, and smooth buffer scrolling).
  4. **Gaming & Macro Hotkeys** ([`custom_modes/gaming_hotkeys.py`](custom_modes/gaming_hotkeys.py)): Quick Save/Load, Map, Inventory, and F13-F16 macro keys.
  5. **Wireless Presentation Clicker** ([`custom_modes/presentation.py`](custom_modes/presentation.py)): Slideshow control for Google Slides, Impress, and PowerPoint.
- **CLI Mode Manager**: Manage, toggle, and scaffold modes directly via CLI (`--list-modes`, `--enable-mode`, `--disable-mode`, `--create-mode`).
- **Standalone Mode Execution**: Every mode script can run independently (`python3 modes/terminal.py`) to output complete visual cheatsheets.
- **1-Click Auto-Start Background Service**: Set up automatic background startup with `joycon-mouse --install-service`.
- **Live Button & Stick Diagnostic Tool**: Interactive diagnostic visualizer (`joycon-mouse --test-buttons`).
- **User Configuration File**: Persistent settings in `~/.config/joycon-mouse/config.json` for sensitivity, speeds, deadzones, rumble, and disabled modes.
- **Auto-Dormant Game Detection**: Non-blocking background thread yields hardware grabbing (`EVIOCGRAB`) when Steam games or emulators launch.
- **Dual Joy-Con Pairing**: Detects simultaneously connected Left and Right Joy-Cons and prompts to bind them into a single unified desktop controller.

---

## 📁 Repository Structure

```text
joycon-mouse/
├── .gitignore                     # Excludes credentials, caches, and local virtualenvs
├── README.md                      # Public documentation
├── CUSTOM_MODES.md                # Modular architecture guide & custom modes manual
├── CONTRIBUTING.md                # Community contribution guidelines
├── LICENSE                        # MIT License
├── install.sh                     # Interactive 1-click installer & directory manager
├── setup.sh                       # Interactive setup wizard launcher
├── setup_wizard.py                # Visual configuration wizard (modes, speeds, rumble)
├── uninstall.sh                   # Clean interactive uninstaller
├── joycon-mouse.py                # Main polling loop, auto-dormant manager, mode manager
├── test_buttons.py                # Interactive live button and stick diagnostic tool
├── security_manager.py.example    # Open-source template for security features
├── modes/                         # Built-in core modes (BaseMode subclasses)
│   ├── __init__.py                # Dynamic plugin auto-loader & template generator
│   ├── base.py                    # BaseMode abstract class & Linux keycode constants
│   ├── air_mouse.py               # Mode 1: Precision Desktop Mouse & browser controls
│   ├── media_remote.py            # Mode 2: Universal media remote with side-rail volume
│   └── terminal.py                # Mode 3: Interactive Terminal & Shell Controller
└── custom_modes/                  # Community & user custom modes (Plug-and-Play)
    ├── gaming_hotkeys.py          # Couch gaming hotkeys & F13-F16 macro keys
    └── presentation.py            # Wireless slideshow presentation clicker
```

---

## 🚀 Quick Start by Operating System

### ⚡ 1-Liner Quick Install (Recommended)

Paste the 1-liner for your operating system into your terminal:

#### 🐧 Linux (Ubuntu, Debian, Fedora, Arch, Steam Deck)
```bash
curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.sh | bash
```

#### 🪟 Windows (PowerShell on Windows 10 & 11) — [`windows` branch]
```powershell
irm https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/windows/install.ps1 | iex
```

#### 🍎 macOS (Terminal) — [`macos` branch]
```bash
curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/macos/install.sh | bash
```

---

### 🪟 Windows (Windows 10 & 11) — [`windows` Branch](https://github.com/ImNotMrReaper/joycon-mouse/tree/windows)

#### Option A: 1-Liner in PowerShell (Fastest)
Open PowerShell (Win + X > Terminal or PowerShell) and run:
```powershell
irm https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/windows/install.ps1 | iex
```
*Auto-detects Python (installs Python 3.12 via winget if missing), creates Desktop & Start Menu shortcuts, and adds `joycon-mouse` to system PATH.*

#### Option B: Offline / Local Installer (`install.bat`)
1. **Pair your Joy-Con:** Hold the round Sync button on the Joy-Con side-rail until lights flash, then connect via **Windows Settings > Bluetooth & devices**.
2. **Download the Windows Branch:**
   * Download the ZIP from the [`windows` branch](https://github.com/ImNotMrReaper/joycon-mouse/tree/windows) and extract it (or `git checkout windows`).
3. **1-Click Installer (`install.bat`):**
   * Double-click **`install.bat`**.
   * Auto-detects Python, sets up user settings in `%APPDATA%\joycon-mouse`, and generates **Desktop and Start Menu shortcuts**.
4. **Launch Anytime:**
   * Double-click the **Joy-Con Mouse** icon on your Desktop or run **`run_windows.bat`**!
   * *Want a standalone `.exe`?* Double-click **`build_exe.bat`** to package `JoyConMouse.exe` in 1 click!
   * *Uninstall:* Double-click **`uninstall.bat`** anytime to cleanly remove shortcuts.

---

### 🐧 Linux (Ubuntu, Debian, Fedora, Arch, Steam Deck) — [`main` Branch](https://github.com/ImNotMrReaper/joycon-mouse/tree/main)

#### Option A: 1-Liner in Terminal (Fastest)
```bash
curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.sh | bash
```

#### Option B: Local Repository Install
1. **Run Installer:**
   ```bash
   ./install.sh
   ```
   * Auto-resolves distro dependencies (APT, DNF, Pacman, Zypper).
   * Installs global command `joycon-mouse` into your `$PATH`.
   * Optimizes BlueZ reconnection and configures uinput permissions.
2. **Interactive Setup Wizard:**
   ```bash
   joycon-mouse --setup
   ```
3. **Clean Uninstaller:**
   ```bash
   joycon-mouse --uninstall
   ```
4. **Manual Run & Controller Listing:**
   ```bash
   joycon-mouse -l      # List detected controllers
   joycon-mouse         # Start polling loop
   ```

---

### 🍎 macOS (Monterey, Ventura, Sonoma, Sequoia) — [`macos` Branch](https://github.com/ImNotMrReaper/joycon-mouse/tree/macos)

#### Option A: 1-Liner in Terminal (Fastest)
```bash
curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/macos/install.sh | bash
```
*Auto-deploys driver, generates Desktop launcher `Joy-Con Mouse.command`, and configures terminal command.*

#### Option B: Offline / Local Run
1. **Pair your Joy-Con:** Hold the Sync button, open **System Settings > Bluetooth**, and click Connect.
2. **Download the Mac Branch:** Download the ZIP from the [`macos` branch](https://github.com/ImNotMrReaper/joycon-mouse/tree/macos) (or `git checkout macos`).
3. **Accessibility Permission:** Ensure Terminal is enabled under **System Settings > Privacy & Security > Accessibility**.
4. **Launch Anytime:** Double-click **`run_macos.command`**!

---

## 🔄 Automatic Background Startup (Systemd)

Run the driver automatically in the background on startup:

```bash
# Install and enable background service
joycon-mouse --install-service

# View live background service logs
journalctl --user -u joycon-mouse.service -f

# Uninstall service
joycon-mouse --uninstall-service
```

---

## 🎮 Real-Time Button & Stick Diagnostic Tool

Run the interactive button tester to inspect real-time raw scancodes, values, and mapped mode actions:

```bash
joycon-mouse --test-buttons
```

---

## ⚙️ Configuration (`~/.config/joycon-mouse/config.json`)

Customize speeds, deadzones, and features in `~/.config/joycon-mouse/config.json`:

```json
{
    "sensitivity": 1.0,
    "speed_x": 36.0,
    "speed_y": 36.0,
    "dead_zone": 0.08,
    "accel_exponent": 1.6,
    "rumble_enabled": true,
    "auto_dormant_enabled": true,
    "scroll_repeat_ms": 70
}
```

---

## 🎮 Universal Gamepads & Full-Sized Controllers (Xbox, PlayStation, Switch Pro, 8BitDo)

While Joy-Cons offer an ultra-compact split form factor ideal for one-handed couch navigation and presentation remotes, **Joy-Con Mouse natively supports full-sized dual-stick gamepads** (Xbox Series X|S, Xbox One / 360, PlayStation DualSense / DualShock 4, Nintendo Switch Pro Controller, 8BitDo, Logitech, and Steam Deck controllers).

### 🕹️ Why Gamepads Differ from Single Joy-Cons
Full-sized gamepads provide significant ergonomic and hardware capabilities compared to a single split Joy-Con:
* **Dual Full Analog Sticks:** Instead of a single thumbstick, full gamepads deliver independent dual-axis control:
  * **Left Analog Stick:** Drives high-precision cursor movement with calibrated acceleration ($x^{1.6}$) and configurable deadzones.
  * **Right Analog Stick:** Drives continuous smooth 2D scrolling (vertical and horizontal in Desktop Mouse mode) or continuous media seeking ($\pm 5\text{s}$ scrubbing in Media Remote mode).
* **Dedicated Screenshot vs. Home Buttons (0ms Delay):**
  * On single Joy-Cons, there is physically only one system button (`Home` on Right, `Capture` on Left), requiring a 0.38s hold timer to distinguish between opening the Application Overview (tap) and taking a screenshot (hold).
  * **On Universal Gamepads & Dual Joy-Cons:** Both functions are separated with **zero delay (0ms latency)**:
    * **Dedicated Capture / Share Button:** Immediately fires an instant screenshot (`PrintScreen` / `KEY_SYSRQ`) with physical haptic rumble confirmation. No holding required!
    * **Dedicated Guide / Home Button:** Immediately fires the `Super` / `Windows` key (`KEY_LEFTMETA`) to bring up your desktop dashboard, Start Menu, or GNOME Overview with 0ms delay.
* **Tactile Stepped D-Pad Navigation:**
  * While the analog sticks offer fluid analog movement, the 4-way digital D-pad provides tactile, discrete stepping:
    * **Media Remote:** D-pad `Up` / `Down` steps volume cleanly without accidental skips; `Left` / `Right` steps tracks.
    * **Terminal Mode:** D-pad `Up` / `Down` scrolls shell command history; `Left` / `Right` steps terminal cursor position.
* **Shoulder Ergonomics & Triggers:**
  * Ergonomic dual triggers (`LT`/`L2` and `RT`/`R2`) and bumpers (`LB`/`L1` and `RB`/`R1`) allow natural one-finger mouse clicks, quick-tabs, and media playback control without hand strain.

### 📊 Comparative Matrix: Single Joy-Con vs. Full Gamepad / Dual Joy-Cons

| Hardware Feature | Single Joy-Con (One-Hand Remote) | Universal Gamepad / Dual Joy-Cons |
| :--- | :--- | :--- |
| **Primary Use Case** | Bed/couch remote, media clicker, presentation presenter | Full desktop replacement, workstation navigation, terminal shell |
| **Analog Sticks** | Single stick (cursor movement OR track seeking) | **Dual sticks** (Left: Cursor; Right: Continuous Scroll / Seek) |
| **Screenshot Trigger** | Hold Home / Capture button (≥ 0.38s) | **Instant Capture / Share button (0ms latency)** |
| **Home / Overview** | Tap Home / Capture button (< 0.38s) | **Instant Guide / Home / PS button (0ms latency)** |
| **Volume Adjustment** | Side rail buttons (`SL` / `SR`) | **Tactile D-Pad Up / Down** + triggers |
| **Track Scrubbing** | Face buttons (`Left`/`Right` or `Y`/`A`) | Right Stick Tilt or D-Pad (`Left`/`Right`) |
| **Ergonomic Profile** | Ultra-lightweight (49g), discrete, fits in pocket | Two-handed balanced grip with full palm support |
| **Supported Devices** | Nintendo Switch Joy-Con (L), Joy-Con (R) | Xbox One / Series, PS4 / PS5, Switch Pro, 8BitDo, Dual Joy-Cons |

---

## 🕹️ Mode Layouts & Button Mappings

Cycle through active modes anytime by pressing **`+`** (Right Joy-Con), **`-`** (Left Joy-Con), or **`Start / +`** on Universal Gamepads.

### Mode 1: Desktop Mouse
| Button | Right Joy-Con | Left Joy-Con | Universal Controller (Xbox / PS / Pro) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Trigger** | `ZR` | `ZL` | `RT / R2` | **Left Mouse Click** |
| **Primary Bumper** | `R` | `L` | `RB / R1` | **Right Mouse Click** |
| **Secondary Trigger** | — | — | `LT / L2` | **Middle Mouse Click** |
| **Side Rail SL** | `SL` | `SL` | `B / Circle` | **Escape (`ESC`)** |
| **Side Rail SR** | `SR` | `SR` | `A / Cross` | **Enter / Open (`ENTER`)** |
| **Face Up / Scroll Up** | `X` | `Up` | `Y / Triangle` or `D-Pad Up` | **Scroll Up** |
| **Face Down / Scroll Down** | `B` | `Down` | `X / Square` or `D-Pad Down` | **Scroll Down** |
| **Face Left / Back** | `Y` | `Left` | `D-Pad Left` | **Browser Back** |
| **Face Right / Forward** | `A` | `Right` | `D-Pad Right` | **Browser Forward** |
| **Left Stick Click** | `R3` | `L3` | `L3` | **Middle Mouse Click** |
| **Right Stick Click** | — | — | `R3` | **Cycle Controller Mode** |
| **Dedicated Screenshot** | — | — | `Capture / Share` | **Instant Screenshot (0ms)** |
| **Dedicated Home / Guide**| `Home` (Hold: Screen) | `Capture` (Hold: Screen) | `Guide / Home / PS` | **Instant Super / Home Key (0ms)** |

### Mode 2: Universal Media Remote
| Button | Right Joy-Con | Left Joy-Con | Universal Controller (Xbox / PS / Pro) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | `RT / R2` | **Play / Pause** |
| **Bumper** | `R` | `L` | `RB / R1` | **Mute / Unmute Audio** |
| **Side Rail SL** | `SL` (Vol Down) | `SL` (Physical Right) | `D-Pad Up` | **Volume Up** (Left Joy-Con & Pad) / Down (Right) |
| **Side Rail SR** | `SR` (Vol Up) | `SR` (Physical Left) | `D-Pad Down` | **Volume Down** (Left Joy-Con & Pad) / Up (Right) |
| **Face Up** | `X` | `Up` | `Y / Triangle` | **Toggle Subtitles / Captions (`C`)** |
| **Face Down** | `B` | `Down` | `A / Cross` | **Instant Rewind (`-10s`)** |
| **Face Left** | `Y` | `Left` | `D-Pad Left` | **Previous Track / Replay** |
| **Face Right** | `A` | `Right` | `D-Pad Right` | **Next Track / Skip** |
| **Stick Click** | `R3` | `L3` | `L3` | **Fullscreen Toggle (`F`)** |
| **Right Stick Click** | — | — | `R3` | **Cycle Controller Mode** |
| **Analog Stick Tilt** | Tilt Left / Right | Tilt Left / Right | Right Stick Tilt | **Continuous Seek ($\pm 5\text{s}$)** |
| **Dedicated Screenshot** | — | — | `Capture / Share` | **Instant Screenshot (0ms)** |
| **Dedicated Home / Guide**| `Home` (Hold: Screen) | `Capture` (Hold: Screen) | `Guide / Home / PS` | **Instant Super / Home Key (0ms)** |

### Mode 3: Interactive Terminal Controller
| Button | Right Joy-Con | Left Joy-Con | Universal Controller (Xbox / PS / Pro) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Trigger** | `ZR` | `ZL` | `RT / R2` | **Enter / Submit Command** |
| **Bumper** | `R` | `L` | `RB / R1` | **Tab Auto-Complete** |
| **Side Rail SL** | `SL` | `SL` | `LT / L2` | **Escape / Normal Mode** |
| **Side Rail SR** | `SR` | `SR` | `LB / L1` | **Cancel / Interrupt (`Ctrl+C`)** |
| **Face Up** | `X` | `Up` | `D-Pad Up` | **Previous Command (History Up)** |
| **Face Down** | `B` | `Down` | `B / Circle` | **Backspace / Erase Character** |
| **Face Left** | `Y` | `Left` | `D-Pad Down` | **Next Command (History Down)** |
| **Face Right** | `A` | `Right` | `A / Cross` | **Enter / Confirm Prompt** |
| **Stick Click** | `R3` | `L3` | `L3` | **Suspend Job (`Ctrl+Z`)** |
| **Right Stick Click** | — | — | `R3` | **EOF / Exit (`Ctrl+D`)** |
| **Analog Stick Tilt** | Stick Up/Down | Stick Up/Down | Stick Up/Down | **Smooth Terminal Buffer Scroll** |
| **Dedicated Screenshot** | — | — | `Capture / Share` | **Instant Screenshot (0ms)** |
| **Dedicated Home / Guide**| `Home` (Hold: Screen) | `Capture` (Hold: Screen) | `Guide / Home / PS` | **Instant Super / Home Key (0ms)** |

### Mode 4: Gaming & Macro Hotkeys (Community Mode)
| Button | Right Joy-Con | Left Joy-Con | Universal Controller (Xbox / PS / Pro) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | `RT / R2` | **Jump / Action (`Space`)** |
| **Bumper** | `R` | `L` | `LT / L2` | **Target / Tab (`Tab`)** |
| **Side Rail SL** | `SL` | `SL` | — | **User Macro 1 (`F13`)** |
| **Side Rail SR** | `SR` | `SR` | — | **User Macro 2 (`F14`)** |
| **Face Up** | `X` | `Up` | `Y / Triangle` | **Inventory (`I`)** |
| **Face Down** | `B` | `Down` | `A / Cross` | **Quick Load (`F9`)** |
| **Face Left** | `Y` | `Left` | `X / Square` | **Map (`M`)** |
| **Face Right** | `A` | `Right` | `B / Circle` | **Quick Save (`F5`)** |
| **Stick Click** | `R3` | `L3` | — | **Character Sheet (`C`)** |
| **Dedicated Screenshot** | — | — | `Capture / Share` | **Instant Screenshot (0ms)** |
| **Dedicated Home / Guide**| `Home` (Hold: Screen) | `Capture` (Hold: Screen) | `Guide / Home / PS` | **Instant Super / Home Key (0ms)** |

### Mode 5: Wireless Presentation Clicker (Community Mode)
| Button | Right Joy-Con | Left Joy-Con | Universal Controller (Xbox / PS / Pro) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | `RT / R2` | **Next Slide (`Space`)** |
| **Bumper** | `R` | `L` | `LT / L2` | **Previous Slide (`Backspace`)** |
| **Face Up** | `X` | `Up` | `Y / Triangle` | **Start Slideshow (`F5`)** |
| **Face Down** | `B` | `Down` | `X / Square` | **Black Screen (`B`)** |
| **Face Left / Right** | `Y` / `A` | `Left` / `Right` | `B` / `A` | **Prev / Next Slide** |
| **Stick Click** | `R3` | `L3` | `L3` | **Exit Slideshow (`Esc`)** |
| **Dedicated Screenshot** | — | — | `Capture / Share` | **Instant Screenshot (0ms)** |
| **Dedicated Home / Guide**| `Home` (Hold: Screen) | `Capture` (Hold: Screen) | `Guide / Home / PS` | **Instant Super / Home Key (0ms)** |

---

## 🧩 Modular Plugins & Community Modes

Joy-Con Mouse features a hot-discoverable plugin system. You can create custom modes, disable built-in modes you don't use, and share modes with the community.

For full architectural details, tutorials, and contribution guides, see [**`CUSTOM_MODES.md`**](CUSTOM_MODES.md).

### CLI Mode Management
```bash
# List all discovered built-in and community modes
joycon-mouse --list-modes

# Disable a mode from cycle loop (e.g. presentation)
joycon-mouse --disable-mode presentation

# Re-enable a mode
joycon-mouse --enable-mode presentation

# Scaffold a brand-new mode template in custom_modes/
joycon-mouse --create-mode my_custom_mode
```

### Standalone Mode Testing
Every mode script is completely standalone and runnable directly with Python without a controller:
```bash
python3 modes/terminal.py
python3 custom_modes/presentation.py
python3 custom_modes/gaming_hotkeys.py
```

---

## 🔒 Security Module

To use the optional local authentication / sudo injection system:
1. Copy `security_manager.py.example` to `security_manager.py`:
   ```bash
   cp security_manager.py.example security_manager.py
   ```
2. Configure your secret unlock sequence:
   ```bash
   joycon-mouse --set-code
   ```
3. Credentials and local salt hashes are encrypted via `/etc/machine-id` and stored strictly in your user directory `~/.config/joycon-mouse/security_config.json`. These files are ignored in `.gitignore`.

---

## 🌐 Multi-Platform Support & Preview Branches

Joy-Con Mouse is expanding across operating systems while preserving its signature zero-dependency architecture!

| Operating System | Branch | Status | Setup Guide |
| :--- | :--- | :--- | :--- |
| **Linux (Wayland & X11)** | [`main`](https://github.com/ImNotMrReaper/joycon-mouse/tree/main) | **Production (v1.1.0+)** | [Quick Start](#-quick-start) |
| **Windows 10 / 11** | [`windows`](https://github.com/ImNotMrReaper/joycon-mouse/tree/windows) | **Beta Preview** | [Testing Guide](TESTING_GUIDE.md#-windows-setup-windows-10--11) |
| **macOS (Sonoma / Ventura / Monterey)** | [`macos`](https://github.com/ImNotMrReaper/joycon-mouse/tree/macos) | **Beta Preview** | [Testing Guide](TESTING_GUIDE.md#-mac-setup-macos-12-monterey-ventura-sonoma-sequoia) |

> [!TIP]
> **Want to help test Joy-Con Mouse on Windows or Mac?**  
> You don't need to know how to code! Check out our friendly [**`TESTING_GUIDE.md`**](TESTING_GUIDE.md) to get started in under 2 minutes and be recognized as an official contributor.

---

## 👥 Contributors & Community Testers

Special thanks to the amazing testers and contributors helping test hardware, discover edge cases, and refine controller ergonomics across platforms:

| Contributor / Tester | Platform | Focus Area |
| :--- | :--- | :--- |
| **[@ImNotMrReaper](https://github.com/ImNotMrReaper)** | Linux / Core | Architecture, Linux evdev/uinput engine, modular plugins |
| *(Community Beta Testers)* | Windows / Mac / Linux | Cross-platform hardware verification & UX feedback |

Want to join our testing crew? Test the driver on your system and submit a report via [Beta Tester Feedback](https://github.com/ImNotMrReaper/joycon-mouse/issues/new?template=tester_feedback.md)!

---

## 🤝 Contributing & Community Standards

Contributions are warmly welcomed! Joy-Con Mouse was designed from the ground up to be modular and community-friendly. If you want to create a custom controller mode, enhance button mappings, or report hardware quirks:
- Read [**`TESTING_GUIDE.md`**](TESTING_GUIDE.md) to learn how non-coders and testers can test and submit reviews.
- Read [**`CUSTOM_MODES.md`**](CUSTOM_MODES.md) to see how to create and submit community modes.
- Read the [Contributing Guide](CONTRIBUTING.md) for code style and standards.
- Please review our [Code of Conduct](CODE_OF_CONDUCT.md).
- Open an [Issue](https://github.com/ImNotMrReaper/joycon-mouse/issues) for feature requests or gamepad compatibility.
- Submit a Pull Request to share your mode with other users!

---

## 📜 Changelog, Security & License

- **Releases & Changes**: See [**`CHANGELOG.md`**](CHANGELOG.md) for detailed version history.
- **Security Policy**: See [**`SECURITY.md`**](SECURITY.md) for vulnerability disclosure guidelines.
- **License**: Distributed under the [MIT License](LICENSE). Designed and crafted for the open-source gaming and accessibility community.
