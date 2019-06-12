import discord
from discord.ext import commands

from utils.message import embeds, colors
import config


class Support(commands.Cog, name="Support"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="patreon", aliases=["donate"], description="Gives you a link to the patreon page of the bot owner.")
    async def _patreon(self, ctx):
        await ctx.send(embed=embeds.one_line(title="Patreon", color=colors.support, ctx=ctx,
                                             message=f"[Click here]({config.patreon}) to get to the official patreon page of the bot owner.\n"
                                             f"Here you can subscribe to pay a kid that makes a bot.:grin:"))

    @commands.command(name="support", description="Gives you a list of links where you can support me.")
    async def _support(self, ctx):
        embed = discord.Embed(title="Support", color=colors.support, description="Thanks for thinking about support me!")
        embed.add_field(name="Patreon", value=f"[Click here]({config.patreon})```"
                        f"Earning money is nice. Here you can donate me monthly and you'll get a nice reward.```", inline=False)
        embed.add_field(name="Server", value=f"[Click here]({config.discord_server})```"
                        f"To get support or just chat with me just join here.```", inline=False)
        embed.add_field(name="Invite", value=f"[Click here]({config.invite})```"
                        f"Get me on your own server! Just invite me.```", inline=False)
        embed.add_field(name="Vote", value=f"[Click here]({config.vote})```"
                        f"Vote for me so that more people see me on discordbots.```", inline=False)
        embed.add_field(name="Website", value=f"[Click here]({config.website})```"
                        f"Here's the website of the owner of the bot.```", inline=False)
        embed.add_field(name="GitHub", value=f"[Click here]({config.repository_url})```"
                        f"Drop a star on the GitHub repository of the bot.```", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="server", description="Join my discord server.")
    async def _server(self, ctx):
        await ctx.send(embed=embeds.one_line(title="Support Server", color=colors.support, ctx=ctx,
                                             message=f"[Click me to join!]({config.discord_server})"))

    @commands.command(name="invite", aliases=["link"], description="Get the invite link of the bot")
    async def _invite(self, ctx):
        await ctx.send(embed=embeds.one_line(title="Invite", color=colors.support, ctx=ctx, message=f"[Click here]({config.invite}) to invite me!"))


def setup(bot):
    bot.add_cog(Support(bot))
