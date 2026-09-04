#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Universal Modular Plugin Engine for Joy-Con Mouse.
Discovers, isolates, and manages built-in, custom, and community controller modes.
Location: modes/__init__.py
"""

import importlib.util
import inspect
import os
import sys
from typing import List, Optional, Set
from modes.base import BaseMode


def get_mode_search_directories(extra_dirs: Optional[List[str]] = None) -> List[str]:
    """Returns all directories searched for controller mode plugins."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    custom_repo_dir = os.path.join(project_root, "custom_modes")
    user_config_dir = os.path.expanduser("~/.config/joycon-mouse/custom_modes")

    search_paths = [base_dir, custom_repo_dir, user_config_dir]
    if extra_dirs:
        search_paths.extend(extra_dirs)

    # Return only existing unique directories
    existing: List[str] = []
    seen = set()
    for p in search_paths:
        abs_p = os.path.abspath(p)
        if abs_p not in seen and os.path.isdir(abs_p):
            seen.add(abs_p)
            existing.append(abs_p)
    return existing


def discover_all_modes(
    custom_dirs: Optional[List[str]] = None,
    disabled_modes: Optional[List[str]] = None
) -> List[BaseMode]:
    """
    Discovers all modular modes across core and custom plugin directories.
    Handles syntax errors gracefully, isolating faulty plugins without crashing.
    """
    discovered: List[BaseMode] = []
    seen_mode_classes: Set[str] = set()
    disabled_set = set(m.lower().strip() for m in (disabled_modes or []))

    search_dirs = get_mode_search_directories(custom_dirs)
    core_dir = os.path.dirname(os.path.abspath(__file__))

    for s_dir in search_dirs:
        is_custom_dir = (os.path.abspath(s_dir) != core_dir)
        try:
            entries = sorted(os.listdir(s_dir))
        except OSError:
            continue

        for fname in entries:
            if not fname.endswith(".py") or fname in ("__init__.py", "base.py"):
                continue

            file_path = os.path.join(s_dir, fname)
            module_name = f"joycon_mode_{os.path.splitext(fname)[0]}"

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None or spec.loader is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Search module for BaseMode subclasses
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseMode) and obj is not BaseMode:
                        cls_name = f"{obj.__module__}.{obj.__name__}"
                        if cls_name in seen_mode_classes:
                            continue
                        seen_mode_classes.add(cls_name)

                        instance: BaseMode = obj()
                        instance.file_path = file_path
                        instance.is_custom = is_custom_dir

                        # Check if mode is disabled by name, class, filename stem, or path
                        mode_stem = os.path.splitext(fname)[0].lower().strip()
                        mode_name = instance.name.lower().strip()
                        class_name = obj.__name__.lower().strip()

                        is_disabled = False
                        for d in disabled_set:
                            clean_d = d.strip()
                            if not clean_d:
                                continue
                            d_stem = os.path.splitext(os.path.basename(clean_d))[0].lower().strip()
                            if (clean_d in (mode_stem, mode_name, class_name) or
                                d_stem == mode_stem or
                                clean_d in mode_name or
                                clean_d in mode_stem or
                                mode_stem in clean_d):
                                is_disabled = True
                                break

                        instance.is_enabled = not is_disabled
                        discovered.append(instance)

            except Exception as e:
                print(f"[Plugin Warning] Could not load mode from '{file_path}': {e}")

    return discovered


def load_all_modes(disabled_modes: Optional[List[str]] = None) -> List[BaseMode]:
    """Returns only the enabled modes ready for active driver execution."""
    all_modes = discover_all_modes(disabled_modes=disabled_modes)
    enabled_modes = [m for m in all_modes if m.is_enabled]
    return enabled_modes


def create_mode_template(mode_name: str, target_dir: Optional[str] = None) -> str:
    """Scaffolds a new custom mode template ready for community contribution."""
    clean_name = mode_name.lower().replace(" ", "_").replace("-", "_")
    if not clean_name.endswith(".py"):
        filename = f"{clean_name}.py"
    else:
        filename = clean_name
        clean_name = filename[:-3]

    class_name = "".join(part.capitalize() for part in clean_name.split("_")) + "Mode"
    display_name = mode_name.replace("_", " ").replace("-", " ").title()

    dest_dir = target_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "custom_modes")
    os.makedirs(dest_dir, exist_ok=True)
    target_file = os.path.join(dest_dir, filename)

    if os.path.exists(target_file):
        raise FileExistsError(f"Mode file already exists at {target_file}")

    template_code = f'''#!/usr/bin/env python3
"""
Custom Community Mode: {display_name}
File: {filename}
"""

import os
import sys
from typing import Any, Dict

# Ensure project root is in sys.path for standalone testing
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from modes.base import (
    BaseMode,
    KEY_ESC, KEY_ENTER, KEY_SPACE, KEY_TAB, KEY_BACKSPACE,
    MOUSE_BTN_LEFT, MOUSE_BTN_RIGHT, MOUSE_BTN_MIDDLE,
    PAD_BTN_NORTH, PAD_BTN_SOUTH, PAD_BTN_WEST, PAD_BTN_EAST,
    PAD_BTN_TL, PAD_BTN_TR, PAD_BTN_TL2, PAD_BTN_TR2,
    PAD_BTN_HOME, PAD_BTN_CAPTURE, PAD_BTN_PLUS, PAD_BTN_MINUS,
    PAD_BTN_THUMBL, PAD_BTN_THUMBR,
    PAD_BTN_DPAD_UP, PAD_BTN_DPAD_DOWN, PAD_BTN_DPAD_LEFT, PAD_BTN_DPAD_RIGHT
)


class {class_name}(BaseMode):
    name = "{display_name}"
    description = "Custom controller mode for {display_name}."
    
    # Feature flags
    enable_joystick_cursor = False  # Set to True to enable analog stick mouse cursor
    enable_media_seek = False       # Set to True to enable analog stick media seeking
    enable_terminal_scroll = False  # Set to True to enable continuous terminal buffer scrolling

    def get_button_map(self, device_type: str) -> Dict[int, Dict[str, Any]]:
        """
        Map hardware controller button codes to virtual actions.
        Supported actions:
          - "key": Emit standard Linux keycode (e.g. KEY_SPACE, KEY_ENTER)
          - "mouse_btn": Emit mouse button (MOUSE_BTN_LEFT, MOUSE_BTN_RIGHT)
          - "scroll": Param 1 (Up) or -1 (Down)
          - "combo": Keys list, e.g. [KEY_LEFTCTRL, KEY_C]
          - "mode_cycle": Switch to next active mode
          - "smart_home": Tap: Super | Hold: Screenshot
        """
        # 1. Right Joy-Con Mapping
        if device_type == "right_joycon":
            return {{
                PAD_BTN_TR2: {{"action": "key", "code": KEY_SPACE, "desc": "ZR (Trigger) -> Space"}},
                PAD_BTN_TR: {{"action": "key", "code": KEY_ENTER, "desc": "R (Bumper) -> Enter"}},
                PAD_BTN_EAST: {{"action": "key", "code": KEY_ENTER, "desc": "A -> Enter / Confirm"}},
                PAD_BTN_SOUTH: {{"action": "key", "code": KEY_ESC, "desc": "B -> Escape / Cancel"}},
                PAD_BTN_NORTH: {{"action": "key", "code": KEY_TAB, "desc": "X -> Tab"}},
                PAD_BTN_WEST: {{"action": "key", "code": KEY_BACKSPACE, "desc": "Y -> Backspace"}},
                PAD_BTN_HOME: {{"action": "smart_home", "desc": "Home -> Tap: Super | Hold: Screenshot"}},
                PAD_BTN_PLUS: {{"action": "mode_cycle", "desc": "+ -> Cycle Mode"}},
            }}

        # 2. Left Joy-Con Mapping
        if device_type == "left_joycon":
            return {{
                PAD_BTN_TL2: {{"action": "key", "code": KEY_SPACE, "desc": "ZL (Trigger) -> Space"}},
                PAD_BTN_TL: {{"action": "key", "code": KEY_ENTER, "desc": "L (Bumper) -> Enter"}},
                PAD_BTN_DPAD_UP: {{"action": "key", "code": KEY_TAB, "desc": "D-Pad Up -> Tab"}},
                PAD_BTN_DPAD_DOWN: {{"action": "key", "code": KEY_BACKSPACE, "desc": "D-Pad Down -> Backspace"}},
                PAD_BTN_CAPTURE: {{"action": "smart_home", "desc": "Capture -> Tap: Super | Hold: Screenshot"}},
                PAD_BTN_MINUS: {{"action": "mode_cycle", "desc": "- -> Cycle Mode"}},
            }}

        # 3. Dual Joy-Cons & Standard Gamepads
        return {{
            PAD_BTN_TR2: {{"action": "key", "code": KEY_SPACE, "desc": "RT / R2 -> Space"}},
            PAD_BTN_SOUTH: {{"action": "key", "code": KEY_ENTER, "desc": "A / Cross -> Enter / Confirm"}},
            PAD_BTN_EAST: {{"action": "key", "code": KEY_ESC, "desc": "B / Circle -> Escape / Cancel"}},
            PAD_BTN_PLUS: {{"action": "mode_cycle", "desc": "Start / + -> Cycle Mode"}},
            PAD_BTN_HOME: {{"action": "smart_home", "desc": "Guide / Home -> Tap: Super | Hold: Screenshot"}},
        }}


if __name__ == "__main__":
    {class_name}().run_standalone()
'''

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(template_code)

    return target_file
