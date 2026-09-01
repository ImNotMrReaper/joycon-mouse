# Joy-Con Mouse & Universal Media Remote for Linux

A zero-dependency, high-performance pure Python driver that transforms Nintendo Switch Joy-Cons and multi-gamepad controllers into an **Air-Mouse (Motion Pointer)**, **Desktop Trackpad**, and **Universal Media Remote** on Linux (Wayland & X11) using native kernel `uinput` and `evdev` ioctls.

---

## 🌟 Key Features

- **Zero External Dependencies**: Built entirely on standard Python 3.12+ libraries (`fcntl`, `struct`, `select`, `math`, `os`). No pip dependencies or third-party wrappers required.
- **Drag-and-Drop Modular Plugin Architecture**: Drop new mode files into the [`modes/`](modes/) directory to automatically add them into the controller runtime rotation.
- **Auto-Dormant Game Detection**: Automatically yields exclusive controller grabbing (`EVIOCGRAB`) when Steam games or emulators launch (e.g., RetroArch, RPCS3, Dolphin, PCSX2, Heroic, Lutris) and reclaims control seamlessly upon exit.
- **Hardware-Accurate Joy-Con Mappings**: Full support for upstream Linux `hid-nintendo` side-rail button quirks (SL/SR opposite-side trigger repurposing and fallbacks).
- **Dual Joy-Con Pairing**: Detects simultaneously connected Left and Right Joy-Cons and prompts to bind them into a single unified desktop controller.
- **Smart Dual-Action Buttons**:
  - **Tap** Home / Capture (< 0.38s): Emits `Super` / `Windows` key (Application Overview).
  - **Hold** Home / Capture (≥ 0.38s): Emits `PrintScreen` (Instant Screenshot).
- **Universal Media Remote**: Dedicated side-rail volume controls (SL = Vol Down, SR = Vol Up), Subtitle toggle (`C`), instant rewind (`-10s`), and analog stick media seeking.
- **Optional Local Security Module**: Encrypted machine-keyed cheat-code injection for lock screen unlocking and terminal `sudo` prompts.

---

## 📁 Repository Structure

```text
joycon-mouse/
├── .gitignore                     # Excludes credentials, caches, and local virtualenvs
├── README.md                      # Public open-source documentation
├── joycon-mouse.py                # Main polling loop, auto-dormant manager, device grabber
├── security_manager.py.example    # Open-source template for security features
└── modes/                         # Modular plugin directory (Drag-and-Drop)
    ├── __init__.py                # Dynamic plugin auto-loader (discovers BaseMode subclasses)
    ├── base.py                    # BaseMode base class & Linux keycode constants
    ├── air_mouse.py               # Mode 1: Wii Air-Mouse, gyro pointer & desktop controls
    └── media_remote.py            # Mode 2: Universal media remote with side-rail volume
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
python3 joycon-mouse.py -l
```

Launch the driver:

```bash
python3 joycon-mouse.py
```

### 3. Command Line Options

```text
usage: joycon-mouse [-h] [-l] [-p {right_joycon,left_joycon,dual_joycon,switch_pro,playstation,xbox,generic_gamepad}]
                    [-s SENSITIVITY] [--set-code] [--horizontal] [--no-grab] [-v] [--no-reconnect]

Nintendo Switch Joy-Con & Multi-Gamepad Air-Mouse, Media Remote, and Secure Unlock Driver for Linux.

options:
  -h, --help            show this help message and exit
  -l, --list            List detected controllers and exit.
  -p, --profile         Force specific device profile.
  -s, --sensitivity     Pointer sensitivity multiplier (e.g. 1.2 or 0.8).
  --set-code            Launch interactive wizard to record unlock cheat-code.
  --horizontal          Use horizontal grip orientation.
  --no-grab             Disable exclusive device grabbing (EVIOCGRAB).
  -v, --verbose         Print debug events and unmapped scan codes.
  --no-reconnect        Do not wait and auto-reconnect on disconnect.
```

---

## 🧩 Adding Custom Modes (Drag-and-Drop Modding)

Creating a custom controller mode is as simple as adding a new Python file inside the [`modes/`](modes/) folder:

1. Create a new file in `modes/`, for example `modes/presentation_mode.py`.
2. Inherit from `BaseMode` and implement `get_button_map(self, device_type: str)`.

```python
from typing import Any, Dict
from modes.base import (
    BaseMode,
    KEY_PAGEUP, KEY_PAGEDOWN, KEY_F11, KEY_ESC,
    PAD_BTN_EAST, PAD_BTN_WEST, PAD_BTN_NORTH, PAD_BTN_SOUTH,
    PAD_BTN_PLUS, PAD_BTN_MINUS, PAD_BTN_HOME, PAD_BTN_CAPTURE
)

class PresentationMode(BaseMode):
    name = "PRESENTATION CLICKER"
    description = "Slide navigation for PowerPoint, Google Slides, and PDF presentations."
    enable_motion = False
    enable_joystick_cursor = True
    enable_media_seek = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        return {
            PAD_BTN_EAST: {"action": "key", "code": KEY_PAGEDOWN, "desc": "Next Slide"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_PAGEUP, "desc": "Previous Slide"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_F11, "desc": "Toggle Fullscreen"},
            PAD_BTN_WEST: {"action": "key", "code": KEY_ESC, "desc": "Exit Presentation"},
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Next Mode"},
            PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Next Mode"},
            PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
        }
```

3. Run `joycon-mouse.py`—your mode is **automatically discovered and included** in mode cycling via `+` or `-`!

---

## 🎮 Controller Layouts

### Mode 1: Wii Air-Mouse (Default)
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
| **Home / Capture** | `Home` | `Capture` | Tap: Super / Win \| Hold: Screenshot |
| **Plus / Minus** | `+` | `-` | Cycle Next Mode |

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
| **Stick Left / Right**| Tilt Left / Right | Tilt Left / Right | Continuous Seek (±5s) |

---

## 🔒 Security Module

To use the optional local authentication / sudo injection system:
1. Copy `security_manager.py.example` to `security_manager.py`:
   ```bash
   cp security_manager.py.example security_manager.py
   ```
2. Configure your secret unlock sequence:
   ```bash
   python3 joycon-mouse.py --set-code
   ```
3. Credentials and local salt hashes are encrypted via `/etc/machine-id` and stored strictly in your user directory `~/.config/joycon-mouse/security_config.json`. These files are ignored in `.gitignore`.

---

## 📜 License

MIT License. Designed and crafted for Linux enthusiasts.
