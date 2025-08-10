# 🚀 GitHub + Cybrancee Integration Guide
## Deploy Your Alpha Discord Bot with Automatic GitHub Integration

This guide provides step-by-step instructions for connecting your GitHub repository to Cybrancee for seamless 24/7 bot hosting with automatic deployments.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- ✅ **GitHub Account** - Free account at https://github.com
- ✅ **Cybrancee Account** - Sign up at https://cybrancee.com  
- ✅ **Discord Bot Token** - From https://discord.com/developers/applications
- ✅ **Alpha Discord Bot Repository** - Already available at: `https://github.com/HydrikMasqued/Alpha-Discord-Bot`

---

## 🔄 Part 1: GitHub Repository Verification

### Step 1: Verify Your Repository is Ready

1. **Visit Your GitHub Repository**
   ```
   https://github.com/HydrikMasqued/Alpha-Discord-Bot
   ```

2. **Confirm These Files Exist:**
   - ✅ `main.py` - Bot entry point
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `Procfile` - Process definition (`web: python main.py`)
   - ✅ `runtime.txt` - Python version (`python-3.11.6`)
   - ✅ `.env.example` - Environment template
   - ✅ `modules/` - Bot functionality folders
   - ✅ `README.md` - Documentation

3. **Check Repository Status**
   - Repository should be **Public** (or Private with Cybrancee Pro)
   - Main branch should be `main` (default)
   - All code should be committed and pushed

---

## 🌐 Part 2: Cybrancee Account Setup

### Step 2: Create Cybrancee Account

1. **Go to Cybrancee Website**
   - Visit: https://cybrancee.com
   - Click **"Sign Up"** or **"Get Started"**

2. **Account Registration**
   - Enter your email address
   - Create a strong password
   - Verify your email address
   - Complete profile setup

3. **Choose Plan**
   - **Free Tier**: Good for testing (if available)
   - **Basic Plan**: Recommended for production ($5-15/month)
   - **Pro Plan**: For high-traffic bots ($20+/month)

### Step 3: Connect GitHub to Cybrancee

1. **Access Dashboard**
   - Login to your Cybrancee account
   - Go to main dashboard/control panel

2. **Connect GitHub Account**
   - Look for **"Connect GitHub"** or **"Integrations"**
   - Click **"Connect GitHub"**
   - You'll be redirected to GitHub

3. **Authorize Cybrancee**
   - GitHub will ask for permissions
   - Review permissions (repository access)
   - Click **"Authorize Cybrancee"**
   - You'll be redirected back to Cybrancee

4. **Verify Connection**
   - You should see "GitHub Connected" status
   - Your repositories should be accessible

---

## 🚀 Part 3: Deploy Your Discord Bot

### Step 4: Create New Application on Cybrancee

1. **Start New Deployment**
   - In Cybrancee dashboard, click **"New App"** or **"Create Application"**
   - Choose **"Deploy from GitHub"**

2. **Configure Basic Settings**
   ```
   Application Name: alpha-discord-bot
   Description: Professional Discord Management Bot
   Region: Choose closest to your users (US/Europe/Asia)
   ```

### Step 5: Select GitHub Repository

1. **Repository Selection**
   - From the dropdown, select: **"HydrikMasqued/Alpha-Discord-Bot"**
   - Branch: **"main"** (should be selected automatically)
   - Deployment method: **"Automatic deploys"**

2. **Build Settings**
   - **Runtime**: Python (should auto-detect from `runtime.txt`)
   - **Python Version**: 3.11.6 (from your `runtime.txt`)
   - **Build Command**: Leave empty (automatic from `requirements.txt`)
   - **Start Command**: `python main.py` (from your `Procfile`)

### Step 6: Configure Environment Variables

This is **CRITICAL** - your bot won't work without these:

1. **In Cybrancee Dashboard, find "Environment Variables" or "Config Vars"**

2. **Add These Variables:**
   ```
   Variable Name: BOT_TOKEN
   Value: your_actual_discord_bot_token_from_discord_developer_portal
   
   Variable Name: BOT_PREFIX  
   Value: !
   
   Variable Name: ANNOUNCEMENT_CHANNEL_ID
   Value: 0
   ```

3. **How to Get Your Discord Bot Token:**
   - Go to https://discord.com/developers/applications
   - Select your bot application
   - Go to "Bot" section
   - Copy the token under "Token"
   - **IMPORTANT**: Never share this token publicly!

### Step 7: Deploy Application

1. **Review Settings**
   - Repository: `HydrikMasqued/Alpha-Discord-Bot`
   - Branch: `main`
   - Environment variables: Set correctly
   - Runtime: Python 3.11.6

2. **Click "Deploy" or "Create App"**
   - Cybrancee will start building your application
   - This process takes 2-5 minutes

3. **Monitor Build Process**
   - Watch the build logs in real-time
   - Look for successful installation of dependencies
   - Wait for "Build succeeded" message

---

## ✅ Part 4: Verify Deployment Success

### Step 8: Check Bot Status

1. **Monitor Application Logs**
   - In Cybrancee dashboard, go to "Logs" or "Activity"
   - Look for these success messages:
   ```
   Alpha has connected to Discord!
   Synced 17 slash commands
   Bot is in X guilds
   ```

2. **Check Bot in Discord**
   - Go to your Discord server
   - Bot should show as **"Online"**
   - Green dot next to bot's name

3. **Test Bot Commands**
   - Try: `/help` - Should show command list
   - Try: `/ping` - Should respond with latency
   - Try: `/info` - Should show bot information

### Step 9: Verify Automatic Deployments

1. **Test GitHub Integration**
   - Make a small change to README.md on GitHub
   - Commit and push the change
   - Cybrancee should automatically detect and redeploy

2. **Monitor Auto-Deploy**
   - Check Cybrancee dashboard for "New deployment triggered"
   - Build should start automatically
   - Bot should update without downtime

---

## 🔧 Part 5: Advanced Configuration

### Step 10: Optional Optimizations

1. **Custom Domain** (If Cybrancee supports it)
   - Not needed for Discord bots
   - Discord bots don't serve web traffic

2. **Database Add-ons** (Future enhancement)
   - PostgreSQL for user data storage
   - Redis for caching (if needed)

3. **Monitoring & Alerts**
   - Set up uptime monitoring
   - Configure email/SMS alerts for downtime

### Step 11: Production Settings

1. **Scaling Configuration**
   ```
   Dyno Type: Basic/Hobby (sufficient for most bots)
   Instance Count: 1 (Discord bots don't need multiple instances)
   Memory: 512MB (recommended minimum)
   ```

2. **Health Checks**
   - Discord bots automatically respond to Discord heartbeats
   - No additional health checks needed

---

## 🎯 Part 6: Maintenance & Updates

### How Automatic Deployments Work

1. **Code Changes**
   - Make changes locally to your bot code
   - Test changes thoroughly

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```

3. **Automatic Deployment**
   - Cybrancee detects GitHub push
   - Automatically builds and deploys new version
   - Zero-downtime deployment (in most cases)

4. **Rollback if Needed**
   - Cybrancee usually provides rollback options
   - Can revert to previous working version

### Best Practices for Updates

1. **Test Locally First**
   - Always test bot changes on your development machine
   - Use a separate test Discord server

2. **Meaningful Commit Messages**
   ```bash
   git commit -m "Add new moderation commands"
   git commit -m "Fix embed formatting issue"
   git commit -m "Update logging module for better performance"
   ```

3. **Monitor After Deployment**
   - Check Cybrancee logs after each deployment
   - Verify bot functionality in Discord
   - Watch for error messages

---

## 🚨 Troubleshooting Common Issues

### Issue 1: "Application Error" on Deploy
**Symptoms**: Build fails or app crashes on startup

**Solutions**:
- ✅ Check that `requirements.txt` exists in repository root
- ✅ Verify `Procfile` contains: `web: python main.py`
- ✅ Ensure `runtime.txt` has: `python-3.11.6`
- ✅ Check Cybrancee build logs for specific error messages

### Issue 2: "Bot Not Responding" in Discord
**Symptoms**: Bot shows offline or doesn't respond to commands

**Solutions**:
- ✅ Verify `BOT_TOKEN` environment variable is set correctly
- ✅ Check Discord Developer Portal - bot should be in your server
- ✅ Ensure bot has necessary Discord permissions
- ✅ Review Cybrancee application logs for connection errors

### Issue 3: "Build Failed" During Deployment
**Symptoms**: Cybrancee can't build your application

**Solutions**:
- ✅ Check Python version compatibility
- ✅ Verify all dependencies in `requirements.txt` are valid
- ✅ Ensure no syntax errors in Python files
- ✅ Check GitHub repository has latest code

### Issue 4: Automatic Deployments Not Working
**Symptoms**: GitHub pushes don't trigger Cybrancee deployments

**Solutions**:
- ✅ Verify GitHub integration is still connected
- ✅ Check webhook settings in GitHub repository
- ✅ Ensure pushing to correct branch (`main`)
- ✅ Re-authorize GitHub connection if needed

---

## 📊 Success Metrics

After successful deployment, you should see:

### ✅ Technical Success Indicators
- Bot status: **Online** in Discord
- Cybrancee logs: No error messages
- Response time: Commands respond within 1-2 seconds
- Uptime: 99%+ availability

### ✅ Functional Success Indicators  
- All slash commands working: `/help`, `/ping`, `/info`
- Logging module capturing server events
- Time management commands functional
- Discord management features active

### ✅ Integration Success Indicators
- GitHub pushes trigger automatic deployments
- Build process completes without errors
- Environment variables properly configured
- No authentication or connection issues

---

## 🎉 Congratulations!

Your **Alpha Discord Bot** is now:

- 🚀 **Live on Cybrancee** - Running 24/7 with professional hosting
- 🔄 **Auto-Deploying** - Updates automatically from GitHub pushes  
- 🛡️ **Production Ready** - Proper error handling and logging
- 📈 **Scalable** - Can handle multiple Discord servers
- 🔧 **Maintainable** - Easy updates through version control

---

## 📞 Support Resources

### Cybrancee Support
- 📚 **Documentation**: Check Cybrancee's official docs
- 💬 **Community**: Look for Cybrancee Discord/forums
- 📧 **Support Tickets**: Use Cybrancee support system

### Bot-Specific Support
- 📖 **Bot Documentation**: Check repository README.md
- 🐛 **Issues**: Report bugs on GitHub Issues
- 💡 **Feature Requests**: Use GitHub Discussions

### Discord Bot Resources
- 📘 **Discord.py Docs**: https://discordpy.readthedocs.io/
- 🏛️ **Discord Developer Portal**: https://discord.com/developers/
- 👥 **Discord.py Community**: Official Discord server

---

**Your professional Discord management solution is now live and ready to serve your community 24/7! 🎊**

---

*Last Updated: 2025-08-10*  
*GitHub Repository: https://github.com/HydrikMasqued/Alpha-Discord-Bot*  
*Status: Production Ready*
