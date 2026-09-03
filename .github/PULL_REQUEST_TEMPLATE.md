## 📝 Description
<!-- Briefly describe what your pull request does, fixes, or adds -->

## 🎮 Type of Change
- [ ] 🌟 New Community Mode (in `custom_modes/`)
- [ ] 🐛 Bug Fix
- [ ] ⚡ Performance Optimization
- [ ] 📖 Documentation Update (`README.md`, `CUSTOM_MODES.md`)
- [ ] 🛠 Core Driver Refactor

## ✅ Checklist
- [ ] My code strictly adheres to **zero external pip dependencies** (Python standard library only).
- [ ] If adding a mode, my mode file is executable standalone (`python3 custom_modes/<mode>.py`) and inherits from `BaseMode`.
- [ ] Verified mode discovery by running `python joycon-mouse.py --list-modes`.
- [ ] Verified Python compilation: `python3 -m py_compile joycon-mouse.py modes/*.py custom_modes/*.py`.
- [ ] Tested on Linux (Wayland and/or X11).
- [ ] Updated documentation (`README.md`, `CUSTOM_MODES.md`) if introducing new features or mappings.
