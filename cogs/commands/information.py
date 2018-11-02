import sys
from datetime import datetime

import discord
from discord import Color
from discord.ext import commands

from cogs.util import version_stuff
from util import data, important


class Information:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo", aliases=["info", "binfo"])
    async def _botinfo(self, ctx):
        embed = discord.Embed(title="Bot information", description="Here is some information about me:",
                              color=Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Prefix", value="{0}".format(important.prefix), inline=False)
        embed.add_field(name="Owner", value="Drainyyy#9339", inline=True)
        embed.add_field(name="Guilds", value="{0} Guilds".format(len(self.bot.guilds)), inline=True)
        embed.add_field(name="User", value="{0} Users".format(len(self.bot.users)), inline=True)
        embed.add_field(name="Version", value=version_stuff.version, inline=True)
        embed.add_field(name="Ping", value="{0}ms".format(round(self.bot.latency * 1000)), inline=True)
        embed.add_field(name="Help", value="For help do {0}help".format(important.prefix), inline=True)
        embed.add_field(name="Library", value="[discord.py](https://github.com/Rapptz/discord.py)\ndiscord.py version: {1}\n"
                                              "Python version: {0[0]}.{0[1]}.{0[2]}".format(sys.version_info, discord.__version__), inline=True)
        embed.add_field(name="Support", value="[Join our server](https://discord.gg/7hwqtSD)"
                                              "\n[Vote on discordbots.org](https://discordbots.org/bot/497000115194822661/vote)"
                                              "\n[My website]({0})"
                                              "\n[Add me to your server]({1})".format(data.website, data.invite_link), inline=True)
        embed.add_field(name="Other", value="If a user abuses the bot report him with a screen as proof. Reason can be whatever you want.",
                        inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["sinfo"])
    async def _serverinfo(self, ctx):
        embed = discord.Embed(title="Server information", description="**{0}**".format(ctx.guild),
                              color=Color.blue())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="Name", value=ctx.guild, inline=True)
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        embed.add_field(name="Member".format(ctx.guild.member_count),
                        value="{0} Users".format(len(ctx.guild.members)), inline=True)
        embed.add_field(name="{0} Channels".format(len(ctx.guild.channels)),
                        value="{0} Categories\n{1} Voice channels\n{2} Text channels\nAFK: {3}\nDefault: {4}"
                        .format(len(ctx.guild.categories), len(ctx.guild.voice_channels)
                                , len(ctx.guild.text_channels), ctx.guild.afk_channel, ctx.guild.system_channel), inline=True)
        embed.add_field(name="Region", value="{0}".format(ctx.guild.region), inline=True)
        embed.add_field(name="Verification-Level", value="{0}".format(ctx.guild.verification_level), inline=True)
        embed.add_field(name="Created at", value="{0}".format(ctx.guild.created_at), inline=True)

        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["uinfo"])
    async def _userinfo(self, ctx, user: discord.Member):

        embed = discord.Embed(title="User information", description="Information about {0}".format(user.mention), color=Color.blue())
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Name#Discriminator", value=str(user), inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="ID", value=str(user.id), inline=False)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Roles", value="This user has **{0}** roles".format(len(user.roles) - 1), inline=True)
        embed.add_field(name="Activity", value="{0}".format(user.activity.name), inline=True)
        embed.add_field(name="Join date", value=user.joined_at.__format__("%A, %d. %B %Y at %H:%M:%S"), inline=False)
        embed.add_field(name="Account creation date", value=user.created_at.__format__("%A, %d. %B %Y at %H:%M:%S"), inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="stats", aliases=["statistics"])
    async def _stats(self, ctx):
        embed = discord.Embed(title="Statistics", description="Here are my stats:", color=Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Guilds", value="{0}".format(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Users", value="{0}".format(len(self.bot.users)), inline=True)
        embed.add_field(name="Version", value="{0}".format(version_stuff.version), inline=False)
        embed.add_field(name="Messages got since last restart", value="{0}".format(data.msgs), inline=True)
        embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
