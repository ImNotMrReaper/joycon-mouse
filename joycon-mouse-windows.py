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
from typing import Dict, Any, Optional

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
    VK_RETURN = 0x0D           # Enter / Submit
    VK_BACK = 0x08             # Backspace
    VK_TAB = 0x09              # Tab Auto-Complete
    VK_UP = 0x26               # Arrow Up (History Up)
    VK_DOWN = 0x28             # Arrow Down (History Down)
    VK_CONTROL = 0x11          # Left Ctrl
    VK_C = 0x43                # C key
    VK_T = 0x54                # T key
    VK_W = 0x57                # W key
    VK_R = 0x52                # R key
    VK_BROWSER_BACK = 0xA6     # Browser Back
    VK_BROWSER_FORWARD = 0xA7  # Browser Forward
else:
    class JOYINFOEX:
        pass

    class JOYCAPSW:
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

DEFAULT_MAPPINGS = {
    "default": {
        "name": "Standard Gamepad / Joy-Con (R)",
        "left_click": 0,
        "right_click": 1,
        "middle_click": 2,
        "trackpad_click": 13,
        "cycle_mode": 9,
        "cycle_mode_alt": 8,
        "screenshot": 13,
        "home": 12,
        "media_play_pause": 0,
        "media_vol_down": 1,
        "media_vol_up": 2,
        "media_next_track": 3,
        "terminal_enter": 0,
        "terminal_backspace": 1,
        "terminal_tab": 2,
        "terminal_esc": 3,
        "slide_next": 0,
        "slide_prev": 1,
        "slide_f5": 2,
        "slide_esc": 3
    },
    "joycon_l": {
        "name": "Nintendo Joy-Con (L)",
        "left_click": 2,
        "right_click": 1,
        "middle_click": 0,
        "trackpad_click": 13,
        "cycle_mode": 8,
        "cycle_mode_alt": 9,
        "screenshot": 13,
        "home": 12,
        "media_play_pause": 2,
        "media_vol_down": 1,
        "media_vol_up": 3,
        "media_next_track": 0,
        "terminal_enter": 2,
        "terminal_backspace": 1,
        "terminal_tab": 0,
        "terminal_esc": 3,
        "slide_next": 1,
        "slide_prev": 2,
        "slide_f5": 3,
        "slide_esc": 0
    },
    "playstation": {
        "name": "Sony PlayStation (DualSense / DualShock 4)",
        "left_click": 0,           # Square / Cross
        "right_click": 1,          # Circle / Cross
        "middle_click": 2,         # Triangle
        "trackpad_click": 13,      # DualSense physical mechanical trackpad click!
        "cycle_mode": 9,           # Options
        "cycle_mode_alt": 8,       # Share / Create
        "screenshot": 8,           # Share / Create (Instant Screenshot)
        "home": 12,                # PS Guide Button
        "media_play_pause": 0,     # Primary action
        "media_vol_down": 4,       # L1
        "media_vol_up": 5,         # R1
        "media_next_track": 1,     # Next Track
        "terminal_enter": 0,       # Enter / Submit
        "terminal_backspace": 1,   # Backspace
        "terminal_tab": 4,         # L1 / Tab Auto-Complete
        "terminal_esc": 8,         # Share / Escape
        "slide_next": 0,
        "slide_prev": 1,
        "slide_f5": 2,
        "slide_esc": 3
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


class WindowsJoyConDriver:
    """Windows Joy-Con & Gamepad Mouse Driver using pure standard library ctypes."""

    def __init__(self, force_map: bool = False, timeout_sec: Optional[int] = None):
        self.sensitivity = 1.0
        self.deadzone = 0.10
        self.current_mode_index = 0
        self.modes = ["DESKTOP MOUSE", "MEDIA REMOTE", "INTERACTIVE TERMINAL", "PRESENTATION CLICKER"]
        self.force_map = force_map
        self.timeout_sec = timeout_sec

        self.last_buttons = 0
        self.last_pov = 65535
        self.last_pov_direction = "CENTER"
        self.last_scroll_time = 0.0
        self.left_pressed = False
        self.right_pressed = False
        self.middle_pressed = False

        self.controller_name = "Unknown Controller"
        self.active_mapping = dict(DEFAULT_MAPPINGS["default"])
        self.load_config()

    def load_config(self):
        config_path = os.path.join(get_config_dir(), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.sensitivity = float(cfg.get("sensitivity", 1.0))
                    self.deadzone = float(cfg.get("deadzone", 0.10))
            except Exception:
                pass

    def send_key(self, vk_code):
        if not IS_WINDOWS or not user32:
            return
        user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.02)
        user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

    def send_combo(self, keys):
        if not IS_WINDOWS or not user32:
            return
        for k in keys:
            user32.keybd_event(k, 0, KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.02)
        for k in reversed(keys):
            user32.keybd_event(k, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

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
            print(f"\r  {BOLD}{BLUE}[Click]{RESET} RIGHT DOWN        ", end="", flush=True)
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

    def cycle_mode(self):
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        mode = self.modes[self.current_mode_index]
        print(f"\n{BOLD}{PURPLE}🔄 Switched Mode:{RESET} {BOLD}{GREEN}[{mode}]{RESET}")

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

        if self.force_map:
            self.active_mapping = self.run_mapping_wizard(dev_id, self.controller_name)
            return

        # Check if saved profile exists
        if self.controller_name in all_profiles:
            self.active_mapping = all_profiles[self.controller_name]
            print(f"  {BOLD}{GREEN}✓ Loaded saved button mapping for:{RESET} '{self.controller_name}'")
            return

        # Check partial name matches (e.g. Joy-Con L vs R, PlayStation)
        norm_name = self.controller_name.lower()
        if "joy-con (l)" in norm_name or "left joy-con" in norm_name:
            self.active_mapping = dict(DEFAULT_MAPPINGS["joycon_l"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Nintendo Joy-Con (L)")
            return
        elif any(ps in norm_name for ps in ["dualsense", "dualshock", "playstation", "wireless controller"]):
            self.active_mapping = dict(DEFAULT_MAPPINGS["playstation"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Sony PlayStation (DualSense / DualShock 4)")
            return
        elif "joy-con" in norm_name or "gamepad" in norm_name or "controller" in norm_name:
            self.active_mapping = dict(DEFAULT_MAPPINGS["default"])
            print(f"  {BOLD}{GREEN}✓ Matched built-in profile:{RESET} Standard Gamepad / Joy-Con (R)")
            return

        # Unrecognized / new controller -> Guided wizard
        print(f"  {YELLOW}ℹ️  New or unrecognized controller detected: '{self.controller_name}'{RESET}")
        print(f"  {DIM}Setting up custom button configuration...{RESET}")
        try:
            self.active_mapping = self.run_mapping_wizard(dev_id, self.controller_name)
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

        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(JOYINFOEX)
        info.dwFlags = JOY_RETURNALL

        btn_left = self.active_mapping.get("left_click", 0)
        btn_right = self.active_mapping.get("right_click", 1)
        btn_middle = self.active_mapping.get("middle_click", 2)
        btn_pad_click = self.active_mapping.get("trackpad_click", 13)
        btn_cycle = self.active_mapping.get("cycle_mode", 9)
        btn_cycle_alt = self.active_mapping.get("cycle_mode_alt", 8)
        btn_screenshot = self.active_mapping.get("screenshot", 13)
        btn_home = self.active_mapping.get("home", 12)

        btn_m_play = self.active_mapping.get("media_play_pause", 0)
        btn_m_voldn = self.active_mapping.get("media_vol_down", 1)
        btn_m_volup = self.active_mapping.get("media_vol_up", 2)
        btn_m_next = self.active_mapping.get("media_next_track", 3)

        btn_t_enter = self.active_mapping.get("terminal_enter", 0)
        btn_t_back = self.active_mapping.get("terminal_backspace", 1)
        btn_t_tab = self.active_mapping.get("terminal_tab", 4)
        btn_t_esc = self.active_mapping.get("terminal_esc", 8)

        btn_s_next = self.active_mapping.get("slide_next", 0)
        btn_s_prev = self.active_mapping.get("slide_prev", 1)
        btn_s_f5 = self.active_mapping.get("slide_f5", 2)
        btn_s_esc = self.active_mapping.get("slide_esc", 3)

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

                # D-Pad POV direction & changes
                pov = info.dwPOV
                pov_dir = self.get_pov_direction(pov)
                pov_changed = (pov_dir != self.last_pov_direction)
                now = time.time()

                # Mode cycling button
                if (pressed & (1 << btn_cycle)) or (pressed & (1 << btn_cycle_alt)):
                    self.cycle_mode()

                # Dedicated Screenshot Button (when not conflicting with pad click)
                if (pressed & (1 << btn_screenshot)) and btn_screenshot != btn_pad_click:
                    self.send_key(VK_SNAPSHOT)
                    print(f"\n  {BOLD}{CYAN}📸 [Screenshot]{RESET} Instant PrintScreen triggered")

                # Dedicated Home / Guide Button
                if pressed & (1 << btn_home):
                    self.send_key(VK_LWIN)

                curr_mode = self.modes[self.current_mode_index]

                if curr_mode == "DESKTOP MOUSE":
                    # Left Click (Standard Left Click or Trackpad Physical Click)
                    is_left_down = bool((buttons & (1 << btn_left)) or (btn_pad_click is not None and (buttons & (1 << btn_pad_click))))
                    if is_left_down:
                        self.mouse_down("left")
                    else:
                        self.mouse_up("left")

                    # Right Click
                    if buttons & (1 << btn_right):
                        self.mouse_down("right")
                    else:
                        self.mouse_up("right")

                    # Middle Click
                    if buttons & (1 << btn_middle):
                        self.mouse_down("middle")
                    else:
                        self.mouse_up("middle")

                    # D-Pad POV Navigation:
                    # UP / DOWN: Smooth Scroll Wheel
                    if pov_dir == "UP":
                        if now - self.last_scroll_time >= 0.07:
                            self.mouse_wheel(1)
                            self.last_scroll_time = now
                    elif pov_dir == "DOWN":
                        if now - self.last_scroll_time >= 0.07:
                            self.mouse_wheel(-1)
                            self.last_scroll_time = now
                    # LEFT / RIGHT: Browser Back / Forward
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_BROWSER_BACK)
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_BROWSER_FORWARD)

                elif curr_mode == "MEDIA REMOTE":
                    fg_app = get_foreground_window_title() or "System Default"
                    if pressed & (1 << btn_m_play):
                        self.send_key(VK_MEDIA_PLAY_PAUSE)
                        print(f"\n  {BOLD}{GREEN}▶/⏸ [Media]{RESET} Play/Pause -> {fg_app}")
                    if pressed & (1 << btn_m_voldn):
                        self.send_key(VK_VOLUME_DOWN)
                    if pressed & (1 << btn_m_volup):
                        self.send_key(VK_VOLUME_UP)
                    if pressed & (1 << btn_m_next):
                        self.send_key(VK_MEDIA_NEXT_TRACK)
                        print(f"\n  {BOLD}{CYAN}⏭ [Media]{RESET} Next Track -> {fg_app}")

                    # D-Pad POV in Media Remote:
                    if pov_dir == "UP":
                        if now - self.last_scroll_time >= 0.12:
                            self.send_key(VK_VOLUME_UP)
                            self.last_scroll_time = now
                    elif pov_dir == "DOWN":
                        if now - self.last_scroll_time >= 0.12:
                            self.send_key(VK_VOLUME_DOWN)
                            self.last_scroll_time = now
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_MEDIA_PREV_TRACK)
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_MEDIA_NEXT_TRACK)

                elif curr_mode == "INTERACTIVE TERMINAL":
                    if pressed & (1 << btn_t_enter):
                        self.send_key(VK_RETURN)
                    if pressed & (1 << btn_t_back):
                        self.send_key(VK_BACK)
                    if pressed & (1 << btn_t_tab):
                        self.send_key(VK_TAB)
                    if pressed & (1 << btn_t_esc):
                        self.send_key(VK_ESCAPE)
                    # Middle click sends Ctrl+C Interrupt in Terminal mode
                    if pressed & (1 << btn_middle):
                        self.send_combo([VK_CONTROL, VK_C])
                        print(f"\n  {BOLD}{YELLOW}🛑 [Terminal]{RESET} Ctrl+C Interrupt sent")

                    # D-Pad POV in Terminal:
                    if pov_dir == "UP" and pov_changed:
                        self.send_key(VK_UP)      # History Up
                    elif pov_dir == "DOWN" and pov_changed:
                        self.send_key(VK_DOWN)    # History Down
                    elif pov_dir == "LEFT" and pov_changed:
                        self.send_key(VK_LEFT)    # Cursor Left
                    elif pov_dir == "RIGHT" and pov_changed:
                        self.send_key(VK_RIGHT)   # Cursor Right

                elif curr_mode == "PRESENTATION CLICKER":
                    if pressed & (1 << btn_s_next):
                        self.send_key(VK_RIGHT)
                    if pressed & (1 << btn_s_prev):
                        self.send_key(VK_LEFT)
                    if pressed & (1 << btn_s_f5):
                        self.send_key(VK_F5)
                    if pressed & (1 << btn_s_esc):
                        self.send_key(VK_ESCAPE)

                self.last_buttons = buttons
                self.last_pov = pov
                self.last_pov_direction = pov_dir
                time.sleep(0.008)  # ~125 Hz polling rate

        except KeyboardInterrupt:
            print(f"\n{GREEN}Joy-Con Mouse for Windows stopped cleanly.{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Joy-Con Mouse & Universal Remote for Windows")
    parser.add_argument("--map", "--configure", action="store_true", help="Launch interactive button calibration wizard")
    parser.add_argument("--list-mappings", action="store_true", help="Display all saved controller button profiles")
    parser.add_argument("--check", action="store_true", help="Non-blocking device check (exits 0 if controller present, 1 otherwise)")
    parser.add_argument("--timeout", type=int, default=None, help="Maximum seconds to wait for controller before exiting")

    args = parser.parse_args()

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

    driver = WindowsJoyConDriver(force_map=args.map, timeout_sec=args.timeout)
    driver.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
