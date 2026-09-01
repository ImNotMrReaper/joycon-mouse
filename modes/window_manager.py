#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Desktop Window & Workspace Manager.
Location: modes/window_manager.py
"""

from typing import Any, Dict
from modes.base import (
    BaseMode,
    KEY_ESC, KEY_ENTER, KEY_TAB, KEY_F4,
    KEY_LEFTMETA, KEY_LEFTALT, KEY_LEFTCTRL,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT,
    SL_GENERIC_CODES, SR_GENERIC_CODES
)


class WindowManagerMode(BaseMode):
    name = "WINDOW & WORKSPACE MANAGER"
    description = "Snap windows, maximize/minimize, Alt+Tab app switch, and cycle virtual desktops."
    enable_joystick_cursor = True
    enable_media_seek = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        if device_type == "right_joycon":
            bm = {
                PAD_BTN_TR2: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_RIGHT], "desc": "ZR -> Snap Window Right (Super+Right)"},
                PAD_BTN_TR: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_LEFT], "desc": "R -> Snap Window Left (Super+Left)"},
                PAD_BTN_NORTH: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_UP], "desc": "X -> Maximize Window (Super+Up)"},
                PAD_BTN_SOUTH: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_DOWN], "desc": "B -> Minimize / Restore (Super+Down)"},
                PAD_BTN_WEST: {"action": "combo", "keys": [KEY_LEFTALT, KEY_TAB], "desc": "Y -> App Switcher (Alt+Tab)"},
                PAD_BTN_EAST: {"action": "combo", "keys": [KEY_LEFTALT, KEY_F4], "desc": "A -> Close Active Window (Alt+F4)"},
                PAD_BTN_TL: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_LEFT], "desc": "Side SL -> Prev Workspace (Ctrl+Alt+Left)"},
                PAD_BTN_TL2: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_RIGHT], "desc": "Side SR -> Next Workspace (Ctrl+Alt+Right)"},
                PAD_BTN_THUMBR: {"action": "key", "code": KEY_LEFTMETA, "desc": "Stick Click -> Overview (Super)"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_LEFT], "desc": "Side SL -> Prev Workspace"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_RIGHT], "desc": "Side SR -> Next Workspace"}
            return bm

        if device_type == "left_joycon":
            bm = {
                PAD_BTN_TL2: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_RIGHT], "desc": "ZL -> Snap Window Right (Super+Right)"},
                PAD_BTN_TL: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_LEFT], "desc": "L -> Snap Window Left (Super+Left)"},
                PAD_BTN_DPAD_UP: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_UP], "desc": "D-Pad Up -> Maximize Window"},
                PAD_BTN_DPAD_DOWN: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_DOWN], "desc": "D-Pad Down -> Minimize / Restore"},
                PAD_BTN_DPAD_LEFT: {"action": "combo", "keys": [KEY_LEFTALT, KEY_TAB], "desc": "D-Pad Left -> App Switcher (Alt+Tab)"},
                PAD_BTN_DPAD_RIGHT: {"action": "combo", "keys": [KEY_LEFTALT, KEY_F4], "desc": "D-Pad Right -> Close Window (Alt+F4)"},
                PAD_BTN_NORTH: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_UP], "desc": "Up (Face) -> Maximize Window"},
                PAD_BTN_SOUTH: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_DOWN], "desc": "Down (Face) -> Minimize / Restore"},
                PAD_BTN_WEST: {"action": "combo", "keys": [KEY_LEFTALT, KEY_TAB], "desc": "Left (Face) -> App Switcher (Alt+Tab)"},
                PAD_BTN_EAST: {"action": "combo", "keys": [KEY_LEFTALT, KEY_F4], "desc": "Right (Face) -> Close Window (Alt+F4)"},
                PAD_BTN_TR: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_LEFT], "desc": "Side SL -> Prev Workspace"},
                PAD_BTN_TR2: {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_RIGHT], "desc": "Side SR -> Next Workspace"},
                PAD_BTN_THUMBL: {"action": "key", "code": KEY_LEFTMETA, "desc": "Stick Click -> Overview (Super)"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_LEFT], "desc": "Side SL -> Prev Workspace"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "combo", "keys": [KEY_LEFTCTRL, KEY_LEFTALT, KEY_RIGHT], "desc": "Side SR -> Next Workspace"}
            return bm

        return {
            PAD_BTN_TR2: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_RIGHT], "desc": "RT / R2 -> Snap Right"},
            PAD_BTN_TR: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_LEFT], "desc": "RB / R1 -> Snap Left"},
            PAD_BTN_NORTH: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_UP], "desc": "Y / Triangle -> Maximize"},
            PAD_BTN_SOUTH: {"action": "combo", "keys": [KEY_LEFTMETA, KEY_DOWN], "desc": "A / Cross -> Minimize"},
            PAD_BTN_WEST: {"action": "combo", "keys": [KEY_LEFTALT, KEY_TAB], "desc": "X / Square -> Alt+Tab"},
            PAD_BTN_EAST: {"action": "combo", "keys": [KEY_LEFTALT, KEY_F4], "desc": "B / Circle -> Close (Alt+F4)"},
            PAD_BTN_THUMBL: {"action": "key", "code": KEY_LEFTMETA, "desc": "L3 -> Overview"},
            PAD_BTN_THUMBR: {"action": "mode_cycle", "desc": "R3 -> Cycle Mode"},
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
        }
