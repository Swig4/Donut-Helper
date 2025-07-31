import discord
from discord import app_commands
import asyncio
from functions import getOnlineStatus
import random

trackedPlayers = {}
userTracking = {}  
ownerID = 1264016430022529124
donutApiKey = None

async def setup(bot):
    global donutApiKey
    donutApiKey = random.choice(bot.donutApiKey)
    async def trackerLoop(playerName, userID):
        await asyncio.sleep(3)
        while playerName in trackedPlayers:
            try:
                status = await getOnlineStatus(donutApiKey, playerName)
                if status:
                    user = await bot.fetch_user(userID)
                    await user.send(f"🔔 `{playerName}` is now online!")
                    trackedPlayers.pop(playerName, None)
                    userTracking.pop(userID, None)
                    break
            except Exception as e:
                print(f"[TRACKER ERROR] {playerName}: {e}")
            await asyncio.sleep(10)

    @bot.tree.command(name="track", description="Track a player and get notified when they come online.")
    @app_commands.describe(playername="Minecraft username to track")
    async def track(interaction: discord.Interaction, playername: str):
        await interaction.response.defer(ephemeral=True)
        userID = interaction.user.id

        if await getOnlineStatus(donutApiKey, playername):
            await interaction.followup.send("🚫 That player is already online!")
            return

        if playername in trackedPlayers:
            await interaction.followup.send("🚫 This player is already being tracked by someone.")
            return

        if userID != ownerID and userID in userTracking:
            await interaction.followup.send("🚫 You’re already tracking a player!")
            return

        if userID != ownerID and len(trackedPlayers) >= 100:
            await interaction.followup.send("🚫 The track list is full. Max 100 players.")
            return

        trackedPlayers[playername] = userID
        userTracking[userID] = playername
        asyncio.create_task(trackerLoop(playername, userID))
        await interaction.followup.send(f"✅ Now tracking `{playername}`. You'll be DM'd when they're online.")

    @bot.tree.command(name="untrack", description="Stop tracking a player.")
    @app_commands.describe(playername="Minecraft username to stop tracking")
    async def untrack(interaction: discord.Interaction, playername: str):
        userID = interaction.user.id
        await interaction.response.defer(ephemeral=True)

        if playername not in trackedPlayers:
            await interaction.followup.send("⚠️ This player is not being tracked.")
            return

        trackerID = trackedPlayers[playername]
        if userID != trackerID and userID != ownerID:
            await interaction.followup.send("🚫 You did not start this player’s tracker!")
            return

        trackedPlayers.pop(playername, None)
        userTracking.pop(trackerID, None)
        await interaction.followup.send(f"✅ Stopped tracking `{playername}`.")