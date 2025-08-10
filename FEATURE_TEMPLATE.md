# 🛠️ Feature Addition Guide

This guide explains how to easily add new features to the Alpha Discord Bot.

## 📋 Quick Checklist for New Features

### 1. Planning Phase
- [ ] Define the feature requirements clearly
- [ ] Determine which module it belongs to (or if it needs a new module)
- [ ] Check for required permissions
- [ ] Plan the user interface (commands, embeds, interactions)

### 2. Implementation Phase
- [ ] Create/modify the appropriate cog file
- [ ] Add configuration options if needed
- [ ] Implement proper error handling
- [ ] Add permission checks
- [ ] Test the feature thoroughly

### 3. Documentation Phase
- [ ] Update CHANGELOG.md with the new feature
- [ ] Update README.md if needed
- [ ] Add docstrings to new functions
- [ ] Update command reference if applicable

## 🏗️ Module Structure Guide

### Adding to Existing Modules

#### Discord Management (`modules/discord_management/management.py`)
For features related to:
- Server announcements
- User messaging
- Role management
- Server administration

#### Time Management (`modules/time_management/timer.py`)
For features related to:
- Timezone operations
- Time tracking
- Scheduling
- Reminders

#### Logs (`modules/logs/logger.py`)
For features related to:
- Event logging
- Audit trails
- Monitoring
- Analytics

### Creating a New Module

1. **Create module directory:**
   ```
   modules/new_module/
   ├── __init__.py
   └── feature.py
   ```

2. **Create cog class:**
   ```python
   import discord
   from discord.ext import commands
   from discord import app_commands
   from utils.user_utils import EmbedBuilder, PermissionChecker
   from config.config import Config

   class NewModule(commands.Cog):
       """New Module Description"""
       
       def __init__(self, bot):
           self.bot = bot
       
       @app_commands.command(name="example", description="Example command")
       async def example_command(self, interaction: discord.Interaction):
           """Example command implementation"""
           embed = EmbedBuilder.success_embed("Success", "Feature working!")
           await interaction.response.send_message(embed=embed)

   async def setup(bot):
       await bot.add_cog(NewModule(bot))
   ```

3. **Register in main.py:**
   ```python
   # Add import
   from modules.new_module.feature import NewModule

   # Add to setup_hook
   await self.add_cog(NewModule(self))
   ```

## 🎨 UI Guidelines

### Embed Styling
Use the EmbedBuilder utility for consistent styling:

```python
# Success message (green)
embed = EmbedBuilder.success_embed("Title", "Description")

# Error message (red)
embed = EmbedBuilder.error_embed("Title", "Description")

# Warning message (yellow)
embed = EmbedBuilder.warning_embed("Title", "Description")

# Info message (blue)
embed = EmbedBuilder.info_embed("Title", "Description")

# Custom embed
embed = EmbedBuilder.create_embed("Title", "Description", Config.COLORS['primary'])
```

### Interactive Elements

#### Confirmation Dialogs
```python
from modules.discord_management.management import ConfirmationView

view = ConfirmationView()
await interaction.response.send_message(embed=confirm_embed, view=view, ephemeral=True)
await view.wait()

if view.confirmed:
    # Proceed with action
    pass
```

#### Reactions for User Input
```python
# Add reactions
await message.add_reaction(Config.EMOJIS['tick'])
await message.add_reaction(Config.EMOJIS['cross'])

# Wait for reaction
def check(reaction, user):
    return (user.id == target_user_id and 
           str(reaction.emoji) in [Config.EMOJIS['tick'], Config.EMOJIS['cross']])

reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
```

## 🔒 Security Guidelines

### Permission Checking
Always check permissions before executing commands:

```python
@app_commands.command(name="admin-command", description="Admin only command")
async def admin_command(self, interaction: discord.Interaction):
    if not PermissionChecker.has_admin_perms(interaction.user):
        await interaction.response.send_message(
            embed=EmbedBuilder.error_embed("Access Denied", "You need administrator permissions."),
            ephemeral=True
        )
        return
    
    # Command implementation here
```

### User Input Sanitization
Always sanitize user input:

```python
from utils.user_utils import sanitize_input

clean_message = sanitize_input(user_input)
```

### Rate Limiting
For operations that could be spammed:

```python
import asyncio

# Add delays between operations
await asyncio.sleep(1)  # 1 second delay

# Track usage per user if needed
if user_id in self.rate_limits:
    # Handle rate limiting
    pass
```

## 💾 Data Storage

### Configuration Storage
Add new config options to `config/config.py`:

```python
class Config:
    # Add your new configuration
    NEW_FEATURE_ENABLED = os.getenv('NEW_FEATURE_ENABLED', 'true').lower() == 'true'
    NEW_FEATURE_TIMEOUT = int(os.getenv('NEW_FEATURE_TIMEOUT', '60'))
```

### Persistent Data
Use JSON files in the `data/` directory:

```python
import json
import os

def load_feature_data(self):
    """Load feature data from file"""
    try:
        if os.path.exists('data/feature_data.json'):
            with open('data/feature_data.json', 'r') as f:
                self.feature_data = json.load(f)
    except Exception as e:
        logging.error(f"Error loading feature data: {e}")
        self.feature_data = {}

def save_feature_data(self):
    """Save feature data to file"""
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/feature_data.json', 'w') as f:
            json.dump(self.feature_data, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving feature data: {e}")
```

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] Test with valid inputs
- [ ] Test with invalid inputs
- [ ] Test permission restrictions
- [ ] Test error scenarios
- [ ] Test with different user roles
- [ ] Test rate limiting if applicable

### Error Scenarios to Test
- Missing permissions
- Invalid user inputs
- Network timeouts
- Discord API errors
- Bot missing permissions
- Invalid channel/role references

## 📝 Changelog Template

When adding a feature, update `CHANGELOG.md`:

```markdown
## [1.X.X] - YYYY-MM-DD

### ✨ Added
- **[NEW]** Feature name with brief description
- **[NEW]** `/new-command` - Command description and usage

### 🔧 Changed
- **[UPDATED]** Modified existing feature description

### 🐛 Fixed
- **[FIXED]** Bug fix description

### 📋 Technical Details
- Added new module/cog for feature
- Implemented proper error handling and permissions
- Added configuration options: `NEW_FEATURE_OPTION`
- Enhanced user experience with interactive elements
```

## 🎯 Feature Ideas for Future Implementation

### High Priority
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Advanced moderation system
- [ ] Custom role reactions
- [ ] Scheduled messages/announcements
- [ ] Member verification system

### Medium Priority
- [ ] Music streaming capabilities
- [ ] Poll and voting system
- [ ] Welcome/farewell messages
- [ ] Auto-moderation (spam detection)
- [ ] Backup and restore functionality

### Low Priority
- [ ] Web dashboard
- [ ] API integrations
- [ ] Custom games and activities
- [ ] Economy system
- [ ] Advanced analytics

---

## 📞 Need Help?

If you need assistance adding a feature:
1. Review existing code in the modules
2. Check the utils for reusable functions
3. Follow the established patterns
4. Test thoroughly before deployment
5. Update documentation

Remember: The bot is designed to be modular and extensible. Each feature should be self-contained, well-documented, and follow the established patterns for consistency and maintainability.

---

**Last Updated**: 2025-08-10  
**Template Version**: 1.0  
**Compatibility**: Alpha Discord Bot v1.0.0+
