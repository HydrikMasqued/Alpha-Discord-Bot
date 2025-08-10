import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Union
from utils.user_utils import UserLookup, EmbedBuilder, PermissionChecker, sanitize_input
from config.config import Config
import asyncio
import logging

class DiscordManagement(commands.Cog):
    """Discord Management Module - Handle announcements, messaging, and role management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    # ANNOUNCEMENT COMMANDS
    @app_commands.command(name="announce", description="Send an announcement to the announcement channel")
    @app_commands.describe(
        message="The announcement message to send",
        channel="The channel to send the announcement (optional, uses configured channel by default)"
    )
    async def announce(self, interaction: discord.Interaction, message: str, 
                      channel: Optional[discord.TextChannel] = None):
        """Send a professional announcement"""
        
        # Check permissions
        if not PermissionChecker.has_admin_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Access Denied", "You need administrator permissions to use this command."),
                ephemeral=True
            )
            return
        
        # Determine target channel
        target_channel = channel
        if not target_channel:
            if Config.ANNOUNCEMENT_CHANNEL_ID:
                target_channel = self.bot.get_channel(Config.ANNOUNCEMENT_CHANNEL_ID)
            else:
                await interaction.response.send_message(
                    embed=EmbedBuilder.error_embed("No Channel Set", "Please specify a channel or set ANNOUNCEMENT_CHANNEL_ID in config."),
                    ephemeral=True
                )
                return
        
        if not target_channel:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Channel Not Found", "The specified announcement channel could not be found."),
                ephemeral=True
            )
            return
        
        # Sanitize and prepare message
        clean_message = sanitize_input(message)
        
        # Create announcement embed
        embed = discord.Embed(
            title="📢 Announcement",
            description=clean_message,
            color=Config.COLORS['primary']
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        
        try:
            # Send announcement
            await target_channel.send(embed=embed)
            
            # Confirm to user
            confirm_embed = EmbedBuilder.success_embed(
                "Announcement Sent",
                f"Your announcement has been posted to {target_channel.mention}"
            )
            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Permission Error", "I don't have permission to send messages in that channel."),
                ephemeral=True
            )
        except Exception as e:
            logging.error(f"Error sending announcement: {e}")
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Error", "Failed to send announcement. Please try again."),
                ephemeral=True
            )
    
    # DIRECT MESSAGING COMMANDS
    @app_commands.command(name="dm", description="Send a direct message to a user through the bot")
    @app_commands.describe(
        user="The user to message (display name, username, or mention)",
        message="The message to send"
    )
    async def direct_message(self, interaction: discord.Interaction, user: str, message: str):
        """Send a direct message to a user"""
        
        # Check permissions
        if not PermissionChecker.has_admin_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Access Denied", "You need administrator permissions to use this command."),
                ephemeral=True
            )
            return
        
        # Find the target user
        target_member = await UserLookup.find_member(interaction.guild, user)
        if not target_member:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("User Not Found", f"Could not find a user matching '{user}'."),
                ephemeral=True
            )
            return
        
        clean_message = sanitize_input(message)
        
        # Create DM embed
        embed = discord.Embed(
            title="📨 Message from Server Staff",
            description=clean_message,
            color=Config.COLORS['info']
        )
        embed.add_field(name="Server", value=interaction.guild.name, inline=True)
        embed.add_field(name="Sent by", value=interaction.user.display_name, inline=True)
        embed.set_footer(text="This message was sent through Alpha Bot")
        
        try:
            # Send DM
            await target_member.send(embed=embed)
            
            # Confirm to sender
            confirm_embed = EmbedBuilder.success_embed(
                "Message Sent",
                f"Your message has been sent to {target_member.display_name}"
            )
            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Cannot Send DM", f"{target_member.display_name} has DMs disabled or blocked the bot."),
                ephemeral=True
            )
        except Exception as e:
            logging.error(f"Error sending DM: {e}")
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Error", "Failed to send message. Please try again."),
                ephemeral=True
            )
    
    # MASS MESSAGING COMMANDS
    @app_commands.command(name="mass-dm", description="Send a message to all users with a specific role")
    @app_commands.describe(
        role="The role to message",
        message="The message to send to all role members"
    )
    async def mass_direct_message(self, interaction: discord.Interaction, role: discord.Role, message: str):
        """Send a direct message to all users with a specific role"""
        
        # Check permissions
        if not PermissionChecker.has_admin_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Access Denied", "You need administrator permissions to use this command."),
                ephemeral=True
            )
            return
        
        # Get all members with the role
        members = role.members
        if not members:
            await interaction.response.send_message(
                embed=EmbedBuilder.warning_embed("No Members", f"No members found with the role {role.name}."),
                ephemeral=True
            )
            return
        
        # Confirm action
        confirm_embed = EmbedBuilder.warning_embed(
            "Mass DM Confirmation",
            f"You are about to send a message to **{len(members)}** members with the role **{role.name}**.\n\nThis action cannot be undone. Are you sure?"
        )
        
        # Create confirmation view
        view = ConfirmationView()
        await interaction.response.send_message(embed=confirm_embed, view=view, ephemeral=True)
        
        # Wait for confirmation
        await view.wait()
        if not view.confirmed:
            return
        
        clean_message = sanitize_input(message)
        
        # Create DM embed
        embed = discord.Embed(
            title=f"📨 Message to {role.name} Members",
            description=clean_message,
            color=Config.COLORS['info']
        )
        embed.add_field(name="Server", value=interaction.guild.name, inline=True)
        embed.add_field(name="Sent by", value=interaction.user.display_name, inline=True)
        embed.set_footer(text="This message was sent through Alpha Bot")
        
        # Send messages
        successful = 0
        failed = 0
        
        status_embed = EmbedBuilder.info_embed("Sending Messages", "Starting mass DM operation...")
        await interaction.edit_original_response(embed=status_embed, view=None)
        
        for member in members:
            try:
                await member.send(embed=embed)
                successful += 1
                await asyncio.sleep(1)  # Rate limiting
            except discord.Forbidden:
                failed += 1
            except Exception as e:
                logging.error(f"Error sending mass DM to {member}: {e}")
                failed += 1
        
        # Final result
        result_embed = EmbedBuilder.success_embed(
            "Mass DM Complete",
            f"**Successful:** {successful}\n**Failed:** {failed}\n**Total:** {len(members)}"
        )
        await interaction.edit_original_response(embed=result_embed)
    
    # ROLE MANAGEMENT COMMANDS
    @app_commands.command(name="add-role", description="Add a role to a user")
    @app_commands.describe(
        user="The user to add the role to (display name, username, or mention)",
        role="The role to add"
    )
    async def add_role(self, interaction: discord.Interaction, user: str, role: discord.Role):
        """Add a role to a user"""
        
        # Check permissions
        if not PermissionChecker.has_manage_roles_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Access Denied", "You need manage roles permissions to use this command."),
                ephemeral=True
            )
            return
        
        # Find the target user
        target_member = await UserLookup.find_member(interaction.guild, user)
        if not target_member:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("User Not Found", f"Could not find a user matching '{user}'."),
                ephemeral=True
            )
            return
        
        # Check if user can modify this member
        if not PermissionChecker.can_modify_member(interaction.user, target_member):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Permission Error", "You cannot modify this user's roles."),
                ephemeral=True
            )
            return
        
        # Check if role can be assigned
        if role >= interaction.user.top_role and not PermissionChecker.has_admin_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Role Too High", "You cannot assign roles higher than or equal to your highest role."),
                ephemeral=True
            )
            return
        
        # Check if user already has the role
        if role in target_member.roles:
            await interaction.response.send_message(
                embed=EmbedBuilder.warning_embed("Already Has Role", f"{target_member.display_name} already has the role {role.name}."),
                ephemeral=True
            )
            return
        
        try:
            # Add the role
            await target_member.add_roles(role, reason=f"Added by {interaction.user} via Alpha Bot")
            
            # Confirm success
            success_embed = EmbedBuilder.success_embed(
                "Role Added",
                f"Successfully added **{role.name}** to {target_member.display_name}"
            )
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Permission Error", "I don't have permission to manage this role."),
                ephemeral=True
            )
        except Exception as e:
            logging.error(f"Error adding role: {e}")
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Error", "Failed to add role. Please try again."),
                ephemeral=True
            )
    
    @app_commands.command(name="remove-role", description="Remove a role from a user")
    @app_commands.describe(
        user="The user to remove the role from (display name, username, or mention)",
        role="The role to remove"
    )
    async def remove_role(self, interaction: discord.Interaction, user: str, role: discord.Role):
        """Remove a role from a user"""
        
        # Check permissions
        if not PermissionChecker.has_manage_roles_perms(interaction.user):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Access Denied", "You need manage roles permissions to use this command."),
                ephemeral=True
            )
            return
        
        # Find the target user
        target_member = await UserLookup.find_member(interaction.guild, user)
        if not target_member:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("User Not Found", f"Could not find a user matching '{user}'."),
                ephemeral=True
            )
            return
        
        # Check if user can modify this member
        if not PermissionChecker.can_modify_member(interaction.user, target_member):
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Permission Error", "You cannot modify this user's roles."),
                ephemeral=True
            )
            return
        
        # Check if user has the role
        if role not in target_member.roles:
            await interaction.response.send_message(
                embed=EmbedBuilder.warning_embed("Doesn't Have Role", f"{target_member.display_name} doesn't have the role {role.name}."),
                ephemeral=True
            )
            return
        
        try:
            # Remove the role
            await target_member.remove_roles(role, reason=f"Removed by {interaction.user} via Alpha Bot")
            
            # Confirm success
            success_embed = EmbedBuilder.success_embed(
                "Role Removed",
                f"Successfully removed **{role.name}** from {target_member.display_name}"
            )
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Permission Error", "I don't have permission to manage this role."),
                ephemeral=True
            )
        except Exception as e:
            logging.error(f"Error removing role: {e}")
            await interaction.response.send_message(
                embed=EmbedBuilder.error_embed("Error", "Failed to remove role. Please try again."),
                ephemeral=True
            )

class ConfirmationView(discord.ui.View):
    """Confirmation view for dangerous actions"""
    
    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.confirmed = True
        await interaction.response.send_message("✅ Confirmed! Processing...", ephemeral=True)
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Cancelled.", ephemeral=True)
        self.stop()
    
    async def on_timeout(self):
        self.confirmed = False
        self.stop()

async def setup(bot):
    await bot.add_cog(DiscordManagement(bot))
