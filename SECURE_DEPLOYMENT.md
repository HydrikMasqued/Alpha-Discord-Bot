# 🔐 Secure Deployment Guide for Alpha Discord Bot

## 🛡️ Security Best Practices

### ⚠️ **NEVER COMMIT THESE FILES TO VERSION CONTROL:**
- `.env` (your actual environment variables)
- Any file containing Discord bot tokens
- Database passwords or connection strings
- API keys or secrets

### ✅ **Safe to Commit:**
- `.env.example` (template without real values)
- Source code files
- Documentation
- Configuration templates

---

## 📋 **Deployment Steps**

### **Step 1: Environment Setup**

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your actual values:**
   ```
   BOT_TOKEN=MTxxxxxxxxxxxxxxxxx.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxx
   BOT_PREFIX=!
   ANNOUNCEMENT_CHANNEL_ID=123456789012345678
   ```

### **Step 2: Pterodactyl Deployment**

**Method 1: Git Clone + Manual .env**
```bash
# Clone repository (safe - no secrets)
git clone https://github.com/HydrikMasqued/Alpha-Discord-Bot.git .

# Create environment file manually
cat > .env << 'EOF'
BOT_TOKEN=your_actual_bot_token_here
BOT_PREFIX=!
ANNOUNCEMENT_CHANNEL_ID=0
EOF
```

**Method 2: Environment Variables in Panel**
- Set environment variables directly in Pterodactyl panel
- BOT_TOKEN=your_actual_token
- BOT_PREFIX=!
- ANNOUNCEMENT_CHANNEL_ID=0

---

## 🔧 **Environment Variable Configuration**

### **Required Variables:**
| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Discord bot token | `MTxxxxxxxxxxxxxxxxx.Gxxxxx.xxx...` |
| `BOT_PREFIX` | Command prefix | `!` |
| `ANNOUNCEMENT_CHANNEL_ID` | Default channel ID | `123456789012345678` |

### **Optional Variables:**
| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `production` |
| `DEBUG` | Enable debug logging | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_TO_FILE` | Save logs to file | `true` |

---

## 🚀 **Cloud Platform Instructions**

### **Pterodactyl Panel**
1. Use git clone method (secure)
2. Create .env manually via console
3. Never upload .env via file manager

### **Heroku**
1. Set config vars in dashboard
2. Never commit .env files
3. Use heroku config:set commands

### **Railway/Render**
1. Use environment variables section
2. Connect GitHub repository
3. Set secrets in platform dashboard

---

## 🔍 **Security Verification**

### **Before Committing:**
```bash
# Check for sensitive files
git status

# Make sure .env files are ignored
git check-ignore .env
# Should output: .env

# Verify no tokens in staged files
git diff --cached | grep -i "token\|secret\|key"
# Should return nothing
```

### **GitHub Security Features:**
- ✅ Push protection enabled (blocks token commits)
- ✅ Secret scanning active
- ✅ Dependency vulnerability alerts

---

## 🆘 **If Token Gets Committed**

### **Immediate Actions:**
1. **Regenerate bot token** in Discord Developer Portal
2. **Update deployed instances** with new token
3. **Clean git history** (if needed):
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
   git push origin --force --all
   ```

---

## ✅ **Secure Deployment Checklist**

- [ ] `.env` files listed in `.gitignore`
- [ ] No tokens in source code files
- [ ] Environment template updated (`.env.example`)
- [ ] Deployment platform configured with environment variables
- [ ] Bot token not visible in logs
- [ ] Repository security scanning enabled
- [ ] Emergency token rotation plan in place

---

## 📞 **Support**

If you accidentally commit sensitive data:
1. **Stop immediately** - don't push
2. **Regenerate all tokens/secrets**
3. **Clean git history** before pushing
4. **Update deployment environments**

**Remember: Security is not optional - it's essential! 🔒**
