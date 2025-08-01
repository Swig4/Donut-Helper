import discord
from discord import app_commands

async def setup(bot):
    @bot.tree.command(name="help", description="Show a list of available commands")
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help - Available Commands",
            description=(
                "/help - Show this help message\n"
                "/auction - Get auction listing for an item\n"
                "/lookup - Get a player's location and rank\n"
                "/stats - Get all stats for a player\n"
                "/track - Track a player and get notified when they come online\n"
                "/untrack - Stop tracking a player\n"
                "/info - View bot info\n"
                "/viewPriceHistory - Get price history graph for a specific item\n"
            ),
            color=0x89CFF0
        )
        embed.set_footer(text="Made by swig5")

        await interaction.response.send_message(embed=embed)