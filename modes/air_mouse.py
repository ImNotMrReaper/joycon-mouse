#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Wii Air-Mouse & Desktop Pointer.
Location: modes/air_mouse.py
"""

from typing import Any, Dict
from modes.base import (
    BaseMode,
    KEY_ESC, KEY_ENTER, KEY_BACK, KEY_FORWARD,
    MOUSE_BTN_LEFT, MOUSE_BTN_RIGHT, MOUSE_BTN_MIDDLE,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT,
    SL_GENERIC_CODES, SR_GENERIC_CODES
)


class AirMouseMode(BaseMode):
    name = "WII AIR-MOUSE (Motion Pointer & Desktop)"
    description = "Gyro motion pointer with desktop mouse, scroll, and browser navigation."
    enable_motion = True
    enable_joystick_cursor = True
    enable_media_seek = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        if device_type == "right_joycon":
            bm = {
                PAD_BTN_TR2: {"action": "mouse_btn", "code": MOUSE_BTN_LEFT, "desc": "ZR (Trigger) -> Left Click"},
                PAD_BTN_TR: {"action": "mouse_btn", "code": MOUSE_BTN_RIGHT, "desc": "R (Bumper) -> Right Click"},
                PAD_BTN_TL: {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape"},
                PAD_BTN_TL2: {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Open"},
                PAD_BTN_NORTH: {"action": "scroll", "param": 1, "desc": "X -> Scroll Up"},
                PAD_BTN_SOUTH: {"action": "scroll", "param": -1, "desc": "B -> Scroll Down"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_BACK, "desc": "Y -> Browser Back"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_FORWARD, "desc": "A -> Browser Forward"},
                PAD_BTN_THUMBR: {"action": "mouse_btn", "code": MOUSE_BTN_MIDDLE, "desc": "Stick Click -> Middle Click"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Open"}
            return bm

        if device_type == "left_joycon":
            bm = {
                PAD_BTN_TL2: {"action": "mouse_btn", "code": MOUSE_BTN_LEFT, "desc": "ZL (Trigger) -> Left Click"},
                PAD_BTN_TL: {"action": "mouse_btn", "code": MOUSE_BTN_RIGHT, "desc": "L (Bumper) -> Right Click"},
                PAD_BTN_TR: {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape"},
                PAD_BTN_TR2: {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Open"},
                PAD_BTN_DPAD_UP: {"action": "scroll", "param": 1, "desc": "D-Pad Up -> Scroll Up"},
                PAD_BTN_DPAD_DOWN: {"action": "scroll", "param": -1, "desc": "D-Pad Down -> Scroll Down"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_BACK, "desc": "D-Pad Left -> Browser Back"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_FORWARD, "desc": "D-Pad Right -> Browser Forward"},
                PAD_BTN_NORTH: {"action": "scroll", "param": 1, "desc": "Up (Face) -> Scroll Up"},
                PAD_BTN_SOUTH: {"action": "scroll", "param": -1, "desc": "Down (Face) -> Scroll Down"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_BACK, "desc": "Left (Face) -> Browser Back"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_FORWARD, "desc": "Right (Face) -> Browser Forward"},
                PAD_BTN_THUMBL: {"action": "mouse_btn", "code": MOUSE_BTN_MIDDLE, "desc": "Stick Click -> Middle Click"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ESC, "desc": "Side SL -> Escape"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_ENTER, "desc": "Side SR -> Enter / Open"}
            return bm

        return {
            PAD_BTN_TR2: {"action": "mouse_btn", "code": MOUSE_BTN_LEFT, "desc": "RT / R2 / ZR -> Left Click"},
            PAD_BTN_TR: {"action": "mouse_btn", "code": MOUSE_BTN_RIGHT, "desc": "RB / R1 / R -> Right Click"},
            PAD_BTN_TL2: {"action": "mouse_btn", "code": MOUSE_BTN_MIDDLE, "desc": "LT / L2 / ZL -> Middle Click"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_ENTER, "desc": "A / Cross -> Enter / Open"},
            PAD_BTN_EAST: {"action": "key", "code": KEY_ESC, "desc": "B / Circle -> Escape"},
            PAD_BTN_NORTH: {"action": "scroll", "param": 1, "desc": "Y / Triangle -> Scroll Up"},
            PAD_BTN_WEST: {"action": "scroll", "param": -1, "desc": "X / Square -> Scroll Down"},
            PAD_BTN_DPAD_UP: {"action": "scroll", "param": 1, "desc": "D-Pad Up -> Scroll Up"},
            PAD_BTN_DPAD_DOWN: {"action": "scroll", "param": -1, "desc": "D-Pad Down -> Scroll Down"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_BACK, "desc": "D-Pad Left -> Browser Back"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_FORWARD, "desc": "D-Pad Right -> Browser Forward"},
            PAD_BTN_THUMBL: {"action": "mouse_btn", "code": MOUSE_BTN_MIDDLE, "desc": "L3 -> Middle Click"},
            PAD_BTN_THUMBR: {"action": "mode_cycle", "desc": "R3 -> Cycle Mode"},
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode"},
            PAD_BTN_HOME: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
        }
