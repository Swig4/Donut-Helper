import discord
from discord import app_commands
import aiohttp
from functions import formatPrice, formatPlaytime, getOnlineStatus
import random

donutApiKey = None

async def setup(bot):
    global donutApiKey
    donutApiKey = random.choice(bot.donutApiKey)

    @bot.tree.command(name="stats", description="Get DonutSMP stats for a player")
    @app_commands.describe(playername="The player name to lookup")
    async def stats(interaction: discord.Interaction, playername: str):
        await interaction.response.defer()

        url = f"https://api.donutsmp.net/v1/stats/{playername}"
        headers = {
            "Authorization": donutApiKey,
            "accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                try:
                    data = await resp.json(content_type=None)
                except Exception as e:
                    await interaction.edit_original_response(embed=discord.Embed(
                        title="Error",
                        description="Failed to decode API response.",
                        color=0xFF0000))
                    return

        if data.get("status") != 200 or "result" not in data:
            await interaction.edit_original_response(embed=discord.Embed(
                title="Error",
                description="Invalid player!",
                color=0xFF0000))
            return

        r = data["result"]

        embed = discord.Embed(
            title=f"📊 Stats for `{playername}`",
            color=0x89CFF0
        )
        embed.add_field(name="💰 Purse", value=formatPrice(r.get("money", 0)), inline=True)
        embed.add_field(name="🔷 Shards", value=formatPrice(r.get("shards", "0")), inline=True)
        embed.add_field(name="⚔️ Kills", value=formatPrice(r.get("kills", "0")), inline=True)
        embed.add_field(name="💀 Deaths", value=formatPrice(r.get("deaths", "0")), inline=True)
        embed.add_field(name="⏱️ Playtime", value=formatPlaytime(int(r.get("playtime", 0))), inline=True)
        embed.add_field(name="📦 Blocks Placed", value=formatPrice(r.get("placed_blocks", "0")), inline=True)
        embed.add_field(name="⛏️ Blocks Broken", value=formatPrice(r.get("broken_blocks", "0")), inline=True)
        embed.add_field(name="👾 Mobs Killed", value=formatPrice(r.get("mobs_killed", "0")), inline=True)
        embed.add_field(name="🛒 Money Spent (/shop)", value=formatPrice(r.get("money_spent_on_shop", 0)), inline=True)
        embed.add_field(name="📤 Money Earned (/sell)", value=formatPrice(r.get("money_made_from_sell", 0)), inline=True)
        isOnline = await getOnlineStatus(donutApiKey, playername)
        embed.add_field(name="🌐 Online Status", value="Online" if isOnline else "Offline", inline=True)

        await interaction.edit_original_response(embed=embed)
