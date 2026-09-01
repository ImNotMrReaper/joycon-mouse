#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Mode: Universal Media Remote (Universal MPRIS + Side Volume Buttons).
Location: modes/media_remote.py
"""

from typing import Any, Dict
from modes.base import (
    BaseMode,
    KEY_C, KEY_F, KEY_MUTE, KEY_VOLUMEDOWN, KEY_VOLUMEUP,
    KEY_LEFT, KEY_RIGHT, KEY_NEXTSONG, KEY_PLAYPAUSE, KEY_PREVIOUSSONG,
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
                PAD_BTN_TR: {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "Side SL -> Volume Down"},
                PAD_BTN_TR2: {"action": "key", "code": KEY_VOLUMEUP, "desc": "Side SR -> Volume Up"},
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
                bm[code] = {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "Side SL -> Volume Down"}
            for code in SR_GENERIC_CODES:
                bm[code] = {"action": "key", "code": KEY_VOLUMEUP, "desc": "Side SR -> Volume Up"}
            return bm

        return {
            PAD_BTN_TR2: {"action": "key", "code": KEY_PLAYPAUSE, "desc": "RT / R2 -> Play / Pause"},
            PAD_BTN_TR: {"action": "key", "code": KEY_MUTE, "desc": "RB / R1 -> Mute Audio"},
            PAD_BTN_NORTH: {"action": "key", "code": KEY_C, "desc": "Y / Triangle -> Toggle Subtitles"},
            PAD_BTN_SOUTH: {"action": "key", "code": KEY_LEFT, "desc": "A / Cross -> Rewind (-10s)"},
            PAD_BTN_DPAD_UP: {"action": "key", "code": KEY_VOLUMEUP, "desc": "D-Pad Up -> Volume Up"},
            PAD_BTN_DPAD_DOWN: {"action": "key", "code": KEY_VOLUMEDOWN, "desc": "D-Pad Down -> Volume Down"},
            PAD_BTN_DPAD_LEFT: {"action": "key", "code": KEY_PREVIOUSSONG, "desc": "D-Pad Left -> Prev Track"},
            PAD_BTN_DPAD_RIGHT: {"action": "key", "code": KEY_NEXTSONG, "desc": "D-Pad Right -> Next Track"},
            PAD_BTN_THUMBL: {"action": "key", "code": KEY_F, "desc": "L3 -> Fullscreen Toggle"},
            PAD_BTN_THUMBR: {"action": "mode_cycle", "desc": "R3 -> Cycle Mode"},
            PAD_BTN_PLUS: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode"},
            PAD_BTN_HOME: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super | Hold: Screenshot"},
            PAD_BTN_CAPTURE: {"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"},
        }
