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

- **Zero External Dependencies**: Pure Python using standard library (`fcntl`, `struct`, `select`, `math`, `os`, `threading`). No pip dependencies or wrappers.
- **Physical Haptic / Rumble Feedback**: Joy-Con provides physical vibration clicks when switching modes, capturing screenshots, or unlocking credentials.
- **3 Built-in Modular Modes** (Drag-and-Drop in [`modes/`](modes/)):
  1. **Desktop Mouse**: Precision analog stick pointer with hybrid acceleration curve ($x^{1.6}$) and zero drift.
  2. **Universal Media Remote**: Dedicated side-rail volume (`SL`/`SR`), subtitles (`C`), instant rewind (`-10s`), and analog stick continuous seek ($\pm 5\text{s}$).
  3. **Interactive Terminal Controller**: Hands-free AI pair programming & shell companion (`Enter`, History `Up`/`Down`, `Tab` auto-complete, `Esc`, `Ctrl+C` interrupt, `Ctrl+L` clear, and smooth buffer scrolling).
- **1-Click Auto-Start Background Service**: Set up automatic background startup with `joycon-mouse --install-service`.
- **Live Button & Stick Diagnostic Tool**: Interactive diagnostic visualizer (`joycon-mouse --test-buttons`).
- **User Configuration File**: Persistent settings in `~/.config/joycon-mouse/config.json` for sensitivity, speeds, deadzones, and rumble.
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
├── joycon-mouse.py                # Main polling loop, auto-dormant manager, device grabber
├── test_buttons.py                # Interactive live button and stick diagnostic tool
├── security_manager.py.example    # Open-source template for security features
└── modes/                         # Modular plugin directory (Drag-and-Drop)
    ├── __init__.py                # Dynamic plugin auto-loader (discovers BaseMode subclasses)
    ├── base.py                    # BaseMode base class & Linux keycode constants
    ├── air_mouse.py               # Mode 1: Precision Desktop Mouse & browser controls
    ├── media_remote.py            # Mode 2: Universal media remote with side-rail volume
    └── terminal.py                # Mode 3: Interactive Terminal & Shell Controller
```

---

## 🚀 Quick Start

### 1. Prerequisites & User Permissions

Add your user to the `input` group to access `/dev/uinput` and `/dev/input/event*`:

```bash
sudo usermod -aG input $USER
```

*(Log out and log back in or restart for group changes to take effect).*

Ensure the `uinput` kernel module is loaded:

```bash
sudo modprobe uinput
```

### 2. Running the Driver

List connected controllers:

```bash
joycon-mouse -l
```

Launch the driver:

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
- Read the [Contributing Guide](CONTRIBUTING.md) to see how to build a custom plugin in under 15 lines of code.
- Open an [Issue](https://github.com/ImNotMrReaper/joycon-mouse/issues) for feature requests or gamepad compatibility.
- Submit a Pull Request to share your mode with other Linux users!

---

## 📜 License

Distributed under the [MIT License](LICENSE). Designed and crafted for the Linux and open-source gaming community.
