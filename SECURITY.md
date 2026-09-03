# 🔒 Security Policy

## Supported Versions

| Version | Supported          |
| :--- | :---: |
| `1.1.x` | :white_check_mark: |
| `1.0.x` | :white_check_mark: |
| `< 1.0` | :x: |

---

## 🛡️ Security Architecture & Philosophy

Joy-Con Mouse is designed with privacy and system safety at its core:

1. **100% Offline & Zero Telemetry**: Joy-Con Mouse makes zero network calls, contains no tracking libraries, and requires no external third-party dependencies.
2. **Hardware Device Isolation (`EVIOCGRAB`)**: When polling controllers, Joy-Con Mouse optionally applies exclusive device grabbing (`EVIOCGRAB`) so other background user-space processes cannot intercept raw controller scancodes.
3. **Optional Credential Encryption (`security_manager.py`)**:
   - If using the optional cheat-code password injection module, credentials are encrypted using AES-style PBKDF2 HMAC-SHA256 derived keys tied to the host's `/etc/machine-id`.
   - Credentials are kept exclusively in `~/.config/joycon-mouse/` and are strictly ignored in `.gitignore`.
4. **Least Privilege**: The driver runs as a regular user via standard Linux `input` group membership; root privileges are never required for active background execution.

---

## 📬 Reporting a Vulnerability

If you discover a potential security vulnerability in Joy-Con Mouse:
1. **Please do not open a public GitHub Issue.**
2. Report the vulnerability privately via GitHub Security Advisories or contact the repository owner directly.
3. Include detailed steps to reproduce the issue, along with relevant kernel version and distribution details.

Security reports will be reviewed promptly, and patches will be released in a timely manner.
