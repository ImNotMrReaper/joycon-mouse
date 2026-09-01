# Joy-Con Mouse & Universal Media Remote for Linux

A zero-dependency, high-performance pure Python driver that transforms Nintendo Switch Joy-Cons and multi-gamepad controllers into a **Precision Desktop Mouse**, **Universal Media Remote**, **Window & Workspace Manager**, and **Presentation Clicker** on Linux (Wayland & X11) using native kernel `uinput` and `evdev` ioctls.

---

## 🌟 Key Features

- **Zero External Dependencies**: Pure Python using standard library (`fcntl`, `struct`, `select`, `math`, `os`, `threading`). No pip dependencies or wrappers.
- **Physical Haptic / Rumble Feedback**: Joy-Con provides physical vibration clicks when switching modes, capturing screenshots, or unlocking credentials.
- **4 Built-in Modular Modes** (Drag-and-Drop in [`modes/`](modes/)):
  1. **Desktop Mouse**: Precision analog stick pointer with hybrid acceleration curve ($x^{1.6}$) and zero drift.
  2. **Universal Media Remote**: Dedicated side-rail volume (`SL`/`SR`), subtitles (`C`), instant rewind (`-10s`), and analog stick continuous seek ($\pm 5	ext{s}$).
  3. **Presentation & Slide Clicker**: Wireless slide clicker for PowerPoint, Google Slides, and PDFs (`PageDown`/`PageUp`, `F5` start, `B` black screen).
  4. **Window & Workspace Manager**: Window snapping (`Super+Left`/`Super+Right`), maximize/minimize (`Super+Up`/`Super+Down`), app switcher (`Alt+Tab`), and workspace cycling (`Ctrl+Alt+Left`/`Right`).
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
    ├── presentation.py            # Mode 3: Wireless presentation & slide clicker
    └── window_manager.py          # Mode 4: Desktop window & workspace manager
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

### Mode 3: Presentation & Slide Clicker
| Button | Right Joy-Con | Left Joy-Con | Action |
| :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | Next Slide (`PageDown`) |
| **Bumper** | `R` | `L` | Previous Slide (`PageUp`) |
| **Face Up** | `X` | `Up` | Start Slideshow (`F5`) |
| **Face Down** | `B` | `Down` | Previous Slide (`PageUp`) |
| **Face Left** | `Y` | `Left` | Blank / Black Screen (`B`) |
| **Face Right** | `A` | `Right` | Next Slide (`PageDown`) |
| **Side Rail SL** | `SL` | `SL` | Exit Slideshow (`ESC`) |
| **Side Rail SR** | `SR` | `SR` | Enter / Activate |
| **Stick Click** | `R3` | `L3` | Laser Click (Left Click) |

### Mode 4: Window & Workspace Manager
| Button | Right Joy-Con | Left Joy-Con | Action |
| :--- | :--- | :--- | :--- |
| **Trigger** | `ZR` | `ZL` | Snap Window Right (`Super + Right`) |
| **Bumper** | `R` | `L` | Snap Window Left (`Super + Left`) |
| **Face Up** | `X` | `Up` | Maximize Window (`Super + Up`) |
| **Face Down** | `B` | `Down` | Minimize / Restore (`Super + Down`) |
| **Face Left** | `Y` | `Left` | App Switcher (`Alt + Tab`) |
| **Face Right** | `A` | `Right` | Close Window (`Alt + F4`) |
| **Side Rail SL** | `SL` | `SL` | Previous Workspace (`Ctrl + Alt + Left`) |
| **Side Rail SR** | `SR` | `SR` | Next Workspace (`Ctrl + Alt + Right`) |
| **Stick Click** | `R3` | `L3` | Overview / Activities (`Super`) |

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

## 📜 License

MIT License. Designed and crafted for Linux enthusiasts.
