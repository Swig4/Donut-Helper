import discord
from ruleManager import hasAccepted, setAccepted, removeAccepted
from commands.whitelistManager import loadWhitelist, saveWhitelist

class RulesView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        setAccepted(self.user_id)
        await interaction.response.edit_message(content="You have accepted the rules. You may now use whitelist commands.", embed=None, view=None)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        wl = loadWhitelist()
        if self.user_id in wl:
            wl.remove(self.user_id)
            saveWhitelist(wl)
        removeAccepted(self.user_id)
        await interaction.response.edit_message(content="You have denied the rules and have been removed from the whitelist.", embed=None, view=None)

async def promptRules(interaction: discord.Interaction):
    wl = loadWhitelist()
    if interaction.user.id not in wl:
        await interaction.response.send_message("❌ You must be whitelisted by Swig to use this command.", ephemeral=True)
        return False
    if not hasAccepted(interaction.user.id):
        embed = discord.Embed(
            title="📜 Whitelist Command Rules",
            description="**Rules for using whitelist commands:**\n"
                        "1. No spamming commands.\n"
                        "2. No showing or sharing the commands to others, it's meant to be kept private.\n\n"
                        "Breaking these rules will lead to your account **being removed from the whitelist.**\n"
                        "Click **Accept** to agree, or **Deny** to be removed from the whitelist.",
            color=0xFFD700
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, view=RulesView(interaction.user.id))
        return False
    return True
