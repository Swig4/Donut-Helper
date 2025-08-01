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

    async def trackerLoop(playerName):
        await asyncio.sleep(3)
        while playerName in trackedPlayers and trackedPlayers[playerName]:
            try:
                status = await getOnlineStatus(donutApiKey, playerName)
                if status:
                    for userID in list(trackedPlayers[playerName]):
                        user = await bot.fetch_user(userID)
                        try:
                            await user.send(f"🔔 `{playerName}` is now online!")
                        except:
                            pass 
                        trackedPlayers[playerName].remove(userID)
                        userTracking.pop(userID, None)

                    if not trackedPlayers[playerName]:
                        trackedPlayers.pop(playerName)
                    break
            except Exception as e:
                print(f"[TRACKER ERROR] {playerName}: {e}")
            await asyncio.sleep(10)

    @bot.tree.command(name="track", description="Track a player and get notified when they come online.")
    @app_commands.describe(playername="Minecraft username to track")
    async def track(interaction: discord.Interaction, playername: str):
        await interaction.response.defer()
        userID = interaction.user.id

        if await getOnlineStatus(donutApiKey, playername):
            await interaction.followup.send("🚫 That player is already online!")
            return

        if userID != ownerID and userID in userTracking:
            await interaction.followup.send("🚫 You’re already tracking a player!")
            return

        if userID != ownerID and sum(len(users) for users in trackedPlayers.values()) >= 100:
            await interaction.followup.send("🚫 The track list is full. Max 100 tracked users.")
            return

        if playername not in trackedPlayers:
            trackedPlayers[playername] = set()
            asyncio.create_task(trackerLoop(playername))

        trackedPlayers[playername].add(userID)
        userTracking[userID] = playername
        await interaction.followup.send(f"✅ Now tracking `{playername}`. You'll be DM'd when they're online.")

    @bot.tree.command(name="untrack", description="Stop tracking a player.")
    @app_commands.describe(playername="Minecraft username to stop tracking")
    async def untrack(interaction: discord.Interaction, playername: str):
        userID = interaction.user.id
        await interaction.response.defer()

        if playername not in trackedPlayers or userID not in trackedPlayers[playername]:
            await interaction.followup.send("⚠️ You're not tracking this player.")
            return

        trackedPlayers[playername].remove(userID)
        userTracking.pop(userID, None)

        if not trackedPlayers[playername]:
            trackedPlayers.pop(playername)

        await interaction.followup.send(f"✅ Stopped tracking `{playername}`.")
