import discord
from discord import app_commands
import json
import os
from functions import getCheapestPrice, formatPrice
import random

WhitelistFile = "whitelist.json"

if not os.path.exists(WhitelistFile):
    with open(WhitelistFile, "w") as f:
        json.dump({"whitelist": []}, f)

def loadWhitelist():
    with open(WhitelistFile, "r") as f:
        whitelist = json.load(f)["whitelist"]
    return whitelist

flips = [
    {
        "output": {"name": "Gray Dye", "amount": 2},
        "ingredients": [
            {"name": "Black Dye", "amount": 1},
            {"name": "White Dye", "amount": 1}
        ]
    },
        {
        "output": {"name": "Pink Dye", "amount": 2},
        "ingredients": [
            {"name": "Red Dye", "amount": 1},
            {"name": "White Dye", "amount": 1}
        ]
    },
    {
        "output": {"name": "Light Blue Dye", "amount": 2},
        "ingredients": [
            {"name": "Blue Dye", "amount": 1},
            {"name": "White Dye", "amount": 1}
        ]
    },
    {
        "output": {"name": "Purple Dye", "amount": 2},
        "ingredients": [
            {"name": "Red Dye", "amount": 1},
            {"name": "Blue Dye", "amount": 1}
        ]
    },
    {
        "output": {"name": "Brown Dye", "amount": 1},
        "ingredients": [
            {"name": "Cocoa Beans", "amount": 1}
        ]
    },
    {
        "output": {"name": "Green Dye", "amount": 1},
        "ingredients": [
            {"name": "Cactus Green", "amount": 1}
        ]
    },
    {
        "output": {"name": "Black Dye", "amount": 1},
        "ingredients": [
            {"name": "Ink Sac", "amount": 1}
        ]
    },
    {
        "output": {"name": "Red Dye", "amount": 1},
        "ingredients": [
            {"name": "Poppy", "amount": 1}
        ]
    },
    {
        "output": {"name": "Blue Dye", "amount": 1},
        "ingredients": [
            {"name": "Lapis Lazuli", "amount": 1}
        ]
    },
    {
        "output": {"name": "Yellow Dye", "amount": 1},
        "ingredients": [
            {"name": "Dandelion", "amount": 1}
        ]
    },
    {
        "output": {"name": "White Dye", "amount": 1},
        "ingredients": [
            {"name": "Bone Meal", "amount": 1}
        ]
    },
    {
        "output": {"name": "Light Gray Dye", "amount": 2},
        "ingredients": [
            {"name": "Gray Dye", "amount": 1},
            {"name": "White Dye", "amount": 1}
        ]
    },
        {
        "output": {"name": "Orange Dye", "amount": 2},
        "ingredients": [
            {"name": "Red Dye", "amount": 1},
            {"name": "Yellow Dye", "amount": 1}
        ]
    },
    {
        "output": {"name": "Magenta Dye", "amount": 2},
        "ingredients": [
            {"name": "Purple Dye", "amount": 1},
            {"name": "Pink Dye", "amount": 1}
        ]
    },
    {
        "output": {"name": "White Carpet", "amount": 3},
        "ingredients": [
            {"name": "White Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Orange Carpet", "amount": 3},
        "ingredients": [
            {"name": "Orange Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Magenta Carpet", "amount": 3},
        "ingredients": [
            {"name": "Magenta Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Light Blue Carpet", "amount": 3},
        "ingredients": [
            {"name": "Light Blue Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Yellow Carpet", "amount": 3},
        "ingredients": [
            {"name": "Yellow Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Lime Carpet", "amount": 3},
        "ingredients": [
            {"name": "Lime Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Pink Carpet", "amount": 3},
        "ingredients": [
            {"name": "Pink Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Gray Carpet", "amount": 3},
        "ingredients": [
            {"name": "Gray Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Light Gray Carpet", "amount": 3},
        "ingredients": [
            {"name": "Light Gray Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Cyan Carpet", "amount": 3},
        "ingredients": [
            {"name": "Cyan Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Purple Carpet", "amount": 3},
        "ingredients": [
            {"name": "Purple Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Blue Carpet", "amount": 3},
        "ingredients": [
            {"name": "Blue Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Brown Carpet", "amount": 3},
        "ingredients": [
            {"name": "Brown Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Green Carpet", "amount": 3},
        "ingredients": [
            {"name": "Green Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Red Carpet", "amount": 3},
        "ingredients": [
            {"name": "Red Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Black Carpet", "amount": 3},
        "ingredients": [
            {"name": "Black Wool", "amount": 2}
        ]
    },
    {
        "output": {"name": "Books", "amount": 1},
        "ingredients": [
            {"name": "Paper", "amount": 3},
            {"name": "Leather", "amount": 1}
        ]
    },
    {
        "output": {"name": "Paper", "amount": 3},
        "ingredients": [
            {"name": "Sugar Cane", "amount": 3}
        ]
    },
    {
        "output": {"name": "Sugar", "amount": 1},
        "ingredients": [
            {"name": "Sugar Cane", "amount": 1}
        ]
    },
]


donutApiKey = None

async def setup(bot):
    global donutApiKey
    donutApiKey = random.choice(bot.donutApiKey)

    @bot.tree.command(name="viewbestflips", description="View the top 5 most profitable craftable items.")
    async def viewBestFlips(interaction: discord.Interaction):
        try:
            whitelist = loadWhitelist()
            if interaction.user.id != 1264016430022529124 and interaction.user.id not in whitelist:
                await interaction.response.send_message("❌ You must be whitelisted by Swig to use this command.", ephemeral=True)
                return
            
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("# Checking prices, this may take a minute...", ephemeral=True)
            profits = []
            for flip in flips:
                outputPrice = await getCheapestPrice(donutApiKey, flip["output"]["name"])
                if outputPrice is None:
                    continue
                outputTotal = outputPrice * flip["output"]["amount"]
                ingredientCost = 0
                validFlip = True

                for ing in flip["ingredients"]:
                    price = await getCheapestPrice(donutApiKey, ing["name"])
                    if price is None:
                        validFlip = False
                        break
                    ingredientCost += price * ing["amount"]

                if not validFlip:
                    continue

                profit = outputTotal - ingredientCost
                if profit <= 0:
                    continue

                profits.append({
                    "name": flip["output"]["name"],
                    "profit": profit,
                    "cost": ingredientCost,
                    "sell": outputTotal,
                    "ingredients": flip["ingredients"]
                })


            if not profits:
                await interaction.followup.send("No profitable flips found right now.", ephemeral=True)
                return

            profits.sort(key=lambda x: x["profit"], reverse=True)
            top = profits[:5]

            embed = discord.Embed(title="💰 Top 5 Craftable Flips", color=0x89CFF0)
            for idx, flip in enumerate(top, start=1):
                recipe = ", ".join(f"{ing['amount']} {ing['name']}" for ing in flip.get('ingredients', []))
                embed.add_field(
                    name=f"{idx}. {flip['name']} ({recipe})",
                    value=(
                        f"Profit: **{formatPrice(flip['profit'])}**\n"
                        f"Cost: {formatPrice(flip['cost'])}\n"
                        f"Sell: {formatPrice(flip['sell'])}"
                    ),
                    inline=False
                )

            embed.set_footer(text="Keep in mind this command doesn't take into account demand. Profit is per item, not stack.")
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception:
            try:
                await interaction.followup.send("⚠️ An error occurred while processing your request.", ephemeral=True)
            except:
                pass
