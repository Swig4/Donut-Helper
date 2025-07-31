import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()
startTime = time.time()
discordToken = os.getenv("DISCORD_TOKEN")
donutApiKey = os.getenv("DONUT_API_KEYS").split(",")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="12345678901", intents=intents)
bot.donutApiKey = [key.strip() for key in donutApiKey]
bot.startTime = startTime 

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help | Made By swig5"))
    print(f"Logged in as {bot.user}")

async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            path = f"commands.{filename[:-3]}"
            cog = __import__(path, fromlist=["setup"])
            await cog.setup(bot)

async def main():
    await load_commands()
    await bot.start(discordToken)

asyncio.run(main())