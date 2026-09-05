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

## 🛠️ What You Need on Your Device (Prerequisites)

Joy-Con Mouse requires **no external Python libraries** (`zero pip install`). To test and explore the code, here is what you will want on your computer:

### 1. Python 3 (Required)
* **Windows:**
  * Download from [python.org/downloads](https://www.python.org/downloads/) (or search "Python 3.12" in the Microsoft Store).
  * ⚠️ **CRITICAL FOR WINDOWS:** On the very first screen of the Python installer, check the box that says **"Add python.exe to PATH"** before clicking Install!
* **Mac:**
  * Download from [python.org/downloads](https://www.python.org/downloads/) or open Terminal and type `xcode-select --install`.
* **Linux / WSL:**
  * Pre-installed on almost all distros, or run: `sudo apt install python3`

### 2. Git (Recommended for getting updates & switching branches)
* **Windows:** Download from [git-scm.com/download/win](https://git-scm.com/download/win). (Click "Next" through the default installer options).
* **Mac:** Type `git` in Terminal; if not installed, macOS will prompt you to install it automatically.
* **Linux / WSL:** `sudo apt install git`

### 3. PyCharm Community Edition (Optional, but great for viewing & editing)
* Download **PyCharm Community Edition** (100% free and open-source) from [jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/).
* **How to open the project in PyCharm:**
  1. Open PyCharm > Click **Open** > Select the `joycon-mouse` folder.
  2. PyCharm will automatically detect your Python setup!
  3. **Switching branches in 1 click:** Look at the bottom-right corner of PyCharm (it says `main`). Click it, select `origin/windows` or `origin/macos`, and click **Checkout**!

---

## 🚀 How to Test on Your Operating System

### ⚡ Instant 1-Liner Install Commands

If your friends want to test right away without downloading zip files or manual cloning, share these 1-liner commands:

* **🪟 Windows (PowerShell):**
  ```powershell
  irm https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.ps1 | iex
  ```
  *(Installs Python if missing, creates Desktop & Start Menu shortcuts, and gets ready in seconds).*

* **🐧 Linux (Terminal):**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.sh | bash
  ```

* **🍎 macOS (Terminal):**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/macos/install.sh | bash
  ```

---

Joy-Con Mouse also maintains dedicated git branches tailored for each operating system:

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

### 🐧 WSL Setup (Windows Subsystem for Linux on Windows 10/11)

If you are running Ubuntu inside WSL on Windows:
* **Recommended for 99% of Users:** Run natively on Windows instead! Switching to the `windows` branch and double-clicking `run_windows.bat` controls your entire Windows screen directly with zero setup.
* **If testing inside WSL 2:**
  1. WSL 2 runs inside a virtual machine and cannot access Windows Bluetooth by default. To attach a USB Bluetooth dongle or controller to WSL, use Microsoft's [usbipd-win](https://github.com/dorssel/usbipd-win):
     ```powershell
     # In Windows PowerShell (Administrator):
     usbipd list
     usbipd wsl attach --busid <your-bus-id>
     ```
  2. Inside WSL, enable kernel uinput:
     ```bash
     sudo modprobe uinput
     ```
  3. Run the driver:
     ```bash
     joycon-mouse
     ```

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

## 🤖 Using AI Coding Assistants (Cursor, Copilot, Claude, ChatGPT)?

If you or your collaborators use AI coding assistants to explore or suggest changes to Joy-Con Mouse:

> [!IMPORTANT]
> **We have pre-configured AI guardrails in the repository root:**
> - [**`AGENTS.md`**](AGENTS.md): Complete architectural blueprint, extension points, and non-negotiables.
> - [**`.cursorrules`**](.cursorrules): Cursor IDE scope rules.
> - [**`CLAUDE.md`**](CLAUDE.md): Claude Code instructions.
> - [**`.github/copilot-instructions.md`**](.github/copilot-instructions.md): GitHub Copilot rules.

**What these files instruct any AI tool:**
1. **Never add external pip packages:** The project must stay 100% pure standard library.
2. **Never build bloated GUIs:** No Electron, PyQt, or Tkinter wrappers.
3. **Never hack shortcuts into the core loop:** All new actions must be created as modular mode plugins in `custom_modes/` inheriting from `BaseMode`.
4. **Keep OS backends cleanly isolated:** Linux kernel code stays on `main`, Windows ctypes on `windows`, macOS CoreGraphics on `macos`.

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
