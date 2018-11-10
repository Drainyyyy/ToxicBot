import time

import discord
from discord import Color
from discord.ext import commands
from cogs.util import perms

disabled = False


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stop", aliases=["shutdown"])
    @perms.is_owner()
    async def _stop(self, ctx):
        embed = discord.Embed(title="Shutdown", description="Shutting down", color=Color.red())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Executor", value="{0} (ID: {1})".format(ctx.author, ctx.author.id), inline=False)
        embed.add_field(name="Executed at", value=time.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="Server", value="{0} (ID: {1})".format(ctx.guild.name, ctx.guild.id), inline=False)
        await ctx.send(embed=embed)
        await self.bot.close()

    @commands.command(name="sendall")
    @perms.is_trusted()
    async def _sendall(self, ctx, *, content):
        for guild in self.bot.guilds:
            if guild.system_channel not in guild.text_channels:
                channel = guild.text_channels[0]
            else:
                channel = guild.system_channel

            embed = discord.Embed(title="Important!", description="**{0}** (One of my devs) wants to say something to you!".format(ctx.author), color=Color.red())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="Message", value="```{0}```".format(content), inline=False)
            await channel.send(embed=embed)

        embed = discord.Embed(title="Sendall", description="Successfully sent your message.",
                              color=Color.green())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Your message was", value="```{0}```".format(content), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="leaveguild")
    @perms.is_trusted()
    async def _leaveguild(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        await guild.leave()
        embed = discord.Embed(title="Leave-Guild", description="Leaving guild", color=Color.red())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Executor", value="{0} (ID: {1})".format(ctx.author, ctx.author.id), inline=False)
        embed.add_field(name="Executed at", value=time.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="Server", value="{0} (ID: {1})".format(ctx.guild.name, ctx.guild.id), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="serverlist", aliases=["servers", "guilds"])
    @perms.is_trusted()
    async def _serverlist(self, ctx):
        embed = discord.Embed(title="Serverlist", color=Color.blue())
        embed.add_field(name="Current Server Count", value="**{}** guilds with a total of **{}** users"
                        .format(len(self.bot.guilds), len(self.bot.users)), inline=False)
        embed.add_field(name="Servers", value="```" + "\n".join(map(str, self.bot.guilds)) + "```", inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="echo")
    @perms.is_trusted()
    async def _echo(self, ctx, *, content):
        await ctx.send(content)

    @commands.group(name="secure", invoke_without_command=True)
    @perms.is_trusted()
    async def _secure(self, ctx):
        embed = discord.Embed(title="Secure", description="You can secure the bot by disabling it and some more...", color=Color.blue())
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @_secure.command(name="disable")
    @perms.is_trusted()
    async def _secure_disable(self, ctx):
        drainyyy = self.bot.get_user(249221746006163467)
        embed = discord.Embed(title="Secure", description="Disabling the bot", color=Color.red())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Executor", value="{0} (ID: {1})".format(ctx.author, ctx.author.id), inline=False)
        embed.add_field(name="Executed at", value=time.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="Server", value="{0} (ID: {1})".format(ctx.guild.name, ctx.guild.id), inline=False)
        await ctx.send(embed=embed)
        await drainyyy.send(embed=embed)
        disabled = True

    @_secure.command(name="enable")
    @perms.is_trusted()
    async def _secure_enable(self, ctx):
        drainyyy = self.bot.get_user(249221746006163467)
        embed = discord.Embed(title="Secure", description="Enabling the bot", color=Color.green())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Executor", value="{0} (ID: {1})".format(ctx.author, ctx.author.id), inline=False)
        embed.add_field(name="Executed at", value=time.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="Server", value="{0} (ID: {1})".format(ctx.guild.name, ctx.guild.id), inline=False)
        await ctx.send(embed=embed)
        await drainyyy.send(embed=embed)
        disabled = False


def setup(bot):
    bot.add_cog(Admin(bot))
