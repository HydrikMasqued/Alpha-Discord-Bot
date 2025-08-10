# 🤖 Alpha Discord Bot

A comprehensive, professional Discord bot with three main modules: Discord Management, Time Management, and Logging.

## ✨ Features

### 🎛️ Discord Management
- **Announcements**: Send professional announcements to designated channels
- **Direct Messaging**: Send DMs to users through the bot using display names
- **Mass Messaging**: Send messages to all users with specific roles
- **Role Management**: Add/remove roles using display names (no pinging required)
- **Smart User Lookup**: Find users by display name, username, or fuzzy matching

### ⏰ Time Management
- **Timezone Support**: Set personal timezones for accurate time displays
- **Time Conversion**: Convert times between different timezones
- **Clock In/Out System**: Professional work session tracking
- **Auto Reminders**: 30-minute reminders with interactive responses
- **Local Time Display**: Shows time in user's local timezone

### 📋 Comprehensive Logging
- **Automatic Setup**: One-command setup for all logging channels
- **Message Logging**: Track message edits, deletions, and bulk deletions
- **Member Activity**: Log joins, leaves, nickname changes, and role updates
- **Voice Activity**: Track voice channel joins, leaves, and moves
- **Moderation Logs**: Record bans, unbans, and other moderation actions
- **Server Changes**: Log channel and role creation/deletion

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Discord bot token ([Create one here](https://discord.com/developers/applications))

### Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your bot token to the `.env` file:
     ```env
     BOT_TOKEN=your_bot_token_here
     ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

## 📖 Command Reference

### Discord Management Commands
- `/announce <message> [channel]` - Send a professional announcement
- `/dm <user> <message>` - Send a direct message to a user
- `/mass-dm <role> <message>` - Send a message to all users with a role
- `/add-role <user> <role>` - Add a role to a user
- `/remove-role <user> <role>` - Remove a role from a user

### Time Management Commands
- `/set-timezone <timezone>` - Set your personal timezone
- `/time [timezone] [time_to_convert]` - Get current time or convert times
- `/list-timezones` - Show common timezones
- `/clockin` - Start a work session
- `/clockout` - End your work session
- `/status` - Check your current clock status

### Logging Commands
- `/setup-logs` - Automatically set up all logging channels
- `/log-status` - Check current logging configuration

## 🔧 Configuration

### Environment Variables (.env file)
```env
# Required
BOT_TOKEN=your_bot_token_here

# Optional
BOT_PREFIX=!
ANNOUNCEMENT_CHANNEL_ID=123456789
```

### Bot Permissions Required
- Send Messages
- Use Slash Commands
- Manage Roles
- Manage Channels
- Read Message History
- Add Reactions
- Embed Links
- Attach Files

## 🏗️ Project Structure
```
Alpha Discord Bot/
├── main.py                    # Main bot file
├── config/
│   └── config.py             # Configuration settings
├── modules/
│   ├── discord_management/
│   │   └── management.py     # Discord management features
│   ├── time_management/
│   │   └── timer.py          # Time and clock features
│   └── logs/
│       └── logger.py         # Comprehensive logging
├── utils/
│   └── user_utils.py         # Utility functions
├── data/                     # Data storage directory
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 💡 Key Features Explained

### Smart User Lookup
The bot can find users by:
- Exact display name match
- Exact username match
- Fuzzy matching for partial names
- User ID or mention

### Professional UI
- Consistent embed styling across all modules
- Color-coded messages (success, error, warning, info)
- Interactive buttons and reactions
- Comprehensive error handling

### Timezone Intelligence
- Supports all IANA timezone identifiers
- Personal timezone preferences
- Discord timestamp integration
- Automatic daylight saving adjustments

### Comprehensive Logging
- Dedicated channels for different log types
- Rich embed formatting with timestamps
- User avatars and IDs included
- Automatic channel creation with proper permissions

## 🔒 Security Features

- Permission checking for all administrative commands
- Role hierarchy respect (can't modify higher roles)
- Input sanitization to prevent @everyone/@here abuse
- Proper error handling and logging

## 🆘 Support & Troubleshooting

### Common Issues

**Bot not responding to slash commands:**
- Ensure the bot has "Use Slash Commands" permission
- Try re-inviting the bot with proper permissions
- Commands may take up to 1 hour to register globally

**Permission errors:**
- Verify the bot's role is higher than roles it needs to manage
- Check that required permissions are granted
- Ensure the bot has access to the channels it needs

**Timezone not working:**
- Use exact timezone identifiers (e.g., "America/New_York")
- Check `/list-timezones` for examples
- Verify timezone spelling and format

### Bot Permissions Invite Link Template
Replace `YOUR_CLIENT_ID` with your bot's Client ID:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

## 📝 License

This project is open source and available under the MIT License.

---

**Created with ❤️ for professional Discord server management**

*Remember to keep your bot token secure and never share it publicly!*
