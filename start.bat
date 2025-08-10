@echo off
title Alpha Discord Bot
cls
echo.
echo ============================================================
echo              ALPHA DISCORD BOT - STARTING
echo ============================================================
echo.

REM Check if configured
if not exist .env (
    echo ERROR: Bot not configured yet
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python or run setup.bat
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip show discord.py >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo Starting bot...
echo.
echo ============================================================
echo                    BOT OUTPUT
echo ============================================================
echo.
echo Look for: "Alpha has connected to Discord!"
echo Use Ctrl+C to stop the bot
echo.

REM Start bot
python main.py

REM Handle exit
echo.
echo ============================================================
echo Bot has stopped
echo.
if errorlevel 1 (
    echo ERROR: Bot stopped with an error
    echo Check the messages above for details
) else (
    echo Bot stopped normally
)
echo.
pause
