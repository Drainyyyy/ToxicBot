import asyncio
import random
import string

import discord
from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import context

from util import data

afk = {}


class Misc:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        ctx = await self.bot.get_context(message, cls=context.Context)
        if ctx.author.id in afk:
            embed = Embed(title="AFK", description="{} returned from afk.".format(ctx.author.mention), color=Color.green())
            embed.add_field(name="Reason", value="```{}```".format(afk[ctx.author.id]))
            await ctx.send(embed=embed)
            afk.pop(ctx.author.id)
            return
        for mention in ctx.message.mentions:
            if mention.id in afk:
                embed = Embed(title="AFK", description="{} is currently afk.".format(mention.mention), color=Color.orange())
                embed.add_field(name="Reason", value="```{}```".format(afk[mention.id]))
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
    async def _afk(self, ctx, *, reason="No reason submitted."):

        if ctx.author.id not in afk:

            embed = Embed(title="AFK", description="{} has gone afk.".format(ctx.author.mention), color=Color.orange())
            embed.add_field(name="Reason", value="```{}```".format(reason), inline=True)
            await ctx.send(embed=embed)

            afk[ctx.author.id] = reason

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

    @commands.command(name="patreon")
    async def _patreon(self, ctx):
        embed = Embed(title="Patreon", description="Hey. If you want to support me than you can donate me money on Patreon."
                                                   "\nAt the moment my only gift for donating is a special rank on my [Discord server]({0})."
                      .format(data.my_server), color=Color.from_rgb(125, 220, 113))
        embed.add_field(name="Link", value="[Click here]({0})".format(data.patreon), inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="google")
    async def _google(self, ctx, *, search):
        embed = Embed(title="Google", description="[Click here to see the search result for **{0}**](http://lmgtfy.com/?q={0})".format(search)
                      , color=Color.from_rgb(125, 220, 113))
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="pwgen", aliases=["passgen", "passwordgenerator"])
    async def _pwgen(self, ctx, length: int):
        chars = string.ascii_letters + string.digits + string.punctuation
        if length < 8:
            embed = Embed(title="Password", description="Passwords should never be less than 8 letters."
                          , color=Color.red())
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif length >= 95:

            embed = Embed(title="Password", description="Unable to handle password length higher than 94."
                          , color=Color.red())
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif length >= 8:
            pw = "".join(random.sample(chars, length))
            embed = Embed(title="Password", description="Password got sent per direct message."
                          , color=Color.green())
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            embed = Embed(title="Password", description="Here's your Password:```{}```".format(pw)
                          , color=Color.from_rgb(125, 220, 113))
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.author.send(embed=embed)

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
