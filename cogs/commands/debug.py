from discord.ext import commands

from util import data


class Debug:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="test", invoke_without_command=True)
    async def _test(self, ctx):
        await ctx.send("I'm up!:white_check_mark:")

    @_test.command(name="private", aliases=["pm"])
    async def _test_pm(self, ctx):
        await ctx.send("Message sent!:white_check_mark:")
        await ctx.author.send("I'm up!:white_check_mark:")

    @_test.command(name="botrole", aliases=["br"])
    @commands.has_role(data.bot_role)
    async def _test_br(self, ctx):
        await ctx.send("Success!:white_check_mark:")


def setup(bot):
    bot.add_cog(Debug(bot))
