# 🚀 Alpha Discord Bot - Deployment Guide

This guide will help you deploy your Alpha Discord Bot from start to finish.

## 📋 Prerequisites

Before deploying the bot, ensure you have:

- **Windows 10/11** (this guide is for Windows)
- **Python 3.8 or higher** installed
- **Internet connection** for downloading dependencies
- **Discord account** with server management permissions

## 🎯 Step-by-Step Deployment

### Step 1: Create Discord Bot Application

1. **Visit Discord Developer Portal**
   - Go to https://discord.com/developers/applications
   - Log in with your Discord account

2. **Create New Application**
   - Click "New Application"
   - Enter name: `Alpha Discord Bot` (or your preferred name)
   - Click "Create"

3. **Create Bot User**
   - Navigate to "Bot" section in left sidebar
   - Click "Add Bot"
   - Confirm by clicking "Yes, do it!"

4. **Configure Bot Settings**
   - **Username**: Set your preferred bot name
   - **Icon**: Upload a bot avatar (optional)
   - **Public Bot**: Turn OFF (recommended for private use)
   - **Privileged Gateway Intents**: Enable ALL intents:
     - ✅ Presence Intent
     - ✅ Server Members Intent
     - ✅ Message Content Intent

5. **Copy Bot Token**
   - In the "Token" section, click "Copy"
   - **⚠️ KEEP THIS SECURE** - Never share your token publicly
   - You'll paste this in the setup script later

### Step 2: Generate Bot Invite Link

1. **Go to OAuth2 > URL Generator**
2. **Select Scopes:**
   - ✅ `bot`
   - ✅ `applications.commands`

3. **Select Bot Permissions:**
   - ✅ Administrator (recommended for full functionality)
   
   *OR select individual permissions:*
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Manage Roles
   - ✅ Manage Channels
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Mention Everyone
   - ✅ Use External Emojis

4. **Copy Generated URL**
   - Copy the generated URL at the bottom
   - Open it in a new tab to invite the bot to your server

5. **Invite Bot to Server**
   - Select your server from the dropdown
   - Click "Continue" → "Authorize"
   - Complete any CAPTCHA if prompted

### Step 3: Deploy the Bot

#### Method 1: Quick Setup (Recommended)

1. **Run Setup Script**
   ```batch
   # Double-click the file:
   setup_bot.bat
   ```
   
2. **Follow the Interactive Setup**
   - The script will check Python installation
   - Install dependencies automatically
   - Prompt you to paste your Discord token
   - Create configuration files
   - Start the bot

#### Method 2: Manual Setup

1. **Install Python Dependencies**
   ```batch
   pip install -r requirements.txt
   ```

2. **Configure Bot Token**
   ```batch
   # Copy .env.example to .env
   copy .env.example .env
   
   # Edit .env file and add your token:
   # BOT_TOKEN=your_bot_token_here
   ```

3. **Start the Bot**
   ```batch
   python main.py
   ```

### Step 4: Verify Deployment

1. **Check Console Output**
   - Look for "Alpha has connected to Discord!"
   - Verify "Synced X slash commands" message
   - No error messages should appear

2. **Test in Discord**
   - Go to your Discord server
   - Type `/help` and press Enter
   - You should see the bot's help menu

3. **Setup Logging (Optional)**
   - Type `/setup-logs` to create log channels
   - This will create a organized logging system

## ⚙️ Configuration Options

### Environment Variables (.env file)

```env
# Required - Your Discord bot token
BOT_TOKEN=your_bot_token_here

# Optional - Bot command prefix for legacy commands
BOT_PREFIX=!

# Optional - Default announcement channel ID
ANNOUNCEMENT_CHANNEL_ID=123456789012345678
```

### Advanced Configuration

Edit `config/config.py` for advanced settings:
- Timer durations
- Embed colors
- Emoji customization
- Database paths

## 🔧 Troubleshooting

### Common Issues

**❌ "Bot token not found" Error**
- Ensure you've created a `.env` file
- Verify the token is correctly pasted
- Check for extra spaces or quotes

**❌ "Invalid bot token provided" Error**
- Generate a new token from Discord Developer Portal
- Ensure you copied the complete token
- Try regenerating the token

**❌ Bot appears offline**
- Check your internet connection
- Verify bot permissions in Discord server
- Ensure all Gateway Intents are enabled

**❌ Slash commands not appearing**
- Wait up to 1 hour for global command registration
- Try leaving and re-joining the server
- Restart Discord client

**❌ Permission errors**
- Ensure bot has Administrator permission
- Check bot role hierarchy (should be high)
- Verify channel-specific permissions

### Getting Help

1. **Check Logs**: Look at `data/bot.log` for error details
2. **Console Output**: Read error messages in the command window
3. **Discord Developer Portal**: Verify bot configuration
4. **Test Commands**: Use `/ping` to check if bot is responsive

## 🔒 Security Best Practices

### Token Security
- ✅ **Never share your bot token** publicly
- ✅ **Use .env files** for token storage
- ✅ **Add .env to .gitignore** if using version control
- ✅ **Regenerate tokens** if compromised

### Permission Management
- ✅ **Use least privilege principle** when possible
- ✅ **Regular permission audits** for bot role
- ✅ **Monitor bot activity** through logs
- ✅ **Restrict admin commands** to trusted users

## 📊 Performance Optimization

### For Large Servers (1000+ members)

1. **Database Integration**
   - Consider upgrading to PostgreSQL/MySQL
   - Implement connection pooling

2. **Caching**
   - Enable Discord.py caching
   - Implement Redis for session storage

3. **Rate Limiting**
   - Monitor API rate limits
   - Implement exponential backoff

### For Production Deployment

1. **Process Management**
   - Use PM2 or similar process manager
   - Set up automatic restarts

2. **Monitoring**
   - Log aggregation (ELK stack)
   - Performance metrics
   - Uptime monitoring

3. **Backup Strategy**
   - Regular data backups
   - Configuration versioning

## 🔄 Maintenance

### Regular Tasks

- **Weekly**: Check logs for errors
- **Monthly**: Update dependencies (`pip install -r requirements.txt --upgrade`)
- **Quarterly**: Review Discord API changes
- **As Needed**: Update bot permissions

### Updates and Upgrades

1. **Backup Current Installation**
   ```batch
   # Backup data folder
   xcopy /E /I data data_backup_YYYY-MM-DD
   ```

2. **Update Dependencies**
   ```batch
   pip install -r requirements.txt --upgrade
   ```

3. **Test After Updates**
   - Verify all commands work
   - Check logs for new errors
   - Test in development server first

## 🆘 Emergency Procedures

### Bot Compromised
1. **Immediately regenerate token** in Discord Developer Portal
2. **Update .env file** with new token
3. **Restart bot** with new token
4. **Review logs** for suspicious activity

### Server Issues
1. **Check bot permissions** in Discord server
2. **Verify role hierarchy** (bot role should be high)
3. **Re-invite bot** if necessary using OAuth2 URL
4. **Contact server administrators** if needed

---

## 🎉 Congratulations!

Your Alpha Discord Bot should now be successfully deployed and running! 

**Next Steps:**
- Test all features with `/help`
- Set up logging with `/setup-logs`
- Configure user timezones with `/set-timezone`
- Explore all the professional features available

**Remember**: Keep your bot token secure and enjoy your professional Discord management solution!

---

**📞 Support**: If you encounter issues, check the troubleshooting section or review the error logs in `data/bot.log`.

**🔄 Updates**: Check `CHANGELOG.md` for version updates and new features.

**📚 Documentation**: Refer to `README.md` and `FEATURE_TEMPLATE.md` for additional information.
