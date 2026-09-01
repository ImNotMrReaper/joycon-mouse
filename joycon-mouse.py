#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Nintendo Switch Joy-Con & Multi-Gamepad Desktop Driver for Linux.
Location: joycon-mouse.py
"""

import argparse
import fcntl
import glob
import math
import os
import select
import struct
import subprocess
import sys
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

# Linux Input Constants & ioctls
EVENT_SYN = 0x00
EVENT_KEY = 0x01
EVENT_REL = 0x02
EVENT_ABS = 0x03
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

GAME_PROCESS_TARGETS = [
    "steamapps", "steam_app", "retroarch", "rpcs3", "dolphin-emu",
    "yuzu", "ryujinx", "pcsx2", "cemu", "heroic", "lutris"
]


def ioctl_code(direction: int, type_char: str, number: int, size: int) -> int:
    return (direction << 30) | (size << 16) | (ord(type_char) << 8) | number


def ioctl_none(type_char: str, number: int) -> int:
    return ioctl_code(0, type_char, number, 0)


def ioctl_write(type_char: str, number: int, size: int) -> int:
    return ioctl_code(1, type_char, number, size)


def eviocgname(length: int = 256) -> int:
    return (2 << 30) | (length << 16) | (ord('E') << 8) | 0x06


EVIOCGRAB = ioctl_write('E', 0x90, 4)

UI_SET_EVBIT = ioctl_write('U', 100, 4)
UI_SET_KEYBIT = ioctl_write('U', 101, 4)
UI_SET_RELBIT = ioctl_write('U', 102, 4)
UI_DEV_CREATE = ioctl_none('U', 1)
UI_DEV_DESTROY = ioctl_none('U', 2)
UI_DEV_SETUP = ioctl_write('U', 3, 92)

IS_64_BIT = struct.calcsize('P') == 8
EVENT_STRUCT_FORMAT = 'llHHi' if IS_64_BIT else 'iiHHi'
EVENT_STRUCT_SIZE = struct.calcsize(EVENT_STRUCT_FORMAT)


@dataclass
class MotionSettings:
    enabled: bool = True
    sensitivity_x: float = 0.048
    sensitivity_y: float = 0.048
    dead_zone: float = 2.0
    smoothing_factor: float = 0.30
    accel_exponent: float = 1.30
    vertical_orientation: bool = True
    invert_x: bool = False
    invert_y: bool = False
    calibration_frames: int = 60


@dataclass
class JoystickSettings:
    enabled: bool = True
    speed_x: float = 20.0
    speed_y: float = 20.0
    dead_zone: float = 0.14
    accel_exponent: float = 2.0
    invert_x: bool = False
    invert_y: bool = False


@dataclass
class DeviceProfile:
    name: str
    description: str
    motion: MotionSettings = field(default_factory=MotionSettings)
    joystick: JoystickSettings = field(default_factory=JoystickSettings)
    scroll_repeat_ms: int = 85


def is_game_active() -> Optional[str]:
    """Checks if a game or emulator is currently running."""
    for proc in GAME_PROCESS_TARGETS:
        try:
            out = subprocess.check_output(["pgrep", "-f", proc], stderr=subprocess.DEVNULL)
            if out.strip():
                return proc
        except Exception:
            pass
    return None


def get_device_profile(profile_name: str) -> DeviceProfile:
    titles = {
        "right_joycon": "Nintendo Switch Right Joy-Con (Vertical Air-Mouse)",
        "left_joycon": "Nintendo Switch Left Joy-Con (Vertical Air-Mouse)",
        "dual_joycon": "Nintendo Switch Combined Dual Joy-Cons (Grip / Split)",
        "switch_pro": "Nintendo Switch Pro Controller (USB / Bluetooth)",
        "playstation": "Sony PlayStation Controller (PS5 DualSense / PS4 / PS3)",
        "xbox": "Microsoft Xbox Controller (Xbox 360 / One / Series X/S)",
        "generic_gamepad": "Universal Gamepad (8BitDo / DirectInput / XInput)"
    }
    is_vertical = profile_name in ("right_joycon", "left_joycon")
    return DeviceProfile(
        name=profile_name,
        description=titles.get(profile_name, "Gamepad Controller"),
        motion=MotionSettings(enabled=True, vertical_orientation=is_vertical),
        joystick=JoystickSettings(enabled=True, speed_x=22.0, speed_y=22.0)
    )


class VirtualMouseDevice:
    """Manages virtual mouse and multimedia keyboard via /dev/uinput."""

    def __init__(self, device_name: str = "Joy-Con Modular Desktop Controller"):
        self.device_name = device_name
        self.file_descriptor: Optional[int] = None
        self.active_keys: Set[int] = set()
        self._initialize_device()

    def _initialize_device(self) -> None:
        candidate_paths = ["/dev/uinput", "/dev/input/uinput"]
        for path in candidate_paths:
            if os.path.exists(path):
                try:
                    self.file_descriptor = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
                    break
                except PermissionError:
                    raise PermissionError(
                        f"Cannot open {path}. Ensure user is in the 'input' group or run with appropriate permissions."
                    )
                except OSError:
                    continue

        if self.file_descriptor is None:
            raise FileNotFoundError(
                "Neither /dev/uinput nor /dev/input/uinput is accessible. Ensure 'uinput' kernel module is loaded."
            )

        fcntl.ioctl(self.file_descriptor, UI_SET_EVBIT, EVENT_SYN)
        fcntl.ioctl(self.file_descriptor, UI_SET_EVBIT, EVENT_KEY)
        fcntl.ioctl(self.file_descriptor, UI_SET_EVBIT, EVENT_REL)

        for relative_axis in [AXIS_REL_X, AXIS_REL_Y, AXIS_REL_WHEEL, AXIS_REL_HWHEEL]:
            fcntl.ioctl(self.file_descriptor, UI_SET_RELBIT, relative_axis)

        for mouse_btn in [MOUSE_BTN_LEFT, MOUSE_BTN_RIGHT, MOUSE_BTN_MIDDLE, MOUSE_BTN_BACK, MOUSE_BTN_FORWARD]:
            fcntl.ioctl(self.file_descriptor, UI_SET_KEYBIT, mouse_btn)

        for key in range(1, 256):
            try:
                fcntl.ioctl(self.file_descriptor, UI_SET_KEYBIT, key)
            except OSError:
                pass

        try:
            name_bytes = self.device_name.encode('utf-8')[:79].ljust(80, b'\x00')
            setup_struct = struct.pack('HHHH80sI', BUS_USB, 0x057E, 0x2009, 1, name_bytes, 0)
            fcntl.ioctl(self.file_descriptor, UI_DEV_SETUP, setup_struct)
            fcntl.ioctl(self.file_descriptor, UI_DEV_CREATE, 0)
        except OSError:
            name_bytes = self.device_name.encode('utf-8')[:79].ljust(80, b'\x00')
            user_dev = struct.pack('80sHHHHII', name_bytes, BUS_USB, 0x057E, 0x2009, 1, 0, 0) + (b'\x00' * 1024)
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


class MotionFilter:
    """Processes IMU gyroscope inputs into smooth cursor deltas with drift auto-calibration."""

    def __init__(self, config: MotionSettings, device_type: str):
        self.config = config
        self.device_type = device_type
        self.bias_x = 0.0
        self.bias_y = 0.0
        self.bias_z = 0.0
        self.calibrating = True
        self.sample_count = 0
        self.sum_x = 0.0
        self.sum_y = 0.0
        self.sum_z = 0.0
        self.smooth_dx = 0.0
        self.smooth_dy = 0.0
        self.subpixel_x = 0.0
        self.subpixel_y = 0.0
        self.gyro_axes = {"rx": 0.0, "ry": 0.0, "rz": 0.0}

    def update_axis(self, code: int, value: int) -> None:
        if code == 0x03:
            self.gyro_axes["rx"] = float(value)
        elif code == 0x04:
            self.gyro_axes["ry"] = float(value)
        elif code == 0x05:
            self.gyro_axes["rz"] = float(value)

    def process(self) -> Tuple[int, int]:
        if not self.config.enabled:
            return 0, 0

        gyro_x = self.gyro_axes["rx"]
        gyro_y = self.gyro_axes["ry"]
        gyro_z = self.gyro_axes["rz"]

        if self.calibrating:
            self.sum_x += gyro_x
            self.sum_y += gyro_y
            self.sum_z += gyro_z
            self.sample_count += 1
            if self.sample_count >= self.config.calibration_frames:
                self.bias_x = self.sum_x / self.sample_count
                self.bias_y = self.sum_y / self.sample_count
                self.bias_z = self.sum_z / self.sample_count
                self.calibrating = False
            return 0, 0

        clean_x = gyro_x - self.bias_x
        clean_y = gyro_y - self.bias_y
        clean_z = gyro_z - self.bias_z

        if self.config.vertical_orientation:
            if self.device_type == "right_joycon":
                raw_dx = -clean_z
                raw_dy = -clean_x
            elif self.device_type == "left_joycon":
                raw_dx = clean_z
                raw_dy = -clean_x
            else:
                raw_dx = -clean_z
                raw_dy = -clean_x
        else:
            raw_dx = -clean_y
            raw_dy = -clean_x

        if self.config.invert_x:
            raw_dx = -raw_dx
        if self.config.invert_y:
            raw_dy = -raw_dy

        magnitude = math.sqrt(raw_dx * raw_dx + raw_dy * raw_dy)
        if magnitude < self.config.dead_zone:
            self.smooth_dx = 0.0
            self.smooth_dy = 0.0
            return 0, 0

        direction_x = raw_dx / magnitude
        direction_y = raw_dy / magnitude
        effective_magnitude = magnitude - self.config.dead_zone
        scaled_magnitude = math.pow(effective_magnitude * self.config.sensitivity_x, self.config.accel_exponent)

        alpha = 1.0 - max(0.0, min(0.95, self.config.smoothing_factor))
        self.smooth_dx = (alpha * direction_x * scaled_magnitude) + ((1.0 - alpha) * self.smooth_dx)
        self.smooth_dy = (alpha * direction_y * scaled_magnitude) + ((1.0 - alpha) * self.smooth_dy)

        self.subpixel_x += self.smooth_dx
        self.subpixel_y += self.smooth_dy
        pixel_dx = int(self.subpixel_x)
        pixel_dy = int(self.subpixel_y)
        self.subpixel_x -= pixel_dx
        self.subpixel_y -= pixel_dy
        return pixel_dx, pixel_dy


class JoystickFilter:
    """Processes analog stick values with radial deadzone and acceleration curves."""

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
        curve = math.pow(effective_magnitude, self.config.accel_exponent)
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
    is_imu: bool
    device_type: str
    connection_type: str = "Bluetooth / Wireless"


def classify_device(device_name: str, event_path: str) -> Optional[ControllerNode]:
    name_lower = device_name.lower()
    if "virtual" in name_lower or "uinput" in name_lower:
        return None
    is_imu = any(keyword in name_lower for keyword in ["imu", "gyro", "motion", "sensor"])
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
        is_imu=is_imu,
        device_type=dev_type,
        connection_type=conn
    )


def discover_input_devices() -> List[Tuple[ControllerNode, Optional[ControllerNode]]]:
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
            device_name = buffer.split(b'\x00', 1)[0].decode('utf-8', errors='ignore').strip()
            os.close(descriptor)
        except OSError:
            continue

        if not device_name:
            continue

        node = classify_device(device_name, event_path)
        if node is not None:
            detected_nodes.append(node)

    pads = [node for node in detected_nodes if not node.is_imu]
    imus = [node for node in detected_nodes if node.is_imu]
    paired_list: List[Tuple[ControllerNode, Optional[ControllerNode]]] = []
    used_imu_paths: Set[str] = set()

    for pad in pads:
        matched_imu: Optional[ControllerNode] = None
        for imu in imus:
            if imu.path in used_imu_paths:
                continue
            if pad.device_type == imu.device_type or \
               ("right" in pad.name.lower() and "right" in imu.name.lower()) or \
               ("left" in pad.name.lower() and "left" in imu.name.lower()) or \
               ("(r)" in pad.name.lower() and "(r)" in imu.name.lower()) or \
               ("(l)" in pad.name.lower() and "(l)" in imu.name.lower()) or \
               ("pro controller" in pad.name.lower() and "pro controller" in imu.name.lower()) or \
               ("dualsense" in pad.name.lower() and "dualsense" in imu.name.lower()):
                matched_imu = imu
                used_imu_paths.add(imu.path)
                break
        paired_list.append((pad, matched_imu))

    return paired_list


def run_controller_session(
    pads: List[Tuple[ControllerNode, Optional[ControllerNode]]],
    profile: DeviceProfile,
    security_mgr: Optional[Any] = None,
    verbose: bool = False,
    exclusive_grab: bool = True
) -> None:
    """Runs the main event polling loop with auto-dormant detection and dynamic mode loading."""
    active_modes = load_all_modes()
    if not active_modes:
        print("[Error] No modes found in 'modes/' directory. Ensure mode files exist.")
        return

    uinput = VirtualMouseDevice(device_name=f"{profile.description} (Virtual Device)")
    open_descriptors: Dict[int, Tuple[ControllerNode, bool]] = {}
    poll_object = select.poll()

    motion_filters: Dict[str, MotionFilter] = {}
    joystick_filters: Dict[str, JoystickFilter] = {}

    for pad_node, imu_node in pads:
        try:
            pad_fd = os.open(pad_node.path, os.O_RDONLY | os.O_NONBLOCK)
            if exclusive_grab:
                try:
                    fcntl.ioctl(pad_fd, EVIOCGRAB, 1)
                except OSError:
                    pass
            open_descriptors[pad_fd] = (pad_node, False)
            poll_object.register(pad_fd, select.POLLIN | select.POLLERR | select.POLLHUP)
            joystick_filters[pad_node.path] = JoystickFilter(profile.joystick)
        except OSError:
            continue

        if imu_node is not None:
            try:
                imu_fd = os.open(imu_node.path, os.O_RDONLY | os.O_NONBLOCK)
                if exclusive_grab:
                    try:
                        fcntl.ioctl(imu_fd, EVIOCGRAB, 1)
                    except OSError:
                        pass
                open_descriptors[imu_fd] = (imu_node, True)
                poll_object.register(imu_fd, select.POLLIN | select.POLLERR | select.POLLHUP)
                motion_filters[imu_node.path] = MotionFilter(profile.motion, pad_node.device_type)
            except OSError:
                pass

    if not open_descriptors:
        return

    mode_index = 0
    total_modes = len(active_modes)
    active_scroll_direction = 0
    last_scroll_timestamp = 0.0
    last_tick_timestamp = time.time()
    last_media_seek_timestamp = 0.0
    last_game_check_time = time.time()

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
        for idx, (p_node, i_node) in enumerate(pads, 1):
            imu_info = f" + Motion IMU ({i_node.path})" if i_node is not None else " (No Gyro IMU)"
            print(f"   [{idx}] {p_node.name} [{p_node.connection_type}]")
            print(f"       Pad: {p_node.path}{imu_info}")
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
        print("\nTip: Enter secret combo anytime to unlock screen or fulfill sudo.")
        print("Tip: Tap Home/Capture for Super (Windows Key) | Hold >= 0.4s for Screenshot.")
        print("Tip: Auto-Dormant enabled (Releases controller automatically when games launch).")
        print("=" * 65 + "\n")

    print_status_banner()

    try:
        while True:
            now_time = time.time()

            # Auto-Dormant: Check for running games every 2 seconds
            if (now_time - last_game_check_time) > 2.0:
                last_game_check_time = now_time
                active_game = is_game_active()

                if active_game and not is_dormant:
                    is_dormant = True
                    set_grab_state(False)
                    print(f"\n>>> [Auto-Dormant] Game detected ({active_game}). Controller released to game.")
                elif not active_game and is_dormant:
                    is_dormant = False
                    set_grab_state(True)
                    print("\n>>> [Auto-Dormant] Game exited. Resuming Joy-Con desktop control.")
                    print_status_banner()

            if is_dormant:
                time.sleep(0.1)
                continue

            poll_events = poll_object.poll(8)

            for descriptor, mask in poll_events:
                if mask & (select.POLLERR | select.POLLHUP):
                    return

                if mask & select.POLLIN:
                    try:
                        raw_data = os.read(descriptor, EVENT_STRUCT_SIZE * 64)
                    except OSError:
                        return

                    node_info, is_imu = open_descriptors.get(descriptor, (None, False))
                    if node_info is None:
                        continue

                    total_events = len(raw_data) // EVENT_STRUCT_SIZE
                    for event_index in range(total_events):
                        offset = event_index * EVENT_STRUCT_SIZE
                        event_chunk = raw_data[offset: offset + EVENT_STRUCT_SIZE]
                        _, _, event_type, code, value = struct.unpack(EVENT_STRUCT_FORMAT, event_chunk)

                        if event_type == EVENT_KEY:
                            if value == 1 and security_mgr:
                                if security_mgr.process_key_event(code, node_info.device_type, uinput):
                                    continue

                            active_mode = get_current_mode()
                            button_map = active_mode.get_button_map(node_info.device_type)
                            action_config = button_map.get(code)

                            if verbose and action_config is None and value == 1:
                                print(f"[Hardware Key Event] Unmapped Code: {code} (Hex: 0x{code:03X}) on {node_info.name}")

                            if action_config is not None:
                                action_type = action_config.get("action")
                                target_code = action_config.get("code", 0)

                                if action_type == "mode_cycle" and value == 1:
                                    mode_index = (mode_index + 1) % total_modes
                                    print_status_banner()

                                elif action_type == "smart_home":
                                    if value == 1:
                                        smart_press_timestamp = time.time()
                                        smart_hold_triggered = False
                                    elif value == 0:
                                        if smart_press_timestamp is not None and not smart_hold_triggered:
                                            uinput.tap_key(KEY_CODE_LEFTMETA)
                                            print("[Smart Button] Tapped -> Home / Application Overview (Super Key)")
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
                                        last_scroll_timestamp = time.time()
                                    elif value == 0 and active_scroll_direction == action_config.get("param", 0):
                                        active_scroll_direction = 0

                        elif event_type == EVENT_ABS:
                            if is_imu:
                                m_filter = motion_filters.get(node_info.path)
                                if m_filter is not None:
                                    m_filter.update_axis(code, value)
                            else:
                                if code in (0x00, 0x01, 0x03, 0x04):
                                    j_filter = joystick_filters.get(node_info.path)
                                    if j_filter is not None:
                                        j_filter.update_axis(code, value)

            delta_time = now_time - last_tick_timestamp
            last_tick_timestamp = now_time

            if smart_press_timestamp is not None and not smart_hold_triggered:
                if (now_time - smart_press_timestamp) >= hold_threshold_sec:
                    uinput.tap_key(KEY_CODE_SYSRQ)
                    smart_hold_triggered = True
                    print("[Smart Button] Held -> Screenshot Captured (PrintScreen)")

            active_mode = get_current_mode()

            if active_mode.enable_motion or active_mode.enable_joystick_cursor:
                total_motion_dx = 0
                total_motion_dy = 0
                if active_mode.enable_motion:
                    for m_filter in motion_filters.values():
                        mdx, mdy = m_filter.process()
                        total_motion_dx += mdx
                        total_motion_dy += mdy

                total_joy_dx = 0
                total_joy_dy = 0
                if active_mode.enable_joystick_cursor:
                    for j_filter in joystick_filters.values():
                        jdx, jdy = j_filter.process(delta_time)
                        total_joy_dx += jdx
                        total_joy_dy += jdy

                if (total_motion_dx + total_joy_dx) != 0 or (total_motion_dy + total_joy_dy) != 0:
                    uinput.move_cursor(total_motion_dx + total_joy_dx, total_motion_dy + total_joy_dy)

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
                            print("[Media Seek] Forward +5s")
                        elif jdx < -4:
                            uinput.tap_key(KEY_CODE_LEFT)
                            last_media_seek_timestamp = now_time
                            print("[Media Seek] Rewind -5s")

    finally:
        for fd in open_descriptors.keys():
            try:
                if exclusive_grab:
                    fcntl.ioctl(fd, EVIOCGRAB, 0)
                os.close(fd)
            except OSError:
                pass
        uinput.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="joycon-mouse",
        description="Nintendo Switch Joy-Con & Multi-Gamepad Air-Mouse, Media Remote, and Secure Unlock Driver for Linux."
    )
    parser.add_argument("-l", "--list", action="store_true", help="List detected controllers and exit.")
    parser.add_argument("-p", "--profile", type=str, default=None,
                        choices=["right_joycon", "left_joycon", "dual_joycon", "switch_pro", "playstation", "xbox", "generic_gamepad"],
                        help="Force specific profile.")
    parser.add_argument("-s", "--sensitivity", type=float, default=1.0, help="Pointer sensitivity multiplier.")
    parser.add_argument("--set-code", action="store_true", help="Launch interactive wizard to set or change cheat-code.")
    parser.add_argument("--horizontal", action="store_true", help="Use horizontal grip orientation.")
    parser.add_argument("--no-grab", action="store_true", help="Disable exclusive device grabbing (not recommended with Steam).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print debug events and unmapped scan codes.")
    parser.add_argument("--no-reconnect", action="store_true", help="Do not wait and auto-reconnect on disconnect.")
    args = parser.parse_args()

    security_mgr = SecurityManager() if SecurityManager is not None else None
    controller_pairs = discover_input_devices()

    if args.list:
        print("\nDetected Controllers in /dev/input/event*:")
        for index, (pad_item, imu_item) in enumerate(controller_pairs, 1):
            imu_label = f" + Motion IMU ({imu_item.path})" if imu_item is not None else ""
            print(f"  [{index}] {pad_item.name} [{pad_item.connection_type}] ({pad_item.device_type}){imu_label} -> {pad_item.path}")
        if not controller_pairs:
            print("  No compatible Joy-Cons or Gamepads detected.")
            print("  Ensure Bluetooth pairing or USB connection is established.")
        print()
        return 0

    while True:
        controller_pairs = discover_input_devices()
        if not controller_pairs:
            print("[Waiting] No Joy-Cons or Gamepads detected. Turn on or plug in controller to connect...")
            time.sleep(2.0)
            continue

        primary_pad, _ = controller_pairs[0]
        chosen_profile_name = args.profile or primary_pad.device_type

        # Interactive Dual Joy-Con Pairing Detection
        if len(controller_pairs) >= 2 and not args.profile:
            has_left = any(p.device_type == "left_joycon" for p, _ in controller_pairs)
            has_right = any(p.device_type == "right_joycon" for p, _ in controller_pairs)
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

        active_profile = get_device_profile(chosen_profile_name)

        if args.horizontal:
            active_profile.motion.vertical_orientation = False
        if args.sensitivity != 1.0:
            active_profile.motion.sensitivity_x *= args.sensitivity
            active_profile.motion.sensitivity_y *= args.sensitivity
            active_profile.joystick.speed_x *= args.sensitivity
            active_profile.joystick.speed_y *= args.sensitivity

        try:
            run_controller_session(
                pads=controller_pairs,
                profile=active_profile,
                security_mgr=security_mgr,
                verbose=args.verbose,
                exclusive_grab=not args.no_grab
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
