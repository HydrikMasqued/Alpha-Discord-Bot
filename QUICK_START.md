# ⚡ Alpha Discord Bot - Quick Start Guide

Get your bot running in **5 minutes**!

## 🚀 Super Quick Deployment

### Step 1: Get Discord Bot Token (2 minutes)
1. **Go to**: https://discord.com/developers/applications
2. **Click**: "New Application" → Enter bot name → "Create"
3. **Navigate**: "Bot" tab → "Add Bot" → "Yes, do it!"
4. **Enable Intents**: Turn ON all 3 switches under "Privileged Gateway Intents"
   - ✅ Presence Intent
   - ✅ Server Members Intent  
   - ✅ Message Content Intent
5. **Copy Token**: Click "Copy" under Token section

### Step 2: Invite Bot to Server (1 minute)
1. **Go to**: "OAuth2" → "URL Generator"
2. **Select**: ✅ `bot` + ✅ `applications.commands`
3. **Permissions**: ✅ Administrator (recommended)
4. **Copy URL** and open in new tab
5. **Select server** and authorize

### Step 3: Run Setup Script (2 minutes)
1. **Double-click**: `setup_bot.bat`
2. **Follow prompts**: Install dependencies → Paste token
3. **Wait for**: "Alpha has connected to Discord!" message
4. **Done!** Bot is running

## 🎯 Test Your Bot

In Discord, type these commands:
- `/help` - See all features
- `/ping` - Check if bot responds  
- `/setup-logs` - Create log channels
- `/info` - View bot information

## 📁 Files You Need

```
📂 Alpha Discord Bot/
├── 🔧 setup_bot.bat          ← Double-click this!
├── 🚀 start_bot.bat          ← Use this to restart later
├── 🔑 reconfigure_token.bat  ← Change token if needed
├── 📄 main.py                ← Main bot code
├── 📋 requirements.txt       ← Dependencies list
└── 📚 Other files...         ← Documentation & modules
```

## ⚡ Commands Summary

| **Script** | **Purpose** |
|------------|-------------|
| `setup_bot.bat` | **First time setup** - Install everything and configure token |
| `start_bot.bat` | **Daily use** - Just start the bot (after setup) |
| `reconfigure_token.bat` | **Token change** - Update token only |

## 🔧 Troubleshooting

**❌ "Python not found"**
- Install Python from: https://python.org/downloads
- ✅ Check "Add Python to PATH" during install

**❌ "Bot token not found"**  
- Run `setup_bot.bat` again
- Make sure you paste the complete token

**❌ "Bot appears offline"**
- Check internet connection
- Verify all 3 intents are enabled in Discord Developer Portal
- Try regenerating token and using `reconfigure_token.bat`

**❌ "No slash commands appear"**
- Wait 5-10 minutes for Discord to sync
- Try typing `/` in chat to see if commands appear
- Restart Discord client

## 🎉 Success! What Next?

Once your bot is running:

1. **Set up logging**: `/setup-logs`
2. **Configure timezone**: `/set-timezone America/New_York`
3. **Test features**: `/announce message:"Bot is online!"`
4. **Read full docs**: Check `README.md` and `DEPLOYMENT_GUIDE.md`

---

## 📞 Need Help?

- **Full Guide**: See `DEPLOYMENT_GUIDE.md`
- **Features**: Check `README.md` 
- **Logs**: Look at `data/bot.log` for errors
- **Discord**: Ensure bot has proper permissions

**Your Alpha Discord Bot is ready for professional Discord management!** 🚀
