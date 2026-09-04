@echo off
title Joy-Con Mouse for Windows (Beta Preview)
color 0B
cls

echo ================================================================================
echo   🎮 JOY-CON MOUSE FOR WINDOWS (Beta Preview)
echo   Double-click launcher for Windows 10/11
echo ================================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Python is not installed or not in your system PATH!
        echo Please install Python from https://www.python.org/downloads/
        echo (Make sure to check "Add Python to PATH" during installation)
        echo.
        pause
        exit /b 1
    ) else (
        set PYCMD=py
    )
) else (
    set PYCMD=python
)

echo [OK] Python detected! Launching Joy-Con Mouse driver...
echo.
%PYCMD% "%~dp0joycon-mouse-windows.py" %*

if %errorlevel% neq 0 (
    echo.
    echo Driver stopped with an error code: %errorlevel%
    pause
)
