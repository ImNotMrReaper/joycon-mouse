# Claude Code Project Guidelines for Joy-Con Mouse

## Non-Negotiable Rules
- **Zero External Dependencies**: Python Standard Library ONLY (`math`, `time`, `os`, `sys`, `json`, `ctypes`, `fcntl`, `struct`, `select`, `threading`). NEVER add pip dependencies.
- **No GUI Bloat**: Terminal CLI & wizards only (`setup_wizard.py`, CLI flags, `config.json`).
- **Modular Plugin Architecture**: All new controller modes must inherit from `BaseMode` in `modes/base.py` and live in `custom_modes/`.
- **Platform Separation**: Keep Linux uinput/evdev on `main`, Windows ctypes on `windows`, macOS CoreGraphics on `macos`.
- For complete architecture and extension points, see `AGENTS.md`.
