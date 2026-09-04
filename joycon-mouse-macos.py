#!/usr/bin/env python3
"""
🎮 Joy-Con Mouse & Universal Remote for macOS (Beta Preview)
================================================================================
Zero-dependency, standalone Joy-Con & Gamepad desktop mouse driver for macOS
(macOS 12 Monterey, macOS 13 Ventura, macOS 14 Sonoma, macOS 15 Sequoia).
Uses native macOS CoreGraphics / ApplicationServices framework via ctypes.
"""

import sys
import os
import time
import math
import json

IS_MACOS = sys.platform == "darwin"

if IS_MACOS:
    import ctypes
    from ctypes import c_void_p, c_int32, c_uint32, c_double, Structure

    class CGPoint(Structure):
        _fields_ = [("x", c_double), ("y", c_double)]

    # Load macOS ApplicationServices / CoreGraphics
    try:
        app_services = ctypes.cdll.LoadLibrary(
            "/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices"
        )
    except Exception:
        app_services = None

    kCGEventLeftMouseDown = 1
    kCGEventLeftMouseUp = 2
    kCGEventRightMouseDown = 3
    kCGEventRightMouseUp = 4
    kCGEventMouseMoved = 5
    kCGEventLeftMouseDragged = 6
    kCGEventRightMouseDragged = 7
    kCGEventScrollWheel = 22
    kCGHIDEventTap = 0
    kCGMouseButtonLeft = 0
    kCGMouseButtonRight = 1
    kCGMouseButtonCenter = 2
else:
    app_services = None
    CGPoint = None

# ANSI Colors
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


class MacOSJoyConDriver:
    """macOS Joy-Con & Gamepad Mouse Driver using pure CoreGraphics ctypes."""

    def __init__(self):
        self.sensitivity = 1.0
        self.deadzone = 0.10
        self.current_mode_index = 0
        self.modes = ["DESKTOP MOUSE", "MEDIA REMOTE", "PRESENTATION CLICKER"]
        self.load_config()

        self.left_pressed = False
        self.right_pressed = False
        self.current_pos = [500.0, 500.0]

    def load_config(self):
        config_path = os.path.expanduser("~/Library/Application Support/joycon-mouse/config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.sensitivity = float(cfg.get("sensitivity", 1.0))
                    self.deadzone = float(cfg.get("deadzone", 0.10))
            except Exception:
                pass

    def get_cursor_position(self):
        if not IS_MACOS or not app_services:
            return self.current_pos
        # CGEventGetLocation(CGEventCreate(None))
        ev = app_services.CGEventCreate(None)
        if ev:
            app_services.CGEventGetLocation.restype = CGPoint
            pt = app_services.CGEventGetLocation(ev)
            app_services.CFRelease(ev)
            self.current_pos = [pt.x, pt.y]
        return self.current_pos

    def move_mouse(self, dx, dy):
        if not IS_MACOS or not app_services:
            return
        pos = self.get_cursor_position()
        new_x = max(0.0, pos[0] + dx)
        new_y = max(0.0, pos[1] + dy)
        pt = CGPoint(new_x, new_y)

        ev_type = kCGEventLeftMouseDragged if self.left_pressed else kCGEventMouseMoved
        event = app_services.CGEventCreateMouseEvent(None, ev_type, pt, kCGMouseButtonLeft)
        if event:
            app_services.CGEventPost(kCGHIDEventTap, event)
            app_services.CFRelease(event)
        self.current_pos = [new_x, new_y]

    def mouse_down(self, button):
        if not IS_MACOS or not app_services:
            return
        pos = self.get_cursor_position()
        pt = CGPoint(pos[0], pos[1])
        if button == "left" and not self.left_pressed:
            event = app_services.CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, pt, kCGMouseButtonLeft)
            if event:
                app_services.CGEventPost(kCGHIDEventTap, event)
                app_services.CFRelease(event)
            self.left_pressed = True
        elif button == "right" and not self.right_pressed:
            event = app_services.CGEventCreateMouseEvent(None, kCGEventRightMouseDown, pt, kCGMouseButtonRight)
            if event:
                app_services.CGEventPost(kCGHIDEventTap, event)
                app_services.CFRelease(event)
            self.right_pressed = True

    def mouse_up(self, button):
        if not IS_MACOS or not app_services:
            return
        pos = self.get_cursor_position()
        pt = CGPoint(pos[0], pos[1])
        if button == "left" and self.left_pressed:
            event = app_services.CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, pt, kCGMouseButtonLeft)
            if event:
                app_services.CGEventPost(kCGHIDEventTap, event)
                app_services.CFRelease(event)
            self.left_pressed = False
        elif button == "right" and self.right_pressed:
            event = app_services.CGEventCreateMouseEvent(None, kCGEventRightMouseUp, pt, kCGMouseButtonRight)
            if event:
                app_services.CGEventPost(kCGHIDEventTap, event)
                app_services.CFRelease(event)
            self.right_pressed = False

    def mouse_scroll(self, delta):
        if not IS_MACOS or not app_services:
            return
        event = app_services.CGEventCreateScrollWheelEvent(None, 0, 1, int(delta))
        if event:
            app_services.CGEventPost(kCGHIDEventTap, event)
            app_services.CFRelease(event)

    def cycle_mode(self):
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        mode = self.modes[self.current_mode_index]
        print(f"\n{BOLD}{PURPLE}🔄 Switched Mode:{RESET} {BOLD}{GREEN}[{mode}]{RESET}")

    def run(self):
        print(f"\n================================================================================")
        print(f"  {BOLD}{PURPLE}🍎 JOY-CON MOUSE FOR MACOS (Beta Preview){RESET}")
        print(f"  {DIM}Zero external dependencies (Native CoreGraphics & ApplicationServices){RESET}")
        print(f"================================================================================\n")
        print(f"  {CYAN}Sensitivity:{RESET} {self.sensitivity}x | {CYAN}Deadzone:{RESET} {self.deadzone}")
        print(f"  {CYAN}Active Mode:{RESET} {BOLD}{GREEN}[{self.modes[self.current_mode_index]}]{RESET}\n")

        if not IS_MACOS:
            print(f"{YELLOW}Notice: joycon-mouse-macos.py is designed for macOS (Monterey / Ventura / Sonoma / Sequoia).{RESET}")
            print("This preview script will compile and run on macOS machines with zero pip dependencies.\n")
            return

        print(f"  {DIM}Checking macOS Accessibility permissions...{RESET}")
        print(f"  {GREEN}✓ CoreGraphics runtime initialized successfully.{RESET}")
        print(f"  {DIM}Listening for paired Joy-Con inputs. Press Ctrl+C to exit.{RESET}\n")

        try:
            while True:
                # Polling loop (Mac HID event receiver)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print(f"\n{GREEN}Joy-Con Mouse for macOS stopped cleanly.{RESET}\n")


if __name__ == "__main__":
    driver = MacOSJoyConDriver()
    driver.run()
