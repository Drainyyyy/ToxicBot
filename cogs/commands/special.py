import random
import time

from discord import Embed, Color, user
from discord.ext import commands

from cogs.util import version_stuff
from util import data


class Special:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="devmsg", aliases=["suggest"])
    async def _devmsg(self, ctx, *, message):
        embed = Embed(title="Devmsg", description="Successfully sent your suggestion to my dev.", color=Color.from_rgb(125, 220, 113))
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

        embed = Embed(title="Devmsg", color=Color.from_rgb(125, 220, 113))
        embed.add_field(name="Sender", value=ctx.author, inline=True)
        embed.add_field(name="Server", value=ctx.guild, inline=True)
        embed.add_field(name="Message", value="```{0}```".format(message), inline=False)
        drainyyy = self.bot.get_user(249221746006163467)
        await drainyyy.send(embed=embed)

    @commands.command(name="changelogs", aliases=["changes", "changenotes"])
    async def _changelogs(self, ctx):
        embed = Embed(title="Changelogs", color=Color.from_rgb(125, 220, 113))
        embed.add_field(name="Recent changes", value="\n".join(map(str, version_stuff.Recent)), inline=False)
        embed.add_field(name="Date", value=version_stuff.Date, inline=False)
        embed.add_field(name="Current version", value=version_stuff.Version, inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Special(bot))
