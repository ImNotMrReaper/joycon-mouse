@echo off
setlocal EnableDelayedExpansion
title Joy-Con Mouse - 1-Click Windows Installer
color 0B
cls

echo ================================================================================
echo   🎮 JOY-CON MOUSE 1-CLICK WINDOWS INSTALLER
echo   Transform Switch Joy-Cons into a wireless PC mouse and media remote!
echo ================================================================================
echo.

set "INSTALL_DIR=%~dp0"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"

:: Step 1: Check Python installation
echo [Step 1/4] Checking Python environment...

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=python"
    echo   [OK] Python detected in system PATH.
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_CMD=py"
        echo   [OK] Python launcher (py) detected.
    ) else (
        echo   [!] Python 3 was not found on your PC.
        echo.
        where winget >nul 2>nul
        if %errorlevel% equ 0 (
            echo   Windows Package Manager (winget) is available!
            set /p "AUTO_INSTALL=  Would you like to automatically install Python 3.12 now? [Y/n]: "
            if /i "!AUTO_INSTALL!"=="" set "AUTO_INSTALL=Y"
            if /i "!AUTO_INSTALL!"=="Y" (
                echo.
                echo   Installing Python 3.12 via winget (please allow any Windows security prompt)...
                winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
                echo.
                echo   [OK] Python installed! Please restart this installer so PATH refreshes.
                pause
                exit /b 0
            )
        )
        echo.
        echo   Opening the official Python downloads page in your browser...
        echo   IMPORTANT: Make sure to check the box "Add python.exe to PATH" during setup!
        start https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

:: Step 2: Create AppData directory & default configuration
echo.
echo [Step 2/4] Setting up user configuration...
set "CONFIG_DIR=%APPDATA%\joycon-mouse"
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

if not exist "%CONFIG_DIR%\config.json" (
    (
        echo {
        echo   "sensitivity": 1.0,
        echo   "deadzone": 0.10,
        echo   "rumble": true,
        echo   "disabled_modes": []
        echo }
    ) > "%CONFIG_DIR%\config.json"
    echo   [OK] Created default configuration at %CONFIG_DIR%\config.json
) else (
    echo   [OK] Existing user configuration preserved.
)

:: Step 3: Create Desktop & Start Menu Shortcuts via PowerShell
echo.
echo [Step 3/4] Creating Windows shortcuts...
set "TARGET_RUNNER=%INSTALL_DIR%\run_windows.bat"

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; " ^
  "$desk = [Environment]::GetFolderPath('Desktop'); " ^
  "$s1 = $ws.CreateShortcut(\"$desk\Joy-Con Mouse.lnk\"); " ^
  "$s1.TargetPath = '%TARGET_RUNNER%'; " ^
  "$s1.WorkingDirectory = '%INSTALL_DIR%'; " ^
  "$s1.Description = 'Nintendo Switch Joy-Con Desktop Mouse & Media Remote'; " ^
  "$s1.IconLocation = '%SystemRoot%\System32\shell32.dll,24'; " ^
  "$s1.Save(); " ^
  "$startMenu = [Environment]::GetFolderPath('Programs'); " ^
  "$s2 = $ws.CreateShortcut(\"$startMenu\Joy-Con Mouse.lnk\"); " ^
  "$s2.TargetPath = '%TARGET_RUNNER%'; " ^
  "$s2.WorkingDirectory = '%INSTALL_DIR%'; " ^
  "$s2.Description = 'Nintendo Switch Joy-Con Desktop Mouse & Media Remote'; " ^
  "$s2.IconLocation = '%SystemRoot%\System32\shell32.dll,24'; " ^
  "$s2.Save();"

if %errorlevel% equ 0 (
    echo   [OK] Created Desktop shortcut: "Joy-Con Mouse"
    echo   [OK] Created Start Menu shortcut in Programs
) else (
    echo   [!] Warning: Could not create shortcuts automatically. You can always run run_windows.bat directly.
)

:: Step 4: Installation complete!
echo.
echo ================================================================================
echo   [SUCCESS] JOY-CON MOUSE IS INSTALLED!
echo ================================================================================
echo.
echo   You can now launch Joy-Con Mouse anytime from your Desktop shortcut
echo   or by double-clicking 'run_windows.bat'.
echo.

set /p "LAUNCH_NOW=Would you like to start Joy-Con Mouse right now? [Y/n]: "
if /i "%LAUNCH_NOW%"=="" set "LAUNCH_NOW=Y"
if /i "%LAUNCH_NOW%"=="Y" (
    start "" "%INSTALL_DIR%\run_windows.bat"
)
exit /b 0
