#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Base Class for all Modular Controller Modes.
Location: modes/base.py
"""

import sys
from typing import Any, Dict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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
KEY_D = 32                 # EOF / Exit (Ctrl+D)
KEY_L = 38                 # Clear Screen (Ctrl+L)
KEY_Z = 44                 # Suspend (Ctrl+Z)
KEY_Y = 21                 # Yes
KEY_N = 49                 # No
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
    enable_terminal_scroll: bool = False

    # Metadata set by the dynamic module loader
    file_path: str = ""
    is_custom: bool = False
    is_enabled: bool = True

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        raise NotImplementedError

    def run_standalone(self) -> None:
        """Prints mode layout and test information when executed directly as a script."""
        mode_type = "Community / Custom Plugin" if self.is_custom else "Built-in Core Mode"
        print("=" * 68)
        print(f"  🎮 JOY-CON MOUSE MODULE: {self.name}")
        print(f"  TYPE:        {mode_type}")
        print(f"  DESCRIPTION: {self.description}")
        print(f"  FEATURES:    Cursor: {'YES' if self.enable_joystick_cursor else 'NO'} | "
              f"Media Seek: {'YES' if self.enable_media_seek else 'NO'} | "
              f"Terminal Scroll: {'YES' if self.enable_terminal_scroll else 'NO'}")
        print("=" * 68)

        for dev in ["right_joycon", "left_joycon", "dual_joycon"]:
            print(f"\n--- Controller Layout: {dev.replace('_', ' ').title()} ---")
            try:
                bm = self.get_button_map(dev)
                seen = set()
                for code, act in sorted(bm.items(), key=lambda x: str(x[1].get("desc", ""))):
                    desc = act.get("desc", "")
                    if desc and desc not in seen:
                        seen.add(desc)
                        print(f"  * {desc}")
            except Exception as e:
                print(f"  (Not defined for this device type: {e})")
        print("\n" + "=" * 68)
