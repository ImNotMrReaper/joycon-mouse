#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Base Class for all Modular Controller Modes.
Location: modes/base.py
"""

from typing import Any, Dict

# Standard Linux Keycodes
KEY_ESC = 1
KEY_BACKSPACE = 14
KEY_TAB = 15
KEY_W = 17
KEY_ENTER = 28
KEY_LEFTCTRL = 29
KEY_C = 46                 # Closed Captions / Subtitles
KEY_B = 48                 # Blank / Black Screen
KEY_F = 33                 # Fullscreen
KEY_LEFTSHIFT = 42
KEY_LEFTALT = 56
KEY_SPACE = 57
KEY_F4 = 62
KEY_F5 = 63                # Presentation Slideshow Start
KEY_F11 = 87
KEY_SYSRQ = 99             # PrintScreen
KEY_UP = 103
KEY_PAGEUP = 104
KEY_LEFT = 105             # Rewind
KEY_RIGHT = 106            # Fast Forward
KEY_DOWN = 108
KEY_PAGEDOWN = 109
KEY_MUTE = 113
KEY_VOLUMEDOWN = 114
KEY_VOLUMEUP = 115
KEY_LEFTMETA = 125         # Super / Windows Key
KEY_BACK = 158
KEY_FORWARD = 159
KEY_NEXTSONG = 163
KEY_PLAYPAUSE = 164
KEY_PREVIOUSSONG = 165

# Mouse Buttons
MOUSE_BTN_LEFT = 0x110
MOUSE_BTN_RIGHT = 0x111
MOUSE_BTN_MIDDLE = 0x112
MOUSE_BTN_BACK = 0x113
MOUSE_BTN_FORWARD = 0x114

# Hardware Controller Buttons
PAD_BTN_SOUTH = 304    # B (Joy-Con R) / Down (Joy-Con L)
PAD_BTN_EAST = 305     # A (Joy-Con R) / Right (Joy-Con L)
PAD_BTN_NORTH = 307    # X (Joy-Con R) / Up (Joy-Con L)
PAD_BTN_WEST = 308     # Y (Joy-Con R) / Left (Joy-Con L)
PAD_BTN_CAPTURE = 309  # Capture Button (Joy-Con L)
PAD_BTN_TL = 310       # L (Left Joy-Con) | SL (Right Joy-Con)
PAD_BTN_TR = 311       # R (Right Joy-Con) | SL (Left Joy-Con)
PAD_BTN_TL2 = 312      # ZL (Left Joy-Con) | SR (Right Joy-Con)
PAD_BTN_TR2 = 313      # ZR (Right Joy-Con) | SR (Left Joy-Con)
PAD_BTN_MINUS = 314    # Minus (-)
PAD_BTN_PLUS = 315     # Plus (+)
PAD_BTN_HOME = 316     # Home Button (Joy-Con R)
PAD_BTN_THUMBL = 317   # Left Stick Click (L3)
PAD_BTN_THUMBR = 318   # Right Stick Click (R3)

SL_GENERIC_CODES = [294, 296, 260, 256, 258, 275, 288, 319, 704]
SR_GENERIC_CODES = [295, 297, 261, 257, 259, 276, 289, 320, 705]

PAD_BTN_DPAD_UP = 544
PAD_BTN_DPAD_DOWN = 545
PAD_BTN_DPAD_LEFT = 546
PAD_BTN_DPAD_RIGHT = 547


class BaseMode:
    """Base class for all modular controller modes."""
    name: str = "BASE MODE"
    description: str = "Base controller mode"
    enable_joystick_cursor: bool = True
    enable_media_seek: bool = False

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        raise NotImplementedError
