import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Alpha Discord Bot"""
    
    # Bot Token (REQUIRED)
    TOKEN = os.getenv('BOT_TOKEN', '')
    
    # Bot Settings
    PREFIX = os.getenv('BOT_PREFIX', '!')
    
    # Channel IDs (Set these for your server)
    ANNOUNCEMENT_CHANNEL_ID = int(os.getenv('ANNOUNCEMENT_CHANNEL_ID', '0'))
    
    # Log Channel Categories - These will be created automatically if they don't exist
    LOG_CATEGORIES = {
        'message_logs': 'Message Logs',
        'member_logs': 'Member Logs', 
        'voice_logs': 'Voice Logs',
        'moderation_logs': 'Moderation Logs',
        'server_logs': 'Server Logs'
    }
    
    # Timer Settings
    CLOCKIN_TIMEOUT = 30 * 60  # 30 minutes in seconds
    
    # Embed Colors
    COLORS = {
        'success': 0x00ff00,
        'error': 0xff0000,
        'warning': 0xffff00,
        'info': 0x0099ff,
        'primary': 0x7289da
    }
    
    # Emojis for reactions
    EMOJIS = {
        'tick': '✅',
        'cross': '❌',
        'clock': '🕐',
        'bell': '🔔',
        'warning': '⚠️'
    }
    
    # Database file paths
    DATABASE_PATH = 'data/alpha_bot.db'
    LOGS_PATH = 'data/logs/'
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.TOKEN:
            errors.append("BOT_TOKEN is required")
            
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
