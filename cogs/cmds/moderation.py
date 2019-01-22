import typing

import discord
from discord.ext import commands

import config
import datetime
from utils.message import colors, embeds


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role(name=config.bot_role)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name="ban", description="Swing the ban hammer!")
    async def _ban(self, ctx, victim: discord.Member, *, reason=config.standard_mod_message):

        await victim.ban(reason=reason)

        embed = discord.Embed(title="Ban", color=colors.moderation, description=f"Banning **{victim}**")
        embed.add_field(name="Victim", value=f"{victim.mention} (**{victim}** ID: {victim.id})", inline=True)
        embed.add_field(name="Executor", value=f"{ctx.author.mention} (**{ctx.author}** ID: {ctx.author.id})", inline=True)
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.add_field(name="Execution", value=f"{datetime.datetime.now().__format__('%A, %d. %B %Y at %H:%M:%S')}", inline=True)
        embed.set_thumbnail(url=victim.avatar_url)
        embed.set_footer(text=f"Banned by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.has_role(name=config.bot_role)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name="kick", description="Kick them out of your server!")
    async def _kick(self, ctx, victim: discord.Member, *, reason=config.standard_mod_message):

        await victim.kick(reason=reason)

        embed = discord.Embed(title="Kick", color=colors.moderation, description=f"Kicking out **{victim}**")
        embed.add_field(name="Victim", value=f"{victim.mention} (**{victim}** ID: {victim.id})", inline=True)
        embed.add_field(name="Executor", value=f"{ctx.author.mention} (**{ctx.author}** ID: {ctx.author.id})", inline=True)
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.add_field(name="Execution", value=f"{datetime.datetime.now().__format__('%A, %d. %B %Y at %H:%M:%S')}", inline=True)
        embed.set_thumbnail(url=victim.avatar_url)
        embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.has_role(name=config.bot_role)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 30)
    @commands.command(name="clear", aliases=["cc"], description="Clear the chat.")
    async def _clear(self, ctx, amount: typing.Union[int, discord.Member]):
        """A bit skidded by github.com/itsVale/Vale.py"""
        if isinstance(amount, int):
            await ctx.channel.purge(limit=min(amount, 1000) + 1)
            await ctx.send(embed=embeds.one_line(title="Clear", color=colors.moderation, ctx=ctx,
                                                 message=f"{ctx.author.mention} wanted me clear **{amount}** messages."), delete_after=2)
        elif isinstance(amount, discord.Member):
            await ctx.channel.purge(check=lambda m: m.author.id == amount.id)
            await ctx.send(embed=embeds.one_line(title="Clear", color=colors.moderation, ctx=ctx,
                                                 message=f"{ctx.author.mention} wanted me clear all messages from **{amount}**."), delete_after=2)


def setup(bot):
    bot.add_cog(Moderation(bot))
