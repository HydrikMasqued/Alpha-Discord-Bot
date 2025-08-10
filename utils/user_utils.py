import discord
from typing import Optional, Union
import re
from fuzzywuzzy import fuzz
import logging

class UserLookup:
    """Utility class for finding Discord members by various identifiers"""
    
    @staticmethod
    async def find_member(guild: discord.Guild, identifier: str) -> Optional[discord.Member]:
        """
        Find a member by display name, username, or user ID
        Returns the best match or None if no match found
        """
        if not identifier:
            return None
            
        identifier = identifier.strip()
        
        # Try to find by ID first (most accurate)
        if identifier.isdigit():
            member = guild.get_member(int(identifier))
            if member:
                return member
        
        # Try to find by mention
        mention_match = re.match(r'<@!?(\d+)>', identifier)
        if mention_match:
            member_id = int(mention_match.group(1))
            member = guild.get_member(member_id)
            if member:
                return member
        
        # Try exact matches first
        for member in guild.members:
            # Exact display name match
            if member.display_name.lower() == identifier.lower():
                return member
            # Exact username match
            if member.name.lower() == identifier.lower():
                return member
        
        # If no exact match, try fuzzy matching
        best_match = None
        best_score = 70  # Minimum similarity score
        
        for member in guild.members:
            # Check display name similarity
            display_score = fuzz.ratio(member.display_name.lower(), identifier.lower())
            if display_score > best_score:
                best_score = display_score
                best_match = member
            
            # Check username similarity
            username_score = fuzz.ratio(member.name.lower(), identifier.lower())
            if username_score > best_score:
                best_score = username_score
                best_match = member
        
        return best_match
    
    @staticmethod
    async def find_members_by_role(guild: discord.Guild, role_name: str) -> list[discord.Member]:
        """Find all members with a specific role"""
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            return []
        return role.members
    
    @staticmethod
    def format_member_info(member: discord.Member) -> str:
        """Format member information for display"""
        return f"{member.display_name} ({member.name}#{member.discriminator})"

class EmbedBuilder:
    """Utility class for creating consistent embeds"""
    
    @staticmethod
    def create_embed(title: str, description: str = "", color: int = 0x7289da, 
                    thumbnail: str = None, footer: str = None) -> discord.Embed:
        """Create a standardized embed"""
        embed = discord.Embed(title=title, description=description, color=color)
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        
        if footer:
            embed.set_footer(text=footer)
        else:
            embed.set_footer(text="Alpha Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    @staticmethod
    def success_embed(title: str, description: str = "") -> discord.Embed:
        """Create a success embed"""
        return EmbedBuilder.create_embed(title, description, 0x00ff00)
    
    @staticmethod
    def error_embed(title: str, description: str = "") -> discord.Embed:
        """Create an error embed"""
        return EmbedBuilder.create_embed(title, description, 0xff0000)
    
    @staticmethod
    def info_embed(title: str, description: str = "") -> discord.Embed:
        """Create an info embed"""
        return EmbedBuilder.create_embed(title, description, 0x0099ff)
    
    @staticmethod
    def warning_embed(title: str, description: str = "") -> discord.Embed:
        """Create a warning embed"""
        return EmbedBuilder.create_embed(title, description, 0xffff00)

class PermissionChecker:
    """Utility class for checking user permissions"""
    
    @staticmethod
    def has_admin_perms(member: discord.Member) -> bool:
        """Check if member has administrator permissions"""
        return member.guild_permissions.administrator
    
    @staticmethod
    def has_manage_roles_perms(member: discord.Member) -> bool:
        """Check if member can manage roles"""
        return member.guild_permissions.manage_roles or member.guild_permissions.administrator
    
    @staticmethod
    def has_manage_channels_perms(member: discord.Member) -> bool:
        """Check if member can manage channels"""
        return member.guild_permissions.manage_channels or member.guild_permissions.administrator
    
    @staticmethod
    def can_modify_member(requester: discord.Member, target: discord.Member) -> bool:
        """Check if requester can modify target member"""
        # Can't modify yourself
        if requester == target:
            return False
        
        # Can't modify bot owner or higher roles
        if target.top_role >= requester.top_role:
            return False
        
        # Must have appropriate permissions
        return PermissionChecker.has_manage_roles_perms(requester)

async def log_action(guild: discord.Guild, action: str, user: discord.Member, 
                    target: Union[discord.Member, str], details: str = ""):
    """Log an action to the appropriate log channel"""
    try:
        # This will be implemented in the logs module
        logging.info(f"Action logged: {action} by {user} on {target} - {details}")
    except Exception as e:
        logging.error(f"Failed to log action: {e}")

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent issues"""
    if not text:
        return ""
    
    # Remove mentions that could cause issues
    text = re.sub(r'@(everyone|here)', '@\u200b\\1', text)
    
    # Limit length
    if len(text) > 2000:
        text = text[:1997] + "..."
    
    return text.strip()
