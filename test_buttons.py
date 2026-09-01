#!/usr/bin/env python3
"""
Interactive Controller & Button Diagnostic Tool for Joy-Con & Gamepads.
Location: test_buttons.py
"""

import fcntl
import glob
import os
import select
import struct
import sys
import time
from typing import Dict, List, Optional, Tuple

from modes import load_all_modes
from modes.base import BaseMode

# Linux Input Event Types
EVENT_SYN = 0x00
EVENT_KEY = 0x01
EVENT_REL = 0x02
EVENT_ABS = 0x03

IS_64_BIT = struct.calcsize("P") == 8
EVENT_STRUCT_FORMAT = "llHHi" if IS_64_BIT else "iiHHi"
EVENT_STRUCT_SIZE = struct.calcsize(EVENT_STRUCT_FORMAT)

BUTTON_NAMES: Dict[int, str] = {
    304: "B (Down / A)",
    305: "A (Right / B)",
    307: "X (Up / Y)",
    308: "Y (Left / X)",
    309: "Capture",
    310: "L / Left Bumper (or Side SL on Right Joy-Con)",
    311: "R / Right Bumper (or Side SL on Left Joy-Con)",
    312: "ZL / Left Trigger (or Side SR on Right Joy-Con)",
    313: "ZR / Right Trigger (or Side SR on Left Joy-Con)",
    314: "Minus (-)",
    315: "Plus (+)",
    316: "Home",
    317: "Stick Click (L3)",
    318: "Stick Click (R3)",
    544: "D-Pad Up",
    545: "D-Pad Down",
    546: "D-Pad Left",
    547: "D-Pad Right",
    256: "Generic Btn 0 (Side SL fallback)",
    257: "Generic Btn 1 (Side SR fallback)",
    294: "Base Btn 0 (Side SL fallback)",
    295: "Base Btn 1 (Side SR fallback)",
    296: "Base Btn 2 (Side SL fallback)",
    297: "Base Btn 3 (Side SR fallback)",
}

AXIS_NAMES: Dict[int, str] = {
    0x00: "Stick X (Horizontal)",
    0x01: "Stick Y (Vertical)",
    0x02: "Z / Left Trigger Axis",
    0x03: "Right Stick X / Gyro Pitch",
    0x04: "Right Stick Y / Gyro Roll",
    0x05: "Right Stick Z / Gyro Yaw",
    0x10: "D-Pad X (Hat0X)",
    0x11: "D-Pad Y (Hat0Y)",
}


def eviocgname(length: int = 256) -> int:
    return (2 << 30) | (length << 16) | (ord("E") << 8) | 0x06


def classify_name(name: str) -> str:
    n = name.lower()
    if "right joy-con" in n or "joy-con (r)" in n:
        return "right_joycon"
    elif "left joy-con" in n or "joy-con (l)" in n:
        return "left_joycon"
    elif "combined joy-con" in n or "joy-con (l/r)" in n:
        return "dual_joycon"
    elif "pro controller" in n or "switch pro" in n:
        return "switch_pro"
    elif any(x in n for x in ["dualsense", "dualshock", "playstation", "sony"]):
        return "playstation"
    elif any(x in n for x in ["xbox", "x-box", "microsoft"]):
        return "xbox"
    return "generic_gamepad"


def find_controllers() -> List[Tuple[str, str, str]]:
    controllers = []
    for path in sorted(glob.glob("/dev/input/event*"), key=lambda p: int(p.replace("/dev/input/event", "") or "0") if p.replace("/dev/input/event", "").isdigit() else 0):
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
            buf = bytearray(256)
            fcntl.ioctl(fd, eviocgname(256), buf)
            name = buf.split(b"\x00", 1)[0].decode("utf-8", errors="ignore").strip()
            os.close(fd)
            n_lower = name.lower()
            if "virtual" in n_lower or "uinput" in n_lower or "imu" in n_lower:
                continue
            if any(k in n_lower for k in ["joy-con", "controller", "gamepad", "joystick", "xbox", "dualsense", "dualshock"]):
                controllers.append((path, name, classify_name(name)))
        except OSError:
            continue
    return controllers


def render_axis_bar(val: int, max_val: int = 32767, width: int = 20) -> str:
    pct = max(-1.0, min(1.0, val / float(max_val)))
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
    return f"[{pct*100:+6.1f}%] [" + "".join(bar) + "]"


def main() -> int:
    print("=" * 70)
    print("   🎮 JOY-CON & GAMEPAD REAL-TIME BUTTON & AXIS DIAGNOSTIC TOOL")
    print("=" * 70)

    devices = find_controllers()
    if not devices:
        print("[Error] No compatible Joy-Cons or Gamepads found in /dev/input/event*.")
        print("Ensure Bluetooth pairing or USB connection is established.")
        return 1

    print("Discovered Controllers:")
    for idx, (path, name, dev_type) in enumerate(devices, 1):
        print(f"  [{idx}] {name} ({dev_type}) -> {path}")
    print("-" * 70)

    chosen_idx = 0
    if len(devices) > 1:
        try:
            choice = input(f"Select controller to test [1-{len(devices)}] (Default 1): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(devices):
                chosen_idx = int(choice) - 1
        except (EOFError, KeyboardInterrupt):
            return 0

    path, name, dev_type = devices[chosen_idx]
    print(f"\n-> Testing {name} on {path}")
    print("-> Press any button or move analog sticks (Press Ctrl+C to exit)\n")

    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except PermissionError:
        print(f"[Error] Permission denied opening {path}. Run with sudo or add user to input group.")
        return 1
    except OSError as e:
        print(f"[Error] Failed to open {path}: {e}")
        return 1

    modes = load_all_modes()
    poll_obj = select.poll()
    poll_obj.register(fd, select.POLLIN)

    last_axis_time: Dict[int, float] = {}

    try:
        while True:
            events = poll_obj.poll(100)
            if not events:
                continue

            for descriptor, mask in events:
                if mask & select.POLLIN:
                    try:
                        raw = os.read(descriptor, EVENT_STRUCT_SIZE * 32)
                    except OSError:
                        print("\nController disconnected.")
                        return 0

                    count = len(raw) // EVENT_STRUCT_SIZE
                    for i in range(count):
                        chunk = raw[i * EVENT_STRUCT_SIZE : (i + 1) * EVENT_STRUCT_SIZE]
                        _, _, etype, code, val = struct.unpack(EVENT_STRUCT_FORMAT, chunk)

                        if etype == EVENT_KEY:
                            state_str = "🔘 PRESSED " if val == 1 else ("⚪ RELEASED" if val == 0 else f"🔁 REPEAT({val})")
                            btn_name = BUTTON_NAMES.get(code, f"Unknown Button ({code})")
                            
                            print(f"[{time.strftime("%H:%M:%S")}] {state_str} | Code: {code:3d} (0x{code:03x}) | Name: {btn_name}")

                            # Display actions across loaded modes when pressed
                            if val == 1 and modes:
                                print("   Mapped Actions:")
                                for m in modes:
                                    b_map = m.get_button_map(dev_type)
                                    action = b_map.get(code)
                                    if action:
                                        print(f"     * [{m.name}]: {action.get("desc", "Action: " + str(action))}")
                                    else:
                                        print(f"     * [{m.name}]: (Unmapped)")
                                print()

                        elif etype == EVENT_ABS:
                            now = time.time()
                            # Rate limit axis printing to avoid terminal flooding
                            if (now - last_axis_time.get(code, 0.0)) > 0.08:
                                last_axis_time[code] = now
                                ax_name = AXIS_NAMES.get(code, f"Axis {code}")
                                gauge = render_axis_bar(val)
                                print(f"[{time.strftime("%H:%M:%S")}] 🕹️  AXIS {code:2d} ({ax_name:24s}) | Raw: {val:+6d} {gauge}")

    except KeyboardInterrupt:
        print("\nDiagnostic tool exited cleanly.")
    finally:
        try:
            os.close(fd)
        except OSError:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
