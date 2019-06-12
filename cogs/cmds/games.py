from discord.ext import commands

import config


class Games(commands.Cog, name="Games"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gamesuggest", description="Suggest game ideas.")
    async def _gamesuggest(self, ctx):
        await ctx.send(f"Use the **{config.prefix}devmsg** command to send the suggestions.")


def setup(bot):
    bot.add_cog(Games(bot))
