import discord
from discord.ext import commands
from discord import app_commands
from utils.user_utils import EmbedBuilder
from config.config import Config
from version import __version__, get_version_info
from datetime import datetime

class BotInfo(commands.Cog):
    """Core information and help commands for the bot"""
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show bot help and command information")
    async def help_command(self, interaction: discord.Interaction):
        """Display comprehensive help information"""
        
        embed = discord.Embed(
            title="🤖 Alpha Discord Bot - Help & Commands",
            description=f"**Version:** {__version__} | **Professional Discord Management Solution**",
            color=Config.COLORS['primary']
        )
        
        # Discord Management Commands
        embed.add_field(
            name="🎛️ Discord Management",
            value=(
                "`/announce <message> [channel]` - Send professional announcements\n"
                "`/dm <user> <message>` - Direct message a user via bot\n"
                "`/mass-dm <role> <message>` - Message all users with a role\n"
                "`/add-role <user> <role>` - Add role to user (by display name)\n"
                "`/remove-role <user> <role>` - Remove role from user"
            ),
            inline=False
        )
        
        # Time Management Commands
        embed.add_field(
            name="⏰ Time Management", 
            value=(
                "`/set-timezone <timezone>` - Set your personal timezone\n"
                "`/time [timezone] [time]` - Get current time or convert times\n"
                "`/list-timezones` - Show common timezone options\n"
                "`/clockin` - Start a work session\n"
                "`/clockout` - End your work session\n"
                "`/status` - Check your current clock status"
            ),
            inline=False
        )
        
        # Logging Commands
        embed.add_field(
            name="📋 Server Logging",
            value=(
                "`/setup-logs` - Automatically set up all logging channels\n"
                "`/log-status` - Check current logging configuration"
            ),
            inline=False
        )
        
        # Core Commands
        embed.add_field(
            name="ℹ️ Bot Information",
            value=(
                "`/help` - Show this help message\n"
                "`/info` - Show detailed bot information\n"
                "`/version` - Show version and changelog"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔗 Key Features",
            value=(
                "• **Smart User Lookup** - Find users by display name (no pinging!)\n"
                "• **Professional UI** - Consistent, beautiful embeds\n" 
                "• **Comprehensive Logging** - Track all server activity\n"
                "• **Timezone Intelligence** - Local time support\n"
                "• **Interactive Elements** - Buttons, reactions, confirmations"
            ),
            inline=False
        )
        
        embed.set_footer(
            text="Use slash commands (/) for all interactions • Need help? Check the documentation!",
            icon_url=self.bot.user.display_avatar.url if self.bot.user else None
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Show detailed bot information and statistics")
    async def show_info(self, interaction: discord.Interaction):
        """Display detailed bot information"""
        
        version_info = get_version_info()
        
        embed = discord.Embed(
            title="🤖 Alpha Discord Bot - Information",
            description=version_info["description"],
            color=Config.COLORS['info']
        )
        
        # Bot Statistics
        total_commands = len([cmd for cmd in self.bot.tree.walk_commands()])
        total_guilds = len(self.bot.guilds)
        total_users = sum(guild.member_count or 0 for guild in self.bot.guilds)
        
        embed.add_field(
            name="📊 Statistics",
            value=(
                f"**Servers:** {total_guilds}\n"
                f"**Users:** {total_users:,}\n"
                f"**Commands:** {total_commands}\n"
                f"**Uptime:** <t:{int(datetime.now().timestamp())}:R>"
            ),
            inline=True
        )
        
        # Version Information
        embed.add_field(
            name="🏷️ Version Info",
            value=(
                f"**Version:** {version_info['version']}\n"
                f"**Released:** {version_info['release_date']}\n"
                f"**Author:** {version_info['author']}\n"
                f"**Language:** Python 3.8+"
            ),
            inline=True
        )
        
        # Technical Details
        embed.add_field(
            name="⚙️ Technical",
            value=(
                "**Framework:** discord.py 2.3+\n"
                "**Architecture:** Modular Cogs\n"
                "**Commands:** Slash Commands\n"
                "**Storage:** JSON Files"
            ),
            inline=True
        )
        
        # Features Overview
        features_text = "\n".join([f"• {feature}" for feature in version_info["features"][:4]])
        embed.add_field(
            name="✨ Core Features",
            value=features_text,
            inline=False
        )
        
        # Permissions Required
        embed.add_field(
            name="🔐 Required Permissions",
            value=(
                "• Send Messages & Use Slash Commands\n"
                "• Manage Roles & Channels\n"
                "• Read Message History & Add Reactions\n"
                "• Embed Links & Attach Files"
            ),
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else None)
        embed.set_footer(
            text=f"Alpha Bot v{version_info['version']} • Professional Discord Management",
            icon_url=self.bot.user.display_avatar.url if self.bot.user else None
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="version", description="Show version information and recent changes")
    async def version_info(self, interaction: discord.Interaction):
        """Display version and changelog information"""
        
        version_info = get_version_info()
        
        embed = discord.Embed(
            title=f"🏷️ Alpha Discord Bot v{version_info['version']}",
            description=f"**{version_info['description']}**\n\nReleased: **{version_info['release_date']}**",
            color=Config.COLORS['success']
        )
        
        # Current Version Features
        features_text = "\n".join([f"✅ {feature}" for feature in version_info["features"]])
        embed.add_field(
            name="🎯 Features in This Version",
            value=features_text,
            inline=False
        )
        
        # What's New (would be updated for future versions)
        embed.add_field(
            name="🆕 What's New in v1.0.0",
            value=(
                "• **Initial Release** - All core functionality implemented\n"
                "• **Professional UI** - Beautiful embeds and interactions\n"
                "• **Smart User Lookup** - No more pinging required\n"
                "• **Comprehensive Logging** - Track everything automatically\n"
                "• **Timezone Support** - Local time for everyone\n"
                "• **Modular Design** - Easy to extend and maintain"
            ),
            inline=False
        )
        
        # Development Info
        embed.add_field(
            name="🔧 Development",
            value=(
                f"**Author:** {version_info['author']}\n"
                "**Framework:** discord.py 2.3+\n"
                "**Architecture:** Modular Cogs\n"
                "**Documentation:** Comprehensive"
            ),
            inline=True
        )
        
        # Links and Resources
        embed.add_field(
            name="📚 Resources",
            value=(
                "**Commands:** `/help`\n"
                "**Bot Info:** `/info`\n"
                "**Setup Guide:** README.md\n"
                "**Changelog:** CHANGELOG.md"
            ),
            inline=True
        )
        
        embed.set_footer(
            text="Thank you for using Alpha Discord Bot!",
            icon_url=self.bot.user.display_avatar.url if self.bot.user else None
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Check bot latency and response time")
    async def ping(self, interaction: discord.Interaction):
        """Display bot latency information"""
        
        # Calculate latencies
        websocket_latency = round(self.bot.latency * 1000, 2)
        
        embed = EmbedBuilder.info_embed(
            "🏓 Pong!",
            f"**WebSocket Latency:** {websocket_latency}ms\n"
            f"**Bot Status:** {'🟢 Online' if self.bot.is_ready() else '🔴 Starting...'}"
        )
        
        embed.add_field(
            name="📊 Performance",
            value=(
                f"**Guilds:** {len(self.bot.guilds)}\n"
                f"**Commands:** {len([cmd for cmd in self.bot.tree.walk_commands()])}\n"
                f"**Ready:** {'Yes' if self.bot.is_ready() else 'No'}"
            ),
            inline=True
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
