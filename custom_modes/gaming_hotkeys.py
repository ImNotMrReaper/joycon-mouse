#!/usr/bin/env python3
"""
Custom Community Mode: Gaming & Macro Hotkeys
File: gaming_hotkeys.py
Maps Joy-Con buttons to standard gaming keys and F13-F24 macro triggers.
"""

import os
import sys
from typing import Any, Dict

# Ensure project root is in sys.path for standalone testing
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from modes.base import (
    BaseMode,
    KEY_ESC, KEY_TAB, KEY_SPACE, KEY_ENTER,
    KEY_LEFTMETA, KEY_SYSRQ,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT
)

# Linux Keycodes for Gaming Hotkeys
KEY_M = 50      # Map
KEY_I = 23      # Inventory
KEY_C = 46      # Character Sheet
KEY_F5 = 63     # Quick Save
KEY_F9 = 67     # Quick Load
KEY_F13 = 183   # Macro 1
KEY_F14 = 184   # Macro 2
KEY_F15 = 185   # Macro 3
KEY_F16 = 186   # Macro 4


class GamingHotkeysMode(BaseMode):
    name = "GAMING & MACRO HOTKEYS"
    description = "Couch gaming companion: Quick Save/Load, Map (M), Inventory (I), and F13-F16 macro keys."
    enable_joystick_cursor = True   # Retain analog stick cursor for menu clicking!
    enable_media_seek = False
    enable_terminal_scroll = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        # 1. Right Joy-Con Mapping
        if device_type == "right_joycon":
            return {
                PAD_BTN_TR2: {"action": "key", "code": KEY_SPACE, "desc": "ZR (Trigger) -> Jump / Action (Space)"},
                PAD_BTN_TR: {"action": "key", "code": KEY_TAB, "desc": "R (Bumper) -> Target / Tab"},
                PAD_BTN_NORTH: {"action": "key", "code": KEY_I, "desc": "X -> Inventory (I)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_M, "desc": "Y -> Map (M)"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_F5, "desc": "A -> Quick Save (F5)"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_F9, "desc": "B -> Quick Load (F9)"},
                PAD_BTN_TL: {"action": "key", "code": KEY_F13, "desc": "Side SL -> Macro 1 (F13)"},
                PAD_BTN_TL2: {"action": "key", "code": KEY_F14, "desc": "Side SR -> Macro 2 (F14)"},
                PAD_BTN_THUMBR: {"action": "key", "code": KEY_C, "desc": "Stick Click -> Character Sheet (C)"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }

        # 2. Left Joy-Con Mapping
        if device_type == "left_joycon":
            return {
                PAD_BTN_TL2: {"action": "key", "code": KEY_SPACE, "desc": "ZL (Trigger) -> Jump / Action (Space)"},
                PAD_BTN_TL: {"action": "key", "code": KEY_TAB, "desc": "L (Bumper) -> Target / Tab"},
                PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_I, "desc": "D-Pad Up -> Inventory (I)"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_M, "desc": "D-Pad Left -> Map (M)"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_F5, "desc": "D-Pad Right -> Quick Save (F5)"},
                PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_F9, "desc": "D-Pad Down -> Quick Load (F9)"},
                PAD_BTN_TR: {"action": "key", "code": KEY_F13, "desc": "Side SL -> Macro 1 (F13)"},
                PAD_BTN_TR2: {"action": "key", "code": KEY_F14, "desc": "Side SR -> Macro 2 (F14)"},
                PAD_BTN_THUMBL: {"action": "key", "code": KEY_C, "desc": "Stick Click -> Character Sheet (C)"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }

        # 3. Dual Joy-Cons & Standard Gamepads
        return {
            # Right Shoulders: Jump & Quick Save
            PAD_BTN_TR2: {"action": "key", "code": KEY_SPACE, "desc": "RT / ZR -> Jump / Action (Space)"},
            PAD_BTN_TR: {"action": "key", "code": KEY_F5, "desc": "RB / R -> Quick Save (F5)"},

            # Left Shoulders: Target & Quick Load
            PAD_BTN_TL2: {"action": "key", "code": KEY_TAB, "desc": "LT / ZL -> Target / Tab"},
            PAD_BTN_TL: {"action": "key", "code": KEY_F9, "desc": "LB / L -> Quick Load (F9)"},

            # Directional Pad: Programmable Gaming Macros (F13-F16)
            PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_F13, "desc": "D-Pad Up -> Macro 1 (F13)"},
            PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_F14, "desc": "D-Pad Down -> Macro 2 (F14)"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_F15, "desc": "D-Pad Left -> Macro 3 (F15)"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_F16, "desc": "D-Pad Right -> Macro 4 (F16)"},

            # Face Buttons: Interact, Cancel, Inventory, Map
            PAD_BTN_EAST: {"action": "key", "code": KEY_ENTER, "desc": "A / East -> Interact / Enter"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_ESC, "desc": "B / South -> Menu / Cancel (Esc)"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_I, "desc": "X / North -> Inventory (I)"},
            PAD_BTN_WEST: {"action": "key", "code": KEY_M, "desc": "Y / West -> Map (M)"},

            # Stick Clicks: Sprint & Character Sheet
            PAD_BTN_THUMBL: {"action": "key", "code": KEY_LEFTSHIFT, "desc": "L3 -> Sprint (Shift)"},
            PAD_BTN_THUMBR: {"action": "key", "code": KEY_C, "desc": "R3 -> Character Sheet (C)"},

            # Navigation & Mode Management
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode"},
            PAD_BTN_HOME: {"action": "key", "code": KEY_LEFTMETA, "desc": "Guide / Home -> Home / Super Key (Instant)"},
            PAD_BTN_CAPTURE: {"action": "key", "code": KEY_SYSRQ, "desc": "Capture / Share -> Instant Screenshot"},
        }


if __name__ == "__main__":
    GamingHotkeysMode().run_standalone()
