import discord
from discord import app_commands
import plotly.graph_objects as go
import io
from functions import getCheapestPrice
import random
import asyncio
import time

donutApiKey = None
priceHistory = {
    "elytra": [],
    "dragon_head": [],
    "mace": []
}

async def setup(bot):
    global donutApiKey
    donutApiKey = random.choice(bot.donutApiKey)

    allowedItems = {
        "elytra": '#636EFA',
        "dragon_head": '#EF553B',
        "mace": '#00CC96'
    }

    async def priceUpdater():
        await bot.wait_until_ready()
        while not bot.is_closed():
            now = time.time()
            for item in priceHistory.keys():
                try:
                    price = await getCheapestPrice(donutApiKey, item)
                    if price is not None:
                        priceHistory[item].append((now, price))
                        if len(priceHistory[item]) > 100:
                            priceHistory[item].pop(0)
                except Exception as e:
                    print(f"Error updating price for {item}: {e}")
            await asyncio.sleep(20)

    bot.loop.create_task(priceUpdater())

    @bot.tree.command(name="viewPriceHistory", description="Get price history graph for a specific item.")
    @app_commands.describe(item="Select an item to graph")
    @app_commands.choices(item=[
        app_commands.Choice(name="Elytra", value="elytra"),
        app_commands.Choice(name="Dragon Head", value="dragon_head"),
        app_commands.Choice(name="Mace", value="mace"),
    ])
    async def priceGraph(interaction: discord.Interaction, item: app_commands.Choice[str]):
        await interaction.response.defer()

        history = priceHistory.get(item.value, [])
        if not history:
            await interaction.followup.send("No price data available yet, please wait a bit.")
            return

        timestamps, prices = zip(*history)

        import datetime
        timesStr = [datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S") for ts in timestamps]

        fig = go.Figure(data=[go.Scatter(
            x=timesStr,
            y=prices,
            mode='lines+markers',
            line=dict(color=allowedItems[item.value]),
            marker=dict(size=6)
        )])

        fig.update_layout(
            title=f"Price History for {item.name}",
            xaxis_title="Time (HH:MM:SS)",
            yaxis_title="Price (coins)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            xaxis=dict(tickangle=45)
        )

        imgBytes = fig.to_image(format="png", width=700, height=450)
        file = discord.File(io.BytesIO(imgBytes), filename="pricehistory.png")
        embed = discord.Embed(title=f"Price History for {item.name}")
        embed.set_image(url="attachment://pricehistory.png")

        await interaction.followup.send(embed=embed, file=file)