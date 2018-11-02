import asyncio
import time

import discord
from discord import Color, message
from discord.ext import commands

from util import data


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="report")
    async def _report(self, ctx, target: discord.Member, proof, *, reason):
        drainyyy = self.bot.get_user(249221746006163467)
        embed = discord.Embed(title="Report", color=Color.red())
        embed.set_thumbnail(url=target.avatar_url)
        embed.add_field(name="Executor", value="**{0}**\n(ID: {1})".format(ctx.author, ctx.author.id), inline=True)
        embed.add_field(name="Victim", value="**{0}**\n(ID: {1})".format(target, target.id), inline=True)
        embed.add_field(name="Server", value=ctx.guild, inline=True)
        embed.add_field(name="Proof", value="```{0}```".format(proof), inline=False)
        embed.add_field(name="Reason", value="```{0}```".format(reason), inline=False)
        embed.set_footer(text="ID: {0}".format(target.id))
        await ctx.send(embed=embed)
        await drainyyy.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_role(data.bot_role)
    async def _ban(self, ctx, target: discord.Member, *, reason="_No reason submitted._"):

        embed = discord.Embed(title="Ban", color=Color.red())
        embed.add_field(name="Executor", value="{0} ({1})".format(ctx.author.mention, ctx.author), inline=False)
        embed.add_field(name="Victim", value="{0} ({1})".format(target.mention, target), inline=False)
        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Executed at", value=time.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="Reason", value="```{0}```".format(reason), inline=False)
        embed.set_footer(text="ID: {0}".format(target.id))

        await target.send(embed=embed)
        await ctx.send(embed=embed)

        await target.ban()

    @commands.command(name="kick")
    @commands.has_role(data.bot_role)
    async def _kick(self, ctx, target: discord.Member, *, reason="_No reason submitted._"):

        embed = discord.Embed(title="Kick", color=Color.red())
        embed.add_field(name="Executor", value="{0} ({1})".format(ctx.author.mention, ctx.author), inline=False)
        embed.add_field(name="Victim", value="{0} ({1})".format(target.mention, target), inline=False)
        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Executed at", value=time.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="Reason", value="```{0}```".format(reason), inline=False)
        embed.set_footer(text="ID: {0}".format(target.id))

        await target.send(embed=embed)
        await ctx.send(embed=embed)

        await target.kick()

    @commands.command(name="clear")
    @commands.has_role(data.bot_role)
    async def _clear(self, ctx, amount: int = 11):
        await ctx.channel.purge(limit=amount + 1)
        if amount == 1:
            msg = await ctx.send("{0} let me delete {1} message...".format(ctx.author.mention, str(amount)))
            await asyncio.sleep(3)
            await msg.delete()
        else:
            msg = await ctx.send("{0} let me delete {1} messages...".format(ctx.author.mention, str(amount)))
            await asyncio.sleep(3)
            await msg.delete()


def setup(bot):
    bot.add_cog(Moderation(bot))
