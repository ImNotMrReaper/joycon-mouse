# Contributing to Joy-Con Mouse & Universal Media Remote

Thank you for your interest in contributing to **Joy-Con Mouse**! Whether you are adding a new controller mode, improving stick deadzones, adding support for new gamepads, or fixing bugs, all contributions are welcome.

---

## 🧩 Building a Custom Controller Mode (Plugins)

Joy-Con Mouse features a hot-discoverable plugin architecture. Community modes live cleanly inside the [`custom_modes/`](custom_modes/) directory.

### Quick Start: Scaffold in 1 Command
```bash
joycon-mouse --create-mode my_custom_mode
```
This generates `custom_modes/my_custom_mode.py` pre-wired with standard button constants and layout handlers.

### Detailed Mode Guide & API Reference
For a complete 3-step tutorial, supported action dictionary types, and architecture overview, see [**`CUSTOM_MODES.md`**](CUSTOM_MODES.md).

### Standalone Mode Testing
Every mode script can be executed standalone with Python to print an ASCII layout cheatsheet without needing a physical controller:
```bash
python3 custom_modes/my_custom_mode.py
```

---

## 🧪 Testing Your Changes

Before submitting a PR, test your changes using the interactive diagnostic tool:

```bash
# Test raw button scancodes and stick axes in real time
python3 test_buttons.py

# Run the driver in debug mode
python3 joycon-mouse.py -v
```

---

## 🛠️ Contribution Guidelines

1. **Zero External Dependencies**: Keep the core driver lightweight and dependent solely on the Python Standard Library (`fcntl`, `struct`, `select`, `math`, `os`, `threading`).
2. **Non-Blocking Execution**: Ensure all polling loops and input processing routines remain non-blocking.
3. **Clean Commit Messages**: Use standard conventional commits (e.g., `feat: ...`, `fix: ...`, `docs: ...`, `perf: ...`).
4. **Pull Requests**:
   - Fork the repository.
   - Create a feature branch (`git checkout -b feat/my-awesome-mode`).
   - Commit and push your changes.
   - Open a Pull Request against `main`.

Thank you for making Joy-Con Mouse better for the entire Linux community!
