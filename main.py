import discord
from discord.ext import commands
import asyncio
import logging
from config.config import Config
from modules.discord_management.management import DiscordManagement
from modules.time_management.timer import TimeManagement
from modules.logs.logger import LogsModule
from modules.core.info import BotInfo
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/bot.log'),
        logging.StreamHandler()
    ]
)

class AlphaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()  # Enable all intents for comprehensive functionality
        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            description="Alpha Discord Bot - Professional Discord Management Solution"
        )
        
    async def setup_hook(self):
        """Load all cogs when bot starts"""
        try:
            await self.add_cog(DiscordManagement(self))
            await self.add_cog(TimeManagement(self))
            await self.add_cog(LogsModule(self))
            await self.add_cog(BotInfo(self))
            
            # Sync slash commands
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} slash commands")
            
        except Exception as e:
            logging.error(f"Error loading cogs: {e}")

    async def on_ready(self):
        """Called when bot is ready"""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="over the server | /help"
            )
        )
        
        # Create data directories if they don't exist
        os.makedirs('data/logs', exist_ok=True)
        os.makedirs('data/timers', exist_ok=True)
        os.makedirs('data/users', exist_ok=True)

    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param}")
        else:
            logging.error(f"Unhandled error: {error}")
            await ctx.send("❌ An unexpected error occurred. Please try again later.")

def main():
    """Main function to run the bot"""
    if not Config.TOKEN:
        print("❌ Bot token not found! Please set your bot token in config/config.py")
        return
    
    bot = AlphaBot()
    
    try:
        bot.run(Config.TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid bot token provided!")
    except KeyboardInterrupt:
        print("\n👋 Bot shutting down...")
    except Exception as e:
        logging.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
