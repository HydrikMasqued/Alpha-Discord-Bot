@echo off
setlocal enabledelayedexpansion
title Alpha Discord Bot - Token Configuration
cls
echo.
echo ============================================================
echo              DISCORD BOT TOKEN CONFIGURATION
echo ============================================================
echo.

if not exist .env (
    echo No configuration file found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Current configuration file found.
echo.
echo To get your Discord bot token:
echo 1. Go to: https://discord.com/developers/applications
echo 2. Select your application
echo 3. Go to "Bot" section  
echo 4. Copy the token (or regenerate if needed)
echo.
echo IMPORTANT: Keep your token private!
echo.

:get_token
set /p new_token="Enter your new Discord bot token: "
if "!new_token!" == "" (
    echo Token cannot be empty
    goto get_token
)

REM Backup current config
copy .env .env.backup >nul 2>&1

REM Create new config
(
echo # Alpha Discord Bot Configuration
echo BOT_TOKEN=!new_token!
echo BOT_PREFIX=^^!
echo ANNOUNCEMENT_CHANNEL_ID=0
) > .env

echo.
echo SUCCESS: Token updated successfully!
echo Previous configuration backed up to .env.backup
echo.
echo To start the bot with the new token, run start.bat
echo.
pause
