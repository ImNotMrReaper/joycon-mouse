<#
.SYNOPSIS
  Joy-Con Mouse & Universal Remote - 1-Click Remote Installer for Windows 10 & 11
.DESCRIPTION
  Zero-dependency installer for Joy-Con Mouse on Windows.
  Can be executed directly via 1-liner:
    irm https://raw.githubusercontent.com/ImNotMrReaper/joycon-mouse/main/install.ps1 | iex
#>

[CmdletBinding()]
param(
    [switch]$NonInteractive,
    [string]$InstallPath = "$env:LOCALAPPDATA\Programs\joycon-mouse"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  🎮 JOY-CON MOUSE 1-CLICK INSTALLER FOR WINDOWS" -ForegroundColor Magenta
Write-Host "  Transform Switch Joy-Cons into a wireless PC mouse & media remote!" -ForegroundColor DarkGray
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python Environment
Write-Host "[Step 1/4] Checking Python environment..." -ForegroundColor Cyan

$pythonCmd = $null
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}

if (-not $pythonCmd) {
    Write-Host "  [!] Python 3 was not detected in system PATH." -ForegroundColor Yellow
    if (Get-Command "winget" -ErrorAction SilentlyContinue) {
        Write-Host "  Detected Windows Package Manager (winget)." -ForegroundColor DarkGray
        Write-Host "  Attempting automated installation of Python 3.12..." -ForegroundColor Cyan
        try {
            Start-Process winget -ArgumentList "install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements" -Wait -NoNewWindow
            # Refresh PATH in current process
            $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
            $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
            $env:Path = "$machinePath;$userPath"
            if (Get-Command "python" -ErrorAction SilentlyContinue) {
                $pythonCmd = "python"
                Write-Host "  [OK] Python 3 successfully installed via winget!" -ForegroundColor Green
            } elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
                $pythonCmd = "py"
                Write-Host "  [OK] Python launcher (py) ready!" -ForegroundColor Green
            }
        } catch {
            Write-Host "  [!] Automatic winget install failed: $_" -ForegroundColor Yellow
        }
    }

    if (-not $pythonCmd) {
        Write-Host ""
        Write-Host "  Please install Python 3 manually from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "  CRITICAL: Be sure to check the box 'Add python.exe to PATH' during installation!" -ForegroundColor Red
        if (-not $NonInteractive) {
            Start-Process "https://www.python.org/downloads/"
            Read-Host "  Press Enter after completing Python setup to continue..."
            $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
            $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
            $env:Path = "$machinePath;$userPath"
            if (Get-Command "python" -ErrorAction SilentlyContinue) {
                $pythonCmd = "python"
            } elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
                $pythonCmd = "py"
            }
        }
    }
} else {
    Write-Host "  [OK] Python environment detected ($pythonCmd)." -ForegroundColor Green
}

# Step 2: Deploy Application Files
Write-Host ""
Write-Host "[Step 2/4] Deploying Joy-Con Mouse application files..." -ForegroundColor Cyan

# Check if running locally inside cloned repository
$isLocal = $false
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "joycon-mouse-windows.py"))) {
    $isLocal = $true
}

if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
}

if ($isLocal) {
    Write-Host "  Copying files from local repository to $InstallPath..." -ForegroundColor DarkGray
    Copy-Item -Path (Join-Path $PSScriptRoot "*") -Destination $InstallPath -Recurse -Force -Exclude ".git",".github"
} else {
    Write-Host "  Downloading latest release from GitHub (windows branch)..." -ForegroundColor DarkGray
    $zipUrl = "https://github.com/ImNotMrReaper/joycon-mouse/archive/refs/heads/windows.zip"
    $tempZip = Join-Path $env:TEMP "joycon-mouse-windows.zip"
    $tempExtract = Join-Path $env:TEMP "joycon-extract-$([Guid]::NewGuid().ToString('N').Substring(0,8))"

    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $zipUrl -OutFile $tempZip -UseBasicParsing
        Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force

        $extractedItems = Get-ChildItem -Path $tempExtract
        if ($extractedItems.Count -eq 1 -and $extractedItems[0].PSIsContainer) {
            $sourceDir = $extractedItems[0].FullName
        } else {
            $sourceDir = $tempExtract
        }
        Copy-Item -Path (Join-Path $sourceDir "*") -Destination $InstallPath -Recurse -Force
        Write-Host "  [OK] Files successfully extracted to $InstallPath" -ForegroundColor Green
    } catch {
        Write-Host "  [!] Failed to download or extract repository archive: $_" -ForegroundColor Red
        throw
    } finally {
        if (Test-Path $tempZip) { Remove-Item -Path $tempZip -Force -ErrorAction SilentlyContinue }
        if (Test-Path $tempExtract) { Remove-Item -Path $tempExtract -Recurse -Force -ErrorAction SilentlyContinue }
    }
}

# Step 3: Configure User Settings
Write-Host ""
Write-Host "[Step 3/4] Configuring user settings..." -ForegroundColor Cyan
$configDir = "$env:APPDATA\joycon-mouse"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Force -Path $configDir | Out-Null
}
$configFile = Join-Path $configDir "config.json"
if (-not (Test-Path $configFile)) {
    $defaultConfig = @{
        sensitivity = 1.0
        deadzone = 0.10
        rumble = $true
        disabled_modes = @()
    } | ConvertTo-Json -Depth 4
    Set-Content -Path $configFile -Value $defaultConfig -Encoding UTF8
    Write-Host "  [OK] Created default config at $configFile" -ForegroundColor Green
} else {
    Write-Host "  [OK] Preserved existing user configuration." -ForegroundColor Green
}

# Step 4: Shortcuts and CLI Setup
Write-Host ""
Write-Host "[Step 4/4] Creating Windows shortcuts and commands..." -ForegroundColor Cyan

# Create Command Wrappers in InstallPath
$cmdLauncher = Join-Path $InstallPath "joycon-mouse.cmd"
$cmdContent = "@echo off`r`npython `"%~dp0joycon-mouse-windows.py`" %*"
Set-Content -Path $cmdLauncher -Value $cmdContent -Encoding ASCII

$runnerBat = Join-Path $InstallPath "run_windows.bat"
if (-not (Test-Path $runnerBat)) {
    $runnerBat = Join-Path $InstallPath "joycon-mouse-windows.py"
}

# Create Desktop and Start Menu Shortcuts via WScript.Shell
try {
    $wsShell = New-Object -ComObject WScript.Shell

    $desktopDir = [Environment]::GetFolderPath('Desktop')
    $shortcutDesk = $wsShell.CreateShortcut((Join-Path $desktopDir "Joy-Con Mouse.lnk"))
    $shortcutDesk.TargetPath = $runnerBat
    $shortcutDesk.WorkingDirectory = $InstallPath
    $shortcutDesk.Description = "Nintendo Switch Joy-Con Desktop Mouse & Media Remote"
    $shortcutDesk.IconLocation = "$env:SystemRoot\System32\shell32.dll,24"
    $shortcutDesk.Save()
    Write-Host "  [OK] Desktop shortcut created: 'Joy-Con Mouse'" -ForegroundColor Green

    $programsDir = [Environment]::GetFolderPath('Programs')
    $shortcutMenu = $wsShell.CreateShortcut((Join-Path $programsDir "Joy-Con Mouse.lnk"))
    $shortcutMenu.TargetPath = $runnerBat
    $shortcutMenu.WorkingDirectory = $InstallPath
    $shortcutMenu.Description = "Nintendo Switch Joy-Con Desktop Mouse & Media Remote"
    $shortcutMenu.IconLocation = "$env:SystemRoot\System32\shell32.dll,24"
    $shortcutMenu.Save()
    Write-Host "  [OK] Start Menu shortcut created in Programs" -ForegroundColor Green
} catch {
    Write-Host "  [!] Notice: Could not create desktop shortcuts automatically: $_" -ForegroundColor Yellow
}

# Add InstallPath to User PATH if not present
try {
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -notlike "*$InstallPath*") {
        [System.Environment]::SetEnvironmentVariable("Path", "$userPath;$InstallPath", "User")
        Write-Host "  [OK] Added '$InstallPath' to user PATH (enables 'joycon-mouse' command in CMD/PowerShell)." -ForegroundColor Green
    }
} catch {
    Write-Host "  [!] Notice: Could not update user PATH: $_" -ForegroundColor Yellow
}

# Step 5: Success Banner
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "  🎉 JOY-CON MOUSE IS INSTALLED ON WINDOWS!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "  • Location:   $InstallPath" -ForegroundColor Cyan
Write-Host "  • Shortcuts:  Desktop & Start Menu ('Joy-Con Mouse')" -ForegroundColor Cyan
Write-Host "  • Terminal:   joycon-mouse" -ForegroundColor Cyan
Write-Host "--------------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "  🎮 Getting Started:" -ForegroundColor Yellow
Write-Host "  1. Pair your Joy-Con: Windows Settings > Bluetooth & devices > Add device." -ForegroundColor Gray
Write-Host "     (Hold the small round Sync button on the side-rail until LEDs cycle)" -ForegroundColor Gray
Write-Host "  2. Double-click the 'Joy-Con Mouse' shortcut on your Desktop!" -ForegroundColor Gray
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

if (-not $NonInteractive) {
    try {
        $launch = Read-Host "Would you like to launch Joy-Con Mouse now? [Y/n]"
        if ($launch -eq "" -or $launch -match "^[yY]") {
            Start-Process $runnerBat
        }
    } catch {
        # Silent ignore in non-interactive / piped environments
    }
}
