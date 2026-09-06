#!/usr/bin/env python3
"""
🎮 Joy-Con Mouse & Universal Remote for Windows (Beta Preview)
================================================================================
Zero-dependency, standalone Joy-Con & Gamepad desktop mouse driver for Windows 10/11.
Uses native Windows Multimedia (winmm.dll) and Win32 User32 via ctypes.
Features universal button mapping, controller profiles, and foreground app awareness.
"""

import sys
import os
import time
import math
import json
import argparse
import threading
from typing import Dict, Any, Optional, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Check if running on Windows
IS_WINDOWS = sys.platform.startswith("win")

if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    winmm = ctypes.windll.winmm
    user32 = ctypes.windll.user32

    class XINPUT_VIBRATION(ctypes.Structure):
        _fields_ = [
            ("wLeftMotorSpeed", wintypes.WORD),
            ("wRightMotorSpeed", wintypes.WORD),
        ]

    class JOYINFOEX(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("dwXpos", wintypes.DWORD),
            ("dwYpos", wintypes.DWORD),
            ("dwZpos", wintypes.DWORD),
            ("dwRpos", wintypes.DWORD),
            ("dwUpos", wintypes.DWORD),
            ("dwVpos", wintypes.DWORD),
            ("dwButtons", wintypes.DWORD),
            ("dwButtonNumber", wintypes.DWORD),
            ("dwPOV", wintypes.DWORD),
            ("dwReserved1", wintypes.DWORD),
            ("dwReserved2", wintypes.DWORD),
        ]

    class JOYCAPSW(ctypes.Structure):
        _fields_ = [
            ("wMid", wintypes.WORD),
            ("wPid", wintypes.WORD),
            ("szPname", wintypes.WCHAR * 32),
            ("wXmin", wintypes.UINT),
            ("wXmax", wintypes.UINT),
            ("wYmin", wintypes.UINT),
            ("wYmax", wintypes.UINT),
            ("wZmin", wintypes.UINT),
            ("wZmax", wintypes.UINT),
            ("wNumButtons", wintypes.UINT),
            ("wPeriodMin", wintypes.UINT),
            ("wPeriodMax", wintypes.UINT),
            ("wRmin", wintypes.UINT),
            ("wRmax", wintypes.UINT),
            ("wUmin", wintypes.UINT),
            ("wUmax", wintypes.UINT),
            ("wVmin", wintypes.UINT),
            ("wVmax", wintypes.UINT),
            ("wCaps", wintypes.UINT),
            ("wMaxAxes", wintypes.UINT),
            ("wNumAxes", wintypes.UINT),
            ("wMaxButtons", wintypes.UINT),
            ("szRegKey", wintypes.WCHAR * 32),
            ("szOEMVxD", wintypes.WCHAR * 260),
        ]

    JOY_RETURNALL = 0x000000FF
    JOYERR_NOERROR = 0

    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    MOUSEEVENTF_WHEEL = 0x0800

    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_EXTENDEDKEY = 0x0001

    # Extended keycodes handled by Windows
    pass
else:
    class JOYINFOEX:
        pass

    class JOYCAPSW:
        pass

    class XINPUT_VIBRATION:
        pass

    winmm = None
    user32 = None

# Multimedia virtual keycodes (Win32 Virtual-Key Codes)
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02
VK_MBUTTON = 0x04
VK_BACK = 0x08             # Backspace
VK_TAB = 0x09              # Tab Auto-Complete
VK_RETURN = 0x0D           # Enter / Submit
VK_SHIFT = 0x10            # Left Shift
VK_CONTROL = 0x11          # Left Ctrl
VK_MENU = 0x12             # Alt
VK_ESCAPE = 0x1B           # Escape
VK_SPACE = 0x20            # Spacebar
VK_PRIOR = 0x21            # Page Up
VK_NEXT = 0x22             # Page Down
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25             # Arrow Left
VK_UP = 0x26               # Arrow Up
VK_RIGHT = 0x27            # Arrow Right
VK_DOWN = 0x28             # Arrow Down
VK_SNAPSHOT = 0x2C         # PrintScreen / Instant Screenshot
VK_B = 0x42                # B key (Black screen in presentation)
VK_C = 0x43                # C key (Subtitles / Captions)
VK_D = 0x44                # D key (Win+D show desktop, Ctrl+D EOF)
VK_F = 0x46                # F key (Fullscreen toggle)
VK_I = 0x49                # I key (Inventory)
VK_L = 0x4C                # L key (Ctrl+L clear screen)
VK_M = 0x4D                # M key (Map)
VK_R = 0x52                # R key (Ctrl+R reload page)
VK_T = 0x54                # T key (YouTube theater mode)
VK_U = 0x55                # U key (Ctrl+U erase line)
VK_W = 0x57                # W key (Ctrl+W close tab, White screen)
VK_Y = 0x59                # Y key (Quick 'y')
VK_Z = 0x5A                # Z key (Ctrl+Z suspend)
VK_LWIN = 0x5B             # Left Windows / Start / Overview Key
VK_F4 = 0x73
VK_F5 = 0x74               # F5 Slideshow start
VK_F9 = 0x78
VK_F11 = 0x7A
VK_BROWSER_BACK = 0xA6     # Browser Back
VK_BROWSER_FORWARD = 0xA7  # Browser Forward
VK_VOLUME_MUTE = 0xAD      # Volume Mute
VK_VOLUME_DOWN = 0xAE      # Volume Down
VK_VOLUME_UP = 0xAF        # Volume Up
VK_MEDIA_NEXT_TRACK = 0xB0 # Next Track
VK_MEDIA_PREV_TRACK = 0xB1 # Previous Track
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3 # Play / Pause

# ANSI Colors
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"

# Canonical Mode Button Maps across All Controller Types (1:1 Linux Behavioral Parity)
MODE_MAPS = {
    "DESKTOP MOUSE": {
        "right_joycon": {
            15: {"action": "mouse_btn", "code": "left", "desc": "ZR (Trigger) -> Left Click"},
            14: {"action": "mouse_btn", "code": "right", "desc": "R (Bumper) -> Right Click"},
            4: {"action": "key", "code": VK_ESCAPE, "desc": "Side SL -> Escape"},
            5: {"action": "key", "code": VK_RETURN, "desc": "Side SR -> Enter / Open"},
            1: {"action": "scroll", "param": 1, "desc": "X -> Scroll Up"},
            2: {"action": "scroll", "param": -1, "desc": "B -> Scroll Down"},
            3: {"action": "key", "code": VK_BROWSER_BACK, "desc": "Y -> Browser Back"},
            0: {"action": "key", "code": VK_BROWSER_FORWARD, "desc": "A -> Browser Forward"},
            11: {"action": "mouse_btn", "code": "middle", "desc": "Stick Click -> Middle Click"},
            12: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
            9: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
        },
        "left_joycon": {
            15: {"action": "mouse_btn", "code": "left", "desc": "ZL (Trigger) -> Left Click"},
            14: {"action": "mouse_btn", "code": "right", "desc": "L (Bumper) -> Right Click"},
            4: {"action": "key", "code": VK_ESCAPE, "desc": "Side SL -> Escape"},
            5: {"action": "key", "code": VK_RETURN, "desc": "Side SR -> Enter / Open"},
            3: {"action": "scroll", "param": 1, "desc": "Up (Face) -> Scroll Up"},
            0: {"action": "scroll", "param": -1, "desc": "Down (Face) -> Scroll Down"},
            2: {"action": "key", "code": VK_BROWSER_BACK, "desc": "Left (Face) -> Browser Back"},
            1: {"action": "key", "code": VK_BROWSER_FORWARD, "desc": "Right (Face) -> Browser Forward"},
            10: {"action": "mouse_btn", "code": "middle", "desc": "Stick Click -> Middle Click"},
            13: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
            8: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
        },
        "playstation": {
            7: {"action": "mouse_btn", "code": "left", "desc": "R2 -> Left Click"},
            5: {"action": "mouse_btn", "code": "right", "desc": "R1 -> Right Click"},
            6: {"action": "mouse_btn", "code": "middle", "desc": "L2 -> Middle Click (New Tab / Auto-Scroll)"},
            4: {"action": "combo", "keys": [VK_CONTROL, VK_W], "desc": "L1 -> Close Tab (Ctrl+W)"},
            2: {"action": "key", "code": VK_RETURN, "desc": "Circle (East) -> Enter / Open"},
            1: {"action": "key", "code": VK_ESCAPE, "desc": "Cross (South) -> Escape / Dismiss"},
            3: {"action": "combo", "keys": [VK_CONTROL, VK_T], "desc": "Triangle (North) -> New Tab (Ctrl+T)"},
            0: {"action": "key", "code": VK_SPACE, "desc": "Square (West) -> Spacebar (Scroll Down / Play-Pause)"},
            10: {"action": "combo", "keys": [VK_LWIN, VK_D], "desc": "L3 -> Show Desktop (Win+D)"},
            11: {"action": "combo", "keys": [VK_CONTROL, VK_R], "desc": "R3 -> Reload Page (Ctrl+R)"},
            9: {"action": "mode_cycle", "desc": "Options -> Cycle Mode Forward"},
            8: {"action": "combo", "keys": [VK_CONTROL, VK_PRIOR], "desc": "Share -> Previous Tab (Ctrl+PageUp)"},
            12: {"action": "smart_home", "desc": "PS Button -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "mouse_btn", "code": "left", "desc": "Trackpad Click -> Left Click"},
        },
        "dual_joycon": {
            7: {"action": "mouse_btn", "code": "left", "desc": "RT / ZR -> Left Click"},
            5: {"action": "mouse_btn", "code": "right", "desc": "RB / R -> Right Click"},
            6: {"action": "mouse_btn", "code": "middle", "desc": "LT / ZL -> Middle Click (New Tab / Auto-Scroll)"},
            4: {"action": "combo", "keys": [VK_CONTROL, VK_W], "desc": "LB / L -> Close Tab (Ctrl+W)"},
            1: {"action": "key", "code": VK_RETURN, "desc": "B / East -> Enter / Open"},
            0: {"action": "key", "code": VK_ESCAPE, "desc": "A / South -> Escape / Dismiss"},
            3: {"action": "combo", "keys": [VK_CONTROL, VK_T], "desc": "Y / North -> New Tab (Ctrl+T)"},
            2: {"action": "key", "code": VK_SPACE, "desc": "X / West -> Spacebar (Scroll Down / Play-Pause)"},
            10: {"action": "combo", "keys": [VK_LWIN, VK_D], "desc": "L3 -> Show Desktop (Win+D)"},
            11: {"action": "combo", "keys": [VK_CONTROL, VK_R], "desc": "R3 -> Reload Page (Ctrl+R)"},
            8: {"action": "combo", "keys": [VK_CONTROL, VK_PRIOR], "desc": "Select / - -> Previous Tab (Ctrl+PageUp)"},
            9: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode Forward"},
            12: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "key", "code": VK_SNAPSHOT, "desc": "Capture / Share -> Instant Screenshot"},
        },
    },
    "UNIVERSAL MEDIA REMOTE": {
        "right_joycon": {
            15: {"action": "media_play_pause", "desc": "ZR (Trigger) -> Play / Pause"},
            14: {"action": "key", "code": VK_VOLUME_MUTE, "desc": "R (Bumper) -> Mute / Unmute"},
            4: {"action": "key", "code": VK_VOLUME_DOWN, "desc": "Side SL -> Volume Down"},
            5: {"action": "key", "code": VK_VOLUME_UP, "desc": "Side SR -> Volume Up"},
            1: {"action": "key", "code": VK_C, "desc": "X -> Toggle Subtitles / Captions (C)"},
            2: {"action": "key", "code": VK_LEFT, "desc": "B -> Instant Rewind (-10s)"},
            3: {"action": "key", "code": VK_MEDIA_PREV_TRACK, "desc": "Y -> Previous Track / Replay"},
            0: {"action": "key", "code": VK_MEDIA_NEXT_TRACK, "desc": "A -> Next Track / Skip"},
            11: {"action": "key", "code": VK_F, "desc": "Stick Click -> Fullscreen Toggle (F)"},
            12: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
            9: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
        },
        "left_joycon": {
            15: {"action": "media_play_pause", "desc": "ZL (Trigger) -> Play / Pause"},
            14: {"action": "key", "code": VK_VOLUME_MUTE, "desc": "L (Bumper) -> Mute / Unmute"},
            4: {"action": "key", "code": VK_VOLUME_UP, "desc": "Side SL (Right) -> Volume Up"},
            5: {"action": "key", "code": VK_VOLUME_DOWN, "desc": "Side SR (Left) -> Volume Down"},
            3: {"action": "key", "code": VK_C, "desc": "Up (Face) -> Toggle Subtitles (C)"},
            0: {"action": "key", "code": VK_LEFT, "desc": "Down (Face) -> Instant Rewind (-10s)"},
            2: {"action": "key", "code": VK_MEDIA_PREV_TRACK, "desc": "Left (Face) -> Previous Track"},
            1: {"action": "key", "code": VK_MEDIA_NEXT_TRACK, "desc": "Right (Face) -> Next Track"},
            10: {"action": "key", "code": VK_F, "desc": "Stick Click -> Fullscreen Toggle (F)"},
            13: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
            8: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
        },
        "playstation": {
            7: {"action": "media_play_pause", "desc": "R2 -> Play / Pause"},
            5: {"action": "key", "code": VK_RIGHT, "desc": "R1 -> Fast Forward (+10s)"},
            6: {"action": "key", "code": VK_VOLUME_MUTE, "desc": "L2 -> Mute Audio"},
            4: {"action": "key", "code": VK_LEFT, "desc": "L1 -> Instant Rewind (-10s)"},
            2: {"action": "key", "code": VK_RETURN, "desc": "Circle (East) -> Enter / Play / Confirm"},
            1: {"action": "key", "code": VK_ESCAPE, "desc": "Cross (South) -> Escape / Exit Fullscreen"},
            3: {"action": "key", "code": VK_C, "desc": "Triangle (North) -> Toggle Subtitles (C)"},
            0: {"action": "key", "code": VK_F, "desc": "Square (West) -> Toggle Fullscreen (F)"},
            10: {"action": "key", "code": VK_T, "desc": "L3 -> Theater Mode (T)"},
            11: {"action": "key", "code": VK_SPACE, "desc": "R3 -> Pause / Space"},
            9: {"action": "mode_cycle", "desc": "Options -> Cycle Mode Forward"},
            8: {"action": "key", "code": VK_VOLUME_MUTE, "desc": "Share -> Mute Audio"},
            12: {"action": "smart_home", "desc": "PS Button -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "media_play_pause", "desc": "Trackpad Click -> Play / Pause"},
        },
        "dual_joycon": {
            7: {"action": "media_play_pause", "desc": "RT / ZR -> Play / Pause"},
            5: {"action": "key", "code": VK_RIGHT, "desc": "RB / R -> Fast Forward (+10s)"},
            6: {"action": "key", "code": VK_VOLUME_MUTE, "desc": "LT / ZL -> Mute Audio"},
            4: {"action": "key", "code": VK_LEFT, "desc": "LB / L -> Instant Rewind (-10s)"},
            1: {"action": "key", "code": VK_RETURN, "desc": "B / East -> Enter / Play / Confirm"},
            0: {"action": "key", "code": VK_ESCAPE, "desc": "A / South -> Escape / Exit Fullscreen"},
            3: {"action": "key", "code": VK_C, "desc": "Y / North -> Toggle Subtitles (C)"},
            2: {"action": "key", "code": VK_F, "desc": "X / West -> Toggle Fullscreen (F)"},
            10: {"action": "key", "code": VK_T, "desc": "L3 -> Theater Mode (T)"},
            11: {"action": "key", "code": VK_SPACE, "desc": "R3 -> Pause / Space"},
            8: {"action": "key", "code": VK_VOLUME_MUTE, "desc": "Select / - -> Mute Audio"},
            9: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode Forward"},
            12: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "key", "code": VK_SNAPSHOT, "desc": "Capture / Share -> Instant Screenshot"},
        },
    },
    "INTERACTIVE TERMINAL": {
        "right_joycon": {
            15: {"action": "key", "code": VK_RETURN, "desc": "ZR (Trigger) -> Enter / Submit"},
            14: {"action": "key", "code": VK_BACK, "desc": "R (Bumper) -> Backspace / Erase"},
            4: {"action": "key", "code": VK_TAB, "desc": "Side SL -> Tab Auto-Complete"},
            5: {"action": "key", "code": VK_ESCAPE, "desc": "Side SR -> Escape / Cancel"},
            1: {"action": "key", "code": VK_UP, "desc": "X (Up) -> Up Arrow (Select Up / History Up)"},
            2: {"action": "key", "code": VK_DOWN, "desc": "B (Down) -> Down Arrow (Select Down / History Down)"},
            3: {"action": "key", "code": VK_LEFT, "desc": "Y (Left) -> Left Arrow (Move Cursor Left)"},
            0: {"action": "key", "code": VK_RIGHT, "desc": "A (Right) -> Right Arrow (Move Cursor Right)"},
            11: {"action": "combo", "keys": [VK_CONTROL, VK_C], "desc": "Stick Click -> Interrupt (Ctrl+C)"},
            12: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
            9: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
        },
        "left_joycon": {
            15: {"action": "key", "code": VK_RETURN, "desc": "ZL (Trigger) -> Enter / Submit"},
            14: {"action": "key", "code": VK_BACK, "desc": "L (Bumper) -> Backspace / Erase"},
            4: {"action": "key", "code": VK_TAB, "desc": "Side SL -> Tab Auto-Complete"},
            5: {"action": "key", "code": VK_ESCAPE, "desc": "Side SR -> Escape / Cancel"},
            3: {"action": "key", "code": VK_UP, "desc": "Up (Face) -> Up Arrow (Select Up / History Up)"},
            0: {"action": "key", "code": VK_DOWN, "desc": "Down (Face) -> Down Arrow (Select Down / History Down)"},
            2: {"action": "key", "code": VK_LEFT, "desc": "Left (Face) -> Left Arrow (Move Cursor Left)"},
            1: {"action": "key", "code": VK_RIGHT, "desc": "Right (Face) -> Right Arrow (Move Cursor Right)"},
            10: {"action": "combo", "keys": [VK_CONTROL, VK_C], "desc": "Stick Click -> Interrupt (Ctrl+C)"},
            13: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
            8: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
        },
        "playstation": {
            7: {"action": "key", "code": VK_TAB, "desc": "R2 -> Tab Auto-Complete"},
            5: {"action": "combo", "keys": [VK_CONTROL, VK_C], "desc": "R1 -> Interrupt (Ctrl+C)"},
            6: {"action": "key", "code": VK_ESCAPE, "desc": "L2 -> Escape / Cancel"},
            4: {"action": "combo", "keys": [VK_CONTROL, VK_L], "desc": "L1 -> Clear Screen (Ctrl+L)"},
            2: {"action": "key", "code": VK_RETURN, "desc": "Circle (East) -> Enter / Confirm Selection"},
            1: {"action": "key", "code": VK_BACK, "desc": "Cross (South) -> Backspace / Erase"},
            3: {"action": "key", "code": VK_Y, "desc": "Triangle (North) -> Quick 'y' (Yes)"},
            0: {"action": "combo", "keys": [VK_CONTROL, VK_U], "desc": "Square (West) -> Erase Line (Ctrl+U)"},
            10: {"action": "combo", "keys": [VK_CONTROL, VK_Z], "desc": "L3 -> Suspend Job (Ctrl+Z)"},
            11: {"action": "combo", "keys": [VK_CONTROL, VK_D], "desc": "R3 -> EOF / Exit (Ctrl+D)"},
            9: {"action": "mode_cycle", "desc": "Options -> Cycle Mode Forward"},
            8: {"action": "key", "code": VK_PRIOR, "desc": "Share -> Page Up"},
            12: {"action": "smart_home", "desc": "PS Button -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "key", "code": VK_RETURN, "desc": "Trackpad Click -> Enter / Submit"},
        },
        "dual_joycon": {
            7: {"action": "key", "code": VK_TAB, "desc": "RT / ZR -> Tab Auto-Complete"},
            5: {"action": "combo", "keys": [VK_CONTROL, VK_C], "desc": "RB / R -> Interrupt (Ctrl+C)"},
            6: {"action": "key", "code": VK_ESCAPE, "desc": "LT / ZL -> Escape / Cancel"},
            4: {"action": "combo", "keys": [VK_CONTROL, VK_L], "desc": "LB / L -> Clear Screen (Ctrl+L)"},
            1: {"action": "key", "code": VK_RETURN, "desc": "B / East -> Enter / Confirm Selection"},
            0: {"action": "key", "code": VK_BACK, "desc": "A / South -> Backspace / Erase"},
            3: {"action": "key", "code": VK_Y, "desc": "Y / North -> Quick 'y' (Yes)"},
            2: {"action": "combo", "keys": [VK_CONTROL, VK_U], "desc": "X / West -> Erase Line (Ctrl+U)"},
            10: {"action": "combo", "keys": [VK_CONTROL, VK_Z], "desc": "L3 -> Suspend Job (Ctrl+Z)"},
            11: {"action": "combo", "keys": [VK_CONTROL, VK_D], "desc": "R3 -> EOF / Exit (Ctrl+D)"},
            8: {"action": "key", "code": VK_PRIOR, "desc": "Select / - -> Page Up"},
            9: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode Forward"},
            12: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "key", "code": VK_SNAPSHOT, "desc": "Capture / Share -> Instant Screenshot"},
        },
    },
    "PRESENTATION CLICKER": {
        "right_joycon": {
            15: {"action": "key", "code": VK_SPACE, "desc": "ZR (Trigger) -> Next Slide (Space)"},
            14: {"action": "key", "code": VK_BACK, "desc": "R (Bumper) -> Previous Slide (Backspace)"},
            0: {"action": "key", "code": VK_SPACE, "desc": "A -> Next Slide (Space)"},
            2: {"action": "key", "code": VK_BACK, "desc": "B -> Previous Slide (Backspace)"},
            1: {"action": "key", "code": VK_F5, "desc": "X -> Start Presentation (F5)"},
            3: {"action": "key", "code": VK_B, "desc": "Y -> Black / Blank Screen (B)"},
            11: {"action": "key", "code": VK_ESCAPE, "desc": "Stick Click -> Exit Slideshow (Esc)"},
            12: {"action": "smart_home", "desc": "Home -> Tap: Super/Win | Hold: Screenshot"},
            9: {"action": "mode_cycle", "desc": "+ -> Cycle Mode"},
        },
        "left_joycon": {
            15: {"action": "key", "code": VK_SPACE, "desc": "ZL (Trigger) -> Next Slide (Space)"},
            14: {"action": "key", "code": VK_BACK, "desc": "L (Bumper) -> Previous Slide (Backspace)"},
            1: {"action": "key", "code": VK_SPACE, "desc": "Right (Face) -> Next Slide (Space)"},
            2: {"action": "key", "code": VK_BACK, "desc": "Left (Face) -> Previous Slide (Backspace)"},
            3: {"action": "key", "code": VK_F5, "desc": "Up (Face) -> Start Presentation (F5)"},
            0: {"action": "key", "code": VK_B, "desc": "Down (Face) -> Black Screen (B)"},
            10: {"action": "key", "code": VK_ESCAPE, "desc": "Stick Click -> Exit Slideshow (Esc)"},
            13: {"action": "smart_home", "desc": "Capture -> Tap: Super/Win | Hold: Screenshot"},
            8: {"action": "mode_cycle", "desc": "- -> Cycle Mode"},
        },
        "playstation": {
            7: {"action": "key", "code": VK_SPACE, "desc": "R2 -> Next Slide (Space)"},
            5: {"action": "key", "code": VK_B, "desc": "R1 -> Black Screen (B)"},
            6: {"action": "key", "code": VK_BACK, "desc": "L2 -> Previous Slide (Backspace)"},
            4: {"action": "key", "code": VK_F5, "desc": "L1 -> Start Presentation (F5)"},
            2: {"action": "key", "code": VK_RETURN, "desc": "Circle (East) -> Next Slide / Confirm"},
            1: {"action": "key", "code": VK_ESCAPE, "desc": "Cross (South) -> Exit Slideshow (Esc)"},
            3: {"action": "key", "code": VK_F5, "desc": "Triangle (North) -> Start Presentation (F5)"},
            0: {"action": "key", "code": VK_W, "desc": "Square (West) -> White Screen (W)"},
            10: {"action": "key", "code": VK_ESCAPE, "desc": "L3 -> Exit Slideshow (Esc)"},
            9: {"action": "mode_cycle", "desc": "Options -> Cycle Mode Forward"},
            12: {"action": "smart_home", "desc": "PS Button -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "key", "code": VK_SPACE, "desc": "Trackpad Click -> Next Slide (Space)"},
        },
        "dual_joycon": {
            7: {"action": "key", "code": VK_SPACE, "desc": "RT / ZR -> Next Slide (Space)"},
            5: {"action": "key", "code": VK_B, "desc": "RB / R -> Black Screen (B)"},
            6: {"action": "key", "code": VK_BACK, "desc": "LT / ZL -> Previous Slide (Backspace)"},
            4: {"action": "key", "code": VK_F5, "desc": "LB / L -> Start Presentation (F5)"},
            1: {"action": "key", "code": VK_RETURN, "desc": "B / East -> Next Slide / Confirm"},
            0: {"action": "key", "code": VK_ESCAPE, "desc": "A / South -> Exit Slideshow (Esc)"},
            3: {"action": "key", "code": VK_F5, "desc": "Y / North -> Start Presentation (F5)"},
            2: {"action": "key", "code": VK_W, "desc": "X / West -> White Screen (W)"},
            10: {"action": "key", "code": VK_ESCAPE, "desc": "L3 -> Exit Slideshow (Esc)"},
            9: {"action": "mode_cycle", "desc": "Start / + -> Cycle Mode Forward"},
            12: {"action": "smart_home", "desc": "Guide / Home -> Tap: Super/Win | Hold: Screenshot"},
            13: {"action": "key", "code": VK_SNAPSHOT, "desc": "Capture / Share -> Instant Screenshot"},
        },
    },
}

DEFAULT_MAPPINGS = {
    "default": {
        "name": "Standard Gamepad / Dual Joy-Con (Two-Handed)",
        "rt": 7, "rb": 5, "lt": 6, "lb": 4,
        "east": 1, "south": 0, "north": 3, "west": 2,
        "l3": 10, "r3": 11, "start": 9, "select": 8, "home": 12, "capture": 13,
        "left_click": 7, "right_click": 5, "middle_click": 6, "trackpad_click": 13,
        "cycle_mode": 9, "cycle_mode_alt": 8, "screenshot": 13, "home_btn": 12,
        "media_play_pause": 7, "media_vol_down": 1, "media_vol_up": 2,
        "media_next_track": 3, "media_prev_track": 4, "media_mute": 6,
        "terminal_enter": 1, "terminal_backspace": 0, "terminal_tab": 7, "terminal_esc": 6,
        "slide_next": 7, "slide_prev": 6, "slide_f5": 4, "slide_esc": 0
    },
    "joycon_r": {
        "name": "Nintendo Switch Joy-Con (R)",
        "rt": 15, "rb": 14, "sl": 4, "sr": 5,
        "east": 0, "north": 1, "south": 2, "west": 3,
        "r3": 11, "home": 12, "start": 9,
        "left_click": 15, "right_click": 14, "middle_click": 11,
        "cycle_mode": 9, "screenshot": 12, "home_btn": 12,
        "media_play_pause": 15, "media_mute": 14,
        "terminal_enter": 15, "terminal_backspace": 14, "terminal_tab": 4, "terminal_esc": 5,
        "slide_next": 15, "slide_prev": 14, "slide_f5": 1, "slide_esc": 11
    },
    "joycon_l": {
        "name": "Nintendo Switch Joy-Con (L)",
        "lt": 15, "lb": 14, "sl": 4, "sr": 5,
        "south": 0, "east": 1, "west": 2, "north": 3,
        "l3": 10, "capture": 13, "select": 8,
        "left_click": 15, "right_click": 14, "middle_click": 10,
        "cycle_mode": 8, "screenshot": 13, "home_btn": 13,
        "media_play_pause": 15, "media_mute": 14,
        "terminal_enter": 15, "terminal_backspace": 14, "terminal_tab": 4, "terminal_esc": 5,
        "slide_next": 15, "slide_prev": 14, "slide_f5": 3, "slide_esc": 10
    },
    "playstation": {
        "name": "Sony PlayStation (DualSense / DualShock 4)",
        "west": 0, "south": 1, "east": 2, "north": 3,
        "lb": 4, "rb": 5, "lt": 6, "rt": 7,
        "select": 8, "start": 9, "l3": 10, "r3": 11, "home": 12, "capture": 13,
        "left_click": 7, "right_click": 5, "middle_click": 6, "trackpad_click": 13,
        "cycle_mode": 9, "cycle_mode_alt": 8, "screenshot": 8, "home_btn": 12,
        "media_play_pause": 7, "media_vol_down": 4, "media_vol_up": 5,
        "media_next_track": 1, "media_prev_track": 2, "media_mute": 6,
        "terminal_enter": 2, "terminal_backspace": 1, "terminal_tab": 7, "terminal_esc": 6,
        "slide_next": 7, "slide_prev": 6, "slide_f5": 4, "slide_esc": 1
    }
}



def get_config_dir() -> str:
    if IS_WINDOWS:
        appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = os.path.join(appdata, "joycon-mouse")
    else:
        path = os.path.expanduser("~/.config/joycon-mouse")
    os.makedirs(path, exist_ok=True)
    return path


def get_mappings_path() -> str:
    return os.path.join(get_config_dir(), "controller_mappings.json")


def load_all_mappings() -> Dict[str, Any]:
    path = get_mappings_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "profiles" in data:
                    return data["profiles"]
                return data
        except Exception:
            pass
    return dict(DEFAULT_MAPPINGS)


def save_all_mappings(profiles: Dict[str, Any]) -> None:
    path = get_mappings_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0", "profiles": profiles}, f, indent=2)
    except Exception as e:
        print(f"{YELLOW}Warning: Could not save mappings file: {e}{RESET}")


def get_foreground_window_title() -> str:
    """Dynamically query the active foreground window title via Win32 User32."""
    if not IS_WINDOWS or not user32:
        return ""
    try:
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return ""
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return ""
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value
    except Exception:
        return ""


class WindowsRumbleManager:
    """Universal controller vibration and haptic feedback manager for Windows.
    Zero external dependencies (pure ctypes + xinput1_4.dll / xinput1_3.dll / xinput9_1_0.dll).
    Provides tactile haptic pulses on connection, disconnection, mode cycling,
    media scrubbing gestures, screenshots, and button diagnostics across all vibrating controllers."""

    def __init__(self, enabled: bool = True, debug: bool = False):
        self.enabled = enabled
        self.debug = debug
        self.xinput = None
        self._load_xinput()

    def _load_xinput(self):
        if not IS_WINDOWS:
            return
        for dll_name in ["xinput1_4.dll", "xinput1_3.dll", "xinput9_1_0.dll"]:
            try:
                lib = ctypes.windll.LoadLibrary(dll_name)
                if lib and hasattr(lib, "XInputSetState"):
                    lib.XInputSetState.argtypes = [wintypes.DWORD, ctypes.POINTER(XINPUT_VIBRATION)]
                    lib.XInputSetState.restype = wintypes.DWORD
                    self.xinput = lib
                    if self.debug:
                        print(f"  [DEBUG] XInput vibration subsystem active: {dll_name}")
                    break
            except Exception:
                continue

    def _pulse_worker(self, duration_ms: int, strong: int, weak: int, count: int, interval_ms: int):
        if not self.xinput:
            return

        vib_on = XINPUT_VIBRATION(max(0, min(65535, int(strong))), max(0, min(65535, int(weak))))
        vib_off = XINPUT_VIBRATION(0, 0)

        for i in range(count):
            active_slots = []
            for slot in range(4):
                try:
                    res = self.xinput.XInputSetState(slot, ctypes.byref(vib_on))
                    if res == 0:  # ERROR_SUCCESS
                        active_slots.append(slot)
                except Exception:
                    pass

            time.sleep(max(0.01, duration_ms / 1000.0))

            for slot in active_slots:
                try:
                    self.xinput.XInputSetState(slot, ctypes.byref(vib_off))
                except Exception:
                    pass

            if count > 1 and i < count - 1:
                time.sleep(max(0.01, interval_ms / 1000.0))

    def pulse(self, duration_ms: int = 50, strong: int = 0x6000, weak: int = 0x6000, count: int = 1, interval_ms: int = 60) -> None:
        if not self.enabled or not self.xinput:
            return
        t = threading.Thread(
            target=self._pulse_worker,
            args=(duration_ms, strong, weak, count, interval_ms),
            daemon=True
        )
        t.start()

    def connect(self) -> None:
        """Crisp double-buzz welcome when a controller connects."""
        self.pulse(duration_ms=65, strong=0x6000, weak=0x8000, count=2, interval_ms=75)

    def disconnect(self) -> None:
        """Distinct warning buzz when a controller disconnects."""
        self.pulse(duration_ms=200, strong=0x9000, weak=0x5000, count=1)

    def mode_switch(self) -> None:
        """Tactile haptic click when cycling controller modes."""
        self.pulse(duration_ms=45, strong=0x5000, weak=0x7000, count=1)

    def screenshot(self) -> None:
        """Double shutter click when capturing a screenshot."""
        self.pulse(duration_ms=35, strong=0x8000, weak=0x9000, count=2, interval_ms=45)

    def tick(self) -> None:
        """Subtle micro-tick on media seek, volume change, or action."""
        self.pulse(duration_ms=25, strong=0x3000, weak=0x4000, count=1)


class WindowsJoyConDriver:
    """Windows Joy-Con & Gamepad Mouse Driver using pure standard library ctypes."""

    def __init__(
        self,
        force_map: bool = False,
        timeout_sec: Optional[int] = None,
        sensitivity: Optional[float] = None,
        deadzone: Optional[float] = None,
        debug: bool = False,
        no_reconnect: bool = False,
        no_rumble: bool = False
    ):
        self.sensitivity = sensitivity if sensitivity is not None else 1.0
        self.deadzone = deadzone if deadzone is not None else 0.10
        self.debug = debug
        self.no_reconnect = no_reconnect
        self.no_rumble = no_rumble
        self.rumble_enabled = not no_rumble
        self.current_mode_index = 0
        self.modes = ["DESKTOP MOUSE", "MEDIA REMOTE", "INTERACTIVE TERMINAL", "PRESENTATION CLICKER"]
        self.force_map = force_map
        self.timeout_sec = timeout_sec

        self.last_buttons = 0
        self.last_pov = 65535
        self.last_pov_direction = "CENTER"
        self.last_scroll_time = 0.0
        self.last_seek_time = 0.0
        self.last_vol_time = 0.0
        self.acc_x = 0.0
        self.acc_y = 0.0
        self.acc_scroll = 0.0
        self.left_pressed = False
        self.right_pressed = False
        self.middle_pressed = False

        self.controller_name = "Unknown Controller"
        self.device_profile = "dual_joycon"
        self.custom_mapping: Optional[Dict[str, Any]] = None
        self.active_mapping = dict(DEFAULT_MAPPINGS["default"])
        self.smart_press_timestamp: Optional[float] = None
        self.smart_hold_triggered: bool = False
        self.hold_threshold_sec: float = 0.38

        self.load_config(user_sens=sensitivity, user_deadzone=deadzone)
        self.rumble = WindowsRumbleManager(enabled=self.rumble_enabled, debug=self.debug)

    def load_config(self, user_sens: Optional[float] = None, user_deadzone: Optional[float] = None):
        config_path = os.path.join(get_config_dir(), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    if user_sens is None:
                        self.sensitivity = float(cfg.get("sensitivity", 1.0))
                    if user_deadzone is None:
                        self.deadzone = float(cfg.get("deadzone", 0.10))
                    if self.no_rumble:
                        self.rumble_enabled = False
                    else:
                        self.rumble_enabled = bool(cfg.get("rumble_enabled", cfg.get("rumble", True)))
            except Exception:
                pass

    def is_browser_or_media_window(self) -> bool:
        """Checks if Opera, Chrome, Edge, YouTube, or another media player is active in the foreground."""
        title = (get_foreground_window_title() or "").lower()
        return any(k in title for k in [
            "youtube", "opera", "chrome", "firefox", "edge", "brave", "twitch", "netflix", "vlc", "spotify"
        ])

    def send_key(self, vk_code: int):
        if not IS_WINDOWS or not user32:
            return
        scan = user32.MapVirtualKeyW(vk_code, 0)
        extended_keys = {
            VK_LWIN, VK_SNAPSHOT, VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK,
            VK_MEDIA_PREV_TRACK, VK_VOLUME_UP, VK_VOLUME_DOWN, VK_VOLUME_MUTE,
            VK_UP, VK_DOWN, VK_LEFT, VK_RIGHT, VK_RETURN, VK_SPACE,
            VK_BROWSER_BACK, VK_BROWSER_FORWARD, VK_PRIOR, VK_NEXT
        }
        flags = KEYEVENTF_EXTENDEDKEY if vk_code in extended_keys else 0
        user32.keybd_event(vk_code, scan, flags, 0)
        time.sleep(0.015)
        user32.keybd_event(vk_code, scan, flags | KEYEVENTF_KEYUP, 0)

    def send_combo(self, keys: List[int]):
        if not IS_WINDOWS or not user32:
            return
        extended_keys = {VK_LWIN, VK_UP, VK_DOWN, VK_LEFT, VK_RIGHT, VK_RETURN, VK_PRIOR, VK_NEXT, VK_SNAPSHOT}
        for k in keys:
            scan = user32.MapVirtualKeyW(k, 0)
            flags = KEYEVENTF_EXTENDEDKEY if k in extended_keys else 0
            user32.keybd_event(k, scan, flags, 0)
        time.sleep(0.015)
        for k in reversed(keys):
            scan = user32.MapVirtualKeyW(k, 0)
            flags = KEYEVENTF_EXTENDEDKEY if k in extended_keys else 0
            user32.keybd_event(k, scan, flags | KEYEVENTF_KEYUP, 0)

    def move_mouse(self, dx, dy):
        if not IS_WINDOWS or not user32:
            return
        user32.mouse_event(MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)

    def mouse_down(self, button):
        if not IS_WINDOWS or not user32:
            return
        if button == "left" and not self.left_pressed:
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            self.left_pressed = True
            print(f"\r  {BOLD}{GREEN}[Click]{RESET} LEFT DOWN         ", end="", flush=True)
        elif button == "right" and not self.right_pressed:
            user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            self.right_pressed = True
            print(f"\r  {BOLD}{CYAN}[Click]{RESET} RIGHT DOWN        ", end="", flush=True)
        elif button == "middle" and not self.middle_pressed:
            user32.mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            self.middle_pressed = True
            print(f"\r  {BOLD}{YELLOW}[Click]{RESET} MIDDLE DOWN       ", end="", flush=True)

    def mouse_up(self, button):
        if not IS_WINDOWS or not user32:
            return
        if button == "left" and self.left_pressed:
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            self.left_pressed = False
        elif button == "right" and self.right_pressed:
            user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            self.right_pressed = False
        elif button == "middle" and self.middle_pressed:
            user32.mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            self.middle_pressed = False

    def mouse_wheel(self, delta):
        if not IS_WINDOWS or not user32:
            return
        user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, int(delta * 120), 0)

    @staticmethod
    def get_pov_direction(pov: int) -> str:
        if pov == 65535 or pov < 0:
            return "CENTER"
        if pov <= 4500 or pov >= 31500:
            return "UP"
        if 4500 < pov < 13500:
            return "RIGHT"
        if 13500 <= pov <= 22500:
            return "DOWN"
        if 22500 < pov < 31500:
            return "LEFT"
        return "CENTER"

    def get_current_mode_map(self) -> Dict[int, Dict[str, Any]]:
        curr_mode = self.modes[self.current_mode_index]
        mode_dict = MODE_MAPS.get(curr_mode, {})
        base_map = mode_dict.get(self.device_profile, mode_dict.get("dual_joycon", {}))
        result = dict(base_map)
        if self.custom_mapping:
            if "cycle_mode" in self.custom_mapping:
                result[self.custom_mapping["cycle_mode"]] = {"action": "mode_cycle", "desc": "Custom -> Cycle Mode"}
            if "screenshot" in self.custom_mapping:
                result[self.custom_mapping["screenshot"]] = {"action": "key", "code": VK_SNAPSHOT, "desc": "Custom -> Screenshot"}
            if "home" in self.custom_mapping:
                result[self.custom_mapping["home"]] = {"action": "smart_home", "desc": "Custom -> Smart Home"}
            if curr_mode == "DESKTOP MOUSE":
                if "left_click" in self.custom_mapping:
                    result[self.custom_mapping["left_click"]] = {"action": "mouse_btn", "code": "left", "desc": "Custom -> Left Click"}
                if "right_click" in self.custom_mapping:
                    result[self.custom_mapping["right_click"]] = {"action": "mouse_btn", "code": "right", "desc": "Custom -> Right Click"}
                if "middle_click" in self.custom_mapping:
                    result[self.custom_mapping["middle_click"]] = {"action": "mouse_btn", "code": "middle", "desc": "Custom -> Middle Click"}
            elif curr_mode == "UNIVERSAL MEDIA REMOTE":
                if "media_play_pause" in self.custom_mapping:
                    result[self.custom_mapping["media_play_pause"]] = {"action": "media_play_pause", "desc": "Custom -> Play / Pause"}
                if "media_mute" in self.custom_mapping:
                    result[self.custom_mapping["media_mute"]] = {"action": "key", "code": VK_VOLUME_MUTE, "desc": "Custom -> Mute Audio"}
                if "media_vol_up" in self.custom_mapping:
                    result[self.custom_mapping["media_vol_up"]] = {"action": "key", "code": VK_VOLUME_UP, "desc": "Custom -> Volume Up"}
                if "media_vol_down" in self.custom_mapping:
                    result[self.custom_mapping["media_vol_down"]] = {"action": "key", "code": VK_VOLUME_DOWN, "desc": "Custom -> Volume Down"}
        return result

    def print_mode_cheatsheet(self):
        curr_mode = self.modes[self.current_mode_index]
        print("\n" + "=" * 76)
        print(f"  {BOLD}{PURPLE}🎮 ACTIVE MODE [{self.current_mode_index + 1}/{len(self.modes)}]: {GREEN}[{curr_mode}]{RESET}")
        print(f"  {CYAN}Device Profile:{RESET} {BOLD}{self.device_profile.upper()}{RESET} ({self.controller_name})")
        print("-" * 76)
        print("Controls Cheatsheet:")
        button_map = self.get_current_mode_map()
        seen = set()
        for act in sorted(button_map.values(), key=lambda x: str(x.get("desc", ""))):
            desc = act.get("desc", "")
            if desc and desc not in seen:
                seen.add(desc)
                print(f"  * {desc}")
        if curr_mode == "DESKTOP MOUSE":
            print("  * D-Pad Up/Down -> Page Scroll Up / Down")
            print("  * D-Pad Left/Right -> Browser History Back / Forward")
            print("  * Left Stick -> Precision Pointer Cursor (x^1.6 curve)")
        elif curr_mode == "UNIVERSAL MEDIA REMOTE":
            print("  * D-Pad Up/Down -> Volume Up / Down")
            print("  * D-Pad Left/Right -> Prev Track / Next Track")
            print("  * Left Stick Left/Right -> Scrub Forward (+5s) / Rewind (-5s)")
            print("  * Left Stick Up/Down -> Volume Up / Down")
        elif curr_mode == "INTERACTIVE TERMINAL":
            print("  * D-Pad Up/Down -> History Up / Down")
            print("  * D-Pad Left/Right -> Move Cursor Left / Right")
            print("  * Left Stick Up/Down -> Scroll Terminal History")
        elif curr_mode == "PRESENTATION CLICKER":
            print("  * D-Pad Up/Down -> First Slide (PageUp) / Last Slide (PageDown)")
            print("  * D-Pad Left/Right -> Previous Slide / Next Slide")
        print("-" * 76)
        print("Tip: Press Start / Plus or Minus to cycle mode (with tactile haptic click).")
        print("Tip: Tap Home/Capture for Start Menu | Hold >= 0.4s for Screenshot.")
        print("=" * 76 + "\n")

    def cycle_mode(self):
        if self.left_pressed:
            self.mouse_up("left")
        if self.right_pressed:
            self.mouse_up("right")
        if self.middle_pressed:
            self.mouse_up("middle")
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        mode = self.modes[self.current_mode_index]
        print(f"\n{BOLD}{PURPLE}🔄 Switched Mode:{RESET} {BOLD}{GREEN}[{mode}]{RESET}")
        if self.rumble:
            self.rumble.mode_switch()
        self.print_mode_cheatsheet()


    def get_controller_name(self, dev_id: int) -> str:
        if not IS_WINDOWS or not winmm:
            return f"Gamepad #{dev_id}"
        try:
            caps = JOYCAPSW()
            if winmm.joyGetDevCapsW(dev_id, ctypes.byref(caps), ctypes.sizeof(JOYCAPSW)) == JOYERR_NOERROR:
                name = caps.szPname.strip()
                if name:
                    return name
        except Exception:
            pass
        return f"Gamepad #{dev_id}"

    def find_connected_controller(self) -> Optional[int]:
        if not IS_WINDOWS or not winmm:
            print("Windows emulation mode (running on non-Windows host).")
            return None
        num_devs = winmm.joyGetNumDevs()
        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(JOYINFOEX)
        info.dwFlags = JOY_RETURNALL

        for dev_id in range(num_devs):
            res = winmm.joyGetPosEx(dev_id, ctypes.byref(info))
            if res == JOYERR_NOERROR:
                return dev_id
        return None

    def wait_for_button_press(self, dev_id: int, timeout_sec: float = 12.0) -> Optional[int]:
        """Poll for next pressed button index, debounce, and return bit index."""
        if not IS_WINDOWS or not winmm:
            return None
        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(JOYINFOEX)
        info.dwFlags = JOY_RETURNALL

        start_t = time.time()
        last_b = 0
        while (time.time() - start_t) < timeout_sec:
            if winmm.joyGetPosEx(dev_id, ctypes.byref(info)) == JOYERR_NOERROR:
                pressed = info.dwButtons & ~last_b
                if pressed:
                    for bit in range(32):
                        if pressed & (1 << bit):
                            # Debounce release
                            while winmm.joyGetPosEx(dev_id, ctypes.byref(info)) == JOYERR_NOERROR and (info.dwButtons & (1 << bit)):
                                time.sleep(0.04)
                            return bit
                last_b = info.dwButtons
            time.sleep(0.02)
        return None

    def run_mapping_wizard(self, dev_id: int, name: str) -> Dict[str, Any]:
        """Interactive Guided Controller Button Calibration Wizard."""
        print(f"\n" + "=" * 76)
        print(f"  {BOLD}{PURPLE}🎮 UNIVERSAL CONTROLLER BUTTON MAPPING WIZARD{RESET}")
        print(f"  {CYAN}Target Device:{RESET} {BOLD}{name}{RESET} (Device #{dev_id})")
        print(f"  {DIM}Press the button on your controller for each requested action.{RESET}")
        print(f"  {DIM}(Wait 12s or press Ctrl+C to keep default){RESET}")
        print("=" * 76 + "\n")

        steps = [
            ("left_click", "LEFT CLICK (Primary action / select)", 0),
            ("right_click", "RIGHT CLICK (Secondary action / menu)", 1),
            ("middle_click", "MIDDLE CLICK (Wheel click / auto-scroll)", 2),
            ("trackpad_click", "TRACKPAD MECHANICAL CLICK (Sensitive pinpoint click)", 13),
            ("cycle_mode", "CYCLE MODES (Mouse / Media / Terminal / Presentation)", 9),
            ("screenshot", "SCREENSHOT (Instant PrintScreen)", 13),
            ("home", "HOME / GUIDE (Windows Start Menu)", 12),
            ("media_play_pause", "MEDIA PLAY / PAUSE", 0),
            ("media_vol_down", "VOLUME DOWN", 1),
            ("media_vol_up", "VOLUME UP", 2),
            ("media_next_track", "NEXT TRACK", 3),
            ("media_prev_track", "PREVIOUS TRACK", 4),
            ("media_mute", "MUTE AUDIO", 5),
            ("terminal_enter", "TERMINAL ENTER / SUBMIT", 0),
            ("terminal_backspace", "TERMINAL BACKSPACE", 1),
            ("terminal_tab", "TERMINAL TAB AUTO-COMPLETE", 2),
            ("terminal_esc", "TERMINAL ESCAPE / CANCEL", 3),
            ("slide_next", "PRESENTATION NEXT SLIDE", 0),
            ("slide_prev", "PRESENTATION PREV SLIDE", 1),
        ]

        mapping: Dict[str, Any] = {"name": name}
        default_ref = DEFAULT_MAPPINGS["default"]

        for key, prompt_label, default_bit in steps:
            print(f"👉 Press button for {BOLD}{CYAN}[{prompt_label}]{RESET} [Default: Button {default_bit}]... ", end="", flush=True)
            detected = self.wait_for_button_press(dev_id, timeout_sec=10.0)
            if detected is not None:
                mapping[key] = detected
                print(f"{BOLD}{GREEN}✓ Assigned to Button {detected}!{RESET}")
            else:
                mapping[key] = default_ref.get(key, default_bit)
                print(f"{YELLOW}Using default (Button {mapping[key]}){RESET}")

        # Save profile
        all_profiles = load_all_mappings()
        all_profiles[name] = mapping
        save_all_mappings(all_profiles)

        print(f"\n{BOLD}{GREEN}✅ Successfully saved button mapping profile for '{name}'!{RESET}")
        print(f"   Saved to: {get_mappings_path()}\n")
        return mapping

    def setup_mapping_profile(self, dev_id: int):
        """Auto-detects controller profile, loads saved config, or launches wizard for new controllers."""
        self.controller_name = self.get_controller_name(dev_id)
        all_profiles = load_all_mappings()

        norm_name = self.controller_name.lower()
        if "joy-con (l)" in norm_name or "left joy-con" in norm_name:
            self.device_profile = "left_joycon"
            self.active_mapping = dict(DEFAULT_MAPPINGS["joycon_l"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Nintendo Joy-Con (L)")
        elif "joy-con (r)" in norm_name or "right joy-con" in norm_name:
            self.device_profile = "right_joycon"
            self.active_mapping = dict(DEFAULT_MAPPINGS["joycon_r"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Nintendo Switch Joy-Con (R)")
        elif any(ps in norm_name for ps in ["dualsense", "dualshock", "playstation", "wireless controller"]):
            self.device_profile = "playstation"
            self.active_mapping = dict(DEFAULT_MAPPINGS["playstation"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Sony PlayStation (DualSense / DualShock 4)")
        else:
            self.device_profile = "dual_joycon"
            self.active_mapping = dict(DEFAULT_MAPPINGS["default"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Standard Gamepad / Dual Joy-Con")

        if self.force_map:
            self.active_mapping = self.run_mapping_wizard(dev_id, self.controller_name)
            self.custom_mapping = self.active_mapping
            return

        # Check if saved profile exists
        if self.controller_name in all_profiles:
            self.active_mapping = all_profiles[self.controller_name]
            self.custom_mapping = self.active_mapping
            print(f"  {BOLD}{GREEN}✓ Loaded saved button mapping for:{RESET} '{self.controller_name}'")
            return

        # Unrecognized / new controller -> Guided wizard
        if not any(k in norm_name for k in ["joy-con", "gamepad", "controller", "dualsense", "dualshock", "playstation", "wireless"]):
            print(f"  {YELLOW}ℹ️  New or unrecognized controller detected: '{self.controller_name}'{RESET}")
            print(f"  {DIM}Setting up custom button configuration...{RESET}")
            try:
                self.active_mapping = self.run_mapping_wizard(dev_id, self.controller_name)
                self.custom_mapping = self.active_mapping
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Wizard cancelled. Using standard defaults.{RESET}")
                self.active_mapping = dict(DEFAULT_MAPPINGS["default"])

    def run(self):
        print(f"\n================================================================================")
        print(f"  {BOLD}{PURPLE}🎮 JOY-CON MOUSE FOR WINDOWS (Universal Edition){RESET}")
        print(f"  {DIM}Zero external dependencies (Native WinMM & Win32 User32){RESET}")
        print(f"================================================================================\n")
        print(f"  {CYAN}Sensitivity:{RESET} {self.sensitivity}x | {CYAN}Deadzone:{RESET} {self.deadzone}")
        print(f"  {CYAN}Active Mode:{RESET} {BOLD}{GREEN}[{self.modes[self.current_mode_index]}]{RESET}\n")

        if not IS_WINDOWS:
            print(f"{YELLOW}Notice: joycon-mouse-windows.py is designed for Windows 10/11.{RESET}")
            print("This universal script compiles and runs on Windows machines with zero pip dependencies.\n")
            return

        print(f"🔍 Searching for paired Joy-Cons or Gamepads...")
        dev_id = self.find_connected_controller()

        start_wait = time.time()
        while dev_id is None:
            if self.timeout_sec and (time.time() - start_wait) >= self.timeout_sec:
                print(f"  {YELLOW}Timed out after {self.timeout_sec}s waiting for controller.{RESET}")
                return

            print(f"  {YELLOW}No controller detected.{RESET} Please ensure your Joy-Con is paired in Windows Bluetooth settings.")
            print(f"  Retrying in 2 seconds (Press Ctrl+C to stop)...")
            time.sleep(2)
            dev_id = self.find_connected_controller()

        self.setup_mapping_profile(dev_id)

        print(f"\n  {GREEN}✓ Active Gamepad Device #{dev_id} ({self.controller_name})!{RESET}")
        print(f"  {DIM}Move the analog stick to guide cursor. Cycle modes with designated mode button.{RESET}\n")
        if self.rumble:
            self.rumble.connect()
            print(f"  {BOLD}{PURPLE}📳 [Haptics]{RESET} Controller vibration active\n")

        self.print_mode_cheatsheet()

        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(JOYINFOEX)
        info.dwFlags = JOY_RETURNALL

        try:
            while True:
                res = winmm.joyGetPosEx(dev_id, ctypes.byref(info))
                if res != JOYERR_NOERROR:
                    if self.rumble:
                        self.rumble.disconnect()
                    if self.no_reconnect:
                        print(f"\n{YELLOW}⚠️  Controller disconnected. Exiting (--no-reconnect).{RESET}")
                        break
                    print(f"\n{YELLOW}⚠️  Controller disconnected. Waiting for reconnect...{RESET}")
                    time.sleep(1)
                    dev_id = self.find_connected_controller()
                    if dev_id is not None and self.rumble:
                        self.rumble.connect()
                        self.setup_mapping_profile(dev_id)
                        self.print_mode_cheatsheet()
                    continue

                # Normalize stick axes: 0..65535, center = 32768
                norm_x = (info.dwXpos - 32768) / 32768.0
                norm_y = (info.dwYpos - 32768) / 32768.0

                # Check button state changes
                buttons = info.dwButtons
                pressed = buttons & ~self.last_buttons
                released = self.last_buttons & ~buttons
                now = time.time()

                if self.debug and pressed:
                    print(f"  [DEBUG] Buttons: 0x{buttons:04X} Pressed: 0x{pressed:04X} POV: {info.dwPOV}")

                # D-Pad POV direction & changes
                pov = info.dwPOV
                pov_dir = self.get_pov_direction(pov)
                pov_changed = (pov_dir != self.last_pov_direction)

                curr_mode = self.modes[self.current_mode_index]
                active_map = self.get_current_mode_map()

                # --- 1. Mouse Button Continuous Down/Up Handling ---
                if curr_mode == "DESKTOP MOUSE":
                    left_bits = [b for b, act in active_map.items() if act.get("action") == "mouse_btn" and act.get("code") == "left"]
                    right_bits = [b for b, act in active_map.items() if act.get("action") == "mouse_btn" and act.get("code") == "right"]
                    middle_bits = [b for b, act in active_map.items() if act.get("action") == "mouse_btn" and act.get("code") == "middle"]

                    # Also check Xbox trigger axis (LT / RT on dwZpos)
                    rt_axis_down = (self.device_profile == "dual_joycon" and hasattr(info, "dwZpos") and 0 < info.dwZpos < 16384)
                    lt_axis_down = (self.device_profile == "dual_joycon" and hasattr(info, "dwZpos") and info.dwZpos > 49152)

                    is_left_down = any(bool(buttons & (1 << b)) for b in left_bits) or rt_axis_down
                    is_right_down = any(bool(buttons & (1 << b)) for b in right_bits)
                    is_middle_down = any(bool(buttons & (1 << b)) for b in middle_bits) or lt_axis_down

                    if is_left_down:
                        self.mouse_down("left")
                    else:
                        self.mouse_up("left")

                    if is_right_down:
                        self.mouse_down("right")
                    else:
                        self.mouse_up("right")

                    if is_middle_down:
                        self.mouse_down("middle")
                    else:
                        self.mouse_up("middle")
                else:
                    if self.left_pressed:
                        self.mouse_up("left")
                    if self.right_pressed:
                        self.mouse_up("right")
                    if self.middle_pressed:
                        self.mouse_up("middle")

                # --- 2. Button Pressed Action Dispatch ---
                for bit in range(32):
                    if pressed & (1 << bit):
                        act = active_map.get(bit)
                        if not act:
                            continue
                        action_type = act.get("action")
                        desc = act.get("desc", "Action")

                        if action_type == "mouse_btn":
                            # Continuous state handled above
                            continue

                        elif action_type == "mode_cycle":
                            self.cycle_mode()

                        elif action_type == "smart_home":
                            self.smart_press_timestamp = now
                            self.smart_hold_triggered = False

                        elif action_type == "media_play_pause":
                            fg_app = get_foreground_window_title() or "System Default"
                            if self.is_browser_or_media_window():
                                self.send_key(VK_SPACE)
                                print(f"\n  {BOLD}{GREEN}▶/⏸ [Media]{RESET} Spacebar (Play/Pause) -> {fg_app}")
                            else:
                                self.send_key(VK_MEDIA_PLAY_PAUSE)
                                print(f"\n  {BOLD}{GREEN}▶/⏸ [Media]{RESET} Play/Pause -> {fg_app}")
                            if self.rumble:
                                self.rumble.tick()

                        elif action_type == "key":
                            vk = act.get("code")
                            self.send_key(vk)
                            print(f"\n  {BOLD}{CYAN}[Action]{RESET} {desc}")
                            if vk == VK_SNAPSHOT:
                                if self.rumble:
                                    self.rumble.screenshot()
                            elif self.rumble:
                                self.rumble.tick()

                        elif action_type == "combo":
                            keys = act.get("keys", [])
                            self.send_combo(keys)
                            print(f"\n  {BOLD}{CYAN}[Action]{RESET} {desc}")
                            if VK_C in keys and VK_CONTROL in keys:
                                if self.rumble:
                                    self.rumble.pulse(duration_ms=60, strong=0x7000, weak=0x7000)
                            elif self.rumble:
                                self.rumble.tick()

                        elif action_type == "scroll":
                            param = act.get("param", 1)
                            self.mouse_wheel(param)

                # --- 3. Smart Home Release & Hold Check ---
                for bit in range(32):
                    if released & (1 << bit):
                        act = active_map.get(bit)
                        if act and act.get("action") == "smart_home":
                            if self.smart_press_timestamp is not None and not self.smart_hold_triggered:
                                self.send_key(VK_LWIN)
                                print(f"\n  {BOLD}{CYAN}🏠 [Smart Button]{RESET} Tapped -> Super (Windows Key)")
                            self.smart_press_timestamp = None
                            self.smart_hold_triggered = False

                if self.smart_press_timestamp is not None and not self.smart_hold_triggered:
                    if (now - self.smart_press_timestamp) >= self.hold_threshold_sec:
                        self.send_key(VK_SNAPSHOT)
                        self.smart_hold_triggered = True
                        if self.rumble:
                            self.rumble.screenshot()
                        print(f"\n  {BOLD}{CYAN}📸 [Smart Button]{RESET} Held -> Instant Screenshot (PrintScreen)")

                # --- 4. D-Pad / POV Hat Actions ---
                if curr_mode == "DESKTOP MOUSE":
                    if pov_dir == "UP":
                        if now - self.last_scroll_time >= 0.07:
                            self.mouse_wheel(1)
                            self.last_scroll_time = now
                    elif pov_dir == "DOWN":
                        if now - self.last_scroll_time >= 0.07:
                            self.mouse_wheel(-1)
                            self.last_scroll_time = now
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_BROWSER_BACK)
                        print(f"\n  {BOLD}{CYAN}⬅️  [Nav]{RESET} Browser Back")
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_BROWSER_FORWARD)
                        print(f"\n  {BOLD}{CYAN}➡️  [Nav]{RESET} Browser Forward")

                elif curr_mode == "UNIVERSAL MEDIA REMOTE":
                    if pov_dir == "UP":
                        if now - self.last_vol_time >= 0.12:
                            self.send_key(VK_VOLUME_UP)
                            self.last_vol_time = now
                            if self.rumble:
                                self.rumble.tick()
                    elif pov_dir == "DOWN":
                        if now - self.last_vol_time >= 0.12:
                            self.send_key(VK_VOLUME_DOWN)
                            self.last_vol_time = now
                            if self.rumble:
                                self.rumble.tick()
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_MEDIA_PREV_TRACK)
                        print(f"\n  {BOLD}{CYAN}⏮ [Media]{RESET} Previous Track")
                        if self.rumble:
                            self.rumble.tick()
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_MEDIA_NEXT_TRACK)
                        print(f"\n  {BOLD}{CYAN}⏭ [Media]{RESET} Next Track")
                        if self.rumble:
                            self.rumble.tick()

                elif curr_mode == "INTERACTIVE TERMINAL":
                    if pov_dir == "UP" and pov_changed:
                        self.send_key(VK_UP)
                        print(f"\n  {BOLD}{CYAN}⬆️  [Terminal]{RESET} History Up")
                    elif pov_dir == "DOWN" and pov_changed:
                        self.send_key(VK_DOWN)
                        print(f"\n  {BOLD}{CYAN}⬇️  [Terminal]{RESET} History Down")
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_LEFT)
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_RIGHT)

                elif curr_mode == "PRESENTATION CLICKER":
                    if pov_dir == "UP" and pov_changed:
                        self.send_key(VK_PRIOR)
                        print(f"\n  {BOLD}{CYAN}⏮ [Slides]{RESET} First Slide / Page Up")
                    elif pov_dir == "DOWN" and pov_changed:
                        self.send_key(VK_NEXT)
                        print(f"\n  {BOLD}{CYAN}⏭ [Slides]{RESET} Last Slide / Page Down")
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_LEFT)
                        print(f"\n  {BOLD}{CYAN}◀️  [Slides]{RESET} Previous Slide")
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_RIGHT)
                        print(f"\n  {BOLD}{CYAN}▶️  [Slides]{RESET} Next Slide")

                # --- 5. Analog Stick Actions ---
                if curr_mode == "DESKTOP MOUSE":
                    mag = math.hypot(norm_x, norm_y)
                    if mag > self.deadzone:
                        eff_mag = min(1.0, (mag - self.deadzone) / (1.0 - self.deadzone))
                        speed = (eff_mag ** 1.6) * 16.0 * self.sensitivity
                        angle = math.atan2(norm_y, norm_x)
                        dx = math.cos(angle) * speed
                        dy = math.sin(angle) * speed
                        self.acc_x += dx
                        self.acc_y += dy
                        step_x = int(self.acc_x)
                        step_y = int(self.acc_y)
                        if step_x != 0 or step_y != 0:
                            self.acc_x -= step_x
                            self.acc_y -= step_y
                            self.move_mouse(step_x, step_y)
                    else:
                        self.acc_x = 0.0
                        self.acc_y = 0.0

                    # Right Stick continuous vertical scroll wheel
                    if hasattr(info, "dwRpos") and info.dwRpos > 0:
                        norm_r = (info.dwRpos - 32768) / 32768.0
                        if abs(norm_r) > self.deadzone:
                            eff_r = (abs(norm_r) - self.deadzone) / (1.0 - self.deadzone)
                            scroll_delta = -math.copysign(eff_r ** 1.5, norm_r) * 0.4
                            self.acc_scroll += scroll_delta
                            step_scroll = int(self.acc_scroll)
                            if step_scroll != 0:
                                self.acc_scroll -= step_scroll
                                self.mouse_wheel(step_scroll)
                        else:
                            self.acc_scroll = 0.0

                elif curr_mode == "UNIVERSAL MEDIA REMOTE":
                    self.acc_x = 0.0
                    self.acc_y = 0.0
                    fg_app = get_foreground_window_title() or "System Default"

                    # Analog Stick Media Seek (Parity with Linux enable_media_seek)
                    if norm_x > 0.55:
                        if now - self.last_seek_time >= 0.25:
                            self.send_key(VK_RIGHT)
                            print(f"\n  {BOLD}{CYAN}⏩ [Media Seek]{RESET} Forward (+5s) -> {fg_app}")
                            self.last_seek_time = now
                            if self.rumble:
                                self.rumble.tick()
                    elif norm_x < -0.55:
                        if now - self.last_seek_time >= 0.25:
                            self.send_key(VK_LEFT)
                            print(f"\n  {BOLD}{CYAN}⏪ [Media Seek]{RESET} Rewind (-5s) -> {fg_app}")
                            self.last_seek_time = now
                            if self.rumble:
                                self.rumble.tick()

                    # Vertical stick adjusts volume up/down
                    if norm_y < -0.65:
                        if now - self.last_vol_time >= 0.15:
                            self.send_key(VK_VOLUME_UP)
                            self.last_vol_time = now
                            if self.rumble:
                                self.rumble.tick()
                    elif norm_y > 0.65:
                        if now - self.last_vol_time >= 0.15:
                            self.send_key(VK_VOLUME_DOWN)
                            self.last_vol_time = now
                            if self.rumble:
                                self.rumble.tick()

                elif curr_mode == "INTERACTIVE TERMINAL":
                    self.acc_x = 0.0
                    self.acc_y = 0.0
                    # Vertical stick scrolls terminal history buffer
                    if abs(norm_y) > 0.40 and (now - self.last_scroll_time >= 0.08):
                        step = 1 if norm_y < 0 else -1
                        self.mouse_wheel(step)
                        self.last_scroll_time = now

                elif curr_mode == "PRESENTATION CLICKER":
                    self.acc_x = 0.0
                    self.acc_y = 0.0

                self.last_buttons = buttons
                self.last_pov = pov
                self.last_pov_direction = pov_dir
                time.sleep(0.008)  # ~125 Hz polling rate

        except KeyboardInterrupt:
            if self.left_pressed:
                self.mouse_up("left")
            if self.right_pressed:
                self.mouse_up("right")
            if self.middle_pressed:
                self.mouse_up("middle")
            print(f"\n{GREEN}Joy-Con Mouse for Windows stopped cleanly.{RESET}\n")


def list_controllers_windows() -> int:
    if not IS_WINDOWS or not winmm:
        print("\nDetected Controllers on Windows (WinMM):")
        print("  [Notice] WinMM controller scanning requires Windows OS.\n")
        return 0
    num_devs = winmm.joyGetNumDevs()
    info = JOYINFOEX()
    info.dwSize = ctypes.sizeof(JOYINFOEX)
    info.dwFlags = JOY_RETURNALL

    found = []
    for dev_id in range(num_devs):
        if winmm.joyGetPosEx(dev_id, ctypes.byref(info)) == JOYERR_NOERROR:
            caps = JOYCAPSW()
            if winmm.joyGetDevCapsW(dev_id, ctypes.byref(caps), ctypes.sizeof(JOYCAPSW)) == JOYERR_NOERROR:
                name = caps.szPname or f"Gamepad #{dev_id}"
                mid = f"0x{caps.wMid:04x}"
                pid = f"0x{caps.wPid:04x}"
                btns = caps.wNumButtons
                axes = caps.wNumAxes
            else:
                name = f"Gamepad #{dev_id}"
                mid, pid, btns, axes = "N/A", "N/A", 16, 6
            found.append((dev_id, name, mid, pid, btns, axes))

    print("\nDetected Controllers on Windows (WinMM):")
    if not found:
        print("  No compatible Joy-Cons or Gamepads detected.")
        print("  Ensure Bluetooth pairing or USB connection is established in Windows Settings.")
    else:
        for dev_id, name, mid, pid, btns, axes in found:
            print(f"  [{dev_id}] {BOLD}{name}{RESET} (MID: {mid}, PID: {pid}, Buttons: {btns}, Axes: {axes})")
    print()
    return 0


def list_modes_windows() -> int:
    modes_data = [
        ("1", "[ENABLED]", "Built-in", "DESKTOP MOUSE (Precision Stick Pointer)", "Left Stick cursor, scroll wheel, click & drag"),
        ("2", "[ENABLED]", "Built-in", "UNIVERSAL MEDIA REMOTE", "Controls YouTube, Spotify, VLC, Netflix, media players"),
        ("3", "[ENABLED]", "Built-in", "INTERACTIVE TERMINAL CONTROLLER", "Hands-free terminal: Enter, Backspace, Tab, History Up/Down, Esc"),
        ("4", "[ENABLED]", "Built-in", "PRESENTATION CLICKER", "Next/Previous slide, F5 slideshow start, Escape"),
    ]
    print("\n" + "=" * 80)
    print("  🎮 JOY-CON MOUSE MODULAR CONTROLLER MODES (Windows Edition)")
    print("=" * 80)
    print(f"  {'#':<4} {'STATUS':<10} {'TYPE':<10} {'MODE NAME':<34} {'FEATURES'}")
    print("-" * 80)
    for idx, status, type_str, name, desc in modes_data:
        print(f"  [{idx}]  {status:<10} {type_str:<10} {name:<34} {desc}")
    print("=" * 80 + "\n")
    return 0


def run_setup_wizard_windows():
    print("\n" + "=" * 70)
    print(f"  {BOLD}{PURPLE}🎮 JOY-CON MOUSE SETUP WIZARD (Windows Edition){RESET}")
    print("=" * 70)
    cfg_dir = get_config_dir()
    cfg_path = os.path.join(cfg_dir, "config.json")
    current_cfg = {}
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                current_cfg = json.load(f)
        except Exception:
            pass

    cur_sens = current_cfg.get("sensitivity", 1.0)
    cur_deadzone = current_cfg.get("deadzone", 0.10)

    print(f"\nCurrent pointer sensitivity: {BOLD}{cur_sens}x{RESET}")
    try:
        new_sens = input("Enter new sensitivity multiplier (or press Enter to keep): ").strip()
        if new_sens:
            current_cfg["sensitivity"] = float(new_sens)
    except (ValueError, EOFError, KeyboardInterrupt):
        pass

    print(f"\nCurrent analog deadzone: {BOLD}{cur_deadzone}{RESET}")
    try:
        new_dz = input("Enter new deadzone 0.0-0.5 (or press Enter to keep): ").strip()
        if new_dz:
            current_cfg["deadzone"] = float(new_dz)
    except (ValueError, EOFError, KeyboardInterrupt):
        pass

    cur_rumble = current_cfg.get("rumble_enabled", current_cfg.get("rumble", True))
    rumble_str = "Enabled" if cur_rumble else "Disabled"
    print(f"\nController Vibration & Haptics: {BOLD}{rumble_str}{RESET}")
    try:
        ans = input("Enable vibration haptics? [Y/n] (or press Enter to keep): ").strip().lower()
        if ans in ("y", "yes"):
            current_cfg["rumble_enabled"] = True
            current_cfg["rumble"] = True
        elif ans in ("n", "no"):
            current_cfg["rumble_enabled"] = False
            current_cfg["rumble"] = False
    except (EOFError, KeyboardInterrupt):
        pass

    try:
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(current_cfg, f, indent=2)
        print(f"\n{BOLD}{GREEN}✓ Settings saved to {cfg_path}{RESET}\n")
    except Exception as e:
        print(f"\n{YELLOW}Could not save settings: {e}{RESET}\n")


def test_rumble_windows() -> int:
    print("\n" + "=" * 70)
    print(f"  {BOLD}{PURPLE}📳 JOY-CON MOUSE HAPTIC VIBRATION DIAGNOSTIC (Windows Edition){RESET}")
    print("=" * 70)

    if not IS_WINDOWS:
        print(f"  {YELLOW}Notice: Controller vibration test requires Windows OS.{RESET}\n")
        return 0

    rumble = WindowsRumbleManager(enabled=True, debug=True)
    if not rumble.xinput:
        print(f"  {RED}❌ XInput vibration subsystem could not be initialized.{RESET}")
        print("     Ensure Windows Game Input or DirectX runtime is available.\n")
        return 1

    print(f"\n  {CYAN}Checking for connected controllers with vibration support...{RESET}")
    active_found = False
    vib_zero = XINPUT_VIBRATION(0, 0)
    for slot in range(4):
        try:
            res = rumble.xinput.XInputSetState(slot, ctypes.byref(vib_zero))
            if res == 0:
                print(f"  {GREEN}✓ Controller #{slot} is CONNECTED and ready for vibration!{RESET}")
                active_found = True
        except Exception:
            pass

    if not active_found:
        print(f"  {YELLOW}⚠️  No active XInput gamepad detected in slots 0-3.{RESET}")
        print("     Make sure your controller is paired and turned on.")
        print("     (Sending diagnostic vibration signals across all slots anyway...)\n")

    steps = [
        ("Left Heavy Motor (Low-Frequency Rumble)", 0xC000, 0x0000, 400),
        ("Right Light Motor (High-Frequency Haptic)", 0x0000, 0xC000, 400),
        ("Dual Motors (Full Power Burst)", 0xFFFF, 0xFFFF, 300),
        ("Mode Switch Haptic Click", 0x5000, 0x7000, 50),
        ("Camera Shutter Double-Pulse", 0x8000, 0x9000, 35),
    ]

    for label, strong, weak, dur in steps:
        print(f"  👉 Testing: {BOLD}{CYAN}{label}{RESET}... ", end="", flush=True)
        if label == "Camera Shutter Double-Pulse":
            rumble.screenshot()
            time.sleep(0.35)
        elif label == "Mode Switch Haptic Click":
            rumble.mode_switch()
            time.sleep(0.30)
        else:
            rumble.pulse(duration_ms=dur, strong=strong, weak=weak)
            time.sleep((dur / 1000.0) + 0.25)
        print(f"{BOLD}{GREEN}✓ Pulse sent!{RESET}")

    print("\n" + "=" * 70)
    print(f"  {BOLD}{GREEN}✅ Haptic vibration test sequence completed!{RESET}")
    print("=" * 70 + "\n")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Joy-Con Mouse & Universal Remote for Windows")
    parser.add_argument("-s", "--sensitivity", type=float, default=None, help="Pointer sensitivity multiplier (e.g. 1.2 or 0.8)")
    parser.add_argument("--deadzone", type=float, default=None, help="Analog stick deadzone threshold (default: 0.10)")
    parser.add_argument("--map", "--configure", action="store_true", help="Launch interactive button calibration wizard")
    parser.add_argument("--list-mappings", action="store_true", help="Display all saved controller button profiles")
    parser.add_argument("--check", action="store_true", help="Non-blocking device check (exits 0 if controller present, 1 otherwise)")
    parser.add_argument("--timeout", type=int, default=None, help="Maximum seconds to wait for controller before exiting")
    parser.add_argument("--test-buttons", action="store_true", help="Launch real-time interactive button and stick diagnostic tool")
    parser.add_argument("--test-rumble", action="store_true", help="Test controller physical haptic vibration and exit")
    parser.add_argument("--no-rumble", action="store_true", help="Disable physical haptic vibration feedback")
    parser.add_argument("--list", action="store_true", help="List detected WinMM gamepads and Joy-Cons")
    parser.add_argument("--list-modes", action="store_true", help="List all modular modes and features")
    parser.add_argument("--setup", action="store_true", help="Launch interactive setup wizard to configure sensitivity and deadzone")
    parser.add_argument("-v", "--verbose", "--debug", dest="debug", action="store_true", help="Print real-time debug events")
    parser.add_argument("--no-reconnect", action="store_true", help="Do not wait and auto-reconnect on disconnect")
    parser.add_argument("-V", "--version", action="version", version="Joy-Con Mouse for Windows v1.2.2")

    args = parser.parse_args()

    if args.test_rumble:
        return test_rumble_windows()

    if args.list_modes:
        return list_modes_windows()

    if args.list:
        return list_controllers_windows()

    if args.setup:
        run_setup_wizard_windows()
        return 0

    if args.test_buttons:
        try:
            import test_buttons
            return test_buttons.main()
        except ImportError:
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_buttons.py")
            if os.path.exists(script_path):
                import runpy
                runpy.run_path(script_path, run_name="__main__")
                return 0
            print(f"{RED}[Error] test_buttons.py not found.{RESET}")
            return 1

    if args.list_mappings:
        profiles = load_all_mappings()
        print(f"\n{BOLD}{PURPLE}🎮 Saved Controller Button Profiles ({get_mappings_path()}):{RESET}\n")
        for key, prof in profiles.items():
            print(f"  • {BOLD}{CYAN}{key}{RESET}:")
            for action, btn in prof.items():
                if action != "name":
                    print(f"      - {action:18}: Button {btn}")
        print()
        return 0

    if args.check:
        driver = WindowsJoyConDriver(timeout_sec=2)
        dev = driver.find_connected_controller()
        if dev is not None:
            name = driver.get_controller_name(dev)
            print(f"CONNECTED: Device #{dev} ({name})")
            return 0
        print("NO_CONTROLLER")
        return 1

    driver = WindowsJoyConDriver(
        force_map=args.map,
        timeout_sec=args.timeout,
        sensitivity=args.sensitivity,
        deadzone=args.deadzone,
        debug=args.debug,
        no_reconnect=args.no_reconnect,
        no_rumble=args.no_rumble
    )
    driver.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
