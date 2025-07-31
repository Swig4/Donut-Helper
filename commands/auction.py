import discord
from discord import app_commands
import aiohttp
import json
from functions import formatPrice
import random
donutApiKey = None

async def setup(bot):
    global donutApiKey
    donutApiKey = random.choice(bot.donutApiKey)

    @bot.tree.command(name="auction", description="Gets auction listing for an item")
    @app_commands.describe(
        item="Item to search for (e.g., diamond)",
        amount="Stack size",
        sort="Sorting method"
    )
    @app_commands.choices(sort=[
        app_commands.Choice(name="Lowest Price", value="lowest_price"),
        app_commands.Choice(name="Highest Price", value="highest_price"),
        app_commands.Choice(name="Recently Listed", value="recently_listed"),
        app_commands.Choice(name="Last Listed", value="last_listed"),
    ])
    async def auction(interaction: discord.Interaction, item: str, amount: int, sort: app_commands.Choice[str]):
        await interaction.response.defer()

        url = "https://api.donutsmp.net/v1/auction/list/1"
        headers = {
            "Authorization": donutApiKey,
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "search": item,
            "sort": sort.value
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, json=payload) as resp:
                if resp.status == 500:
                    errorEmbed = discord.Embed(title="No Valid Items", description="There is no valid item that matches your query. Did you spell it right?", color=0xFF0000)
                    await interaction.edit_original_response(embed=errorEmbed)
                    return
                elif resp.status != 200:
                    errorEmbed = discord.Embed(title="Error", description=f"There was an error with the backend. (Code {resp.status})", color=0xFF0000)
                    await interaction.edit_original_response(embed=errorEmbed)
                    return
                text = await resp.text()
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    errorEmbed = discord.Embed(title="Error", description="There was an error with the backend.", color=0xFF0000)
                    await interaction.edit_original_response(embed=errorEmbed)
                    return

        results = data.get("result", [])
        match = None
        for auctionItem in results:
            if auctionItem["item"].get("count", 0) >= amount:
                match = auctionItem
                break

        sellerName = match["seller"]["name"]
        itemPrice = match["price"]
        itemCount = match["item"]["count"]
        timeLeftSeconds = match["time_left"] // 1000

        embed = discord.Embed(title="📦 Auction Listing", color=0x00ff99)
        embed.add_field(name="Item", value=item.capitalize(), inline=True)
        embed.add_field(name="Amount", value=str(itemCount), inline=True)
        embed.add_field(name="Price", value=formatPrice(itemPrice), inline=True)
        embed.add_field(name="Seller", value=sellerName, inline=True)
        embed.set_footer(text=f"Time left: {timeLeftSeconds // 86400}d {(timeLeftSeconds % 86400) // 3600}h {(timeLeftSeconds % 3600) // 60}m")

        await interaction.edit_original_response(embed=embed)