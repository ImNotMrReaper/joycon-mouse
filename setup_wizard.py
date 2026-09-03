#!/usr/bin/env python3
"""
Interactive Setup Wizard for Joy-Con Mouse & Universal Remote for Linux.
Guides users through mode selection, pointer sensitivity, rumble, and autostart daemon.
Location: setup_wizard.py
"""

import json
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional

# Add project root to sys.path
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# ANSI Styling helpers
BOLD = "\033[1m"
CYAN = "\033[96m"
PURPLE = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner(title: str, subtitle: Optional[str] = None) -> None:
    print("\n" + "=" * 76)
    print(f"  {BOLD}{PURPLE}🎮 {title}{RESET}")
    if subtitle:
        print(f"  {CYAN}{subtitle}{RESET}")
    print("=" * 76 + "\n")


def prompt_choice(prompt_text: str, default: str) -> str:
    """Prompts user with a default value. Safe against EOFError and KeyboardInterrupt."""
    try:
        val = input(f"{BOLD}{prompt_text}{RESET} [{GREEN}{default}{RESET}]: ").strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return default


def get_config_paths() -> tuple[str, str]:
    config_dir = os.path.expanduser("~/.config/joycon-mouse")
    config_file = os.path.join(config_dir, "config.json")
    return config_dir, config_file


def load_config() -> Dict[str, Any]:
    default_config: Dict[str, Any] = {
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
    _, config_file = get_config_paths()
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                default_config.update(data)
        except Exception:
            pass
    return default_config


def save_config(cfg: Dict[str, Any]) -> None:
    config_dir, config_file = get_config_paths()
    os.makedirs(config_dir, exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)


def setup_modes(cfg: Dict[str, Any]) -> None:
    """Interactive mode toggle picker."""
    from modes import discover_all_modes

    disabled_modes = list(cfg.get("disabled_modes", []))

    while True:
        discovered = discover_all_modes(disabled_modes=disabled_modes)
        if not discovered:
            print(f"{YELLOW}No controller modes discovered in modes/ or custom_modes/.{RESET}\n")
            return

        print(f"{BOLD}{CYAN}Step 1: Choose Active Controller Modes{RESET}")
        print(f"{DIM}Cycle through enabled modes anytime with the '+' or '-' button.{RESET}\n")

        for idx, m in enumerate(discovered, 1):
            status_tag = f"{GREEN}[✓ ENABLED]{RESET}" if m.is_enabled else f"{RED}[✗ DISABLED]{RESET}"
            type_tag = f"{PURPLE}(Custom){RESET}" if m.is_custom else f"{DIM}(Built-in){RESET}"
            print(f"  {BOLD}[{idx}]{RESET} {status_tag} {BOLD}{m.name:<32}{RESET} {type_tag}")
            print(f"      {DIM}Description:{RESET} {m.description}")

        print("\n  " + "-" * 72)
        print(f"  {BOLD}Commands:{RESET} Enter number {BOLD}[1-{len(discovered)}]{RESET} to toggle on/off")
        print(f"            Type {BOLD}'all'{RESET} to enable all | Type {BOLD}'done'{RESET} or press {BOLD}[ENTER]{RESET} to continue")
        print("  " + "-" * 72)

        ans = prompt_choice("  Toggle mode or continue", "done").lower()

        if ans in ("done", ""):
            break
        elif ans == "all":
            disabled_modes = []
            print(f"\n{GREEN}✓ Enabled all controller modes.{RESET}\n")
            continue

        try:
            choice_num = int(ans)
            if 1 <= choice_num <= len(discovered):
                target_mode = discovered[choice_num - 1]
                norm_name = target_mode.name.lower().strip()
                norm_file = os.path.splitext(os.path.basename(target_mode.file_path))[0].lower().strip() if target_mode.file_path else ""

                if target_mode.is_enabled:
                    # Disable it
                    if norm_file and norm_file not in disabled_modes:
                        disabled_modes.append(norm_file)
                    elif norm_name not in disabled_modes:
                        disabled_modes.append(norm_name)
                    print(f"\n{YELLOW}Disabled '{target_mode.name}'{RESET}\n")
                else:
                    # Enable it
                    disabled_modes = [d for d in disabled_modes if d.lower() not in (norm_name, norm_file)]
                    print(f"\n{GREEN}Enabled '{target_mode.name}'{RESET}\n")
            else:
                print(f"{RED}Please enter a number between 1 and {len(discovered)}.{RESET}\n")
        except ValueError:
            print(f"{RED}Invalid input. Enter a number, 'all', or press [ENTER] when done.{RESET}\n")

    cfg["disabled_modes"] = disabled_modes


def setup_sensitivity(cfg: Dict[str, Any]) -> None:
    """Interactive pointer sensitivity selection."""
    print(f"\n{BOLD}{CYAN}Step 2: Pointer Speed & Mouse Sensitivity{RESET}")
    print(f"{DIM}Adjusts how fast the mouse cursor travels across your screen.{RESET}\n")

    current_sens = float(cfg.get("sensitivity", 1.0))
    print(f"  Current sensitivity: {BOLD}{current_sens}x{RESET}\n")
    print(f"  {BOLD}[1] Balanced (1.0x){RESET}          - Standard pointer speed with smooth acceleration {GREEN}(Recommended){RESET}")
    print(f"  {BOLD}[2] Precision / Casual (0.7x){RESET} - Slower, highly precise cursor for fine clicking")
    print(f"  {BOLD}[3] High-DPI / Fast (1.4x){RESET}    - Quick pointer navigation for 2K/4K displays")
    print(f"  {BOLD}[4] Custom Multiplier{RESET}        - Enter your own decimal value (e.g. 1.25)\n")

    ans = prompt_choice("  Select sensitivity preset [1-4]", "1")

    if ans == "1":
        cfg["sensitivity"] = 1.0
        print(f"{GREEN}✓ Set sensitivity to 1.0x (Balanced).{RESET}\n")
    elif ans == "2":
        cfg["sensitivity"] = 0.7
        print(f"{GREEN}✓ Set sensitivity to 0.7x (Precision).{RESET}\n")
    elif ans == "3":
        cfg["sensitivity"] = 1.4
        print(f"{GREEN}✓ Set sensitivity to 1.4x (High-DPI).{RESET}\n")
    elif ans == "4":
        while True:
            custom_val = prompt_choice("  Enter custom sensitivity multiplier (0.2 - 5.0)", "1.0")
            try:
                sens = float(custom_val)
                if 0.1 <= sens <= 10.0:
                    cfg["sensitivity"] = sens
                    print(f"{GREEN}✓ Set sensitivity to {sens}x.{RESET}\n")
                    break
                else:
                    print(f"{RED}Please enter a realistic sensitivity value between 0.2 and 5.0.{RESET}")
            except ValueError:
                print(f"{RED}Invalid decimal number. Example: 1.25{RESET}")
    else:
        cfg["sensitivity"] = 1.0
        print(f"{GREEN}✓ Set sensitivity to 1.0x (Default).{RESET}\n")


def setup_rumble(cfg: Dict[str, Any]) -> None:
    """Interactive haptic feedback toggle."""
    print(f"{BOLD}{CYAN}Step 3: Controller Rumble & Physical Haptics{RESET}")
    print(f"{DIM}Provides subtle physical vibration clicks when switching modes or taking screenshots.{RESET}\n")

    current_rumble = bool(cfg.get("rumble_enabled", True))
    current_str = "Enabled" if current_rumble else "Disabled"
    print(f"  Current setting: {BOLD}{current_str}{RESET}\n")
    print(f"  {BOLD}[1] Enabled{RESET}  - Physical vibration clicks on mode cycle & actions {GREEN}(Recommended){RESET}")
    print(f"  {BOLD}[2] Disabled{RESET} - Silent operation and maximum controller battery life\n")

    ans = prompt_choice("  Select rumble option [1-2]", "1" if current_rumble else "2")

    if ans == "1":
        cfg["rumble_enabled"] = True
        print(f"{GREEN}✓ Controller rumble enabled.{RESET}\n")
    elif ans == "2":
        cfg["rumble_enabled"] = False
        print(f"{YELLOW}✓ Controller rumble disabled.{RESET}\n")
    else:
        cfg["rumble_enabled"] = True
        print(f"{GREEN}✓ Controller rumble enabled (Default).{RESET}\n")


def setup_systemd_service() -> None:
    """Interactive autostart background daemon configuration."""
    print(f"{BOLD}{CYAN}Step 4: Automatic Background Startup (Systemd){RESET}")
    print(f"{DIM}Automatically runs Joy-Con Mouse in the background whenever you log into Linux.{RESET}\n")

    # Check current systemd service status
    is_active = False
    try:
        res = subprocess.run(
            ["systemctl", "--user", "is-enabled", "joycon-mouse.service"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        is_active = (res.returncode == 0)
    except Exception:
        pass

    status_str = f"{GREEN}Enabled & Auto-Starting{RESET}" if is_active else f"{DIM}Disabled (Manual Start Only){RESET}"
    print(f"  Current background status: {status_str}\n")
    print(f"  {BOLD}[1] Auto-start in background on login{RESET} {GREEN}(Recommended){RESET}")
    print(f"      Seamlessly connects when you press any Joy-Con button. Zero terminal needed.")
    print(f"  {BOLD}[2] Manual start only{RESET}")
    print(f"      Run 'joycon-mouse' in the terminal only when you want to use it.\n")

    ans = prompt_choice("  Select startup mode [1-2]", "1")

    if ans == "1":
        try:
            # Check for joycon-mouse binary or script
            main_script = os.path.join(_project_root, "joycon-mouse.py")
            cmd = ["python3", main_script, "--install-service"]
            subprocess.run(cmd, check=True)
            print(f"{GREEN}✓ Background systemd service enabled and started successfully.{RESET}\n")
        except Exception as e:
            print(f"{YELLOW}Could not enable systemd service automatically: {e}{RESET}\n")
    elif ans == "2":
        try:
            main_script = os.path.join(_project_root, "joycon-mouse.py")
            cmd = ["python3", main_script, "--uninstall-service"]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{YELLOW}✓ Background service disabled. Run 'joycon-mouse' manually anytime.{RESET}\n")
        except Exception:
            pass


def run_setup_wizard() -> int:
    """Executes the complete guided setup workflow."""
    print_banner(
        "Joy-Con Mouse Interactive Setup Wizard",
        "Configure your controller modes, sensitivity, rumble, and startup behavior"
    )

    cfg = load_config()

    try:
        # Step 1: Modes
        setup_modes(cfg)

        # Step 2: Sensitivity
        setup_sensitivity(cfg)

        # Step 3: Rumble
        setup_rumble(cfg)

        # Step 4: Systemd Autostart
        setup_systemd_service()

        # Save configuration
        save_config(cfg)

        # Final Summary
        _, cfg_file = get_config_paths()
        print("=" * 76)
        print(f"  {GREEN}{BOLD}🎉 CONFIGURATION SAVED SUCCESSFULLY!{RESET}")
        print(f"  {DIM}Saved to: {cfg_file}{RESET}")
        print("=" * 76)
        print(f"  • Sensitivity:    {BOLD}{cfg.get('sensitivity', 1.0)}x{RESET}")
        print(f"  • Haptic Rumble:  {BOLD}{'Enabled' if cfg.get('rumble_enabled', True) else 'Disabled'}{RESET}")
        disabled = cfg.get("disabled_modes", [])
        if disabled:
            print(f"  • Disabled Modes: {YELLOW}{', '.join(disabled)}{RESET}")
        else:
            print(f"  • Active Modes:   {GREEN}All modes enabled{RESET}")
        print("-" * 76)
        print(f"  💡 {BOLD}Quick Commands:{RESET}")
        print(f"  • Start driver manually:       {CYAN}joycon-mouse{RESET}")
        print(f"  • List detected controllers:   {CYAN}joycon-mouse -l{RESET}")
        print(f"  • Live button test diagnostic: {CYAN}joycon-mouse --test-buttons{RESET}")
        print(f"  • Re-run this setup wizard:    {CYAN}joycon-mouse --setup{RESET}")
        print("=" * 76 + "\n")

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Setup wizard cancelled by user. Current settings were preserved.{RESET}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_setup_wizard())
