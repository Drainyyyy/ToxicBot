from discord.ext import commands


class Translate(commands.Cog, name="Translate"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="binary", aliases=["ttb"], description="Translate a text to binary.")
    async def _binary(self, ctx, *, text):
        binary = ' '.join(map(bin, bytearray(text)))
        await ctx.send(str(binary))


def setup(bot):
    bot.add_cog(Translate(bot))
