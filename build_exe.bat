@echo off
setlocal EnableDelayedExpansion
title Joy-Con Mouse - Standalone Executable (.exe) Builder
color 0E
cls

echo ================================================================================
echo   📦 JOY-CON MOUSE STANDALONE EXECUTABLE BUILDER
echo   Builds a single standalone JoyConMouse.exe for Windows 10/11
echo ================================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is required to build the executable!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import PyInstaller" >nul 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller is not currently installed.
    set /p "INSTALL_PI=Would you like to install PyInstaller now via pip? [Y/n]: "
    if /i "!INSTALL_PI!"=="" set "INSTALL_PI=Y"
    if /i "!INSTALL_PI!"=="Y" (
        pip install --upgrade pyinstaller
    ) else (
        echo Cannot proceed without PyInstaller.
        pause
        exit /b 1
    )
)

echo.
echo Building standalone executable 'JoyConMouse.exe'...
echo (This may take 30-60 seconds)...
echo.

pyinstaller --onefile --noconsole --name "JoyConMouse" "%~dp0joycon-mouse-windows.py"

if exist "dist\JoyConMouse.exe" (
    copy "dist\JoyConMouse.exe" "%~dp0JoyConMouse.exe" >nul
    echo.
    echo ================================================================================
    echo   [SUCCESS] Standalone executable created successfully!
    echo   Location: %~dp0JoyConMouse.exe
    echo ================================================================================
    echo.
    echo You can now send or copy JoyConMouse.exe to any Windows computer.
    echo It runs completely standalone with zero dependencies!
) else (
    echo.
    echo [ERROR] Build failed. Please check the PyInstaller log output above.
)

pause
exit /b 0
