# GitHub Copilot Instructions for Joy-Con Mouse

- Maintain zero external pip dependencies. Only use Python standard library modules.
- Do not suggest heavy GUI frameworks (Electron, Qt, Tkinter).
- When implementing new controller actions or button presets, create modular modes in `custom_modes/` inheriting from `modes/base.py:BaseMode`.
- Linux-specific features (uinput, evdev ioctls) belong on `main`; Windows ctypes belong on `windows`; macOS CoreGraphics belong on `macos`.
- See `AGENTS.md` for full design principles and guidelines.
