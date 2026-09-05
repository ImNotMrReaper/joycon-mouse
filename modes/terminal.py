#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Interactive Terminal & Shell Controller.
Designed for hands-free AI pair programming sessions, command execution, and CLI navigation.
Location: modes/terminal.py
"""

import os
import sys
from typing import Any, Dict

# Ensure project root is in sys.path for standalone execution
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from modes.base import (
    BaseMode,
    KEY_ESC, KEY_ENTER, KEY_TAB, KEY_BACKSPACE,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    KEY_PAGEUP, KEY_PAGEDOWN,
    KEY_LEFTCTRL, KEY_LEFTSHIFT, KEY_C, KEY_L, KEY_D, KEY_Z, KEY_Y, KEY_U,
    KEY_LEFTMETA, KEY_SYSRQ,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT,
    SL_GENERIC_CODES, SR_GENERIC_CODES
)


class TerminalMode(BaseMode):
    name = "INTERACTIVE TERMINAL CONTROLLER"
    description = "Hands-free terminal navigation: Enter, History Up/Down, Tab auto-complete, Esc, and Ctrl+C interrupt."
    enable_joystick_cursor = False   # Stick is repurposed for terminal buffer scrolling
    enable_media_seek = False
    enable_terminal_scroll = True


    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        # ======================================================================
        # 1. Single Right Joy-Con (Held vertically)
        # ======================================================================
        if device_type == "right_joycon":
            bm = {
                # Primary Triggers
                PAD_BTN_TR2: {"action": "key", "code": KEY_ENTER, "desc": "ZR (Trigger) -> Enter / Submit"},
                PAD_BTN_TR: {"action": "key", "code": KEY_BACKSPACE, "desc": "R (Bumper) -> Backspace / Erase"},

                # Side Rail SL / SR
                PAD_BTN_TL: {"action": "key", "code": KEY_TAB, "desc": "Side SL -> Tab Auto-Complete"},
                PAD_BTN_TL2: {"action": "key", "code": KEY_ESC, "desc": "Side SR -> Escape / Cancel"},

                # Face Buttons (Directional Pad Navigation for selecting options)
                PAD_BTN_NORTH: {"action": "key", "code": KEY_UP, "desc": "X (Up) -> Up Arrow (Select Up / History Up)"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_DOWN, "desc": "B (Down) -> Down Arrow (Select Down / History Down)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_LEFT, "desc": "Y (Left) -> Left Arrow (Move Cursor Left)"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_RIGHT, "desc": "A (Right) -> Right Arrow (Move Cursor Right)"},

                # Stick Click & Home
                PAD_BTN_THUMBR: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Stick Click -> Interrupt (Ctrl+C)"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super/Overview | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_TAB, "desc": "Side SL -> Tab Auto-Complete"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SR -> Escape / Cancel"}
            return bm

        # ======================================================================
        # 2. Single Left Joy-Con (Held vertically)
        # ======================================================================
        if device_type == "left_joycon":
            bm = {
                # Primary Triggers
                PAD_BTN_TL2: {"action": "key", "code": KEY_ENTER, "desc": "ZL (Trigger) -> Enter / Submit"},
                PAD_BTN_TL: {"action": "key", "code": KEY_BACKSPACE, "desc": "L (Bumper) -> Backspace / Erase"},

                # Side Rail SL / SR
                PAD_BTN_TR: {"action": "key", "code": KEY_TAB, "desc": "Side SL -> Tab Auto-Complete"},
                PAD_BTN_TR2: {"action": "key", "code": KEY_ESC, "desc": "Side SR -> Escape / Cancel"},

                # Directional Pad (Keyboard Arrow Keys for selecting items in CLI prompts & menus)
                PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_UP, "desc": "D-Pad Up -> Up Arrow (Select Up / History Up)"},
                PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_DOWN, "desc": "D-Pad Down -> Down Arrow (Select Down / History Down)"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_LEFT, "desc": "D-Pad Left -> Left Arrow (Move Cursor Left)"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_RIGHT, "desc": "D-Pad Right -> Right Arrow (Move Cursor Right)"},

                # Alternate face button names emitted by kernel hid-nintendo on Left Joy-Con
                PAD_BTN_NORTH: {"action": "key", "code": KEY_UP, "desc": "Up (Face) -> Up Arrow (Select Up / History Up)"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_DOWN, "desc": "Down (Face) -> Down Arrow (Select Down / History Down)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_LEFT, "desc": "Left (Face) -> Left Arrow (Move Cursor Left)"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_RIGHT, "desc": "Right (Face) -> Right Arrow (Move Cursor Right)"},

                # Stick Click & Capture
                PAD_BTN_THUMBL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Stick Click -> Interrupt (Ctrl+C)"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super/Overview | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_TAB, "desc": "Side SL -> Tab Auto-Complete"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SR -> Escape / Cancel"}
            return bm

        # ======================================================================
        # 3. Universal Gamepads & Dual Joy-Cons (Two-handed workstation layout, zero duplicate buttons)
        # ======================================================================
        bm = {
            # Right Triggers: Tab Auto-Complete & Clear Line
            PAD_BTN_TR2: {"action": "key", "code": KEY_TAB, "desc": "RT / ZR -> Tab Auto-Complete"},
            PAD_BTN_TR: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "RB / R -> Interrupt (Ctrl+C)"},

            # Left Triggers: Interrupt & Clear Screen
            PAD_BTN_TL2: {"action": "key", "code": KEY_ESC, "desc": "LT / ZL -> Escape / Cancel"},
            PAD_BTN_TL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_L], "desc": "LB / L -> Clear Screen (Ctrl+L)"},

            # Left Hand Directional Pad (Keyboard Arrow Keys to select options)
            PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_UP, "desc": "D-Pad Up -> Up Arrow (Select Up / History Up)"},
            PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_DOWN, "desc": "D-Pad Down -> Down Arrow (Select Down / History Down)"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_LEFT, "desc": "D-Pad Left -> Move Cursor Left"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_RIGHT, "desc": "D-Pad Right -> Move Cursor Right"},

            # Right Hand Face Buttons: Enter, Backspace, Quick 'y', Escape
            PAD_BTN_EAST: {"action": "key", "code": KEY_ENTER, "desc": "A / East -> Enter / Confirm Selection"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_BACKSPACE, "desc": "B / South -> Backspace / Erase"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_Y, "desc": "X / North -> Quick 'y' (Yes)"},
            PAD_BTN_WEST: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_U], "desc": "Y / West -> Erase Line (Ctrl+U)"},

            # Stick Clicks
            PAD_BTN_THUMBL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_Z], "desc": "L3 -> Suspend Job (Ctrl+Z)"},
            PAD_BTN_THUMBR: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_D], "desc": "R3 -> EOF / Exit (Ctrl+D)"},

            # Navigation & Mode Management
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode Forward"},
            PAD_BTN_MINUS: {"action": "key", "code": KEY_PAGEUP, "desc": "Select / - -> Page Up"},
            PAD_BTN_HOME: {"action": "key", "code": KEY_LEFTMETA, "desc": "Guide / Home -> Home / Super Key (Instant)"},
            PAD_BTN_CAPTURE: {"action": "key", "code": KEY_SYSRQ, "desc": "Capture / Share -> Instant Screenshot"},
        }
        return bm


if __name__ == "__main__":
    TerminalMode().run_standalone()
