from discord import Embed, Color
from discord.ext import commands

from cogs import error
from util import data


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands"])
    async def _help(self, ctx):

        embed = Embed(title="HELP", description="For the some commands a special role is required. "
                                                "This role is called **{0}**.".format(data.bot_role), color=Color.blue())
        embed.add_field(name="INFORMATION", value="``" + "``, ``".join(map(str, list(self.bot.get_cog_commands("Information")))) + "``", inline=False)
        embed.add_field(name="MISC", value="``" + "``, ``".join(map(str, list(self.bot.get_cog_commands("Misc")))) + "``", inline=False)
        embed.add_field(name="MODERATION", value="``" + "``, ``".join(map(str, list(self.bot.get_cog_commands("Moderation")))) + "``", inline=False)
        embed.add_field(name="SPECIAL", value="``" + "``, ``".join(map(str, list(self.bot.get_cog_commands("Special")))) + "``", inline=False)
        embed.add_field(name="ADMIN", value="``" + "``, ``".join(map(str, list(self.bot.get_cog_commands("Admin")))) + "``", inline=False)
        embed.add_field(name="DEBUG", value="``" + "``, ``".join(map(str, list(self.bot.get_cog_commands("Debug")))) + "``", inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
