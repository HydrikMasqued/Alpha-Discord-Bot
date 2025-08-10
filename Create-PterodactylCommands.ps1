# PowerShell Script to Generate Pterodactyl Commands
Write-Host "===============================================" -ForegroundColor Green
Write-Host "PTERODACTYL DISCORD BOT SETUP COMMAND GENERATOR" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Ask for Discord Bot Token
Write-Host "Enter your Discord Bot Token (from https://discord.com/developers/applications):" -ForegroundColor Yellow
$BotToken = Read-Host "Bot Token"

if ([string]::IsNullOrWhiteSpace($BotToken)) {
    Write-Host "Error: Bot token is required!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "GENERATED COMMANDS FOR PTERODACTYL CONSOLE:" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$Commands = @"
# STEP 1: Stop your server in Pterodactyl panel first!

# STEP 2: Clear existing files and setup bot
rm -rf * && git clone https://github.com/HydrikMasqued/Alpha-Discord-Bot.git . && cat > .env << 'EOF'
BOT_TOKEN=$BotToken
BOT_PREFIX=!
ANNOUNCEMENT_CHANNEL_ID=0
EOF

# STEP 3: Verify setup
echo "Files in directory:" && ls -la && echo "Environment variables:" && cat .env

# STEP 4: Start your server in Pterodactyl panel!
"@

Write-Host $Commands -ForegroundColor White
Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "INSTRUCTIONS:" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "1. STOP your server in Pterodactyl panel" -ForegroundColor Yellow
Write-Host "2. COPY the commands above" -ForegroundColor Yellow
Write-Host "3. PASTE into your Pterodactyl console" -ForegroundColor Yellow
Write-Host "4. Press ENTER to execute" -ForegroundColor Yellow
Write-Host "5. START your server in Pterodactyl panel" -ForegroundColor Yellow
Write-Host ""

# Save to file for easy access
$Commands | Out-File -FilePath "pterodactyl_commands.txt" -Encoding UTF8
Write-Host "Commands also saved to: pterodactyl_commands.txt" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
