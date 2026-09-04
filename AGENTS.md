# 🤖 Joy-Con Mouse & Universal Remote - AI Assistant & Agent Guidelines
**Target Audience:** Autonomous Coding Agents, LLM Pair Programmers, GitHub Copilot, Cursor, Claude Code, Antigravity.

---

## 🎯 1. Project Vision & Architecture Overview

**Joy-Con Mouse** is an ultra-low-latency, zero-dependency desktop mouse driver, couch media remote, and modular controller framework that transforms Nintendo Switch Joy-Cons and standard gamepads into precision input devices.

### Core Architectural Axioms
1. **Zero External Dependencies (Strict Non-Negotiable):**  
   The codebase relies **strictly on the Python Standard Library** (`math`, `time`, `os`, `sys`, `json`, `ctypes`, `fcntl`, `struct`, `select`, `threading`, `importlib`).  
   **NEVER** introduce external `pip` dependencies (e.g. `pygame`, `pynput`, `pyautogui`, python-evdev, etc.). All kernel interactions, system calls (`ioctl`), and OS event injections must be implemented natively.

2. **Zero GUI Bloat (CLI & Terminal Wizard First):**  
   Do **NOT** introduce heavy GUI frameworks (Electron, Qt/PyQt, wxPython, Tkinter, web wrappers). Configuration is handled via:
   - Interactive terminal wizards (`setup_wizard.py`)
   - CLI flags (`joycon-mouse --list-modes`, `--setup`, etc.)
   - Pure JSON configuration (`config.json`)
   - Background systemd services / batch / command scripts

3. **Offline & Zero-Telemetry:**  
   The project has zero telemetry, zero tracking, and requires no cloud services, API keys, or external AI models. Everything runs 100% locally on the host.

---

## 🚫 2. Absolute Boundaries & Anti-Patterns (What NOT to Do)

Any AI assistant modifying this repository **MUST NOT**:
* ❌ **DO NOT break zero-pip:** Do not generate a `requirements.txt` with external packages or suggest installing pip libraries.
* ❌ **DO NOT hack features into the main polling loop:** Never hardcode application-specific shortcuts directly inside `joycon-mouse.py`.
* ❌ **DO NOT mix OS backends:**  
  - Linux kernel `/dev/uinput` and `ioctl` must remain cleanly on the Linux `main` branch.
  - Windows `winmm.dll` and `user32.dll` ctypes live strictly on the `windows` branch.
  - macOS `CoreGraphics` ctypes live strictly on the `macos` branch.
* ❌ **DO NOT build game cheats, aimbots, or macro-spammers:** This project is strictly for desktop navigation, media control, accessibility, and productivity.
* ❌ **DO NOT remove existing comments, docs, or safety checks:** Maintain docstring integrity and non-blocking thread safety.

---

## 📁 3. Codebase File Structure & Purpose

```text
joycon-mouse/
├── joycon-mouse.py        # Core Linux driver engine (event polling loop, auto-dormant, CLI manager)
├── setup_wizard.py         # Visual terminal wizard (modes, sensitivity, rumble, autostart)
├── test_buttons.py         # Real-time hardware diagnostic visualizer (axes & button IDs)
├── install.sh              # Multi-distro Linux installer & PATH configuration
├── uninstall.sh            # Safe interactive uninstaller
├── setup.sh                # Launcher wrapper for setup_wizard.py
│
├── modes/                  # Built-in Core Controller Modes (BaseMode subclasses)
│   ├── __init__.py         # Plugin auto-discovery engine & template generator
│   ├── base.py             # Abstract BaseMode class & Linux keycode definitions
│   ├── air_mouse.py        # Mode 1: Precision cursor with x^1.6 acceleration curve
│   ├── media_remote.py     # Mode 2: Media seek, side-rail volume, rewind/play
│   └── terminal.py         # Mode 3: Interactive shell companion (Enter, Tab, Esc, Ctrl+C)
│
├── custom_modes/           # Hot-discoverable user & community modes (Plug-and-Play)
│   ├── gaming_hotkeys.py   # Couch gaming shortcuts & F13-F16 macro keys
│   └── presentation.py     # Slide clicker for PowerPoint / Google Slides
│
├── completions/            # Shell auto-completion scripts
│   └── joycon-mouse        # Bash programmable completion & autosuggestion script
│
├── .github/                # GitHub workflows & templates
│   ├── workflows/ci.yml    # Continuous Integration across Python 3.8 - 3.13
│   └── ISSUE_TEMPLATE/     # Guided issue templates (Bug, Mode, Beta Tester Report)
│
├── TESTING_GUIDE.md        # Jargon-free guide for non-coder beta testers & collaborators
├── CUSTOM_MODES.md         # API guide for authoring new controller mode plugins
├── CONTRIBUTING.md         # General contributor standards & commit rules
└── README.md               # Hero documentation, badges, and quick start guide
```

---

## 🧩 4. How to Extend the Project Correctly

### Adding a New Controller Mode
To add new shortcuts, game controls, or specialized navigation modes:
1. **Always inherit from `BaseMode`:** Create a new file in `custom_modes/<mode_name>.py`.
2. **Implement Required Methods:**
   - `get_name()`: Short uppercase title (e.g. `"BLENDER NAVIGATOR"`).
   - `get_description()`: Concise 1-sentence summary.
   - `get_features()`: List of feature flags (e.g. `["Analog Cursor"]`).
   - `on_button_event(btn_name, is_pressed, uinput_dev)`: Handles button presses and returns an action dictionary (`{"action": "key", "code": ...}`).
   - `draw_layout()`: Terminal ASCII cheatsheet layout for standalone execution.
3. **Template Scaffolding:** Use the built-in generator:
   ```bash
   joycon-mouse --create-mode <mode_name>
   ```

### Modifying Sensitivity & Hardware Physics
All analog stick math must preserve:
* **Deadzone Thresholding:** Ignore small stick noise ($< 0.10$).
* **Effective Magnitude Scaling:** Normalize remaining range ($0.0 \to 1.0$).
* **Power Curve Acceleration:** Default exponent is $x^{1.6}$ for micro-precision without sacrificing screen-travel velocity.

---

## 💻 5. Multi-OS & WSL Guidelines

* **Windows (`windows` branch):**  
  Uses standard library `ctypes` accessing `winmm.joyGetPosEx` for gamepad polling and `user32.mouse_event` / `user32.keybd_event` for input injection. Double-clickable via `run_windows.bat`.
* **macOS (`macos` branch):**  
  Uses standard library `ctypes` accessing Apple `CoreGraphics` (`CGEventCreateMouseEvent`, `CGEventPost`). Double-clickable via `run_macos.command`.
* **WSL (Windows Subsystem for Linux):**  
  WSL 2 runs in a VM without direct access to Windows Bluetooth by default.  
  - If a user wants to control the *Windows host*, advise running natively on Windows via `run_windows.bat`.
  - If running in WSL, check for Microsoft kernel (`/proc/version`) and verify `/dev/uinput` permissions before attempting to grab `/dev/input/event*`.

---

## ✅ 6. Checklist Before Finalizing Changes
- [ ] Code compiles cleanly with zero syntax errors (`python3 -m py_compile <file>`).
- [ ] No external pip dependencies were added.
- [ ] Thread safety and non-blocking loops are preserved.
- [ ] `git status` shows no stray files, caches, or credentials.
- [ ] GitHub Actions CI passes.
