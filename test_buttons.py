#!/usr/bin/env python3
"""
🎮 Joy-Con & Gamepad Real-Time Button & Axis Diagnostic Tool for Windows
================================================================================
Pure Python Standard Library (ctypes + winmm.dll). Zero pip dependencies.
Diagnostic visualizer for buttons, analog sticks, and D-pad POV hats on Windows 10/11.
"""

import ctypes
from ctypes import wintypes
import os
import sys
import time
import math
from typing import Dict, List, Optional, Tuple

# Ensure Windows terminal can print Unicode / UTF-8 without crashing on cp1252
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

IS_WINDOWS = sys.platform.startswith("win")
winmm = ctypes.windll.winmm if IS_WINDOWS else None

# --- XInput Haptic Vibration for Button Testing ---
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [
        ("wLeftMotorSpeed", wintypes.WORD),
        ("wRightMotorSpeed", wintypes.WORD),
    ]

xinput_dll = None
if IS_WINDOWS:
    for dll in ["xinput1_4.dll", "xinput1_3.dll", "xinput9_1_0.dll"]:
        try:
            xinput_dll = ctypes.windll.LoadLibrary(dll)
            if xinput_dll and hasattr(xinput_dll, "XInputSetState"):
                xinput_dll.XInputSetState.argtypes = [wintypes.DWORD, ctypes.POINTER(XINPUT_VIBRATION)]
                xinput_dll.XInputSetState.restype = wintypes.DWORD
                break
        except Exception:
            continue

def trigger_button_haptic(duration_ms: int = 35, strong: int = 0x5000, weak: int = 0x6000):
    if not xinput_dll:
        return
    import threading
    def _worker():
        vib_on = XINPUT_VIBRATION(max(0, min(65535, strong)), max(0, min(65535, weak)))
        vib_off = XINPUT_VIBRATION(0, 0)
        active = []
        for s in range(4):
            try:
                if xinput_dll.XInputSetState(s, ctypes.byref(vib_on)) == 0:
                    active.append(s)
            except Exception:
                pass
        time.sleep(max(0.01, duration_ms / 1000.0))
        for s in active:
            try:
                xinput_dll.XInputSetState(s, ctypes.byref(vib_off))
            except Exception:
                pass
    threading.Thread(target=_worker, daemon=True).start()

# --- WinMM Structures & Constants ---
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
        ("wXmin", wintypes.UINT), ("wXmax", wintypes.UINT),
        ("wYmin", wintypes.UINT), ("wYmax", wintypes.UINT),
        ("wZmin", wintypes.UINT), ("wZmax", wintypes.UINT),
        ("wNumButtons", wintypes.UINT),
        ("wPeriodMin", wintypes.UINT), ("wPeriodMax", wintypes.UINT),
        ("wRmin", wintypes.UINT), ("wRmax", wintypes.UINT),
        ("wUmin", wintypes.UINT), ("wUmax", wintypes.UINT),
        ("wVmin", wintypes.UINT), ("wVmax", wintypes.UINT),
        ("wCaps", wintypes.UINT),
        ("wMaxAxes", wintypes.UINT),
        ("wNumAxes", wintypes.UINT),
        ("wMaxButtons", wintypes.UINT),
        ("szRegKey", wintypes.WCHAR * 32),
        ("szOEMVxD", wintypes.WCHAR * 260),
    ]

JOY_RETURNALL = 0x000000FF
JOYERR_NOERROR = 0
JOY_POVCENTERED = 65535

# ANSI Colors
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"

# Common Joy-Con & Gamepad button aliases in WinMM
WINMM_BUTTON_NAMES: Dict[int, str] = {
    0: "Button 0  (A / Cross / ZR)",
    1: "Button 1  (B / Circle / R)",
    2: "Button 2  (X / Square)",
    3: "Button 3  (Y / Triangle)",
    4: "Button 4  (L / LB / Left Bumper / SL)",
    5: "Button 5  (R / RB / Right Bumper / SR)",
    6: "Button 6  (ZL / LT / Left Trigger)",
    7: "Button 7  (ZR / RT / Right Trigger)",
    8: "Button 8  (Minus / Select / Share)",
    9: "Button 9  (Plus / Start / Options)",
    10: "Button 10 (L3 / Left Stick Click)",
    11: "Button 11 (R3 / Right Stick Click)",
    12: "Button 12 (Home / PS / Guide / Xbox)",
    13: "Button 13 (Capture / Share / Touchpad Click)",
    14: "Button 14 (Generic Btn 14)",
    15: "Button 15 (Generic Btn 15)",
}

POV_DIRECTIONS: Dict[int, str] = {
    0: "⬆️  UP",
    4500: "↗️  UP-RIGHT",
    9000: "➡️  RIGHT",
    13500: "↘️  DOWN-RIGHT",
    18000: "⬇️  DOWN",
    22500: "↙️  DOWN-LEFT",
    27000: "⬅️  LEFT",
    31500: "↖️  UP-LEFT",
}

# Mode action descriptions for WinMM button scancodes
MODE_BUTTON_ACTIONS = {
    "DESKTOP MOUSE": {
        0: "Left Click (Down/Up)",
        1: "Right Click (Down/Up)",
        2: "Middle Click (Down/Up)",
        8: "Cycle Mode",
        9: "Cycle Mode",
        12: "Windows Key / Start Menu",
        13: "Screenshot (PrintScreen)",
    },
    "MEDIA REMOTE": {
        0: "Play / Pause",
        1: "Volume Down",
        2: "Volume Up",
        3: "Next Track",
        8: "Cycle Mode",
        9: "Cycle Mode",
        12: "Windows Key / Start Menu",
        13: "Screenshot (PrintScreen)",
    },
    "TERMINAL CONTROLLER": {
        0: "Enter / Submit",
        1: "Backspace / Cancel",
        2: "History Up (Previous Command)",
        3: "History Down (Next Command)",
        4: "Escape",
        5: "Ctrl+C (Interrupt)",
        8: "Cycle Mode",
        9: "Cycle Mode",
        10: "Ctrl+L (Clear Screen)",
        11: "Ctrl+D (EOF / Exit)",
        12: "Windows Key / Start Menu",
        13: "Screenshot (PrintScreen)",
    },
    "PRESENTATION CLICKER": {
        0: "Next Slide (Right Arrow)",
        1: "Previous Slide (Left Arrow)",
        2: "Start Slideshow (F5)",
        3: "Exit Slideshow (Escape)",
        8: "Cycle Mode",
        9: "Cycle Mode",
        12: "Windows Key / Start Menu",
        13: "Screenshot (PrintScreen)",
    },
}


def render_axis_bar(val: int, center: int = 32768, span: int = 32768, width: int = 20) -> str:
    """Renders a bi-directional visual gauge bar for an analog axis."""
    pct = max(-1.0, min(1.0, (val - center) / float(span)))
    half = width // 2
    pos = int(round(pct * half))
    bar = [" "] * width
    bar[half] = "|"
    if pos > 0:
        for i in range(half + 1, min(width, half + 1 + pos)):
            bar[i] = "="
    elif pos < 0:
        for i in range(max(0, half + pos), half):
            bar[i] = "="
    return f"[{pct * 100:+6.1f}%] [" + "".join(bar) + f"] (raw: {val:5d})"


def find_controllers() -> List[Tuple[int, str, JOYCAPSW]]:
    """Discovers all currently active WinMM joystick devices."""
    controllers = []
    num_devs = winmm.joyGetNumDevs()
    info = JOYINFOEX()
    info.dwSize = ctypes.sizeof(JOYINFOEX)
    info.dwFlags = JOY_RETURNALL

    for dev_id in range(num_devs):
        if winmm.joyGetPosEx(dev_id, ctypes.byref(info)) == JOYERR_NOERROR:
            caps = JOYCAPSW()
            if winmm.joyGetDevCapsW(dev_id, ctypes.byref(caps), ctypes.sizeof(JOYCAPSW)) == JOYERR_NOERROR:
                name = caps.szPname or f"Gamepad #{dev_id}"
            else:
                name = f"Gamepad #{dev_id}"
            controllers.append((dev_id, name, caps))
    return controllers


def main() -> int:
    print(f"\n================================================================================")
    print(f"  {BOLD}{PURPLE}🎮 JOY-CON & GAMEPAD REAL-TIME DIAGNOSTIC TOOL (Windows){RESET}")
    print(f"  {DIM}Zero-bloat diagnostic visualizer (Native WinMM & Win32 User32){RESET}")
    print(f"================================================================================\n")

    if not IS_WINDOWS:
        print(f"  {YELLOW}Note: test_buttons.py (Windows Edition) is designed for Windows 10/11.{RESET}")
        print("  On Linux, run: python3 joycon-mouse.py --test-buttons\n")
        return 0

    devices = find_controllers()
    if not devices:
        print(f"{RED}[Error] No compatible Joy-Cons or Gamepads found on Windows.{RESET}")
        print("Please pair your Joy-Con in Windows Settings > Bluetooth & devices, then retry.")
        return 1

    print(f"{CYAN}Discovered Controllers on Windows:{RESET}")
    for dev_id, name, caps in devices:
        mid_str = f"0x{caps.wMid:04x}" if caps else "N/A"
        pid_str = f"0x{caps.wPid:04x}" if caps else "N/A"
        btns = caps.wNumButtons if caps else 16
        axes = caps.wNumAxes if caps else 6
        print(f"  [{dev_id}] {BOLD}{name}{RESET} (MID: {mid_str}, PID: {pid_str}, Buttons: {btns}, Axes: {axes})")
    print("-" * 80)

    chosen_id = devices[0][0]
    if len(devices) > 1:
        try:
            choice = input(f"Select controller ID to test [{devices[0][0]}-{devices[-1][0]}] (Default {devices[0][0]}): ").strip()
            if choice.isdigit() and any(d[0] == int(choice) for d in devices):
                chosen_id = int(choice)
        except (EOFError, KeyboardInterrupt):
            return 0

    chosen_dev = next(d for d in devices if d[0] == chosen_id)
    print(f"\n-> {GREEN}Testing Controller [{chosen_id}]: {chosen_dev[1]}{RESET}")
    print(f"-> Press buttons, move sticks, or press D-Pad. {YELLOW}(Press Ctrl+C to exit){RESET}\n")

    info = JOYINFOEX()
    info.dwSize = ctypes.sizeof(JOYINFOEX)
    info.dwFlags = JOY_RETURNALL

    last_buttons = 0
    last_pov = JOY_POVCENTERED
    last_axis_time: Dict[str, float] = {}
    last_axis_vals: Dict[str, int] = {}

    try:
        while True:
            res = winmm.joyGetPosEx(chosen_id, ctypes.byref(info))
            if res != JOYERR_NOERROR:
                trigger_button_haptic(duration_ms=150, strong=0x8000, weak=0x4000)
                print(f"\n{YELLOW}⚠️  Controller disconnected or sleeping. Waiting for reconnection...{RESET}")
                time.sleep(1)
                devices = find_controllers()
                if any(d[0] == chosen_id for d in devices):
                    trigger_button_haptic(duration_ms=80, strong=0x6000, weak=0x8000)
                    print(f"{GREEN}✓ Reconnected to Controller #{chosen_id}!{RESET}")
                continue

            # --- 1. Button Detection ---
            buttons = info.dwButtons
            if buttons != last_buttons:
                changed = buttons ^ last_buttons
                for bit in range(16):
                    if changed & (1 << bit):
                        is_pressed = bool(buttons & (1 << bit))
                        state_str = f"{BOLD}{GREEN}🔘 PRESSED {RESET}" if is_pressed else f"{DIM}⚪ RELEASED{RESET}"
                        btn_name = WINMM_BUTTON_NAMES.get(bit, f"Button {bit}")
                        hex_val = f"0x{(1 << bit):04X}"
                        t_stamp = time.strftime("%H:%M:%S")

                        print(f"[{t_stamp}] {state_str} | Bit: {bit:2d} ({hex_val}) | {btn_name}")

                        # Show mapped mode actions when pressed & trigger tactile haptic click
                        if is_pressed:
                            trigger_button_haptic(duration_ms=30, strong=0x4000, weak=0x5000)
                            print("   Mapped Actions Across Modes:")
                            for mode_name, actions in MODE_BUTTON_ACTIONS.items():
                                action = actions.get(bit, "(Unmapped)")
                                print(f"     * [{mode_name}]: {action}")
                            print()
                last_buttons = buttons

            # --- 2. D-Pad / POV Hat Detection ---
            pov = info.dwPOV
            if pov != last_pov:
                t_stamp = time.strftime("%H:%M:%S")
                if pov == JOY_POVCENTERED:
                    print(f"[{t_stamp}] 🧭 D-Pad Hat: {DIM}Centered / Released{RESET}")
                else:
                    dir_name = POV_DIRECTIONS.get(pov, f"Angle {pov / 100:.1f}°")
                    print(f"[{t_stamp}] 🧭 D-Pad Hat: {BOLD}{CYAN}{dir_name}{RESET} (raw: {pov})")
                last_pov = pov

            # --- 3. Analog Sticks & Axes Detection ---
            now = time.time()
            axes_to_check = [
                ("Left Stick X ", info.dwXpos),
                ("Left Stick Y ", info.dwYpos),
                ("Right Stick X", info.dwZpos),
                ("Right Stick Y", info.dwRpos),
                ("Axis U (Aux) ", info.dwUpos),
                ("Axis V (Aux) ", info.dwVpos),
            ]

            for ax_name, raw_val in axes_to_check:
                prev_val = last_axis_vals.get(ax_name, 32768)
                # If changed by more than deadzone noise (approx 2000 units)
                if abs(raw_val - prev_val) > 2000:
                    if (now - last_axis_time.get(ax_name, 0.0)) > 0.12:
                        last_axis_time[ax_name] = now
                        last_axis_vals[ax_name] = raw_val
                        gauge = render_axis_bar(raw_val)
                        t_stamp = time.strftime("%H:%M:%S")
                        print(f"[{t_stamp}] 🕹️  {ax_name:14s} | {gauge}")

            time.sleep(0.008)  # ~125 Hz polling

    except KeyboardInterrupt:
        print(f"\n{GREEN}Diagnostic tool stopped cleanly.{RESET}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
