<div align="center">

# 🎮 Joy-Con Mouse & Universal Media Remote for Linux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux%20(Wayland%20%26%20X11)-lightgrey.svg)](https://kernel.org)
[![Dependencies](https://img.shields.io/badge/dependencies-zero%20external-success.svg)](https://github.com/ImNotMrReaper/joycon-mouse)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Transform Nintendo Switch Joy-Cons into a wireless precision desktop mouse, couch media remote, and terminal companion on Linux with zero external dependencies.**

</div>

---

## 🌟 Key Features

- **Zero External Dependencies**: Pure Python using standard library (`fcntl`, `struct`, `select`, `math`, `os`, `threading`, `importlib`). No pip dependencies or wrappers.
- **Physical Haptic / Rumble Feedback**: Joy-Con provides physical vibration clicks when switching modes, capturing screenshots, or unlocking credentials.
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
- **Smart Dual-Action Buttons**:
  - **Tap** Home / Capture (< 0.38s): Emits `Super` / `Windows` key (Application Overview).
  - **Hold** Home / Capture (≥ 0.38s): Emits `PrintScreen` (Instant Screenshot with haptic double-click).

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

## 🚀 Quick Start

### 1. Interactive 1-Click Installer (Recommended)

Simply run the installer to set up Joy-Con Mouse in under 30 seconds:

```bash
./install.sh
```

The installer will guide you through:
* **Smart Location Selection**: Installs into `~/.local/share/joycon-mouse` by default (no root needed), keeps in-place if you cloned via git, or allows entering any custom directory.
* **Global Command Link**: Installs the `joycon-mouse` command globally into your `PATH`.
* **Hardware Permissions**: Automatically checks Linux `input` group and loads `/dev/uinput`.
* **Bluetooth Reconnect Optimization**: Automatically optimizes BlueZ so Joy-Cons reconnect immediately upon pressing any button.
* **Guided Setup Wizard**: Chains directly into the visual setup wizard to customize your enabled modes, sensitivity, and autostart daemon.

---

### 2. Interactive Setup Wizard (`joycon-mouse --setup`)

Re-adjust modes, mouse sensitivity presets, haptic rumble, and background autostart anytime:

```bash
# Via global CLI command:
joycon-mouse --setup

# Or via script in project folder:
./setup.sh
```

---

### 3. Clean Uninstaller (`joycon-mouse --uninstall`)

Cleanly remove Joy-Con Mouse, background services, and binary links anytime:

```bash
# Via global CLI command:
joycon-mouse --uninstall

# Or via script in project folder:
./uninstall.sh
```

---

### 4. Running the Driver Manually

List connected controllers:

```bash
joycon-mouse -l
```

Launch the desktop driver:

```bash
joycon-mouse
```

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

## 🎮 Controller Layouts & Modes

Cycle through active modes anytime by pressing **`+`** (Right Joy-Con) or **`-`** (Left Joy-Con).

### Mode 1: Desktop Mouse
| Button | Right Joy-Con | Left Joy-Con | Action |
| :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | Left Mouse Click |
| **Bumper** | `R` | `L` | Right Mouse Click |
| **Side Rail SL** | `SL` | `SL` | Escape (`ESC`) |
| **Side Rail SR** | `SR` | `SR` | Enter / Open (`ENTER`) |
| **Face Up** | `X` | `Up` | Scroll Up |
| **Face Down** | `B` | `Down` | Scroll Down |
| **Face Left** | `Y` | `Left` | Browser Back |
| **Face Right** | `A` | `Right` | Browser Forward |
| **Stick Click** | `R3` | `L3` | Middle Mouse Click |
| **Home / Capture** | `Home` | `Capture` | Tap: Super / Win | Hold: Screenshot |

### Mode 2: Universal Media Remote
| Button | Right Joy-Con | Left Joy-Con | Action |
| :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | Play / Pause |
| **Bumper** | `R` | `L` | Mute / Unmute Audio |
| **Side Rail SL** | `SL` | `SL` | Volume Down |
| **Side Rail SR** | `SR` | `SR` | Volume Up |
| **Face Up** | `X` | `Up` | Toggle Subtitles / Captions (`C`) |
| **Face Down** | `B` | `Down` | Instant Rewind (`-10s`) |
| **Face Left** | `Y` | `Left` | Previous Track |
| **Face Right** | `A` | `Right` | Next Track |
| **Stick Click** | `R3` | `L3` | Fullscreen Toggle (`F`) |
| **Stick Left / Right**| Tilt Left / Right | Tilt Left / Right | Continuous Seek ($\pm 5	ext{s}$) |

### Mode 3: Interactive Terminal Controller
| Button | Right Joy-Con | Left Joy-Con | Universal Controller | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Trigger** | `ZR` | `ZL` | `RT / R2` | **Enter / Submit Command** |
| **Bumper** | `R` | `L` | `RB / R1` | **Tab Auto-Complete** |
| **Side Rail SL** | `SL` | `SL` | `LT / L2` | **Escape / Normal Mode** |
| **Side Rail SR** | `SR` | `SR` | `LB / L1` | **Cancel / Interrupt (`Ctrl+C`)** |
| **Face Up** | `X` | `Up` | `D-Pad Up` | **Previous Command (History Up)** |
| **Face Down** | `B` | `Down` | `B / Circle` | **Backspace / Erase Character** |
| **Face Left** | `Y` | `Left` | `D-Pad Down` | **Next Command (History Down)** |
| **Face Right** | `A` | `Right` | `A / Cross` | **Enter / Confirm Prompt** |
| **Stick Click** | `R3` | `L3` | `X / Square` | **Clear Screen (`Ctrl+L`)** |
| **Analog Stick Tilt** | Stick Up/Down | Stick Up/Down | Stick Up/Down | **Smooth Terminal Buffer Scroll** |
| **Home / Capture** | `Home` | `Capture` | `Guide` | Tap: Super / Win \| Hold: Screenshot |
| **Plus / Minus** | `+` | `-` | `+ / Start` | **Cycle Controller Mode** |

### Mode 4: Gaming & Macro Hotkeys (Community Mode)
| Button | Right Joy-Con | Left Joy-Con | Action |
| :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | Jump / Action (`Space`) |
| **Bumper** | `R` | `L` | Target / Tab (`Tab`) |
| **Side Rail SL** | `SL` | `SL` | User Macro 1 (`F13`) |
| **Side Rail SR** | `SR` | `SR` | User Macro 2 (`F14`) |
| **Face Up** | `X` | `Up` | Inventory (`I`) |
| **Face Down** | `B` | `Down` | Quick Load (`F9`) |
| **Face Left** | `Y` | `Left` | Map (`M`) |
| **Face Right** | `A` | `Right` | Quick Save (`F5`) |
| **Stick Click** | `R3` | `L3` | Character Sheet (`C`) |

### Mode 5: Wireless Presentation Clicker (Community Mode)
| Button | Right Joy-Con | Left Joy-Con | Action |
| :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | Next Slide (`Space`) |
| **Bumper** | `R` | `L` | Previous Slide (`Backspace`) |
| **Face Up** | `X` | `Up` | Start Slideshow (`F5`) |
| **Face Down** | `B` | `Down` | Black Screen (`B`) |
| **Face Left / Right** | `Y` / `A` | `Left` / `Right` | Prev / Next Slide |
| **Stick Click** | `R3` | `L3` | Exit Slideshow (`Esc`) |

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

## 🤝 Contributing

Contributions are warmly welcomed! Joy-Con Mouse was designed from the ground up to be modular and community-friendly. If you want to create a custom controller mode, enhance button mappings, or report hardware quirks:
- Read [**`CUSTOM_MODES.md`**](CUSTOM_MODES.md) to see how to create and submit community modes.
- Read the [Contributing Guide](CONTRIBUTING.md) for code style and standards.
- Open an [Issue](https://github.com/ImNotMrReaper/joycon-mouse/issues) for feature requests or gamepad compatibility.
- Submit a Pull Request to share your mode with other Linux users!

---

## 📜 License

Distributed under the [MIT License](LICENSE). Designed and crafted for the Linux and open-source gaming community.
