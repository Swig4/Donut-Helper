import discord
from discord import app_commands
from discord.ext import commands

async def setup(bot: commands.Bot):
    @bot.tree.command(name="getservers", description="list all servers and their id.", guild=bot.devGuild)
    async def listservers(interaction: discord.Interaction):
        if interaction.user.id != bot.swigID:
            await interaction.response.send_message("This command is for Swig only.", ephemeral=True)
            return

        if not bot.guilds:
            await interaction.response.send_message("The bot is not in any servers.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Bot is in {len(bot.guilds)} servers",
            color=discord.Color.blue()

        )

        for guild in bot.guilds:
            embed.add_field(
                name=f"{guild.name} ({guild.id})",
                value=f"Members: {guild.member_count}\nOwner: {guild.owner}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="getinvite", description="get a servers inv if it can", guild=bot.devGuild)
    async def getinvite(interaction: discord.Interaction, id: str):
        if interaction.user.id != bot.swigID:
            await interaction.response.send_message("This command is for Swig only.", ephemeral=True)
            return

        guild = bot.get_guild(int(id))
        if not guild:
            await interaction.response.send_message("Bot is not in that server.", ephemeral=True)
            return
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).create_instant_invite:
                invite = await channel.create_invite(max_age=0, max_uses=0)
                await interaction.response.send_message(f"Invite for **{guild.name}**: {invite.url}", ephemeral=True)
                return

        await interaction.response.send_message("No channels found where I can create invites.", ephemeral=True)
