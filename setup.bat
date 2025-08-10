@echo off
setlocal enabledelayedexpansion
title Alpha Discord Bot Setup
cls
echo.
echo ============================================================
echo              ALPHA DISCORD BOT - SETUP
echo ============================================================
echo Professional Discord Management Solution v1.0.0
echo ============================================================
echo.

REM Step 1: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ from:
    echo https://python.org/downloads
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo SUCCESS: Python is installed

REM Step 2: Check pip
echo [2/5] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found
    pause
    exit /b 1
)
echo SUCCESS: pip is available

REM Step 3: Install dependencies
echo [3/5] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try manually: pip install -r requirements.txt
    pause
    exit /b 1
)
echo SUCCESS: Dependencies installed

REM Step 4: Configure token
echo [4/5] Bot token configuration...
if exist .env (
    echo WARNING: Configuration file already exists
    set /p reconfigure="Reconfigure token? (y/N): "
    if /i "!reconfigure!" neq "y" goto skip_token
)

echo.
echo ============================================================
echo                    BOT TOKEN SETUP
echo ============================================================
echo.
echo To get your Discord bot token:
echo 1. Go to: https://discord.com/developers/applications
echo 2. Create new application or select existing
echo 3. Go to "Bot" section
echo 4. Copy the token
echo.
echo IMPORTANT: Keep your token private!
echo ============================================================
echo.

:get_token
set /p bot_token="Enter your Discord bot token: "
if "!bot_token!" == "" (
    echo Token cannot be empty
    goto get_token
)

REM Create config file
(
echo # Alpha Discord Bot Configuration
echo BOT_TOKEN=!bot_token!
echo BOT_PREFIX=^^!
echo ANNOUNCEMENT_CHANNEL_ID=0
) > .env

echo SUCCESS: Configuration saved

:skip_token

REM Step 5: Create directories
echo [5/5] Setting up directories...
if not exist data mkdir data
if not exist data\logs mkdir data\logs
echo SUCCESS: Setup complete

echo.
echo ============================================================
echo                   SETUP COMPLETE
echo ============================================================
echo.
echo Your Alpha Discord Bot is ready!
echo.
echo Next steps:
echo 1. Invite bot to your Discord server
echo 2. Grant Administrator permissions
echo 3. Run start.bat to launch the bot
echo.
echo Commands to test:
echo /help     - Show all commands
echo /ping     - Test bot response
echo /info     - Bot information
echo.
echo ============================================================
pause
