# Project Contributors & Acknowledgments

Thank you to everyone who has contributed to the design, engineering, testing, and documentation of `joycon-mouse`!

---

## 👥 Core Team & Maintainers

| Contributor | GitHub | Role | Primary Platform |
| :--- | :--- | :--- | :--- |
| **Mr. Reaper** | [@ImNotMrReaper](https://github.com/ImNotMrReaper) | Creator & Lead Architect | Linux (Ubuntu / Wayland / `evdev`) |
| **Senpai59** | [@Senpai59](https://github.com/Senpai59) | Windows Lead Tester & Contributor | Windows (Win10/11 / `winmm` / `ctypes`) |

---

## 🎯 Platform Responsibilities

### Linux (Mainline)
- **Architect:** @ImNotMrReaper
- **Focus:** Low-level `uinput` virtual device creation, kernel `evdev` hardware polling, systemd daemon management, Wayland/X11 integration, and zero-redundancy controller layouts.

### Windows (`windows` branch)
- **Lead Tester:** @Senpai59
- **Focus:** Native Windows hardware testing, Bluetooth Joy-Con pairing stability, `ctypes.windll.winmm` low-latency polling, deadzone calibration, and 1-click batch installers.

---

## 🤝 Becoming a Contributor
We welcome community contributions! Please review [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) before submitting Pull Requests.
