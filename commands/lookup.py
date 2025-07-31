import discord
from discord import app_commands
import aiohttp
import random
donutApiKey = None

async def setup(bot):
    global donutApiKey
    donutApiKey = random.choice(bot.donutApiKey)

    @bot.tree.command(name="lookup", description="Get player info by player name")
    @app_commands.describe(playername="The player name to lookup")
    async def lookup(interaction: discord.Interaction, playername: str):
        await interaction.response.defer(ephemeral=True)

        url = f"https://api.donutsmp.net/v1/lookup/{playername}"
        headers = {
            "Authorization": donutApiKey,
            "accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                try:
                    data = await resp.json(content_type=None)
                except Exception as e:
                    print(f"JSON decode error: {e}")
                    await interaction.edit_original_response(embed=discord.Embed(
                        title="Error",
                        description="There was an error with this command! (Error: Failed to decode API)",
                        color=0xFF0000))
                    return

        status = data.get("status", 0)

        if status == 500:
            msg = data.get("message", "Unknown error.")
            embed = discord.Embed(
                title="Player must be online!",
                description=msg,
                color=0xFF0000
            )
            await interaction.edit_original_response(embed=embed)
            return

        if status != 200 or "result" not in data:
            embed = discord.Embed(
                title="Error",
                description="Could not retrieve player info.",
                color=0xFF0000
            )
            await interaction.edit_original_response(embed=embed)
            return

        result = data["result"]
        username = result.get("username", playername)
        rank = result.get("rank", "default")
        location = result.get("location", "Unknown")

        embed = discord.Embed(title=f"Player Info - {username}", color=0x89CFF0)
        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="Location", value=location, inline=True)

        await interaction.edit_original_response(embed=embed)