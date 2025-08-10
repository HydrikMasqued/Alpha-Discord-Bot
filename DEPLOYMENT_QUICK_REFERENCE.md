# 🚀 Quick Deployment Reference Card

## GitHub Repository
```
https://github.com/HydrikMasqued/Alpha-Discord-Bot
```

## Required Environment Variables for Cybrancee
```
BOT_TOKEN=your_actual_discord_bot_token
BOT_PREFIX=!
ANNOUNCEMENT_CHANNEL_ID=0
```

## Deployment Files ✅
- `main.py` - Entry point
- `requirements.txt` - Dependencies 
- `Procfile` - `web: python main.py`
- `runtime.txt` - `python-3.11.6`
- `.env.example` - Environment template

## Cybrancee Setup Checklist
1. ✅ Create account at https://cybrancee.com
2. ✅ Connect GitHub integration
3. ✅ Select repository: `HydrikMasqued/Alpha-Discord-Bot`
4. ✅ Set environment variables (BOT_TOKEN, BOT_PREFIX, ANNOUNCEMENT_CHANNEL_ID)
5. ✅ Deploy and verify bot is online

## Test Commands After Deployment
- `/help` - Command list
- `/ping` - Connection test
- `/info` - Bot information

## Success Indicators
- Bot shows "Online" in Discord
- All slash commands respond
- No errors in Cybrancee logs
- Automatic deployments from GitHub pushes

---
*Your Alpha Discord Bot is production-ready! 🎉*
