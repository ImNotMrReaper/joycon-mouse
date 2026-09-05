#!/usr/bin/env python3
"""
Custom Community Mode: Wireless Presentation Clicker
File: presentation.py
Compatible with Google Slides, LibreOffice Impress, PowerPoint, PDF viewers.
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
    KEY_ESC, KEY_SPACE, KEY_BACKSPACE, KEY_B, KEY_F5, KEY_LEFTSHIFT,
    KEY_PAGEUP, KEY_PAGEDOWN, KEY_ENTER, KEY_W, KEY_LEFT, KEY_RIGHT,
    KEY_LEFTMETA, KEY_SYSRQ,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT
)


class PresentationMode(BaseMode):
    name = "WIRELESS PRESENTATION CLICKER"
    description = "Wireless slideshow presenter: Next/Prev Slide, Start/Exit Slideshow, and Black Screen."
    enable_joystick_cursor = False
    enable_media_seek = False
    enable_terminal_scroll = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        # 1. Right Joy-Con Mapping
        if device_type == "right_joycon":
            return {
                PAD_BTN_TR2: {"action": "key", "code": KEY_SPACE, "desc": "ZR (Trigger) -> Next Slide (Space)"},
                PAD_BTN_TR: {"action": "key", "code": KEY_BACKSPACE, "desc": "R (Bumper) -> Previous Slide (Backspace)"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_SPACE, "desc": "A -> Next Slide (Space)"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_BACKSPACE, "desc": "B -> Previous Slide (Backspace)"},
                PAD_BTN_NORTH: {"action": "key", "code": KEY_F5, "desc": "X -> Start Presentation (F5)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_B, "desc": "Y -> Black / Blank Screen (B)"},
                PAD_BTN_THUMBR: {"action": "key", "code": KEY_ESC, "desc": "Stick Click -> Exit Slideshow (Esc)"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }

        # 2. Left Joy-Con Mapping
        if device_type == "left_joycon":
            return {
                PAD_BTN_TL2: {"action": "key", "code": KEY_SPACE, "desc": "ZL (Trigger) -> Next Slide (Space)"},
                PAD_BTN_TL: {"action": "key", "code": KEY_BACKSPACE, "desc": "L (Bumper) -> Previous Slide (Backspace)"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_SPACE, "desc": "D-Pad Right -> Next Slide"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_BACKSPACE, "desc": "D-Pad Left -> Previous Slide"},
                PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_F5, "desc": "D-Pad Up -> Start Presentation (F5)"},
                PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_B, "desc": "D-Pad Down -> Black Screen (B)"},
                PAD_BTN_THUMBL: {"action": "key", "code": KEY_ESC, "desc": "Stick Click -> Exit Slideshow (Esc)"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }

        # 3. Dual Joy-Cons & Standard Gamepads
        return {
            # Right Shoulders: Advance & Blank Screen
            PAD_BTN_TR2: {"action": "key", "code": KEY_SPACE, "desc": "RT / ZR -> Next Slide (Space)"},
            PAD_BTN_TR: {"action": "key", "code": KEY_B, "desc": "RB / R -> Black Screen (B)"},

            # Left Shoulders: Return & Start Slideshow
            PAD_BTN_TL2: {"action": "key", "code": KEY_BACKSPACE, "desc": "LT / ZL -> Previous Slide (Backspace)"},
            PAD_BTN_TL: {"action": "key", "code": KEY_F5, "desc": "LB / L -> Start Presentation (F5)"},

            # Directional Pad: Jump to Beginning / End & Step
            PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_PAGEUP, "desc": "D-Pad Up -> Page Up / First Slide"},
            PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_PAGEDOWN, "desc": "D-Pad Down -> Page Down / Last Slide"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_LEFT, "desc": "D-Pad Left -> Previous Slide (Arrow Left)"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_RIGHT, "desc": "D-Pad Right -> Next Slide (Arrow Right)"},

            # Face Buttons: Advance, Exit, Start, White Screen
            PAD_BTN_EAST: {"action": "key", "code": KEY_ENTER, "desc": "A / East -> Next Slide / Confirm"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_ESC, "desc": "B / South -> Exit Slideshow (Esc)"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_F5, "desc": "X / North -> Start Presentation (F5)"},
            PAD_BTN_WEST: {"action": "key", "code": KEY_W, "desc": "Y / West -> White Screen (W)"},

            # Stick Clicks: Exit Slideshow
            PAD_BTN_THUMBL: {"action": "key", "code": KEY_ESC, "desc": "L3 -> Exit Slideshow (Esc)"},

            # Navigation & Mode Management
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode"},
            PAD_BTN_HOME: {"action": "key", "code": KEY_LEFTMETA, "desc": "Guide / Home -> Home / Super Key (Instant)"},
            PAD_BTN_CAPTURE: {"action": "key", "code": KEY_SYSRQ, "desc": "Capture / Share -> Instant Screenshot"},
        }


if __name__ == "__main__":
    PresentationMode().run_standalone()
