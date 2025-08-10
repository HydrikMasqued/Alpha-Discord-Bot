import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, Dict, Tuple
import asyncio
import json
import os
from datetime import datetime, timezone
import pytz
from utils.user_utils import EmbedBuilder
from config.config import Config
import logging

class TimeManagement(commands.Cog):
    """Time Management Module - Handle timers, timezone conversion, and clock in/out system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_sessions = {}  # user_id: session_data
        self.timezone_db = {}  # user_id: timezone_string
        self.load_timezone_data()
        # Don't start the task here - it will be started when the cog is loaded
    
    async def cog_load(self):
        """Called when the cog is loaded - start the background task"""
        self.check_clockin_timeout.start()
        logging.info("TimeManagement cog loaded and clock timeout task started")
    
    async def cog_unload(self):
        """Called when the cog is unloaded - stop the background task"""
        self.check_clockin_timeout.cancel()
        logging.info("TimeManagement cog unloaded and clock timeout task stopped")
    
    def load_timezone_data(self):
        """Load timezone preferences from file"""
        try:
            if os.path.exists('data/timezones.json'):
                with open('data/timezones.json', 'r') as f:
                    self.timezone_db = json.load(f)
        except Exception as e:
            logging.error(f"Error loading timezone data: {e}")
            self.timezone_db = {}
    
    def save_timezone_data(self):
        """Save timezone preferences to file"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/timezones.json', 'w') as f:
                json.dump(self.timezone_db, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving timezone data: {e}")
    
    # TIMEZONE COMMANDS
    @app_commands.command(name="set-timezone", description="Set your timezone for time displays")
    @app_commands.describe(timezone="Your timezone (e.g., America/New_York, Europe/London, Asia/Tokyo)")
    async def set_timezone(self, interaction: discord.Interaction, timezone: str):
        """Set user's timezone preference"""
        try:
            # Validate timezone
            tz = pytz.timezone(timezone)
            
            # Save timezone
            self.timezone_db[str(interaction.user.id)] = timezone
            self.save_timezone_data()
            
            # Show current time in their timezone
            current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            
            success_embed = EmbedBuilder.success_embed(
                "Timezone Set",
                f"Your timezone has been set to **{timezone}**\n"
                f"Current time: **{current_time}**"
            )
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
        except pytz.exceptions.UnknownTimeZoneError:
            error_embed = EmbedBuilder.error_embed(
                "Invalid Timezone",
                f"'{timezone}' is not a valid timezone.\n"
                "Examples: `America/New_York`, `Europe/London`, `Asia/Tokyo`\n"
                "Use `/list-timezones` to see common timezones."
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
    
    @app_commands.command(name="time", description="Get current time in your timezone or convert between timezones")
    @app_commands.describe(
        target_timezone="Timezone to show time for (optional, uses your saved timezone)",
        time_to_convert="Time to convert (format: HH:MM or YYYY-MM-DD HH:MM)"
    )
    async def get_time(self, interaction: discord.Interaction, 
                      target_timezone: Optional[str] = None,
                      time_to_convert: Optional[str] = None):
        """Get current time or convert time between timezones"""
        
        user_tz_name = self.timezone_db.get(str(interaction.user.id))
        
        # If no timezone specified, use user's saved timezone or UTC
        if not target_timezone:
            if user_tz_name:
                target_timezone = user_tz_name
            else:
                await interaction.response.send_message(
                    embed=EmbedBuilder.warning_embed(
                        "No Timezone Set",
                        "Please set your timezone first using `/set-timezone` or specify a timezone in this command."
                    ),
                    ephemeral=True
                )
                return
        
        try:
            target_tz = pytz.timezone(target_timezone)
            
            if time_to_convert:
                # Convert specific time
                try:
                    # Parse time string
                    if len(time_to_convert.split()) == 1:  # Just time (HH:MM)
                        time_obj = datetime.strptime(time_to_convert, "%H:%M")
                        today = datetime.now().date()
                        time_obj = datetime.combine(today, time_obj.time())
                    else:  # Date and time
                        time_obj = datetime.strptime(time_to_convert, "%Y-%m-%d %H:%M")
                    
                    # Assume input is in user's timezone if they have one set
                    if user_tz_name:
                        user_tz = pytz.timezone(user_tz_name)
                        localized_time = user_tz.localize(time_obj)
                    else:
                        localized_time = pytz.utc.localize(time_obj)
                    
                    # Convert to target timezone
                    converted_time = localized_time.astimezone(target_tz)
                    
                    embed = EmbedBuilder.info_embed(
                        "⏰ Time Conversion",
                        f"**Original:** {time_to_convert} ({user_tz_name or 'UTC'})\n"
                        f"**Converted:** {converted_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
                        f"**Timezone:** {target_timezone}"
                    )
                    
                except ValueError:
                    await interaction.response.send_message(
                        embed=EmbedBuilder.error_embed(
                            "Invalid Time Format",
                            "Please use format: `HH:MM` or `YYYY-MM-DD HH:MM`\nExample: `14:30` or `2024-12-25 14:30`"
                        ),
                        ephemeral=True
                    )
                    return
            else:
                # Show current time
                current_time = datetime.now(target_tz)
                
                embed = discord.Embed(
                    title="🕐 Current Time",
                    color=Config.COLORS['info']
                )
                embed.add_field(
                    name="Time",
                    value=f"**{current_time.strftime('%H:%M:%S')}**",
                    inline=True
                )
                embed.add_field(
                    name="Date", 
                    value=f"**{current_time.strftime('%Y-%m-%d')}**",
                    inline=True
                )
                embed.add_field(
                    name="Timezone",
                    value=f"**{target_timezone}**",
                    inline=True
                )
                
                # Add Discord timestamp
                timestamp = int(current_time.timestamp())
                embed.add_field(
                    name="Discord Timestamp",
                    value=f"<t:{timestamp}:F>",
                    inline=False
                )
                
                embed.set_footer(text="Use /set-timezone to set your default timezone")
            
            await interaction.response.send_message(embed=embed)
            
        except pytz.exceptions.UnknownTimeZoneError:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed(
                    "Invalid Timezone",
                    f"'{target_timezone}' is not a valid timezone."
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="mytimezone", description="Show your current timezone and time")
    async def my_timezone(self, interaction: discord.Interaction):
        """Show user's current timezone and local time"""
        
        user_id = str(interaction.user.id)
        user_tz_name = self.timezone_db.get(user_id)
        
        if not user_tz_name:
            # No timezone set - show UTC and suggest setting timezone
            utc_time = datetime.now(pytz.UTC)
            
            embed = discord.Embed(
                title="⏰ Your Timezone Info",
                description="You haven't set your timezone yet!",
                color=Config.COLORS['warning']
            )
            
            embed.add_field(
                name="Current UTC Time",
                value=f"{utc_time.strftime('%I:%M:%S %p')} UTC\n{utc_time.strftime('%A, %B %d, %Y')}",
                inline=False
            )
            
            embed.add_field(
                name="How to Set Your Timezone",
                value="Use `/set-timezone` followed by your timezone:\n\n"
                      "🇺🇸 `/set-timezone America/New_York`\n"
                      "🇬🇧 `/set-timezone Europe/London`\n"
                      "🇯🇵 `/set-timezone Asia/Tokyo`\n\n"
                      "Use `/list-timezones` to see more options!",
                inline=False
            )
            
        else:
            try:
                # Get user's timezone and current time
                user_tz = pytz.timezone(user_tz_name)
                local_time = datetime.now(user_tz)
                
                # Get timezone info
                tz_offset = local_time.strftime('%z')
                tz_name = local_time.strftime('%Z')
                
                # Format offset nicely (e.g., +0500 -> +05:00)
                if len(tz_offset) == 5:
                    formatted_offset = f"{tz_offset[:3]}:{tz_offset[3:]}"
                else:
                    formatted_offset = tz_offset
                
                # Create a cleaner timezone display name
                timezone_display = user_tz_name.replace('_', ' ').replace('/', ' → ')
                
                embed = discord.Embed(
                    title="🌍 Your Current Time",
                    color=Config.COLORS['success']
                )
                
                # Main time display - large and prominent
                embed.add_field(
                    name="🕐 Right Now",
                    value=f"# {local_time.strftime('%I:%M:%S %p')}\n"
                          f"**{local_time.strftime('%A, %B %d, %Y')}**",
                    inline=False
                )
                
                # Timezone info in a clean format
                embed.add_field(
                    name="🌐 Your Timezone",
                    value=f"**{timezone_display}**\n"
                          f"UTC {formatted_offset} ({tz_name})",
                    inline=False
                )
                
                # Additional useful info
                day_name = local_time.strftime('%A')
                week_number = local_time.isocalendar()[1]
                embed.add_field(
                    name="📅 Additional Info",
                    value=f"Week {week_number} of the year\n"
                          f"Day {local_time.timetuple().tm_yday} of {local_time.year}",
                    inline=True
                )
                
                # Discord timestamp for sharing
                timestamp = int(local_time.timestamp())
                embed.add_field(
                    name="🔗 Share This Time",
                    value=f"`<t:{timestamp}:F>`",
                    inline=True
                )
                
                embed.set_footer(text="💡 Use /set-timezone to change • This message is only visible to you")
                
            except pytz.exceptions.UnknownTimeZoneError:
                # Handle invalid timezone in database
                embed = discord.Embed(
                    title="❌ Timezone Error",
                    description=f"Your saved timezone '{user_tz_name}' is no longer valid.",
                    color=Config.COLORS['error']
                )
                embed.add_field(
                    name="What to do",
                    value="Please set a new timezone using `/set-timezone`\n"
                          "Use `/list-timezones` to see available options.",
                    inline=False
                )
                # Remove invalid timezone from database
                del self.timezone_db[user_id]
                self.save_timezone_data()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="list-timezones", description="Browse all available timezones by region")
    @app_commands.describe(region="Filter by region (optional)")
    @app_commands.choices(region=[
        app_commands.Choice(name="🇺🇸 North America", value="north_america"),
        app_commands.Choice(name="🇲🇽 Central/South America", value="south_america"),
        app_commands.Choice(name="🇬🇧 Europe/UK", value="europe"),
        app_commands.Choice(name="🇯🇵 Asia/Pacific", value="asia_pacific"),
        app_commands.Choice(name="🌍 Africa/Middle East", value="africa_middle_east"),
        app_commands.Choice(name="🌊 Oceania/Islands", value="oceania"),
        app_commands.Choice(name="⏰ UTC/GMT", value="utc")
    ])
    async def list_timezones(self, interaction: discord.Interaction, region: str = None):
        """Show comprehensive list of timezones by region"""
        
        all_timezones = {
            "north_america": {
                "title": "🇺🇸 North America",
                "zones": [
                    "America/New_York - Eastern Time (US & Canada)",
                    "America/Chicago - Central Time (US & Canada)",
                    "America/Denver - Mountain Time (US & Canada)", 
                    "America/Phoenix - Arizona (No DST)",
                    "America/Los_Angeles - Pacific Time (US & Canada)",
                    "America/Anchorage - Alaska Time",
                    "Pacific/Honolulu - Hawaii Time",
                    "America/Toronto - Eastern Canada",
                    "America/Vancouver - Pacific Canada",
                    "America/Montreal - Eastern Canada",
                    "America/Winnipeg - Central Canada",
                    "America/Edmonton - Mountain Canada",
                    "America/Halifax - Atlantic Canada",
                    "America/St_Johns - Newfoundland"
                ]
            },
            "south_america": {
                "title": "🇲🇽 Central & South America",
                "zones": [
                    "America/Mexico_City - Mexico Central",
                    "America/Tijuana - Mexico Pacific",
                    "America/Cancun - Mexico Eastern",
                    "America/Guatemala - Guatemala",
                    "America/Costa_Rica - Costa Rica",
                    "America/Panama - Panama",
                    "America/Bogota - Colombia",
                    "America/Caracas - Venezuela",
                    "America/Lima - Peru",
                    "America/La_Paz - Bolivia",
                    "America/Santiago - Chile",
                    "America/Argentina/Buenos_Aires - Argentina",
                    "America/Sao_Paulo - Brazil (São Paulo)",
                    "America/Brasilia - Brazil (Brasília)",
                    "America/Manaus - Brazil (Amazonas)"
                ]
            },
            "europe": {
                "title": "🇬🇧 Europe & UK",
                "zones": [
                    "Europe/London - United Kingdom (GMT/BST)",
                    "Europe/Dublin - Ireland",
                    "Europe/Paris - France (CET)",
                    "Europe/Berlin - Germany (CET)",
                    "Europe/Amsterdam - Netherlands (CET)",
                    "Europe/Brussels - Belgium (CET)",
                    "Europe/Madrid - Spain (CET)",
                    "Europe/Rome - Italy (CET)",
                    "Europe/Vienna - Austria (CET)",
                    "Europe/Zurich - Switzerland (CET)",
                    "Europe/Stockholm - Sweden (CET)",
                    "Europe/Oslo - Norway (CET)",
                    "Europe/Copenhagen - Denmark (CET)",
                    "Europe/Warsaw - Poland (CET)",
                    "Europe/Prague - Czech Republic (CET)",
                    "Europe/Budapest - Hungary (CET)",
                    "Europe/Athens - Greece (EET)",
                    "Europe/Helsinki - Finland (EET)",
                    "Europe/Moscow - Russia (MSK)",
                    "Europe/Kiev - Ukraine (EET)",
                    "Europe/Istanbul - Turkey (TRT)"
                ]
            },
            "asia_pacific": {
                "title": "🇯🇵 Asia & Pacific",
                "zones": [
                    "Asia/Tokyo - Japan (JST)",
                    "Asia/Seoul - South Korea (KST)",
                    "Asia/Shanghai - China (CST)",
                    "Asia/Hong_Kong - Hong Kong",
                    "Asia/Taipei - Taiwan",
                    "Asia/Singapore - Singapore",
                    "Asia/Manila - Philippines",
                    "Asia/Jakarta - Indonesia (Western)",
                    "Asia/Bangkok - Thailand",
                    "Asia/Ho_Chi_Minh - Vietnam",
                    "Asia/Kuala_Lumpur - Malaysia",
                    "Asia/Kolkata - India (IST)",
                    "Asia/Karachi - Pakistan",
                    "Asia/Dhaka - Bangladesh",
                    "Asia/Kathmandu - Nepal",
                    "Asia/Colombo - Sri Lanka",
                    "Asia/Almaty - Kazakhstan",
                    "Asia/Tashkent - Uzbekistan"
                ]
            },
            "africa_middle_east": {
                "title": "🌍 Africa & Middle East",
                "zones": [
                    "Africa/Cairo - Egypt",
                    "Africa/Lagos - Nigeria (West Africa)",
                    "Africa/Johannesburg - South Africa",
                    "Africa/Nairobi - Kenya (East Africa)",
                    "Africa/Casablanca - Morocco",
                    "Africa/Tunis - Tunisia",
                    "Africa/Algiers - Algeria",
                    "Asia/Dubai - UAE",
                    "Asia/Riyadh - Saudi Arabia",
                    "Asia/Qatar - Qatar",
                    "Asia/Kuwait - Kuwait",
                    "Asia/Baghdad - Iraq",
                    "Asia/Tehran - Iran",
                    "Asia/Jerusalem - Israel",
                    "Asia/Beirut - Lebanon",
                    "Asia/Damascus - Syria"
                ]
            },
            "oceania": {
                "title": "🌊 Oceania & Islands",
                "zones": [
                    "Australia/Sydney - Australia Eastern",
                    "Australia/Melbourne - Australia Eastern",
                    "Australia/Brisbane - Australia Eastern (No DST)",
                    "Australia/Adelaide - Australia Central",
                    "Australia/Perth - Australia Western",
                    "Australia/Darwin - Australia Central (No DST)",
                    "Pacific/Auckland - New Zealand",
                    "Pacific/Fiji - Fiji",
                    "Pacific/Guam - Guam",
                    "Pacific/Tahiti - French Polynesia",
                    "Pacific/Marquesas - Marquesas Islands",
                    "Pacific/Galapagos - Galapagos Islands",
                    "Pacific/Easter - Easter Island"
                ]
            },
            "utc": {
                "title": "⏰ UTC & Standard Times", 
                "zones": [
                    "UTC - Coordinated Universal Time",
                    "GMT - Greenwich Mean Time", 
                    "EST - Eastern Standard Time",
                    "CST - Central Standard Time",
                    "MST - Mountain Standard Time",
                    "PST - Pacific Standard Time",
                    "CET - Central European Time",
                    "EET - Eastern European Time",
                    "JST - Japan Standard Time",
                    "IST - India Standard Time",
                    "AEST - Australian Eastern Standard Time"
                ]
            }
        }
        
        if region and region in all_timezones:
            # Show specific region
            region_data = all_timezones[region]
            embed = discord.Embed(
                title=f"{region_data['title']} Timezones",
                description="Copy and paste the timezone name (before the dash) into `/set-timezone`",
                color=Config.COLORS['info']
            )
            
            # Split zones into chunks of 10 for readability
            zones = region_data['zones']
            for i in range(0, len(zones), 10):
                chunk = zones[i:i+10]
                field_name = f"Timezones {i//10 + 1}" if len(zones) > 10 else "Available Timezones"
                embed.add_field(
                    name=field_name,
                    value="\n".join([f"`{tz}`" for tz in chunk]),
                    inline=False
                )
                
        else:
            # Show all regions overview
            embed = discord.Embed(
                title="🌍 All Timezone Regions",
                description="Choose a region to see detailed timezone list, or use the command with a region filter.",
                color=Config.COLORS['info']
            )
            
            for region_key, region_data in all_timezones.items():
                zone_count = len(region_data['zones'])
                embed.add_field(
                    name=region_data['title'],
                    value=f"{zone_count} timezones available\nUse `/list-timezones region:{region_key}`",
                    inline=True
                )
        
        embed.add_field(
            name="💡 How to Use",
            value="1. Find your timezone in the list\n"
                  "2. Copy the name before the dash (e.g., `America/New_York`)\n"
                  "3. Use `/set-timezone America/New_York`\n"
                  "4. Then use `/mytimezone` to see your time!",
            inline=False
        )
        
        embed.set_footer(text="Need help? The timezone name is always the part before the ' - ' dash")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # CLOCK IN/OUT SYSTEM
    @app_commands.command(name="clockin", description="Clock in to start a work session")
    async def clock_in(self, interaction: discord.Interaction):
        """Clock in to start a work session"""
        
        user_id = interaction.user.id
        
        # Check if already clocked in
        if user_id in self.active_sessions:
            current_session = self.active_sessions[user_id]
            start_time = datetime.fromtimestamp(current_session['start_time'])
            
            await interaction.response.send_message(
                embed=EmbedBuilder.warning_embed(
                    "Already Clocked In",
                    f"You're already clocked in since {start_time.strftime('%H:%M:%S')}\n"
                    f"Use `/clockout` to end your current session."
                ),
                ephemeral=True
            )
            return
        
        # Get user's timezone
        user_tz_name = self.timezone_db.get(str(user_id))
        if user_tz_name:
            user_tz = pytz.timezone(user_tz_name)
            clock_time = datetime.now(user_tz)
        else:
            clock_time = datetime.now(pytz.UTC)
            user_tz_name = "UTC"
        
        # Start session
        session_data = {
            'start_time': clock_time.timestamp(),
            'user': interaction.user,
            'channel': interaction.channel,
            'timezone': user_tz_name,
            'reminded': False
        }
        
        self.active_sessions[user_id] = session_data
        
        # Create embed
        embed = EmbedBuilder.success_embed(
            "🕐 Clocked In",
            f"**Time:** {clock_time.strftime('%H:%M:%S %Z')}\n"
            f"**Date:** {clock_time.strftime('%Y-%m-%d')}\n\n"
            f"You'll be reminded after 30 minutes if you're still clocked in."
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="clockout", description="Clock out to end your work session")
    async def clock_out(self, interaction: discord.Interaction):
        """Clock out to end work session"""
        
        user_id = interaction.user.id
        
        # Check if clocked in
        if user_id not in self.active_sessions:
            await interaction.response.send_message(
                embed=EmbedBuilder.warning_embed(
                    "Not Clocked In",
                    "You're not currently clocked in. Use `/clockin` to start a session."
                ),
                ephemeral=True
            )
            return
        
        # Get session data
        session = self.active_sessions[user_id]
        
        # Get user's timezone
        user_tz_name = session['timezone']
        user_tz = pytz.timezone(user_tz_name)
        
        start_time = datetime.fromtimestamp(session['start_time'], user_tz)
        end_time = datetime.now(user_tz)
        
        # Calculate duration
        duration = end_time - start_time
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Remove from active sessions
        del self.active_sessions[user_id]
        
        # Create embed
        embed = EmbedBuilder.success_embed(
            "🕐 Clocked Out",
            f"**Clock In:** {start_time.strftime('%H:%M:%S')}\n"
            f"**Clock Out:** {end_time.strftime('%H:%M:%S')}\n"
            f"**Duration:** {hours}h {minutes}m {seconds}s\n"
            f"**Date:** {end_time.strftime('%Y-%m-%d %Z')}"
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="status", description="Check your current clock status")
    async def clock_status(self, interaction: discord.Interaction):
        """Check current clock status"""
        
        user_id = interaction.user.id
        
        if user_id not in self.active_sessions:
            embed = EmbedBuilder.info_embed(
                "🕐 Clock Status",
                "You are currently **not clocked in**.\n\nUse `/clockin` to start a work session."
            )
        else:
            session = self.active_sessions[user_id]
            
            # Get timezone info
            user_tz = pytz.timezone(session['timezone'])
            start_time = datetime.fromtimestamp(session['start_time'], user_tz)
            current_time = datetime.now(user_tz)
            
            # Calculate duration
            duration = current_time - start_time
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            embed = EmbedBuilder.info_embed(
                "🕐 Clock Status",
                f"You are currently **clocked in**.\n\n"
                f"**Started:** {start_time.strftime('%H:%M:%S')}\n"
                f"**Duration:** {hours}h {minutes}m {seconds}s\n"
                f"**Timezone:** {session['timezone']}"
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @tasks.loop(minutes=1)
    async def check_clockin_timeout(self):
        """Check for users who need to be reminded about clocking out"""
        current_time = datetime.now().timestamp()
        
        for user_id, session in list(self.active_sessions.items()):
            # Check if 30 minutes have passed and user hasn't been reminded
            if (current_time - session['start_time'] >= Config.CLOCKIN_TIMEOUT and 
                not session['reminded']):
                
                try:
                    # Create reminder embed
                    embed = EmbedBuilder.warning_embed(
                        "⏰ Clock Out Reminder",
                        f"You've been clocked in for 30 minutes!\n\n"
                        f"React with {Config.EMOJIS['tick']} to continue working\n"
                        f"React with {Config.EMOJIS['cross']} to clock out now\n\n"
                        f"If you don't respond, you'll be automatically clocked out."
                    )
                    
                    # Send reminder
                    user = session['user']
                    message = await session['channel'].send(f"{user.mention}", embed=embed)
                    
                    # Add reactions
                    await message.add_reaction(Config.EMOJIS['tick'])
                    await message.add_reaction(Config.EMOJIS['cross'])
                    
                    # Mark as reminded
                    session['reminded'] = True
                    session['reminder_message'] = message
                    
                    # Wait for reaction or timeout
                    self.bot.loop.create_task(
                        self.handle_clockout_reminder(user_id, message)
                    )
                    
                except Exception as e:
                    logging.error(f"Error sending clock reminder: {e}")
    
    async def handle_clockout_reminder(self, user_id: int, message: discord.Message):
        """Handle the clock out reminder reaction"""
        try:
            # Wait for reaction
            def check(reaction, user):
                return (user.id == user_id and 
                       str(reaction.emoji) in [Config.EMOJIS['tick'], Config.EMOJIS['cross']] and
                       reaction.message.id == message.id)
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300)  # 5 minutes
                
                if str(reaction.emoji) == Config.EMOJIS['tick']:
                    # Continue working - reset timer
                    if user_id in self.active_sessions:
                        self.active_sessions[user_id]['start_time'] = datetime.now().timestamp()
                        self.active_sessions[user_id]['reminded'] = False
                    
                    await message.edit(
                        embed=EmbedBuilder.success_embed(
                            "✅ Continuing Work",
                            "Your work session continues. Timer has been reset."
                        )
                    )
                    
                elif str(reaction.emoji) == Config.EMOJIS['cross']:
                    # Clock out
                    if user_id in self.active_sessions:
                        # Calculate final duration
                        session = self.active_sessions[user_id]
                        user_tz = pytz.timezone(session['timezone'])
                        start_time = datetime.fromtimestamp(session['start_time'], user_tz)
                        end_time = datetime.now(user_tz)
                        duration = end_time - start_time
                        hours, remainder = divmod(int(duration.total_seconds()), 3600)
                        minutes, _ = divmod(remainder, 60)
                        
                        del self.active_sessions[user_id]
                        
                        await message.edit(
                            embed=EmbedBuilder.success_embed(
                                "🕐 Clocked Out",
                                f"You have been clocked out.\n"
                                f"Total session: {hours}h {minutes}m"
                            )
                        )
                
            except asyncio.TimeoutError:
                # Auto clock out
                if user_id in self.active_sessions:
                    session = self.active_sessions[user_id]
                    user_tz = pytz.timezone(session['timezone'])
                    start_time = datetime.fromtimestamp(session['start_time'], user_tz)
                    end_time = datetime.now(user_tz)
                    duration = end_time - start_time
                    hours, remainder = divmod(int(duration.total_seconds()), 3600)
                    minutes, _ = divmod(remainder, 60)
                    
                    del self.active_sessions[user_id]
                    
                    await message.edit(
                        embed=EmbedBuilder.warning_embed(
                            "⏰ Auto Clocked Out",
                            f"You've been automatically clocked out due to inactivity.\n"
                            f"Total session: {hours}h {minutes}m"
                        )
                    )
        
        except Exception as e:
            logging.error(f"Error handling clock reminder: {e}")
    
    @check_clockin_timeout.before_loop
    async def before_check_clockin_timeout(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TimeManagement(bot))
