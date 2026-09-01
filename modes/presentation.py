#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Wireless Presentation & Slide Clicker.
Location: modes/presentation.py
"""

from typing import Any, Dict
from modes.base import (
    BaseMode,
    KEY_ESC, KEY_ENTER, KEY_B, KEY_F5, KEY_F11,
    KEY_PAGEUP, KEY_PAGEDOWN,
    MOUSE_BTN_LEFT,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT,
    SL_GENERIC_CODES, SR_GENERIC_CODES
)


class PresentationMode(BaseMode):
    name = "PRESENTATION & SLIDE CLICKER"
    description = "Wireless slide clicker for PowerPoint, Google Slides, LibreOffice, and PDF presentations."
    enable_joystick_cursor = True
    enable_media_seek = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        if device_type == "right_joycon":
            bm = {
                PAD_BTN_TR2: {"action": "key", "code": KEY_PAGEDOWN, "desc": "ZR (Trigger) -> Next Slide (PageDown)"},
                PAD_BTN_TR: {"action": "key", "code": KEY_PAGEUP, "desc": "R (Bumper) -> Previous Slide (PageUp)"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_PAGEDOWN, "desc": "A -> Next Slide"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_PAGEUP, "desc": "B -> Previous Slide"},
                PAD_BTN_NORTH: {"action": "key", "code": KEY_F5, "desc": "X -> Start Slideshow (F5)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_B, "desc": "Y -> Blank / Black Screen (B)"},
                PAD_BTN_TL: {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Exit Slideshow (Escape)"},
                PAD_BTN_TL2: {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Activate"},
                PAD_BTN_THUMBR: {"action": "mouse_btn", "code": MOUSE_BTN_LEFT, "desc": "Stick Click -> Laser Click"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Exit Slideshow"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Activate"}
            return bm

        if device_type == "left_joycon":
            bm = {
                PAD_BTN_TL2: {"action": "key", "code": KEY_PAGEDOWN, "desc": "ZL (Trigger) -> Next Slide"},
                PAD_BTN_TL: {"action": "key", "code": KEY_PAGEUP, "desc": "L (Bumper) -> Previous Slide"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_PAGEDOWN, "desc": "D-Pad Right -> Next Slide"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_PAGEUP, "desc": "D-Pad Left -> Prev Slide"},
                PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_F5, "desc": "D-Pad Up -> Start Slideshow"},
                PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_B, "desc": "D-Pad Down -> Blank Screen"},
                PAD_BTN_NORTH: {"action": "key", "code": KEY_F5, "desc": "Up (Face) -> Start Slideshow"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_B, "desc": "Down (Face) -> Blank Screen"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_PAGEUP, "desc": "Left (Face) -> Prev Slide"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_PAGEDOWN, "desc": "Right (Face) -> Next Slide"},
                PAD_BTN_TR: {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Exit Slideshow"},
                PAD_BTN_TR2: {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Activate"},
                PAD_BTN_THUMBL: {"action": "mouse_btn", "code": MOUSE_BTN_LEFT, "desc": "Stick Click -> Laser Click"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Exit Slideshow"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Activate"}
            return bm

        return {
            PAD_BTN_TR2: {"action": "key", "code": KEY_PAGEDOWN, "desc": "RT / R2 -> Next Slide"},
            PAD_BTN_TR: {"action": "key", "code": KEY_PAGEUP, "desc": "RB / R1 -> Prev Slide"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_PAGEDOWN, "desc": "A / Cross -> Next Slide"},
            PAD_BTN_EAST: {"action": "key", "code": KEY_PAGEUP, "desc": "B / Circle -> Prev Slide"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_F5, "desc": "Y / Triangle -> Start Slideshow"},
            PAD_BTN_WEST: {"action": "key", "code": KEY_B, "desc": "X / Square -> Blank Screen"},
            PAD_BTN_THUMBL: {"action": "mouse_btn", "code": MOUSE_BTN_LEFT, "desc": "L3 -> Laser Click"},
            PAD_BTN_THUMBR: {"action": "mode_cycle", "desc": "R3 -> Cycle Mode"},
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
        }
