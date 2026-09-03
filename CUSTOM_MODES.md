# 🧩 Joy-Con Mouse Modular Plugin Architecture & Custom Modes

Welcome to the **Joy-Con Mouse Modular Plugin Architecture**!

Joy-Con Mouse features a **zero-dependency, hot-discoverable plugin engine**. Every controller mode operates as an isolated Python module that can be executed, tested, and shared completely independently.

---

## 📑 Table of Contents
1. [Architecture Overview](#-architecture-overview)
2. [Mode Locations & Discovery](#-mode-locations--discovery)
3. [CLI Mode Management](#-cli-mode-management)
4. [Standalone Mode Execution](#-standalone-mode-execution)
5. [Creating a Custom Mode (Tutorial)](#-creating-a-custom-mode-tutorial)
6. [Supported Actions & Keycodes](#-supported-actions--keycodes)
7. [Contributing Custom Modes to the Repository](#-contributing-custom-modes-to-the-repository)

---

## 🏗 Architecture Overview

Unlike monolithic input drivers where all buttons and behaviors are hardcoded into a single event loop, Joy-Con Mouse decouples hardware polling from input behavior:

* **Hardware Polling Engine (`joycon-mouse.py`):** Handles raw Linux `evdev` events, joystick deadzones, exponential acceleration curves, low-latency `uinput` virtual device creation, cheat-code security locks, and Bluetooth auto-reconnects.
* **Modular Modes (`BaseMode`):** Pure Python modules that define what the buttons and analog sticks do. Modes can be swapped at runtime with the **+** or **-** button, enabled/disabled via CLI or configuration, and created without touching the core driver codebase.

---

## 📂 Mode Locations & Discovery

Joy-Con Mouse automatically searches three locations for mode plugins (in order of discovery):

| Directory | Scope | Purpose |
| :--- | :--- | :--- |
| `modes/` | **Core Built-in** | Official baseline modes shipped with the driver (`air_mouse.py`, `media_remote.py`, `terminal.py`). |
| `custom_modes/` | **Community Shared** | Contributed community modes tracked in the git repository (`presentation.py`, `gaming_hotkeys.py`). |
| `~/.config/joycon-mouse/custom_modes/` | **User Private** | Your personal, local mode scripts that persist outside git updates. |

Any `.py` file placed in one of these directories that inherits from `BaseMode` is **automatically discovered and loaded**. If a custom mode has a syntax error or exception, the engine isolates the error, prints a friendly warning, and continues running without crashing the driver.

---

## ⚡ CLI Mode Management

You can inspect, enable, disable, and scaffold modes directly from the terminal:

### 1. List All Available Modes
View a formatted status table of all built-in and custom modes, their enabled/disabled state, and their active features:
```bash
joycon-mouse --list-modes
```

### 2. Scaffold a New Mode Template
Generate a clean, fully documented mode skeleton with one command:
```bash
joycon-mouse --create-mode my_awesome_mode
```
This generates `custom_modes/my_awesome_mode.py`, pre-wired with standard button constants and layout handlers.

### 3. Disable a Mode
Don't want to cycle through a mode? Disable it without deleting the file:
```bash
joycon-mouse --disable-mode presentation
```
*(Persisted cleanly in `~/.config/joycon-mouse/config.json`)*

### 4. Enable a Mode
Re-enable a previously disabled mode:
```bash
joycon-mouse --enable-mode presentation
```

---

## 🚀 Standalone Mode Execution

Every mode script can be executed directly with Python to verify its layout and button mappings without needing a physical controller connected:

```bash
# Test built-in terminal mode
python3 modes/terminal.py

# Test presentation mode
python3 custom_modes/presentation.py

# Test your custom mode
python3 custom_modes/my_awesome_mode.py
```

Running a mode file directly outputs a clean ASCII cheatsheet detailing every mapped button for:
* **Right Joy-Con** (vertical single-hand grip)
* **Left Joy-Con** (vertical single-hand grip)
* **Dual Joy-Cons & Standard Gamepads** (Pro Controller, Xbox, PlayStation)

---

## 🛠 Creating a Custom Mode (Tutorial)

Let's build a **Web Video / Streaming Mode** in 3 easy steps.

### Step 1: Scaffold the Template
```bash
joycon-mouse --create-mode streaming
```

### Step 2: Edit `custom_modes/streaming.py`
```python
#!/usr/bin/env python3
"""
Custom Community Mode: Streaming & Web Video
File: custom_modes/streaming.py
"""

import os
import sys
from typing import Any, Dict

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from modes.base import (
    BaseMode,
    KEY_SPACE, KEY_F, KEY_M, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN,
    PAD_BTN_EAST, PAD_BTN_SOUTH, PAD_BTN_NORTH, PAD_BTN_WEST,
    PAD_BTN_TR, PAD_BTN_TR2, PAD_BTN_HOME, PAD_BTN_PLUS
)


class StreamingMode(BaseMode):
    name = "STREAMING CONTROLLER"
    description = "Hands-free video playback for YouTube, Netflix, Twitch, and Plex."
    
    enable_joystick_cursor = True   # Keep stick as mouse cursor
    enable_media_seek = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        return {
            PAD_BTN_TR2:   {"action": "key", "code": KEY_SPACE, "desc": "ZR -> Play / Pause"},
            PAD_BTN_EAST:  {"action": "key", "code": KEY_SPACE, "desc": "A -> Play / Pause"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_F,     "desc": "X -> Fullscreen Toggle (F)"},
            PAD_BTN_WEST:  {"action": "key", "code": KEY_M,     "desc": "Y -> Mute Toggle (M)"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_RIGHT, "desc": "B -> Skip 5s Forward"},
            PAD_BTN_TR:    {"action": "key", "code": KEY_LEFT,  "desc": "R -> Seek 5s Backward"},
            PAD_BTN_HOME:  {"action": "smart_home",             "desc": "Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_PLUS:  {"action": "mode_cycle",             "desc": "+ -> Cycle Next Mode"},
        }


if __name__ == "__main__":
    StreamingMode().run_standalone()
```

### Step 3: Verify Standalone Execution
```bash
python3 custom_modes/streaming.py
```
That's it! Launch `joycon-mouse`, tap **+** to cycle to your new **Streaming Controller**, and enjoy hands-free media playback.

---

## 🎮 Supported Actions & Keycodes

When defining your button map in `get_button_map(device_type)`, each entry maps a button ID to an action dictionary:

### Supported Actions:
| Action | Parameters | Description | Example |
| :--- | :--- | :--- | :--- |
| `"key"` | `"code": <KEY_*>` | Emits standard Linux keystroke press and release | `{"action": "key", "code": KEY_SPACE}` |
| `"mouse_btn"` | `"code": <MOUSE_BTN_*>` | Emits mouse click (Left, Right, Middle) | `{"action": "mouse_btn", "code": MOUSE_BTN_LEFT}` |
| `"scroll"` | `"direction": 1 \| -1` | Emits continuous vertical scroll step | `{"action": "scroll", "direction": 1}` |
| `"combo"` | `"keys": [<KEY_1>, <KEY_2>]` | Emits key combinations (e.g., shortcuts) | `{"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C]}` |
| `"mode_cycle"` | *(none)* | Cycles to the next available enabled mode | `{"action": "mode_cycle"}` |
| `"smart_home"` | *(none)* | Tap: Overview/Super key \| Hold: Screenshot | `{"action": "smart_home"}` |

### Common Linux Keycodes (from `modes.base`):
* **Letters / Numbers:** `KEY_A`–`KEY_Z`, `KEY_0`–`KEY_9`
* **Navigation:** `KEY_UP`, `KEY_DOWN`, `KEY_LEFT`, `KEY_RIGHT`, `KEY_PAGEUP`, `KEY_PAGEDOWN`, `KEY_HOME`, `KEY_END`
* **Editing:** `KEY_SPACE`, `KEY_ENTER`, `KEY_TAB`, `KEY_BACKSPACE`, `KEY_ESC`, `KEY_DELETE`
* **Modifiers:** `KEY_LEFTCTRL`, `KEY_LEFTSHIFT`, `KEY_LEFTALT`, `KEY_LEFTMETA`
* **Function Keys:** `KEY_F1` through `KEY_F24`
* **Media Keys:** `KEY_PLAYPAUSE`, `KEY_NEXTSONG`, `KEY_PREVIOUSSONG`, `KEY_VOLUMEUP`, `KEY_VOLUMEDOWN`, `KEY_MUTE`

---

## 🌟 Contributing Custom Modes to the Repository

Have you created an awesome mode for:
* Video Editing (DaVinci Resolve / Kdenlive)?
* 3D Modeling (Blender / FreeCAD)?
* Reading / Manga viewer (Foliate / Calibre)?
* Emulators or specific couch games?

We welcome community mode submissions!

1. **Fork the repository:** [github.com/ImNotMrReaper/joycon-mouse](https://github.com/ImNotMrReaper/joycon-mouse)
2. **Add your mode:** Place your file in `custom_modes/<your_mode_name>.py`.
3. **Verify standalone execution:** Run `python3 custom_modes/<your_mode_name>.py` and ensure zero external pip dependencies are required.
4. **Submit a Pull Request:** Open a PR with the title `feat(mode): Add <Your Mode Name> mode`.

Your mode will be included in the next official release for all users worldwide!
