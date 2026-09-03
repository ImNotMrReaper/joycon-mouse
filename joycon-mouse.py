#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Nintendo Switch Joy-Con & Multi-Gamepad Ultra-Low Latency Desktop Driver for Linux.
Zero-dependency, pure Python Linux kernel interface using fcntl, struct, select, and uinput.
Location: joycon-mouse.py
"""

import argparse
import fcntl
import glob
import json
import math
import os
import select
import struct
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

# Dynamic plugin auto-loader
from modes import load_all_modes
from modes.base import BaseMode

# Load optional security manager if present locally
try:
    from security_manager import SecurityManager
except ImportError:
    SecurityManager = None

# Linux Input Event Types & ioctls
EVENT_SYN = 0x00
EVENT_KEY = 0x01
EVENT_REL = 0x02
EVENT_ABS = 0x03
EVENT_FF = 0x15
SYN_REPORT = 0

AXIS_REL_X = 0x00
AXIS_REL_Y = 0x01
AXIS_REL_HWHEEL = 0x06
AXIS_REL_WHEEL = 0x08
BUS_USB = 0x03

KEY_CODE_LEFTMETA = 125
KEY_CODE_SYSRQ = 99
KEY_CODE_RIGHT = 106
KEY_CODE_LEFT = 105

MOUSE_BTN_LEFT = 0x110
MOUSE_BTN_RIGHT = 0x111
MOUSE_BTN_MIDDLE = 0x112
MOUSE_BTN_BACK = 0x113
MOUSE_BTN_FORWARD = 0x114

GAME_PROCESS_PATTERN = "steamapps|steam_app|retroarch|rpcs3|dolphin-emu|yuzu|ryujinx|pcsx2|cemu|heroic|lutris"


def ioctl_code(direction: int, type_char: str, number: int, size: int) -> int:
    return (direction << 30) | (size << 16) | (ord(type_char) << 8) | number


def ioctl_none(type_char: str, number: int) -> int:
    return ioctl_code(0, type_char, number, 0)


def ioctl_write(type_char: str, number: int, size: int) -> int:
    return ioctl_code(1, type_char, number, size)


def eviocgname(length: int = 256) -> int:
    return (2 << 30) | (length << 16) | (ord("E") << 8) | 0x06


EVIOCGRAB = ioctl_write("E", 0x90, 4)
EVIOCSFF = ioctl_write("E", 0x80, 48)
EVIOCRMFF = ioctl_write("E", 0x81, 4)

UI_SET_EVBIT = ioctl_write("U", 100, 4)
UI_SET_KEYBIT = ioctl_write("U", 101, 4)
UI_SET_RELBIT = ioctl_write("U", 102, 4)
UI_DEV_CREATE = ioctl_none("U", 1)
UI_DEV_DESTROY = ioctl_none("U", 2)
UI_DEV_SETUP = ioctl_write("U", 3, 92)

IS_64_BIT = struct.calcsize("P") == 8
EVENT_STRUCT_FORMAT = "llHHi" if IS_64_BIT else "iiHHi"
EVENT_STRUCT_SIZE = struct.calcsize(EVENT_STRUCT_FORMAT)


class ConfigManager:
    """Manages user configuration in ~/.config/joycon-mouse/config.json."""

    DEFAULT_CONFIG = {
        "sensitivity": 1.0,
        "speed_x": 36.0,
        "speed_y": 36.0,
        "dead_zone": 0.08,
        "accel_exponent": 1.6,
        "rumble_enabled": True,
        "auto_dormant_enabled": True,
        "scroll_repeat_ms": 70,
        "disabled_modes": []
    }

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.expanduser("~/.config/joycon-mouse")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        cfg = dict(self.DEFAULT_CONFIG)
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_cfg = json.load(f)
                    if isinstance(user_cfg, dict):
                        cfg.update(user_cfg)
            except Exception as e:
                print(f"[Config Warning] Could not read {self.config_file}: {e}")
        else:
            try:
                os.makedirs(self.config_dir, exist_ok=True)
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=4)
            except Exception:
                pass
        return cfg

    def save_config(self) -> None:
        """Persists current configuration to disk."""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[Config Error] Could not save {self.config_file}: {e}")

    def disable_mode(self, mode_name: str) -> None:
        """Disables a mode in user configuration."""
        d_modes = list(self.config.get("disabled_modes", []))
        norm = mode_name.lower().strip()
        if norm not in [m.lower().strip() for m in d_modes]:
            d_modes.append(norm)
            self.config["disabled_modes"] = d_modes
            self.save_config()

    def enable_mode(self, mode_name: str) -> None:
        """Enables a mode in user configuration."""
        d_modes = list(self.config.get("disabled_modes", []))
        norm = mode_name.lower().strip()
        filtered = [m for m in d_modes if m.lower().strip() != norm]
        self.config["disabled_modes"] = filtered
        self.save_config()


class DriverLogger:
    """Structured driver logger for console and optional log file."""

    def __init__(self, debug: bool = False, log_file: Optional[str] = None):
        self.debug = debug
        self.log_file = log_file
        if self.log_file:
            try:
                os.makedirs(os.path.dirname(os.path.abspath(self.log_file)), exist_ok=True)
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"\n--- Session Started: {time.strftime("%Y-%m-%d %H:%M:%S")} ---\n")
            except Exception as e:
                print(f"[Logger Warning] Could not open log file {self.log_file}: {e}")

    def log(self, message: str, level: str = "INFO") -> None:
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}"
        if level in ("INFO", "WARN", "ERROR") or self.debug:
            print(formatted)
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(formatted + "\n")
            except Exception:
                pass


class BackgroundGameDetector:
    """Asynchronous background game detector to prevent polling loop lag."""

    def __init__(self, enabled: bool = True, check_interval: float = 2.0):
        self.enabled = enabled
        self.check_interval = check_interval
        self.active_game: Optional[str] = None
        self._running = True
        if self.enabled:
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()

    def _monitor_loop(self) -> None:
        while self._running:
            try:
                out = subprocess.check_output(
                    ["pgrep", "-f", "-E", GAME_PROCESS_PATTERN],
                    stderr=subprocess.DEVNULL
                )
                if out.strip():
                    self.active_game = "Active Game"
                else:
                    self.active_game = None
            except Exception:
                self.active_game = None
            time.sleep(self.check_interval)

    def stop(self) -> None:
        self._running = False


class RumbleManager:
    """Controls physical haptic feedback (EV_FF) on connected Joy-Cons & gamepads."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.open_descriptors: List[int] = []

    def set_descriptors(self, fds: List[int]) -> None:
        self.open_descriptors = fds

    def _pulse_thread(self, fds: List[int], duration_ms: int, strong: int, weak: int, count: int, interval_ms: int) -> None:
        for _ in range(count):
            for fd in fds:
                try:
                    ff_struct = struct.pack("HhHHHHHHH30x", 0x50, -1, 0, 0, 0, duration_ms, 0, strong, weak)
                    buf = bytearray(ff_struct)
                    fcntl.ioctl(fd, EVIOCSFF, buf)
                    effect_id = struct.unpack("Hh", buf[:4])[1]
                    play_event = struct.pack(EVENT_STRUCT_FORMAT, 0, 0, EVENT_FF, effect_id, 1)
                    os.write(fd, play_event)
                    time.sleep(duration_ms / 1000.0)
                    fcntl.ioctl(fd, EVIOCRMFF, effect_id)
                except Exception:
                    pass
            if count > 1:
                time.sleep(interval_ms / 1000.0)

    def pulse(self, duration_ms: int = 50, strong: int = 0x6000, weak: int = 0x6000, count: int = 1, interval_ms: int = 60) -> None:
        if not self.enabled or not self.open_descriptors:
            return
        t = threading.Thread(
            target=self._pulse_thread,
            args=(list(self.open_descriptors), duration_ms, strong, weak, count, interval_ms),
            daemon=True
        )
        t.start()

    def mode_switch(self) -> None:
        self.pulse(duration_ms=45, strong=0x5000, weak=0x5000, count=1)

    def screenshot(self) -> None:
        self.pulse(duration_ms=40, strong=0x7000, weak=0x7000, count=2, interval_ms=50)

    def unlock_success(self) -> None:
        self.pulse(duration_ms=80, strong=0x8000, weak=0x8000, count=1)


@dataclass
class JoystickSettings:
    enabled: bool = True
    speed_x: float = 36.0
    speed_y: float = 36.0
    dead_zone: float = 0.08
    accel_exponent: float = 1.6
    invert_x: bool = False
    invert_y: bool = False


@dataclass
class DeviceProfile:
    name: str
    description: str
    joystick: JoystickSettings = field(default_factory=JoystickSettings)
    scroll_repeat_ms: int = 70


def get_device_profile(profile_name: str, config: Dict[str, Any]) -> DeviceProfile:
    titles = {
        "right_joycon": "Nintendo Switch Right Joy-Con (Desktop Controller)",
        "left_joycon": "Nintendo Switch Left Joy-Con (Desktop Controller)",
        "dual_joycon": "Nintendo Switch Combined Dual Joy-Cons (Grip / Split)",
        "switch_pro": "Nintendo Switch Pro Controller (USB / Bluetooth)",
        "playstation": "Sony PlayStation Controller (DualSense / DualShock)",
        "xbox": "Microsoft Xbox Controller (Xbox 360 / One / Series)",
        "generic_gamepad": "Universal Gamepad (8BitDo / DirectInput / XInput)"
    }
    return DeviceProfile(
        name=profile_name,
        description=titles.get(profile_name, "Gamepad Controller"),
        joystick=JoystickSettings(
            enabled=True,
            speed_x=float(config.get("speed_x", 36.0)),
            speed_y=float(config.get("speed_y", 36.0)),
            dead_zone=float(config.get("dead_zone", 0.08)),
            accel_exponent=float(config.get("accel_exponent", 1.6))
        ),
        scroll_repeat_ms=int(config.get("scroll_repeat_ms", 70))
    )


class VirtualMouseDevice:
    """Manages virtual mouse and keyboard events via /dev/uinput."""

    def __init__(self, device_name: str = "Joy-Con Desktop Controller"):
        self.device_name = device_name
        self.file_descriptor: Optional[int] = None
        self.active_keys: Set[int] = set()
        self._initialize_device()

    def _initialize_device(self) -> None:
        candidate_paths = ["/dev/uinput", "/dev/input/uinput"]
        for path in candidate_paths:
            if os.path.exists(path):
                try:
                    self.file_descriptor = os.open(path, os.O_RDWR | os.O_NONBLOCK)
                    break
                except PermissionError:
                    raise PermissionError(
                        f"Cannot open {path}. Ensure user is in the input group: sudo usermod -aG input $USER"
                    )
                except OSError:
                    continue

        if self.file_descriptor is None:
            raise FileNotFoundError(
                "Neither /dev/uinput nor /dev/input/uinput is accessible. Ensure uinput module is loaded: sudo modprobe uinput"
            )

        fcntl.ioctl(self.file_descriptor, UI_SET_EVBIT, EVENT_SYN)
        fcntl.ioctl(self.file_descriptor, UI_SET_EVBIT, EVENT_KEY)
        fcntl.ioctl(self.file_descriptor, UI_SET_EVBIT, EVENT_REL)

        for rel_axis in [AXIS_REL_X, AXIS_REL_Y, AXIS_REL_WHEEL, AXIS_REL_HWHEEL]:
            fcntl.ioctl(self.file_descriptor, UI_SET_RELBIT, rel_axis)

        for btn in [MOUSE_BTN_LEFT, MOUSE_BTN_RIGHT, MOUSE_BTN_MIDDLE, MOUSE_BTN_BACK, MOUSE_BTN_FORWARD]:
            fcntl.ioctl(self.file_descriptor, UI_SET_KEYBIT, btn)

        for key in range(1, 256):
            try:
                fcntl.ioctl(self.file_descriptor, UI_SET_KEYBIT, key)
            except OSError:
                pass

        try:
            name_bytes = self.device_name.encode("utf-8")[:79].ljust(80, b"\x00")
            setup_struct = struct.pack("HHHH80sI", BUS_USB, 0x057E, 0x2009, 1, name_bytes, 0)
            fcntl.ioctl(self.file_descriptor, UI_DEV_SETUP, setup_struct)
            fcntl.ioctl(self.file_descriptor, UI_DEV_CREATE, 0)
        except OSError:
            name_bytes = self.device_name.encode("utf-8")[:79].ljust(80, b"\x00")
            user_dev = struct.pack("80sHHHHII", name_bytes, BUS_USB, 0x057E, 0x2009, 1, 0, 0) + (b"\x00" * 1024)
            os.write(self.file_descriptor, user_dev)
            fcntl.ioctl(self.file_descriptor, UI_DEV_CREATE, 0)

    def move_cursor(self, delta_x: int, delta_y: int) -> None:
        if (delta_x == 0 and delta_y == 0) or self.file_descriptor is None:
            return

        now = time.time()
        sec = int(now)
        micro_sec = int((now - sec) * 1_000_000)

        payload = b""
        if delta_x != 0:
            payload += struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_REL, AXIS_REL_X, delta_x)
        if delta_y != 0:
            payload += struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_REL, AXIS_REL_Y, delta_y)
        payload += struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_SYN, SYN_REPORT, 0)

        try:
            os.write(self.file_descriptor, payload)
        except OSError:
            pass

    def emit_scroll(self, steps_y: int) -> None:
        if steps_y == 0 or self.file_descriptor is None:
            return

        now = time.time()
        sec = int(now)
        micro_sec = int((now - sec) * 1_000_000)

        payload = struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_REL, AXIS_REL_WHEEL, steps_y)
        payload += struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_SYN, SYN_REPORT, 0)

        try:
            os.write(self.file_descriptor, payload)
        except OSError:
            pass

    def emit_key(self, code: int, value: int) -> None:
        if self.file_descriptor is None:
            return

        now = time.time()
        sec = int(now)
        micro_sec = int((now - sec) * 1_000_000)

        if value == 1:
            self.active_keys.add(code)
        elif value == 0:
            self.active_keys.discard(code)

        payload = struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_KEY, code, value)
        payload += struct.pack(EVENT_STRUCT_FORMAT, sec, micro_sec, EVENT_SYN, SYN_REPORT, 0)

        try:
            os.write(self.file_descriptor, payload)
        except OSError:
            pass

    def tap_key(self, code: int, duration: float = 0.02) -> None:
        self.emit_key(code, 1)
        time.sleep(duration)
        self.emit_key(code, 0)

    def tap_combo(self, key_codes: List[int], duration: float = 0.03) -> None:
        for code in key_codes:
            self.emit_key(code, 1)
        time.sleep(duration)
        for code in reversed(key_codes):
            self.emit_key(code, 0)

    def close(self) -> None:
        if self.file_descriptor is not None:
            try:
                for key_code in list(self.active_keys):
                    self.emit_key(key_code, 0)
                fcntl.ioctl(self.file_descriptor, UI_DEV_DESTROY, 0)
                os.close(self.file_descriptor)
            except OSError:
                pass
            finally:
                self.file_descriptor = None

    def __del__(self) -> None:
        self.close()


class JoystickFilter:
    """Processes analog stick deflection with responsive hybrid acceleration curves."""

    def __init__(self, config: JoystickSettings):
        self.config = config
        self.normalized_x = 0.0
        self.normalized_y = 0.0
        self.subpixel_x = 0.0
        self.subpixel_y = 0.0

    def update_axis(self, code: int, value: int) -> None:
        normalized = max(-1.0, min(1.0, value / 32767.0))
        if code in (0x00, 0x03):
            self.normalized_x = normalized
        elif code in (0x01, 0x04):
            self.normalized_y = normalized

    def process(self, delta_time: float) -> Tuple[int, int]:
        if not self.config.enabled:
            return 0, 0

        stick_x = -self.normalized_x if self.config.invert_x else self.normalized_x
        stick_y = -self.normalized_y if self.config.invert_y else self.normalized_y

        magnitude = math.sqrt(stick_x * stick_x + stick_y * stick_y)
        if magnitude < self.config.dead_zone:
            return 0, 0

        effective_magnitude = min(1.0, (magnitude - self.config.dead_zone) / (1.0 - self.config.dead_zone))
        curve = 0.25 * effective_magnitude + 0.75 * math.pow(effective_magnitude, self.config.accel_exponent)
        direction_x = stick_x / magnitude
        direction_y = stick_y / magnitude

        self.subpixel_x += direction_x * curve * (self.config.speed_x * 60.0 * delta_time)
        self.subpixel_y += direction_y * curve * (self.config.speed_y * 60.0 * delta_time)

        pixel_dx = int(self.subpixel_x)
        pixel_dy = int(self.subpixel_y)
        self.subpixel_x -= pixel_dx
        self.subpixel_y -= pixel_dy
        return pixel_dx, pixel_dy


@dataclass
class ControllerNode:
    path: str
    name: str
    device_type: str
    connection_type: str = "Bluetooth / Wireless"


def classify_device(device_name: str, event_path: str) -> Optional[ControllerNode]:
    name_lower = device_name.lower()
    if "virtual" in name_lower or "uinput" in name_lower or "imu" in name_lower or "sensor" in name_lower or "gyro" in name_lower:
        return None

    conn = "Wired USB" if "usb" in name_lower or "wired" in name_lower else "Bluetooth / Wireless"

    if "right joy-con" in name_lower or "joy-con (r)" in name_lower:
        dev_type = "right_joycon"
    elif "left joy-con" in name_lower or "joy-con (l)" in name_lower:
        dev_type = "left_joycon"
    elif "combined joy-con" in name_lower or "joy-con (l/r)" in name_lower:
        dev_type = "dual_joycon"
    elif "pro controller" in name_lower or "switch pro" in name_lower:
        dev_type = "switch_pro"
    elif any(ps in name_lower for ps in ["dualsense", "dualshock", "playstation", "sony"]):
        dev_type = "playstation"
    elif any(xb in name_lower for xb in ["xbox", "x-box", "microsoft"]):
        dev_type = "xbox"
    elif any(gp in name_lower for gp in ["gamepad", "joystick", "controller", "8bitdo"]):
        dev_type = "generic_gamepad"
    else:
        return None

    return ControllerNode(
        path=event_path,
        name=device_name,
        device_type=dev_type,
        connection_type=conn
    )


def discover_input_devices() -> List[ControllerNode]:
    detected_nodes: List[ControllerNode] = []

    for event_path in sorted(
        glob.glob("/dev/input/event*"),
        key=lambda path_str: int(path_str.replace("/dev/input/event", "") or "0")
        if path_str.replace("/dev/input/event", "").isdigit() else 0
    ):
        try:
            descriptor = os.open(event_path, os.O_RDONLY | os.O_NONBLOCK)
            buffer = bytearray(256)
            fcntl.ioctl(descriptor, eviocgname(256), buffer)
            device_name = buffer.split(b"\x00", 1)[0].decode("utf-8", errors="ignore").strip()
            os.close(descriptor)
        except OSError:
            continue

        if not device_name:
            continue

        node = classify_device(device_name, event_path)
        if node is not None:
            detected_nodes.append(node)

    return detected_nodes


def run_controller_session(
    pads: List[ControllerNode],
    profile: DeviceProfile,
    security_mgr: Optional[Any] = None,
    logger: Optional[DriverLogger] = None,
    rumble: Optional[RumbleManager] = None,
    auto_dormant: bool = True,
    exclusive_grab: bool = True,
    disabled_modes: Optional[List[str]] = None
) -> None:
    """Runs event polling with auto-dormant detection, haptics, and dynamic mode execution."""
    active_modes = load_all_modes(disabled_modes=disabled_modes)
    if not active_modes:
        print("[Error] No active modes found. Check your disabled_modes or modes/ directory.")
        return

    log = logger or DriverLogger()
    game_detector = BackgroundGameDetector(enabled=auto_dormant, check_interval=2.0)
    uinput = VirtualMouseDevice(device_name=f"{profile.description} (Virtual Device)")
    open_descriptors: Dict[int, ControllerNode] = {}
    poll_object = select.poll()
    joystick_filters: Dict[str, JoystickFilter] = {}

    for pad_node in pads:
        try:
            pad_fd = os.open(pad_node.path, os.O_RDWR | os.O_NONBLOCK)
            if exclusive_grab:
                try:
                    fcntl.ioctl(pad_fd, EVIOCGRAB, 1)
                except OSError:
                    pass
            open_descriptors[pad_fd] = pad_node
            poll_object.register(pad_fd, select.POLLIN | select.POLLERR | select.POLLHUP)
            joystick_filters[pad_node.path] = JoystickFilter(profile.joystick)
        except OSError:
            continue

    if not open_descriptors:
        game_detector.stop()
        return

    if rumble:
        rumble.set_descriptors(list(open_descriptors.keys()))
        rumble.pulse(duration_ms=60, strong=0x5000, weak=0x5000)

    mode_index = 0
    total_modes = len(active_modes)
    active_scroll_direction = 0
    last_scroll_timestamp = 0.0
    last_media_seek_timestamp = 0.0
    last_tick_timestamp = time.perf_counter()

    is_dormant = False
    smart_press_timestamp: Optional[float] = None
    smart_hold_triggered = False
    hold_threshold_sec = 0.38

    def get_current_mode() -> BaseMode:
        return active_modes[mode_index % total_modes]

    def set_grab_state(grab: bool) -> None:
        if not exclusive_grab:
            return
        for fd in open_descriptors.keys():
            try:
                fcntl.ioctl(fd, EVIOCGRAB, 1 if grab else 0)
            except OSError:
                pass

    def print_status_banner() -> None:
        current_active_mode = get_current_mode()
        sec_status = "ENABLED" if (security_mgr and security_mgr.has_code(profile.name)) else "DISABLED"

        print("\n" + "=" * 65)
        print("  CONNECTED CONTROLLERS:")
        for idx, p_node in enumerate(pads, 1):
            print(f"   [{idx}] {p_node.name} [{p_node.connection_type}] -> {p_node.path}")
        print("-" * 65)
        print(f"  ACTIVE MODE [{mode_index + 1}/{total_modes}]: [{current_active_mode.name}]")
        print(f"  CHEAT-CODE UNLOCK & SUDO: [{sec_status}]")
        print("=" * 65)
        print("Controls Cheatsheet:")

        current_map = current_active_mode.get_button_map(profile.name)
        seen_descriptions = set()
        unique_actions = []
        for action_dict in current_map.values():
            desc = action_dict.get("desc", "")
            if desc and desc not in seen_descriptions:
                seen_descriptions.add(desc)
                unique_actions.append(desc)

        for desc in sorted(unique_actions):
            print(f"  * {desc}")
        print("\nTip: Press + or - to cycle active mode (with haptic vibration click).")
        print("Tip: Tap Home/Capture for Super (Windows Key) | Hold >= 0.4s for Screenshot.")
        print("Tip: Auto-Dormant enabled (Releases controller automatically when games launch).")
        print("=" * 65 + "\n")

    print_status_banner()

    try:
        while True:
            # Check game state from background thread with 0 latency
            active_game = game_detector.active_game
            if active_game and not is_dormant:
                is_dormant = True
                set_grab_state(False)
                log.log(f"Game detected ({active_game}). Controller released to game.", level="INFO")
            elif not active_game and is_dormant:
                is_dormant = False
                set_grab_state(True)
                log.log("Game exited. Resuming Joy-Con desktop control.", level="INFO")
                print_status_banner()

            if is_dormant:
                time.sleep(0.1)
                last_tick_timestamp = time.perf_counter()
                continue

            # High-performance 250Hz polling (4ms timeout)
            poll_events = poll_object.poll(4)
            now_time = time.perf_counter()
            delta_time = now_time - last_tick_timestamp
            last_tick_timestamp = now_time

            if delta_time > 0.05:
                delta_time = 0.016
            elif delta_time <= 0.0:
                delta_time = 0.004

            for descriptor, mask in poll_events:
                if mask & (select.POLLERR | select.POLLHUP):
                    return

                if mask & select.POLLIN:
                    try:
                        raw_data = os.read(descriptor, EVENT_STRUCT_SIZE * 64)
                    except OSError:
                        return

                    node_info = open_descriptors.get(descriptor)
                    if node_info is None:
                        continue

                    total_events = len(raw_data) // EVENT_STRUCT_SIZE
                    for event_index in range(total_events):
                        offset = event_index * EVENT_STRUCT_SIZE
                        event_chunk = raw_data[offset : offset + EVENT_STRUCT_SIZE]
                        _, _, event_type, code, value = struct.unpack(EVENT_STRUCT_FORMAT, event_chunk)

                        if event_type == EVENT_KEY:
                            if value == 1 and security_mgr:
                                if security_mgr.process_key_event(code, node_info.device_type, uinput):
                                    if rumble:
                                        rumble.unlock_success()
                                    continue

                            active_mode = get_current_mode()
                            button_map = active_mode.get_button_map(node_info.device_type)
                            action_config = button_map.get(code)

                            if log.debug:
                                log.log(f"Key Event: code={code} (0x{code:03x}) val={value} on {node_info.name}", level="DEBUG")

                            if action_config is not None:
                                action_type = action_config.get("action")
                                target_code = action_config.get("code", 0)

                                if action_type == "mode_cycle" and value == 1:
                                    mode_index = (mode_index + 1) % total_modes
                                    if rumble:
                                        rumble.mode_switch()
                                    log.log(f"Switched mode to [{get_current_mode().name}]", level="INFO")
                                    print_status_banner()

                                elif action_type == "smart_home":
                                    if value == 1:
                                        smart_press_timestamp = time.perf_counter()
                                        smart_hold_triggered = False
                                    elif value == 0:
                                        if smart_press_timestamp is not None and not smart_hold_triggered:
                                            uinput.tap_key(KEY_CODE_LEFTMETA)
                                            log.log("[Smart Button] Tapped -> Super (Windows Key)", level="INFO")
                                        smart_press_timestamp = None
                                        smart_hold_triggered = False

                                elif action_type == "combo" and value == 1:
                                    keys_to_press = action_config.get("keys", [])
                                    uinput.tap_combo(keys_to_press)

                                elif action_type in ("mouse_btn", "key"):
                                    uinput.emit_key(target_code, value)

                                elif action_type == "scroll":
                                    if value == 1:
                                        active_scroll_direction = action_config.get("param", 0)
                                        uinput.emit_scroll(active_scroll_direction)
                                        last_scroll_timestamp = time.perf_counter()
                                    elif value == 0 and active_scroll_direction == action_config.get("param", 0):
                                        active_scroll_direction = 0

                        elif event_type == EVENT_ABS:
                            if code in (0x00, 0x01, 0x03, 0x04):
                                j_filter = joystick_filters.get(node_info.path)
                                if j_filter is not None:
                                    j_filter.update_axis(code, value)

            if smart_press_timestamp is not None and not smart_hold_triggered:
                if (now_time - smart_press_timestamp) >= hold_threshold_sec:
                    uinput.tap_key(KEY_CODE_SYSRQ)
                    smart_hold_triggered = True
                    if rumble:
                        rumble.screenshot()
                    log.log("[Smart Button] Held -> Screenshot (PrintScreen)", level="INFO")

            active_mode = get_current_mode()

            if active_mode.enable_joystick_cursor:
                total_joy_dx = 0
                total_joy_dy = 0
                for j_filter in joystick_filters.values():
                    jdx, jdy = j_filter.process(delta_time)
                    total_joy_dx += jdx
                    total_joy_dy += jdy

                if total_joy_dx != 0 or total_joy_dy != 0:
                    uinput.move_cursor(total_joy_dx, total_joy_dy)

                if active_scroll_direction != 0 and (now_time - last_scroll_timestamp) >= (profile.scroll_repeat_ms / 1000.0):
                    uinput.emit_scroll(active_scroll_direction)
                    last_scroll_timestamp = now_time

            if active_mode.enable_media_seek:
                for j_filter in joystick_filters.values():
                    jdx, _ = j_filter.process(delta_time)
                    if (now_time - last_media_seek_timestamp) >= 0.25:
                        if jdx > 4:
                            uinput.tap_key(KEY_CODE_RIGHT)
                            last_media_seek_timestamp = now_time
                            log.log("[Media Seek] Forward +5s", level="INFO")
                        elif jdx < -4:
                            uinput.tap_key(KEY_CODE_LEFT)
                            last_media_seek_timestamp = now_time
                            log.log("[Media Seek] Rewind -5s", level="INFO")

            if getattr(active_mode, "enable_terminal_scroll", False):
                for j_filter in joystick_filters.values():
                    _, jdy = j_filter.process(delta_time)
                    if abs(jdy) > 2 and (now_time - last_scroll_timestamp) >= 0.08:
                        scroll_step = 1 if jdy < 0 else -1
                        uinput.emit_scroll(scroll_step)
                        last_scroll_timestamp = now_time


    finally:
        game_detector.stop()
        for fd in open_descriptors.keys():
            try:
                if exclusive_grab:
                    fcntl.ioctl(fd, EVIOCGRAB, 0)
                os.close(fd)
            except OSError:
                pass
        uinput.close()


def install_systemd_service() -> int:
    """Installs and enables the systemd user background service."""
    service_dir = os.path.expanduser("~/.config/systemd/user")
    service_file = os.path.join(service_dir, "joycon-mouse.service")
    bin_path = "/usr/local/bin/joycon-mouse"
    if not os.path.exists(bin_path):
        bin_path = sys.executable + " " + os.path.abspath(__file__)

    service_content = f"""[Unit]
Description=Joy-Con Mouse & Universal Remote Background Driver
After=bluetooth.target

[Service]
ExecStart={bin_path}
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
"""
    try:
        os.makedirs(service_dir, exist_ok=True)
        with open(service_file, "w", encoding="utf-8") as f:
            f.write(service_content)

        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "--user", "enable", "--now", "joycon-mouse.service"], check=True)
        print(f"\n[SUCCESS] Installed and started background service: {service_file}")
        print("Driver is now running automatically in the background on startup!")
        print("To view live logs: journalctl --user -u joycon-mouse.service -f\n")
        return 0
    except Exception as e:
        print(f"[Error] Failed to install systemd service: {e}")
        return 1


def uninstall_systemd_service() -> int:
    """Disables and removes the systemd user background service."""
    service_file = os.path.expanduser("~/.config/systemd/user/joycon-mouse.service")
    try:
        subprocess.run(["systemctl", "--user", "disable", "--now", "joycon-mouse.service"], check=False)
        if os.path.exists(service_file):
            os.remove(service_file)
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
        print(f"\n[SUCCESS] Uninstalled background service: {service_file}\n")
        return 0
    except Exception as e:
        print(f"[Error] Failed to uninstall systemd service: {e}")
        return 1


def list_all_modes_cli(config_mgr: ConfigManager) -> int:
    """Prints a structured table of all discovered built-in and community modes."""
    from modes import discover_all_modes
    disabled_modes = config_mgr.config.get("disabled_modes", [])
    modes_list = discover_all_modes(disabled_modes=disabled_modes)

    print("\n" + "=" * 80)
    print("  🎮 JOY-CON MOUSE MODULAR CONTROLLER MODES")
    print("=" * 80)
    print(f"  {'STATUS':<10} {'TYPE':<12} {'MODE NAME':<34} {'SOURCE FILE'}")
    print("-" * 80)

    if not modes_list:
        print("  No controller modes found in modes/ or custom_modes/.")
        print("=" * 80 + "\n")
        return 0

    for m in modes_list:
        status_str = "[ENABLED]" if m.is_enabled else "[DISABLED]"
        type_str = "Custom" if m.is_custom else "Built-in"
        rel_path = os.path.relpath(m.file_path, os.getcwd()) if m.file_path else "unknown"
        print(f"  {status_str:<10} {type_str:<12} {m.name:<34} {rel_path}")
        print(f"             Description: {m.description}")
        features = []
        if m.enable_joystick_cursor:
            features.append("Analog Cursor")
        if m.enable_media_seek:
            features.append("Media Seek")
        if m.enable_terminal_scroll:
            features.append("Terminal Scroll")
        feat_str = ", ".join(features) if features else "Button Mappings Only"
        print(f"             Features:    {feat_str}\n")

    print("=" * 80)
    print("  💡 MANAGEMENT COMMANDS:")
    print("  * Enable a mode:   joycon-mouse --enable-mode <name_or_file>")
    print("  * Disable a mode:  joycon-mouse --disable-mode <name_or_file>")
    print("  * Create new mode: joycon-mouse --create-mode <name>")
    print("  * Test a mode:     python3 custom_modes/<name>.py")
    print("=" * 80 + "\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="joycon-mouse",
        description="Nintendo Switch Joy-Con & Multi-Gamepad Ultra-Low Latency Desktop Driver for Linux."
    )
    parser.add_argument("-l", "--list", action="store_true", help="List detected controllers and exit.")
    parser.add_argument("--list-modes", action="store_true", help="List all available controller modes (built-in and custom) and exit.")
    parser.add_argument("--enable-mode", type=str, metavar="NAME", help="Enable a controller mode in user configuration.")
    parser.add_argument("--disable-mode", type=str, metavar="NAME", help="Disable a controller mode in user configuration.")
    parser.add_argument("--create-mode", type=str, metavar="NAME", help="Scaffold a new custom controller mode template in custom_modes/.")
    parser.add_argument("-p", "--profile", type=str, default=None,
                        choices=["right_joycon", "left_joycon", "dual_joycon", "switch_pro", "playstation", "xbox", "generic_gamepad"],
                        help="Force specific profile.")
    parser.add_argument("-s", "--sensitivity", type=float, default=None, help="Pointer sensitivity multiplier (e.g. 1.2 or 0.8).")
    parser.add_argument("--set-code", action="store_true", help="Launch interactive wizard to set or change cheat-code.")
    parser.add_argument("--test-buttons", action="store_true", help="Launch real-time interactive button and stick diagnostic tool.")
    parser.add_argument("--install-service", action="store_true", help="Install & start automatic background startup service.")
    parser.add_argument("--uninstall-service", action="store_true", help="Uninstall background startup service.")
    parser.add_argument("--log-file", type=str, default=None, help="Save driver logs to a specified file.")
    parser.add_argument("--no-rumble", action="store_true", help="Disable physical haptic vibration feedback.")
    parser.add_argument("--no-grab", action="store_true", help="Disable exclusive device grabbing (not recommended with Steam).")
    parser.add_argument("-v", "--verbose", "--debug", dest="debug", action="store_true", help="Print real-time debug events.")
    parser.add_argument("--no-reconnect", action="store_true", help="Do not wait and auto-reconnect on disconnect.")
    args = parser.parse_args()

    if args.install_service:
        return install_systemd_service()

    if args.uninstall_service:
        return uninstall_systemd_service()

    if args.test_buttons:
        from test_buttons import main as test_main
        return test_main()

    config_mgr = ConfigManager()
    cfg = config_mgr.config

    if args.list_modes:
        return list_all_modes_cli(config_mgr)

    if args.enable_mode:
        config_mgr.enable_mode(args.enable_mode)
        print(f"\n[SUCCESS] Enabled mode '{args.enable_mode}' in {config_mgr.config_file}\n")
        return 0

    if args.disable_mode:
        config_mgr.disable_mode(args.disable_mode)
        print(f"\n[SUCCESS] Disabled mode '{args.disable_mode}' in {config_mgr.config_file}\n")
        return 0

    if args.create_mode:
        from modes import create_mode_template
        try:
            new_file = create_mode_template(args.create_mode)
            print(f"\n[SUCCESS] Created new modular mode template at:\n  -> {new_file}\n")
            print("Edit this file to customize your button mappings!")
            print(f"Test your mode standalone anytime by running: python3 {new_file}\n")
            return 0
        except Exception as e:
            print(f"[Error] Could not create mode template: {e}")
            return 1

    if args.sensitivity is not None:
        cfg["sensitivity"] = args.sensitivity
    if args.no_rumble:
        cfg["rumble_enabled"] = False

    logger = DriverLogger(debug=args.debug, log_file=args.log_file)
    rumble = RumbleManager(enabled=bool(cfg.get("rumble_enabled", True)))
    security_mgr = SecurityManager() if SecurityManager is not None else None

    if args.list:
        controllers = discover_input_devices()
        print("\nDetected Controllers in /dev/input/event*:")
        for idx, pad in enumerate(controllers, 1):
            print(f"  [{idx}] {pad.name} [{pad.connection_type}] ({pad.device_type}) -> {pad.path}")
        if not controllers:
            print("  No compatible Joy-Cons or Gamepads detected.")
            print("  Ensure Bluetooth pairing or USB connection is established.")
        print()
        return 0

    while True:
        controllers = discover_input_devices()
        if not controllers:
            print("[Waiting] No Joy-Cons or Gamepads detected. Turn on or plug in controller...")
            time.sleep(2.0)
            continue

        primary_pad = controllers[0]
        chosen_profile_name = args.profile or primary_pad.device_type

        # Interactive Dual Joy-Con Pairing Detection
        if len(controllers) >= 2 and not args.profile:
            has_left = any(p.device_type == "left_joycon" for p in controllers)
            has_right = any(p.device_type == "right_joycon" for p in controllers)
            if has_left and has_right:
                print("\n[Pairing Prompt] Detected both Left and Right Joy-Cons connected!")
                try:
                    user_resp = input("  Would you like to pair them into a single Dual Joy-Con controller? [Y/n]: ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    user_resp = "y"

                if user_resp in ("", "y", "yes"):
                    chosen_profile_name = "dual_joycon"
                    print("  -> Initialized in Combined Dual Joy-Con mode.\n")
                else:
                    chosen_profile_name = primary_pad.device_type
                    print(f"  -> Initialized separate mode for {primary_pad.name}.\n")

        # Interactive Cheat-Code Setup Wizard if requested
        if security_mgr and (args.set_code or not security_mgr.has_code(chosen_profile_name)):
            try:
                temp_fd = os.open(primary_pad.path, os.O_RDONLY | os.O_NONBLOCK)
                if not security_mgr.has_code(chosen_profile_name):
                    print(f"\n[Security Prompt] No unlock cheat-code found for {chosen_profile_name}.")
                    prompt_resp = input("  Would you like to record a secret button combination now? [Y/n]: ").strip().lower()
                    if prompt_resp in ("", "y", "yes"):
                        security_mgr.record_code_interactive(temp_fd, chosen_profile_name, primary_pad.name)
                elif args.set_code:
                    security_mgr.record_code_interactive(temp_fd, chosen_profile_name, primary_pad.name)
                    os.close(temp_fd)
                    return 0
                os.close(temp_fd)
            except OSError as err:
                print(f"[Warning] Could not access controller for cheat-code recording: {err}")

        active_profile = get_device_profile(chosen_profile_name, cfg)

        sens_multiplier = float(cfg.get("sensitivity", 1.0))
        if sens_multiplier != 1.0:
            active_profile.joystick.speed_x *= sens_multiplier
            active_profile.joystick.speed_y *= sens_multiplier

        try:
            run_controller_session(
                pads=controllers,
                profile=active_profile,
                security_mgr=security_mgr,
                logger=logger,
                rumble=rumble,
                auto_dormant=bool(cfg.get("auto_dormant_enabled", True)),
                exclusive_grab=not args.no_grab,
                disabled_modes=cfg.get("disabled_modes", [])
            )
        except KeyboardInterrupt:
            print("\nSession stopped by user.")
            break
        except PermissionError as error:
            print(f"\n[Permission Error] {error}")
            break

        if args.no_reconnect:
            break
        time.sleep(2.0)

    return 0


if __name__ == "__main__":
    sys.exit(main())
