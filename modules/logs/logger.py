import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Dict, List
import asyncio
import json
import os
from datetime import datetime
from utils.user_utils import EmbedBuilder, PermissionChecker
from config.config import Config
import logging

class LogsModule(commands.Cog):
    """Comprehensive Logging Module - Log all server activities with professional UI"""
    
    def __init__(self, bot):
        self.bot = bot
        self.log_channels = {}  # guild_id: {log_type: channel_id}
        self.load_log_config()
    
    def load_log_config(self):
        """Load logging configuration from file"""
        try:
            if os.path.exists('data/log_config.json'):
                with open('data/log_config.json', 'r') as f:
                    self.log_channels = json.load(f)
        except Exception as e:
            logging.error(f"Error loading log config: {e}")
            self.log_channels = {}
    
    def save_log_config(self):
        """Save logging configuration to file"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/log_config.json', 'w') as f:
                json.dump(self.log_channels, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving log config: {e}")
    
    # SETUP COMMANDS
    @app_commands.command(name="setup-logs", description="Automatically set up all logging channels")
    async def setup_logs(self, interaction: discord.Interaction):
        """Set up all logging channels automatically"""
        
        # Check permissions
        if not PermissionChecker.has_admin_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Access Denied", "You need administrator permissions to set up logging."),
                ephemeral=True
            )
            return
        
        guild = interaction.guild
        guild_id = str(guild.id)
        
        # Initialize guild config
        if guild_id not in self.log_channels:
            self.log_channels[guild_id] = {}
        
        try:
            # Create or find logging category
            log_category = None
            for category in guild.categories:
                if category.name.lower() == "📋 server logs":
                    log_category = category
                    break
            
            if not log_category:
                # Create new category
                log_category = await guild.create_category(
                    name="📋 Server Logs",
                    overwrites={
                        guild.default_role: discord.PermissionOverwrite(
                            read_messages=False,
                            send_messages=False
                        ),
                        guild.me: discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            manage_messages=True
                        )
                    }
                )
            
            # Define channels to create
            log_channels_to_create = {
                'message_logs': '💬-message-logs',
                'member_logs': '👤-member-logs',
                'voice_logs': '🔊-voice-logs',
                'moderation_logs': '🔨-moderation-logs',
                'server_logs': '⚙️-server-logs'
            }
            
            created_channels = []
            
            # Create channels
            for log_type, channel_name in log_channels_to_create.items():
                # Check if channel already exists
                existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
                
                if existing_channel:
                    # Use existing channel
                    self.log_channels[guild_id][log_type] = existing_channel.id
                    created_channels.append(f"✅ {channel_name} (existing)")
                else:
                    # Create new channel
                    channel = await guild.create_text_channel(
                        name=channel_name,
                        category=log_category,
                        topic=f"Automated logging for {log_type.replace('_', ' ').title()}"
                    )
                    self.log_channels[guild_id][log_type] = channel.id
                    created_channels.append(f"✅ {channel_name} (created)")
            
            # Save configuration
            self.save_log_config()
            
            # Success response
            embed = EmbedBuilder.success_embed(
                "🎉 Logging Setup Complete",
                f"**Category:** {log_category.mention}\\n\\n" +
                "\\n".join(created_channels) +
                "\\n\\n**Features Enabled:**\\n" +
                "• Message logging (edit, delete, bulk delete)\\n" +
                "• Member logging (join, leave, nickname changes)\\n" +
                "• Voice logging (join, leave, channel moves)\\n" +
                "• Moderation logging (kicks, bans, timeouts)\\n" +
                "• Server logging (channel/role changes)\\n\\n" +
                "All server activity will now be logged automatically!"
            )
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Permission Error", "I don't have permission to create channels or categories."),
                ephemeral=True
            )
        except Exception as e:
            logging.error(f"Error setting up logs: {e}")
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Setup Error", "An error occurred while setting up logging. Please try again."),
                ephemeral=True
            )
    
    @app_commands.command(name="log-status", description="Check logging configuration status")
    async def log_status(self, interaction: discord.Interaction):
        """Check current logging configuration"""
        
        guild_id = str(interaction.guild.id)
        
        if guild_id not in self.log_channels or not self.log_channels[guild_id]:
            embed = EmbedBuilder.warning_embed(
                "⚠️ Logging Not Configured",
                "Logging is not set up for this server.\\n\\nUse `/setup-logs` to configure automatic logging."
            )
        else:
            # Check channel status
            status_lines = []
            for log_type, channel_id in self.log_channels[guild_id].items():
                channel = self.bot.get_channel(channel_id)
                if channel:
                    status_lines.append(f"✅ **{log_type.replace('_', ' ').title()}**: {channel.mention}")
                else:
                    status_lines.append(f"❌ **{log_type.replace('_', ' ').title()}**: Channel not found")
            
            embed = EmbedBuilder.info_embed(
                "📋 Logging Status",
                "\\n".join(status_lines)
            )
            embed.add_field(
                name="Active Features",
                value="• Message logging\\n• Member activity\\n• Voice activity\\n• Moderation actions\\n• Server changes",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # UTILITY METHODS
    async def log_to_channel(self, guild: discord.Guild, log_type: str, embed: discord.Embed):
        """Log an embed to the appropriate channel"""
        try:
            guild_id = str(guild.id)
            if guild_id not in self.log_channels or log_type not in self.log_channels[guild_id]:
                return
            
            channel_id = self.log_channels[guild_id][log_type]
            channel = self.bot.get_channel(channel_id)
            
            if channel:
                await channel.send(embed=embed)
        except Exception as e:
            logging.error(f"Error logging to channel: {e}")
    
    def create_log_embed(self, title: str, description: str, color: int, user: discord.Member = None) -> discord.Embed:
        """Create a standardized log embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        
        if user:
            embed.set_author(
                name=f"{user.display_name} ({user.name}#{user.discriminator})",
                icon_url=user.display_avatar.url
            )
            embed.add_field(name="User ID", value=user.id, inline=True)
        
        return embed
    
    # MESSAGE LOGGING
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Log message deletions"""
        if message.author.bot or not message.guild:
            return
        
        embed = self.create_log_embed(
            "🗑️ Message Deleted",
            f"**Channel:** {message.channel.mention}\\n"
            f"**Content:** {message.content[:1000] if message.content else '*No content*'}\\n"
            f"**Message ID:** {message.id}",
            Config.COLORS['error'],
            message.author
        )
        
        if message.attachments:
            attachments = "\\n".join([f"• {att.filename}" for att in message.attachments])
            embed.add_field(name="Attachments", value=attachments, inline=False)
        
        await self.log_to_channel(message.guild, 'message_logs', embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Log message edits"""
        if before.author.bot or not before.guild or before.content == after.content:
            return
        
        embed = self.create_log_embed(
            "✏️ Message Edited",
            f"**Channel:** {before.channel.mention}\\n"
            f"**Message ID:** {before.id}\\n"
            f"**[Jump to Message]({after.jump_url})**",
            Config.COLORS['warning'],
            before.author
        )
        
        embed.add_field(
            name="Before",
            value=before.content[:1000] if before.content else "*No content*",
            inline=False
        )
        embed.add_field(
            name="After",
            value=after.content[:1000] if after.content else "*No content*",
            inline=False
        )
        
        await self.log_to_channel(before.guild, 'message_logs', embed)
    
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: List[discord.Message]):
        """Log bulk message deletions"""
        if not messages or not messages[0].guild:
            return
        
        guild = messages[0].guild
        channel = messages[0].channel
        
        embed = discord.Embed(
            title="🗑️ Bulk Message Delete",
            description=f"**{len(messages)}** messages were deleted from {channel.mention}",
            color=Config.COLORS['error'],
            timestamp=datetime.utcnow()
        )
        
        # Show authors involved
        authors = set()
        for msg in messages:
            if not msg.author.bot:
                authors.add(f"{msg.author.display_name}")
        
        if authors:
            embed.add_field(
                name="Users Affected",
                value="\\n".join(list(authors)[:10]) + (f"\\n... and {len(authors) - 10} more" if len(authors) > 10 else ""),
                inline=False
            )
        
        await self.log_to_channel(guild, 'message_logs', embed)
    
    # MEMBER LOGGING
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Log member joins"""
        embed = self.create_log_embed(
            "📥 Member Joined",
            f"**Account Created:** <t:{int(member.created_at.timestamp())}:R>\\n"
            f"**Member #{len(member.guild.members)}**",
            Config.COLORS['success'],
            member
        )
        
        await self.log_to_channel(member.guild, 'member_logs', embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Log member leaves"""
        embed = self.create_log_embed(
            "📤 Member Left",
            f"**Joined Server:** <t:{int(member.joined_at.timestamp())}:R>\\n"
            f"**Roles:** {', '.join([role.name for role in member.roles[1:]]) or 'None'}",
            Config.COLORS['error'],
            member
        )
        
        await self.log_to_channel(member.guild, 'member_logs', embed)
    
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Log member updates (nickname, roles)"""
        embed = None
        
        # Nickname change
        if before.nick != after.nick:
            embed = self.create_log_embed(
                "🏷️ Nickname Changed",
                f"**Before:** {before.nick or before.name}\\n"
                f"**After:** {after.nick or after.name}",
                Config.COLORS['info'],
                after
            )
        
        # Role changes
        elif before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            
            if added_roles or removed_roles:
                description_parts = []
                if added_roles:
                    description_parts.append(f"**Added:** {', '.join([role.name for role in added_roles])}")
                if removed_roles:
                    description_parts.append(f"**Removed:** {', '.join([role.name for role in removed_roles])}")
                
                embed = self.create_log_embed(
                    "🎭 Roles Updated",
                    "\\n".join(description_parts),
                    Config.COLORS['info'],
                    after
                )
        
        if embed:
            await self.log_to_channel(after.guild, 'member_logs', embed)
    
    # VOICE LOGGING
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Log voice activity"""
        if before.channel == after.channel:
            return
        
        embed = None
        
        if before.channel is None and after.channel is not None:
            # Joined voice channel
            embed = self.create_log_embed(
                "🔊 Voice Join",
                f"**Channel:** {after.channel.name}\\n"
                f"**Category:** {after.channel.category.name if after.channel.category else 'None'}",
                Config.COLORS['success'],
                member
            )
        
        elif before.channel is not None and after.channel is None:
            # Left voice channel
            embed = self.create_log_embed(
                "🔇 Voice Leave",
                f"**Channel:** {before.channel.name}\\n"
                f"**Category:** {before.channel.category.name if before.channel.category else 'None'}",
                Config.COLORS['error'],
                member
            )
        
        elif before.channel is not None and after.channel is not None:
            # Moved between channels
            embed = self.create_log_embed(
                "🔄 Voice Move",
                f"**From:** {before.channel.name}\\n"
                f"**To:** {after.channel.name}",
                Config.COLORS['info'],
                member
            )
        
        if embed:
            await self.log_to_channel(member.guild, 'voice_logs', embed)
    
    # MODERATION LOGGING
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        """Log member bans"""
        # Try to get ban reason
        try:
            ban_info = await guild.fetch_ban(user)
            reason = ban_info.reason or "No reason provided"
        except:
            reason = "No reason provided"
        
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"**User:** {user.mention}\\n"
                       f"**Reason:** {reason}",
            color=Config.COLORS['error'],
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"{user.display_name} ({user.name}#{user.discriminator})", 
                        icon_url=user.display_avatar.url)
        embed.add_field(name="User ID", value=user.id, inline=True)
        
        await self.log_to_channel(guild, 'moderation_logs', embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        """Log member unbans"""
        embed = discord.Embed(
            title="🔓 Member Unbanned",
            description=f"**User:** {user.mention}",
            color=Config.COLORS['success'],
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"{user.display_name} ({user.name}#{user.discriminator})", 
                        icon_url=user.display_avatar.url)
        embed.add_field(name="User ID", value=user.id, inline=True)
        
        await self.log_to_channel(guild, 'moderation_logs', embed)
    
    # SERVER LOGGING
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Log channel creation"""
        embed = discord.Embed(
            title="📝 Channel Created",
            description=f"**Channel:** {channel.mention}\\n"
                       f"**Type:** {str(channel.type).title()}\\n"
                       f"**Category:** {channel.category.name if channel.category else 'None'}",
            color=Config.COLORS['success'],
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Channel ID", value=channel.id, inline=True)
        
        await self.log_to_channel(channel.guild, 'server_logs', embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Log channel deletion"""
        embed = discord.Embed(
            title="🗑️ Channel Deleted",
            description=f"**Channel:** #{channel.name}\\n"
                       f"**Type:** {str(channel.type).title()}\\n"
                       f"**Category:** {channel.category.name if channel.category else 'None'}",
            color=Config.COLORS['error'],
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Channel ID", value=channel.id, inline=True)
        
        await self.log_to_channel(channel.guild, 'server_logs', embed)
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Log role creation"""
        embed = discord.Embed(
            title="🎭 Role Created",
            description=f"**Role:** {role.mention}\\n"
                       f"**Color:** {str(role.color)}\\n"
                       f"**Hoisted:** {'Yes' if role.hoist else 'No'}\\n"
                       f"**Mentionable:** {'Yes' if role.mentionable else 'No'}",
            color=Config.COLORS['success'],
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Role ID", value=role.id, inline=True)
        
        await self.log_to_channel(role.guild, 'server_logs', embed)
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Log role deletion"""
        embed = discord.Embed(
            title="🗑️ Role Deleted",
            description=f"**Role:** {role.name}\\n"
                       f"**Color:** {str(role.color)}\\n"
                       f"**Members:** {len(role.members)}",
            color=Config.COLORS['error'],
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Role ID", value=role.id, inline=True)
        
        await self.log_to_channel(role.guild, 'server_logs', embed)

async def setup(bot):
    await bot.add_cog(LogsModule(bot))
