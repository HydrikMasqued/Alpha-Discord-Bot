@echo off
echo ========================================
echo PTERODACTYL SETUP COMMANDS GENERATOR
echo ========================================
echo.
echo Copy and paste these commands into your Pterodactyl console:
echo.
echo ----------------------------------------
echo 1. STOP YOUR SERVER FIRST IN PTERODACTYL PANEL
echo ----------------------------------------
echo.
echo ----------------------------------------
echo 2. CLEAR EXISTING FILES:
echo ----------------------------------------
echo rm -rf *
echo.
echo ----------------------------------------
echo 3. CLONE REPOSITORY:
echo ----------------------------------------
echo git clone https://github.com/HydrikMasqued/Alpha-Discord-Bot.git .
echo.
echo ----------------------------------------
echo 4. VERIFY FILES:
echo ----------------------------------------
echo ls -la
echo.
echo ----------------------------------------
echo 5. CREATE .ENV FILE (REPLACE YOUR_TOKEN):
echo ----------------------------------------
echo cat ^> .env ^<^< 'EOF'
echo BOT_TOKEN=YOUR_ACTUAL_DISCORD_BOT_TOKEN_HERE
echo BOT_PREFIX=!
echo ANNOUNCEMENT_CHANNEL_ID=0
echo EOF
echo.
echo ----------------------------------------
echo 6. VERIFY .ENV FILE:
echo ----------------------------------------
echo cat .env
echo.
echo ----------------------------------------
echo 7. START YOUR SERVER IN PTERODACTYL PANEL
echo ----------------------------------------
echo.
echo ========================================
echo IMPORTANT NOTES:
echo ========================================
echo - Get your Discord bot token from: https://discord.com/developers/applications
echo - Replace YOUR_ACTUAL_DISCORD_BOT_TOKEN_HERE with your real token
echo - Run these commands in your PTERODACTYL CONSOLE, not here
echo ========================================
echo.
pause
