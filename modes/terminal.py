#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Interactive Terminal & Shell Controller.
Designed for hands-free AI pair programming sessions, command execution, and CLI navigation.
Location: modes/terminal.py
"""

from typing import Any, Dict
from modes.base import (
    BaseMode,
    KEY_ESC, KEY_ENTER, KEY_TAB, KEY_BACKSPACE,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    KEY_PAGEUP, KEY_PAGEDOWN,
    KEY_LEFTCTRL, KEY_LEFTSHIFT, KEY_C, KEY_L, KEY_D, KEY_Z, KEY_Y,
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
        # 1. Single Right Joy-Con (Held vertically or sideways)
        # ======================================================================
        if device_type == "right_joycon":
            bm = {
                # Primary Triggers
                PAD_BTN_TR2: {"action": "key", "code": KEY_ENTER, "desc": "ZR (Trigger) -> Enter / Submit"},
                PAD_BTN_TR: {"action": "key", "code": KEY_TAB, "desc": "R (Bumper) -> Tab Auto-Complete"},

                # Side Rail SL / SR
                PAD_BTN_TL: {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape / Normal Mode"},
                PAD_BTN_TL2: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Side SR -> Cancel / Interrupt (Ctrl+C)"},

                # Face Buttons (ABXY)
                PAD_BTN_NORTH: {"action": "key", "code": KEY_UP, "desc": "X -> Previous Command (History Up)"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_BACKSPACE, "desc": "B -> Backspace / Erase"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_DOWN, "desc": "Y -> Next Command (History Down)"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_ENTER, "desc": "A -> Enter / Confirm"},

                # Stick Click & Home
                PAD_BTN_THUMBR: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_L], "desc": "Stick Click -> Clear Screen (Ctrl+L)"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super/Overview | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }
            # Fallback mappings for side-rail buttons
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Side SR -> Cancel (Ctrl+C)"}
            return bm

        # ======================================================================
        # 2. Single Left Joy-Con
        # ======================================================================
        if device_type == "left_joycon":
            bm = {
                # Primary Triggers
                PAD_BTN_TL2: {"action": "key", "code": KEY_ENTER, "desc": "ZL (Trigger) -> Enter / Submit"},
                PAD_BTN_TL: {"action": "key", "code": KEY_TAB, "desc": "L (Bumper) -> Tab Auto-Complete"},

                # Side Rail SL / SR
                PAD_BTN_TR: {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape / Normal Mode"},
                PAD_BTN_TR2: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Side SR -> Cancel / Interrupt (Ctrl+C)"},

                # D-Pad / Face Buttons
                PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_UP, "desc": "D-Pad Up -> Previous Command"},
                PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_DOWN, "desc": "D-Pad Down -> Next Command"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_BACKSPACE, "desc": "D-Pad Left -> Backspace"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_ENTER, "desc": "D-Pad Right -> Enter / Confirm"},

                # Alternate face button names emitted by kernel hid-nintendo
                PAD_BTN_NORTH: {"action": "key", "code": KEY_UP, "desc": "Up (Face) -> Previous Command"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_BACKSPACE, "desc": "Down (Face) -> Backspace"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_DOWN, "desc": "Left (Face) -> Next Command"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_ENTER, "desc": "Right (Face) -> Enter"},

                # Stick Click & Capture
                PAD_BTN_THUMBL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_L], "desc": "Stick Click -> Clear Screen (Ctrl+L)"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super/Overview | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Side SR -> Cancel (Ctrl+C)"}
            return bm

        # ======================================================================
        # 3. Universal Gamepads (Dual Joy-Cons, Pro Controller, Xbox, PS, 8BitDo)
        # ======================================================================
        return {
            # Right Triggers: Execute & Tab
            PAD_BTN_TR2: {"action": "key", "code": KEY_ENTER, "desc": "RT / R2 -> Enter / Submit"},
            PAD_BTN_TR: {"action": "key", "code": KEY_TAB, "desc": "RB / R1 -> Tab Auto-Complete"},

            # Left Triggers: Escape & Interrupt
            PAD_BTN_TL2: {"action": "key", "code": KEY_ESC, "desc": "LT / L2 -> Escape"},
            PAD_BTN_TL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "LB / L1 -> Interrupt (Ctrl+C)"},

            # D-Pad: History & Cursor
            PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_UP, "desc": "D-Pad Up -> Command History Up"},
            PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_DOWN, "desc": "D-Pad Down -> Command History Down"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_LEFT, "desc": "D-Pad Left -> Move Cursor Left"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_RIGHT, "desc": "D-Pad Right -> Move Cursor Right"},

            # Face Buttons: Confirmation & Quick-Keys
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_ENTER, "desc": "A / Cross -> Enter / Confirm"},
            PAD_BTN_EAST: {"action": "key", "code": KEY_BACKSPACE, "desc": "B / Circle -> Backspace"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_Y, "desc": "Y / Triangle -> Quick 'y' (Yes)"},
            PAD_BTN_WEST: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_L], "desc": "X / Square -> Clear Screen (Ctrl+L)"},

            # Stick Clicks
            PAD_BTN_THUMBL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_Z], "desc": "L3 -> Suspend Job (Ctrl+Z)"},
            PAD_BTN_THUMBR: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_D], "desc": "R3 -> EOF / Exit (Ctrl+D)"},

            # Navigation & Mode Management
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode"},
            PAD_BTN_MINUS: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_C], "desc": "Select / - -> Interrupt (Ctrl+C)"},
            PAD_BTN_HOME: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
        }
