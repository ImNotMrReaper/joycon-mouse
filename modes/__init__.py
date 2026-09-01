#!/usr/bin/env python3
# noinspection SpellCheckingInspection,PyUnusedLocal,PyBroadException
"""
Dynamic Plugin Auto-Loader for Modes.
Location: modes/__init__.py
"""

import importlib
import os
import pkgutil
from typing import List
from modes.base import BaseMode


def load_all_modes() -> List[BaseMode]:
    """Dynamically discovers and loads all BaseMode subclasses in the modes folder."""
    discovered: List[BaseMode] = []
    package_dir = os.path.dirname(__file__)

    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name in ("base", "__init__"):
            continue
        try:
            module = importlib.import_module(f"modes.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseMode) and attr is not BaseMode:
                    discovered.append(attr())
        except Exception as e:
            print(f"[Plugin Warning] Failed to load mode '{module_name}': {e}")

    return discovered
