# 🚀 Alpha Discord Bot - Cybrancee Cloud Deployment

Deploy your Alpha Discord Bot to Cybrancee cloud hosting for 24/7 operation.

## 📋 Prerequisites

- **Cybrancee Account** - Sign up at https://cybrancee.com
- **Discord Bot Token** - From Discord Developer Portal
- **GitHub Repository** - Your bot code (created in this guide)

## 🎯 Quick Deployment Steps

### Step 1: Prepare for Cloud Deployment

1. **Update Environment Configuration**
   - Your bot is already configured for cloud deployment
   - Environment variables will be set in Cybrancee dashboard

2. **Verify Project Structure**
   ```
   Alpha Discord Bot/
   ├── main.py              # Main bot entry point
   ├── requirements.txt     # Python dependencies
   ├── .env.example        # Environment template
   ├── Procfile            # Process definition (created below)
   ├── runtime.txt         # Python version (created below)
   └── modules/            # Bot modules
   ```

### Step 2: Create Cloud Configuration Files

The bot needs these files for cloud deployment (they'll be created automatically).

### Step 3: Deploy to Cybrancee

1. **Login to Cybrancee Dashboard**
   - Go to https://cybrancee.com
   - Login to your account

2. **Create New Application**
   - Click "New App" or "Create Application"
   - Name: `alpha-discord-bot`
   - Select: **Python** runtime

3. **Connect GitHub Repository**
   - Choose "GitHub" as deployment source
   - Select your `Alpha-Discord-Bot` repository
   - Branch: `main`

4. **Configure Environment Variables**
   In the Cybrancee dashboard, set these environment variables:
   ```
   BOT_TOKEN=your_actual_discord_bot_token_here
   BOT_PREFIX=!
   ANNOUNCEMENT_CHANNEL_ID=0
   ```

5. **Deploy Application**
   - Click "Deploy" or "Create App"
   - Cybrancee will automatically:
     - Install Python dependencies
     - Start your bot
     - Provide 24/7 hosting

### Step 4: Verify Deployment

1. **Check Application Logs**
   - In Cybrancee dashboard, view logs
   - Look for: `"Alpha has connected to Discord!"`
   - Verify: `"Synced X slash commands"`

2. **Test Bot in Discord**
   - Go to your Discord server
   - Try: `/help`, `/ping`, `/info`
   - Bot should respond immediately

## ⚙️ Advanced Configuration

### Custom Domains (Optional)
- Cybrancee may offer custom domain support
- Not required for Discord bots (they don't serve web traffic)

### Scaling Settings
- **Dyno Type**: Basic/Hobby (sufficient for most Discord bots)
- **Auto-scaling**: Usually not needed for Discord bots
- **Memory**: 512MB recommended minimum

### Database (If Needed Later)
- Cybrancee may offer PostgreSQL/MySQL add-ons
- Current bot uses JSON files (works great for most uses)
- Upgrade to database later if needed

## 🔧 Cybrancee-Specific Features

### Process Management
```procfile
worker: python main.py
```

### Health Checks
- Bot automatically responds to Discord heartbeats
- No additional health checks needed

### Logging
- All bot logs appear in Cybrancee dashboard
- Automatic log rotation included

### Monitoring
- Monitor bot uptime through Cybrancee dashboard
- Discord status shows online/offline

## 🛠️ Troubleshooting

### Common Issues on Cybrancee:

**"Application Error" on Deploy**
- Check that `requirements.txt` is in root directory
- Verify `Procfile` exists and is formatted correctly
- Check environment variables are set

**"Bot Not Responding"**
- Verify `BOT_TOKEN` environment variable is correct
- Check application logs for connection errors
- Ensure bot has proper Discord permissions

**"Dependency Errors"**
- All dependencies are in `requirements.txt`
- Python version should be 3.8+ (specified in `runtime.txt`)

**"Worker Timeout"**
- This is normal during initial connection
- Bot should stabilize within 30-60 seconds

### Log Analysis
Look for these success messages in Cybrancee logs:
```
Alpha has connected to Discord!
Synced 17 slash commands
Bot is in X guilds
```

## 💰 Cost Estimation

### Cybrancee Pricing (Estimated)
- **Free Tier**: May be available for basic bots
- **Basic Plan**: Usually $5-10/month for small bots
- **Pro Plan**: $20-50/month for high-traffic bots

### Resource Usage
- **RAM**: ~100-200MB typical usage
- **CPU**: Very low (Discord bots are mostly idle)
- **Bandwidth**: Minimal (just Discord API calls)

## 🔄 Maintenance

### Updates
1. Push changes to GitHub repository
2. Cybrancee auto-deploys from `main` branch
3. Zero-downtime deployments

### Monitoring
- Check Cybrancee dashboard regularly
- Monitor Discord bot status
- Review logs for errors

### Backups
- Code backed up in GitHub
- Configuration in environment variables
- Data files stored in cloud (persistent storage)

## 📞 Support

### Cybrancee Support
- Check Cybrancee documentation
- Contact their support team
- Community forums if available

### Bot Issues
- Check `TROUBLESHOOTING.md` in repository
- Review Discord API status
- Verify bot permissions in Discord

## 🎉 Success Checklist

After deployment, verify:
- ✅ Bot shows "Online" in Discord
- ✅ `/help` command works
- ✅ All slash commands available
- ✅ No errors in Cybrancee logs
- ✅ Bot responds to commands

---

## 🌟 Production Ready

Your Alpha Discord Bot is now:
- ✅ **24/7 Online** - Hosted on Cybrancee cloud
- ✅ **Scalable** - Can handle multiple Discord servers
- ✅ **Reliable** - Professional hosting with uptime monitoring
- ✅ **Secure** - Environment variables protected
- ✅ **Maintainable** - Easy updates through GitHub

**Your professional Discord management solution is live! 🚀**

---

**Last Updated**: 2025-08-10  
**Version**: 1.0.0  
**Cloud Platform**: Cybrancee  
**Status**: Production Ready
