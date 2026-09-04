# 🧪 Joy-Con Mouse Beta Tester & Collaborator Guide

Welcome to the **Joy-Con Mouse** testing team! 🎮

You do **not** need to know how to write code, install complex developer software, or know anything about AI to help test and improve this project. Testing real hardware in real environments (Windows, Mac, and Linux) is one of the most critical parts of open-source software.

This guide walks you through testing, customizing your controller without coding, and sharing your feedback so you can be credited as an official contributor!

---

## 🎯 Project Scope & Guardrails (Staying on Target)

To keep Joy-Con Mouse fast, clean, and reliable, our project follows three core rules:

* **✅ What We DO:**
  * Turn standard Joy-Cons and gamepads into a fast, wireless mouse and couch media remote.
  * Keep everything **zero extra downloads** (pure Python standard library—no huge software suites, no bloatware, no sketchy third-party drivers).
  * Make controller modes modular so anyone can toggle or customize their button presets.
* **❌ What We DON'T DO (Off-Scope):**
  * We don't build heavy electron/browser GUI wrappers that eat 500MB of RAM.
  * We don't make game cheat engines or aimbots.
  * We don't require external AI installations or cloud subscriptions. Everything runs 100% locally and offline.

---

## 🚀 How to Test on Your Operating System

Joy-Con Mouse has dedicated branches tailored for each operating system:

| Operating System | GitHub Branch | Pairing Method | Launch Command |
| :--- | :--- | :--- | :--- |
| **Linux (Ubuntu, Arch, Steam Deck)** | `main` | Bluetooth Settings | `./install.sh` or `joycon-mouse` |
| **Windows 10 / 11** | `windows` | Windows Bluetooth Settings | Double-click `run_windows.bat` |
| **macOS (Sonoma, Ventura, Monterey)**| `macos` | System Settings > Bluetooth | Double-click `run_macos.command` |

---

### 🪟 Windows Setup (Windows 10 & 11)

1. **Pair your Joy-Con:**
   * On your Joy-Con, hold down the small round **Sync button** on the black side-rail until the green lights start flashing up and down.
   * On Windows: Open **Settings** > **Bluetooth & devices** > **Add device** > **Bluetooth**.
   * Select **Joy-Con (R)** or **Joy-Con (L)** from the list.
2. **Download or Switch to the `windows` branch:**
   * Visit the repository on GitHub: `https://github.com/ImNotMrReaper/joycon-mouse/tree/windows`
   * Click the green **Code** button > **Download ZIP** and extract it (or `git checkout windows`).
3. **Launch the Driver:**
   * Make sure Python is installed (from [python.org](https://www.python.org/downloads/) or the Windows Microsoft Store).
   * Double-click **`run_windows.bat`**.
   * Move the Joy-Con analog stick: Your mouse pointer will glide across the screen!

---

### 🍎 Mac Setup (macOS 12+ Monterey, Ventura, Sonoma, Sequoia)

1. **Pair your Joy-Con:**
   * Hold down the small round **Sync button** on the Joy-Con side-rail until the green lights cycle.
   * Open **System Settings** > **Bluetooth**.
   * Look under "Nearby Devices" and click **Connect** next to Joy-Con.
2. **Download or Switch to the `macos` branch:**
   * Visit `https://github.com/ImNotMrReaper/joycon-mouse/tree/macos`.
   * Download the ZIP and extract it (or `git checkout macos`).
3. **Grant Accessibility Permission (Required for any Mac mouse utility):**
   * Go to **System Settings** > **Privacy & Security** > **Accessibility**.
   * Make sure **Terminal** (or your Python runner) is allowed to control your computer.
4. **Launch the Driver:**
   * Double-click **`run_macos.command`** (or open Terminal, navigate to the folder, and run `python3 joycon-mouse-macos.py`).

---

## 🎨 Customizing Your Controls (Without Writing Code!)

You don't need to write code to change how your Joy-Con behaves. All user settings are stored in a simple configuration file:

* **Windows:** `%APPDATA%\joycon-mouse\config.json` (or in the app folder)
* **Mac:** `~/Library/Application Support/joycon-mouse/config.json`
* **Linux:** `~/.config/joycon-mouse/config.json`

### Example `config.json` (You can edit these numbers with Notepad or TextEdit!):

```json
{
  "sensitivity": 1.2,
  "deadzone": 0.08,
  "rumble": true,
  "disabled_modes": [
    "terminal"
  ]
}
```

* **`sensitivity`**: Change `1.0` to `1.5` to make the cursor faster, or `0.8` to make it slower and more precise.
* **`deadzone`**: If your analog stick has slight hardware drift, increase `0.08` to `0.12` or `0.15`.
* **`disabled_modes`**: Don't need the terminal mode? Add `"terminal"` to disable it and keep only the mouse and media remote!

---

## 📝 How to Submit Your Test Review

Whenever you test a controller, let us know how it felt!

### Option A: The 1-Click GitHub Review Form (Recommended)
1. Head to [**GitHub Issues**](https://github.com/ImNotMrReaper/joycon-mouse/issues).
2. Click **New Issue** > **Beta Tester Feedback & Review** (Click *Get Started*).
3. Check the boxes for your OS and controller, rate the sensitivity, and share any notes!

### Option B: Send a Quick Review Directly to Mr. Reaper
If you don't use GitHub, just message your feedback directly (Discord, text, DM):
* *What OS did you test? (Windows 11, Mac, etc.)*
* *Which controller? (Right Joy-Con, Left Joy-Con, Pair)*
* *Did the mouse glide smoothly?*
* *Were the buttons easy to press?*
* *What should we add or tweak next?*

Mr. Reaper will review your notes, push any needed adjustments, and officially record your test review on GitHub!

---

## 🌟 Contributor Recognition

Every tester who provides hardware reports, catches bugs, or helps shape mode layouts is officially recognized on the project:

* **README Shoutout:** Added to the **Contributors & Community Testers** wall in the main project `README.md`.
* **Release Notes:** Credited in the official GitHub Release announcements and `CHANGELOG.md`.
* **GitHub Collaborator:** Optionally invited to the GitHub repository as a recognized collaborator!

Thank you for helping bring Joy-Con Mouse to gamers, couch streamers, and productivity enthusiasts worldwide! 🚀
