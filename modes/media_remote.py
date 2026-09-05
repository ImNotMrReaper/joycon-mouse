#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Universal Media Remote (Universal MPRIS + Side Volume Buttons).
Location: modes/media_remote.py
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
    KEY_C, KEY_F, KEY_MUTE, KEY_VOLUMEDOWN, KEY_VOLUMEUP,
    KEY_LEFT, KEY_RIGHT, KEY_NEXTSONG, KEY_PLAYPAUSE, KEY_PREVIOUSSONG,
    KEY_ESC, KEY_ENTER, KEY_T, KEY_SPACE,
    KEY_LEFTMETA, KEY_SYSRQ,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT,
    SL_GENERIC_CODES, SR_GENERIC_CODES
)


class MediaRemoteMode(BaseMode):
    name = "UNIVERSAL MEDIA REMOTE"
    description = "Controls Spotify, YouTube, VLC, Netflix, browsers, and all Linux media players."
    enable_joystick_cursor = False
    enable_media_seek = True

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        if device_type == "right_joycon":
            bm = {
                PAD_BTN_TR2: {"action": "key", "code": KEY_PLAYPAUSE, "desc": "ZR (Trigger) -> Play / Pause"},
                PAD_BTN_TR: {"action": "key", "code": KEY_MUTE, "desc": "R (Bumper) -> Mute / Unmute"},
                PAD_BTN_TL: {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "Side SL -> Volume Down"},
                PAD_BTN_TL2: {"action": "key", "code": KEY_VOLUMEUP, "desc": "Side SR -> Volume Up"},
                PAD_BTN_NORTH: {"action": "key", "code": KEY_C, "desc": "X -> Toggle Subtitles / Captions (C)"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_LEFT, "desc": "B -> Instant Rewind (-10s)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_PREVIOUSSONG, "desc": "Y -> Previous Track / Replay"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_NEXTSONG, "desc": "A -> Next Track / Skip"},
                PAD_BTN_THUMBR: {"action": "key", "code": KEY_F, "desc": "Stick Click -> Fullscreen Toggle (F)"},
                PAD_BTN_HOME: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "Side SL -> Volume Down"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_VOLUMEUP, "desc": "Side SR -> Volume Up"}
            return bm

        if device_type == "left_joycon":
            bm = {
                PAD_BTN_TL2: {"action": "key", "code": KEY_PLAYPAUSE, "desc": "ZL (Trigger) -> Play / Pause"},
                PAD_BTN_TL: {"action": "key", "code": KEY_MUTE, "desc": "L (Bumper) -> Mute / Unmute"},
                PAD_BTN_TR: {"action": "key", "code": KEY_VOLUMEUP, "desc": "Side SL (Right) -> Volume Up"},
                PAD_BTN_TR2: {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "Side SR (Left) -> Volume Down"},
                PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_C, "desc": "Up -> Toggle Subtitles / Captions"},
                PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_LEFT, "desc": "Down -> Instant Rewind (-10s)"},
                PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_PREVIOUSSONG, "desc": "Left -> Previous Track"},
                PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_NEXTSONG, "desc": "Right -> Next Track"},
                PAD_BTN_NORTH: {"action": "key", "code": KEY_C, "desc": "Up (Face) -> Toggle Subtitles"},
                PAD_BTN_SOUTH: {"action": "key", "code": KEY_LEFT, "desc": "Down (Face) -> Instant Rewind (-10s)"},
                PAD_BTN_WEST: {"action": "key", "code": KEY_PREVIOUSSONG, "desc": "Left (Face) -> Previous Track"},
                PAD_BTN_EAST: {"action": "key", "code": KEY_NEXTSONG, "desc": "Right (Face) -> Next Track"},
                PAD_BTN_THUMBL: {"action": "key", "code": KEY_F, "desc": "Stick Click -> Fullscreen Toggle (F)"},
                PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
                PAD_BTN_MINUS: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
            }
            for code in SL_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_VOLUMEUP, "desc": "Side SL (Right) -> Volume Up"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "Side SR (Left) -> Volume Down"}
            return bm

        return {
            # Right Shoulders: Play/Pause & Fast Forward
            PAD_BTN_TR2: {"action": "key", "code": KEY_PLAYPAUSE, "desc": "RT / ZR -> Play / Pause"},
            PAD_BTN_TR: {"action": "key", "code": KEY_RIGHT, "desc": "RB / R -> Fast Forward (+10s)"},

            # Left Shoulders: Mute & Rewind
            PAD_BTN_TL2: {"action": "key", "code": KEY_MUTE, "desc": "LT / ZL -> Mute Audio"},
            PAD_BTN_TL: {"action": "key", "code": KEY_LEFT, "desc": "LB / L -> Instant Rewind (-10s)"},

            # Left Hand Directional Pad: Volume & Track Skipping
            PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_VOLUMEUP, "desc": "D-Pad Up -> Volume Up"},
            PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "D-Pad Down -> Volume Down"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_PREVIOUSSONG, "desc": "D-Pad Left -> Prev Track"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_NEXTSONG, "desc": "D-Pad Right -> Next Track"},

            # Right Hand Face Buttons: Enter, Exit, Subtitles, Fullscreen
            PAD_BTN_EAST: {"action": "key", "code": KEY_ENTER, "desc": "A / East -> Enter / Play / Confirm"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_ESC, "desc": "B / South -> Escape / Exit Fullscreen"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_C, "desc": "X / North -> Toggle Subtitles (C)"},
            PAD_BTN_WEST: {"action": "key", "code": KEY_F, "desc": "Y / West -> Toggle Fullscreen (F)"},

            # Stick Clicks: Theater Mode & Quick Seek
            PAD_BTN_THUMBL: {"action": "key", "code": KEY_T, "desc": "L3 -> Theater Mode (T)"},
            PAD_BTN_THUMBR: {"action": "key", "code": KEY_SPACE, "desc": "R3 -> Pause / Space"},

            # Navigation & Mode Management
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode Forward"},
            PAD_BTN_MINUS: {"action": "key", "code": KEY_MUTE, "desc": "Select / - -> Mute Audio"},
            PAD_BTN_HOME: {"action": "key", "code": KEY_LEFTMETA, "desc": "Guide / Home -> Home / Super Key (Instant)"},
            PAD_BTN_CAPTURE: {"action": "key", "code": KEY_SYSRQ, "desc": "Capture / Share -> Instant Screenshot"},
        }


if __name__ == "__main__":
    MediaRemoteMode().run_standalone()
