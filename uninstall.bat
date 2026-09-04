@echo off
setlocal EnableDelayedExpansion
title Joy-Con Mouse - Windows Uninstaller
color 0C
cls

echo ================================================================================
echo   🗑️  JOY-CON MOUSE WINDOWS UNINSTALLER
echo ================================================================================
echo.

set /p "CONFIRM=Are you sure you want to uninstall Joy-Con Mouse? [y/N]: "
if /i not "%CONFIRM%"=="Y" (
    echo.
    echo Uninstallation cancelled. Joy-Con Mouse remains installed.
    pause
    exit /b 0
)

echo.
echo Removing shortcuts...

:: Remove Desktop Shortcut
powershell -NoProfile -Command ^
  "$desk = [Environment]::GetFolderPath('Desktop'); " ^
  "$file = Join-Path $desk 'Joy-Con Mouse.lnk'; " ^
  "if (Test-Path $file) { Remove-Item $file -Force; Write-Host '  [OK] Removed Desktop shortcut.' }"

:: Remove Start Menu Shortcut
powershell -NoProfile -Command ^
  "$prog = [Environment]::GetFolderPath('Programs'); " ^
  "$file = Join-Path $prog 'Joy-Con Mouse.lnk'; " ^
  "if (Test-Path $file) { Remove-Item $file -Force; Write-Host '  [OK] Removed Start Menu shortcut.' }"

echo.
set "CONFIG_DIR=%APPDATA%\joycon-mouse"
if exist "%CONFIG_DIR%" (
    echo Found user configuration folder at: %CONFIG_DIR%
    set /p "DEL_CONF=Do you want to delete your custom sensitivity and settings too? [y/N]: "
    if /i "!DEL_CONF!"=="Y" (
        rmdir /s /q "%CONFIG_DIR%"
        echo   [OK] Removed user configuration folder.
    ) else (
        echo   [OK] Kept user settings safe.
    )
)

echo.
echo ================================================================================
echo   [SUCCESS] JOY-CON MOUSE SHORTCUTS HAVE BEEN REMOVED!
echo ================================================================================
echo.
pause
exit /b 0
