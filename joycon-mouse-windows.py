#!/usr/bin/env python3
"""
🎮 Joy-Con Mouse & Universal Remote for Windows (Beta Preview)
================================================================================
Zero-dependency, standalone Joy-Con & Gamepad desktop mouse driver for Windows 10/11.
Uses native Windows Multimedia (winmm.dll) and Win32 User32 via ctypes.
"""

import sys
import os
import time
import math
import json

# Check if running on Windows
IS_WINDOWS = sys.platform.startswith("win")

if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    winmm = ctypes.windll.winmm
    user32 = ctypes.windll.user32

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

    # Multimedia virtual keycodes
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_STOP = 0xB2
    VK_MEDIA_PLAY_PAUSE = 0xB3
    VK_RIGHT = 0x27
    VK_LEFT = 0x25
    VK_SPACE = 0x20
    VK_ESCAPE = 0x1B
    VK_F5 = 0x74
    VK_SNAPSHOT = 0x2C         # PrintScreen / Instant Screenshot
    VK_LWIN = 0x5B             # Left Windows / Start / Overview Key
else:
    class JOYINFOEX:
        pass
    winmm = None
    user32 = None

# ANSI Colors
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


class WindowsJoyConDriver:
    """Windows Joy-Con & Gamepad Mouse Driver using pure standard library ctypes."""

    def __init__(self):
        self.sensitivity = 1.0
        self.deadzone = 0.10
        self.current_mode_index = 0
        self.modes = ["DESKTOP MOUSE", "MEDIA REMOTE", "PRESENTATION CLICKER"]
        self.load_config()

        self.last_buttons = 0
        self.left_pressed = False
        self.right_pressed = False
        self.middle_pressed = False

    def load_config(self):
        config_path = os.path.expandvars(r"%APPDATA%\joycon-mouse\config.json") if IS_WINDOWS else "config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.sensitivity = float(cfg.get("sensitivity", 1.0))
                    self.deadzone = float(cfg.get("deadzone", 0.10))
            except Exception:
                pass

    def send_key(self, vk_code):
        if not IS_WINDOWS:
            return
        user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.02)
        user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

    def move_mouse(self, dx, dy):
        if not IS_WINDOWS:
            return
        user32.mouse_event(MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)

    def mouse_down(self, button):
        if not IS_WINDOWS:
            return
        if button == "left" and not self.left_pressed:
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            self.left_pressed = True
        elif button == "right" and not self.right_pressed:
            user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            self.right_pressed = True
        elif button == "middle" and not self.middle_pressed:
            user32.mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            self.middle_pressed = True

    def mouse_up(self, button):
        if not IS_WINDOWS:
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
        if not IS_WINDOWS:
            return
        user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, int(delta * 120), 0)

    def cycle_mode(self):
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        mode = self.modes[self.current_mode_index]
        print(f"\n{BOLD}{PURPLE}🔄 Switched Mode:{RESET} {BOLD}{GREEN}[{mode}]{RESET}")

    def find_connected_controller(self):
        if not IS_WINDOWS:
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

    def run(self):
        print(f"\n================================================================================")
        print(f"  {BOLD}{PURPLE}🎮 JOY-CON MOUSE FOR WINDOWS (Beta Preview){RESET}")
        print(f"  {DIM}Zero external dependencies (Native WinMM & Win32 User32){RESET}")
        print(f"================================================================================\n")
        print(f"  {CYAN}Sensitivity:{RESET} {self.sensitivity}x | {CYAN}Deadzone:{RESET} {self.deadzone}")
        print(f"  {CYAN}Active Mode:{RESET} {BOLD}{GREEN}[{self.modes[self.current_mode_index]}]{RESET}\n")

        if not IS_WINDOWS:
            print(f"{YELLOW}Notice: joycon-mouse-windows.py is designed for Windows 10/11.{RESET}")
            print("This preview script will compile and run on Windows machines with zero pip dependencies.\n")
            return

        print(f"🔍 Searching for paired Joy-Cons or Gamepads...")
        dev_id = self.find_connected_controller()

        while dev_id is None:
            print(f"  {YELLOW}No controller detected.{RESET} Please ensure your Joy-Con is paired in Windows Bluetooth settings.")
            print(f"  Retrying in 2 seconds (Press Ctrl+C to stop)...")
            time.sleep(2)
            dev_id = self.find_connected_controller()

        print(f"\n  {GREEN}✓ Connected to Gamepad Device #{dev_id}!{RESET}")
        print(f"  {DIM}Move the analog stick to guide cursor. Press Home/Capture or Button 8 to cycle modes.{RESET}\n")

        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(JOYINFOEX)
        info.dwFlags = JOY_RETURNALL

        try:
            while True:
                res = winmm.joyGetPosEx(dev_id, ctypes.byref(info))
                if res != JOYERR_NOERROR:
                    print(f"\n{YELLOW}⚠️  Controller disconnected. Waiting for reconnect...{RESET}")
                    time.sleep(1)
                    dev_id = self.find_connected_controller()
                    continue

                # Normalize stick axes: 0..65535, center = 32768
                norm_x = (info.dwXpos - 32768) / 32768.0
                norm_y = (info.dwYpos - 32768) / 32768.0

                mag = math.hypot(norm_x, norm_y)
                if mag > self.deadzone:
                    eff_mag = min(1.0, (mag - self.deadzone) / (1.0 - self.deadzone))
                    speed = (eff_mag ** 1.6) * 16.0 * self.sensitivity
                    angle = math.atan2(norm_y, norm_x)
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    self.move_mouse(dx, dy)

                # Check button state changes
                buttons = info.dwButtons
                pressed = buttons & ~self.last_buttons

                # Mode cycling button (Button 8 or 9: usually Plus / Minus or Start)
                if pressed & (1 << 8) or pressed & (1 << 9):
                    self.cycle_mode()

                # Dedicated Screenshot Button (Button 13 / Share / Capture)
                if pressed & (1 << 13):
                    self.send_key(VK_SNAPSHOT)
                    print(f"  {BOLD}{CYAN}📸 [Screenshot]{RESET} Instant PrintScreen triggered")

                # Dedicated Home / Guide Button (Button 12 / Guide / Home / Xbox)
                if pressed & (1 << 12):
                    self.send_key(VK_LWIN)

                curr_mode = self.modes[self.current_mode_index]

                if curr_mode == "DESKTOP MOUSE":
                    # Button 0 (A or ZR): Left Click
                    if buttons & (1 << 0):
                        self.mouse_down("left")
                    else:
                        self.mouse_up("left")

                    # Button 1 (B or R): Right Click
                    if buttons & (1 << 1):
                        self.mouse_down("right")
                    else:
                        self.mouse_up("right")

                    # Button 2 (X): Middle Click
                    if buttons & (1 << 2):
                        self.mouse_down("middle")
                    else:
                        self.mouse_up("middle")

                elif curr_mode == "MEDIA REMOTE":
                    # Button 0: Play/Pause
                    if pressed & (1 << 0):
                        self.send_key(VK_MEDIA_PLAY_PAUSE)
                    # Button 1: Volume Down
                    if pressed & (1 << 1):
                        self.send_key(VK_VOLUME_DOWN)
                    # Button 2: Volume Up
                    if pressed & (1 << 2):
                        self.send_key(VK_VOLUME_UP)
                    # Button 3: Next Track
                    if pressed & (1 << 3):
                        self.send_key(VK_MEDIA_NEXT_TRACK)

                elif curr_mode == "PRESENTATION CLICKER":
                    # Button 0: Next Slide (Right Arrow)
                    if pressed & (1 << 0):
                        self.send_key(VK_RIGHT)
                    # Button 1: Previous Slide (Left Arrow)
                    if pressed & (1 << 1):
                        self.send_key(VK_LEFT)
                    # Button 2: Start Slideshow (F5)
                    if pressed & (1 << 2):
                        self.send_key(VK_F5)
                    # Button 3: Exit (Escape)
                    if pressed & (1 << 3):
                        self.send_key(VK_ESCAPE)

                self.last_buttons = buttons
                time.sleep(0.008)  # ~125 Hz polling rate

        except KeyboardInterrupt:
            print(f"\n{GREEN}Joy-Con Mouse for Windows stopped cleanly.{RESET}\n")


if __name__ == "__main__":
    driver = WindowsJoyConDriver()
    driver.run()
