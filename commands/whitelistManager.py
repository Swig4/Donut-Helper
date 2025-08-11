import discord
from discord import app_commands
import json
import os

whitelistFile = "whitelist.json"

if not os.path.exists(whitelistFile):
    with open(whitelistFile, "w") as f:
        json.dump({"whitelist": []}, f)

def saveWhitelist(data):
    with open(whitelistFile, "w") as f:
        json.dump({"whitelist": data}, f, indent=4)

def loadWhitelist():
    with open(whitelistFile, "r") as f:
        return json.load(f)["whitelist"]

async def setup(bot):
    @bot.tree.command(name="whitelist", description="Add a user to the whitelist.")
    async def whitelist(interaction: discord.Interaction, user: discord.User):
        if interaction.user.id != bot.swigID:
            await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
            return
        wl = loadWhitelist()
        if user.id not in wl:
            wl.append(user.id)
            saveWhitelist(wl)
            await interaction.response.send_message(f"✅ `{user}` has been added to the whitelist.")
        else:
            await interaction.response.send_message(f"`{user}` is already whitelisted.")

    @bot.tree.command(name="unwhitelist", description="Remove a user from the whitelist.")
    async def unwhitelist(interaction: discord.Interaction, user: discord.User):
        if interaction.user.id != bot.swigID:
            await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
            return
        wl = loadWhitelist()
        if user.id in wl:
            wl.remove(user.id)
            saveWhitelist(wl)
            await interaction.response.send_message(f"✅ `{user}` has been removed from the whitelist.")
        else:
            await interaction.response.send_message(f"`{user}` is not in the whitelist.")

    @bot.tree.command(name="iswhitelisted", description="Check if a user is whitelisted.")
    async def iswhitelisted(interaction: discord.Interaction, user: discord.User):
        if interaction.user.id != bot.swigID:
            await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
            return
        wl = loadWhitelist()
        if user.id in wl:
            await interaction.response.send_message(f"✅ `{user}` is whitelisted.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ `{user}` is not whitelisted.", ephemeral=True)