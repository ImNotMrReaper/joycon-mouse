---
name: 🎮 Custom Mode Proposal
about: Propose a new community controller mode for Joy-Con Mouse
title: '[MODE] <Your Mode Name>'
labels: ['mode-proposal', 'community']
assignees: ''
---

### 🎮 Mode Overview
- **Mode Name:** <!-- e.g., Blender Viewport Navigator, DaVinci Video Scrub -->
- **Target Application(s):** <!-- e.g., Blender 4.x, DaVinci Resolve, YouTube, LibreOffice -->
- **Controller Type(s):** <!-- Right Joy-Con, Left Joy-Con, Dual Joy-Cons, Pro Controller -->

### 🎯 Feature Flags
- [ ] Analog Stick Mouse Pointer (`enable_joystick_cursor`)
- [ ] Continuous Media Seek (`enable_media_seek`)
- [ ] Terminal Buffer Scroll (`enable_terminal_scroll`)

### 🕹 Proposed Button Mapping
| Controller Button | Hardware ID | Target Action | Description / Shortcut |
| :--- | :--- | :--- | :--- |
| **Trigger (ZR/ZL)** | `PAD_BTN_TR2` | `{"action": "key", "code": ...}` | e.g. Space |
| **Bumper (R/L)** | `PAD_BTN_TR` | `{"action": "key", "code": ...}` | |
| **Action East (A)** | `PAD_BTN_EAST` | `{"action": "key", "code": ...}` | |
| **Action South (B)**| `PAD_BTN_SOUTH` | `{"action": "key", "code": ...}` | |
| **Action North (X)**| `PAD_BTN_NORTH` | `{"action": "key", "code": ...}` | |
| **Action West (Y)** | `PAD_BTN_WEST` | `{"action": "key", "code": ...}` | |
| **Side Rail SL** | `PAD_BTN_TL` | `{"action": "key", "code": ...}` | |
| **Side Rail SR** | `PAD_BTN_TL2` | `{"action": "key", "code": ...}` | |

### 💡 Additional Context
<!-- Add any other context, shortcuts, or application quirks here -->
