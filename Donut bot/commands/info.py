import discord
from discord import app_commands
import time
from functions import formatPlaytime
from commands.tracker import trackedPlayers
startTime = None

async def setup(bot):
    global startTime
    startTime = bot.startTime
    @bot.tree.command(name="info", description="View bot info")
    async def info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(title="🤖 Bot Info", color=0x89CFF0)
        embed.add_field(name="Uptime", value=formatPlaytime(int(time.time() - startTime)), inline=True)
        embed.add_field(name="Total Servers", value=str(len(bot.guilds)), inline=True)
        embed.add_field(name="Owner", value="swig5", inline=True)
        embed.add_field(name="Client Ping", value=f"{round((time.time() - interaction.created_at.timestamp()) * 1000) }ms", inline=True)
        embed.add_field(name="WebSocket Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Players Being Tracked", value=str(len(trackedPlayers)), inline=True)

        await interaction.edit_original_response(embed=embed)