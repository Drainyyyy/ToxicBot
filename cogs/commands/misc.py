import asyncio
import random

import discord
from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import context

afk = []


class Misc:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        ctx = await self.bot.get_context(message, cls=context.Context)
        if ctx.author.id in afk:
            embed = Embed(title="AFK", description="{0} returned from afk.".format(ctx.author), color=Color.green())
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            afk.remove(ctx.author.id)
            return
        for mention in ctx.message.mentions:
            if mention.id in afk:
                embed = Embed(title="AFK", description="{0} is currently afk".format(mention.mention), color=Color.orange())
                embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(name="say", aliases=["embed"])
    async def _say(self, ctx, *, message):
        embed = Embed(description=message, color=Color.from_rgb(125, 220, 113))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases=["latency"])
    async def _ping(self, ctx):
        await ctx.send("{0}ms".format(round(self.bot.latency * 1000)))

    @commands.command(name="coinflip")
    async def _coinflip(self, ctx):
        coins = [
            "It's heads!",
            "It's heads!",
            "It's tails!",
            "It's tails!",
            "Oh. You lost the coin... Try again."
        ]
        await ctx.send(random.choice(coins))

    @commands.command(name="yesno")
    async def _yesno(self, ctx, *, question):
        yesno = random.randint(1, 2)
        if yesno == 1:
            embed = Embed(title="Yes/No", description="Let me answer your question.", color=Color.green())
            embed.add_field(name="Your question", value="```{0}```".format(question), inline=False)
            embed.add_field(name="My answer", value="Yes", inline=False)
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if yesno == 2:
            embed = Embed(title="Yes/No", description="Let me answer your question.", color=Color.red())
            embed.add_field(name="Your question", value="```{0}```".format(question), inline=False)
            embed.add_field(name="My answer", value="No", inline=False)
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="afk")
    async def _afk(self, ctx, *, reason="_No reason submitted._"):

        if ctx.author.id not in afk:

            embed = Embed(title="AFK", description="{0} has gone afk.".format(ctx.author), color=Color.orange())
            embed.add_field(name="Reason", value="```{0}```".format(reason), inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            afk.insert(0, ctx.author.id)

    @commands.command(name="mail")
    async def _mail(self, ctx, reciever: discord.Member, *, message):

        embed = Embed(title="You got a new mail:love_letter:", color=Color.from_rgb(125, 220, 113))
        embed.add_field(name="Sender", value="{0}".format(ctx.author), inline=True)
        embed.add_field(name="Server", value="{0}".format(ctx.guild), inline=True)
        embed.add_field(name="Message", value="```{0}```".format(message), inline=False)
        await reciever.send(embed=embed)

        embed = Embed(title="Mail", description="Successfully sent your mail to {0}".format(reciever.mention), color=Color.from_rgb(125, 220, 113))
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def _avatar(self, ctx, target: discord.Member):
        embed = Embed(title="Avatar", description="Avatar of {0}".format(target.mention), color=Color.from_rgb(125, 220, 113))
        embed.set_image(url=target.avatar_url)
        embed.add_field(name="Link", value=target.avatar_url, inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="google")
    async def _google(self, ctx, search):
        embed = Embed(title="Google", description="[Click here to see the search result](http://lmgtfy.com/?q={0})".format(search)
                      , color=Color.from_rgb(125, 220, 113))
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="alarm")
    async def _alarm(self, ctx, amount: int, *, notification):
        embed = Embed(title="Alarm", description="Set alarm for {0}s with notification:```{1}```".format(amount, notification),
                      color=Color.orange())
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        await asyncio.sleep(amount)

        await ctx.send("{0} riiiiing:alarm_clock:".format(ctx.author.mention))
        embed = Embed(title="Alarm", description="Alarm for ```{0}```".format(notification),
                      color=Color.from_rgb(125, 220, 113))
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
