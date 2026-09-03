# Contributing to Joy-Con Mouse & Universal Media Remote

Thank you for your interest in contributing to **Joy-Con Mouse**! Whether you are adding a new controller mode, improving stick deadzones, adding support for new gamepads, or fixing bugs, all contributions are welcome.

---

## 🧩 Building a Custom Controller Mode (Plugins)

Joy-Con Mouse uses a modular plugin architecture. Any `.py` file placed inside the [`modes/`](modes/) directory is automatically discovered and loaded dynamically at runtime.

### How to Create a New Mode in 5 Minutes:

1. Create a new file in `modes/`, e.g., `modes/gaming.py` or `modes/presentation.py`.
2. Inherit from `BaseMode` and define your name, description, and event handler:

```python
from modes.base import BaseMode, KEY_SPACE, KEY_F5, KEY_ESC, PAD_BTN_SOUTH, PAD_BTN_EAST

class PresentationMode(BaseMode):
    name = "Presentation Clicker"
    description = "Wireless slideshow presenter for LibreOffice Impress and Google Slides"

    def handle_event(self, event_type: int, code: int, value: int, joycon) -> bool:
        # A button: Next Slide (Space)
        if code == PAD_BTN_EAST:
            joycon.emit_key(KEY_SPACE, value)
            return True
            
        # B button: Start Presentation (F5)
        elif code == PAD_BTN_SOUTH:
            joycon.emit_key(KEY_F5, value)
            return True
            
        return False
```

3. Run `joycon-mouse -l` or restart the driver. Your new mode is immediately active!

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
