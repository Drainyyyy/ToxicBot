import sys

import discord
from discord.ext import commands

import config
from cogs.utils import guild
from cogs.utils.counter import Counter
from utils.message import embeds, colors
from utils import versions, github


class Information(commands.Cog, name="Information"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", aliases=["statistics"], description="Shows statistics of the bot.")
    async def _stats(self, ctx):

        embed = discord.Embed(title="Statistics", color=colors.information)
        embed.add_field(name="Uptime", value=Counter.uptime(), inline=True)
        embed.add_field(name="Commands", value=f"""**Total**: {Counter.commands}
        **Completed**: {Counter.completed_commands}
        **Failed**: {Counter.failed_commands}""", inline=True)
        embed.add_field(name="Messages", value=f"I received **{Counter.messages}** messages.", inline=False)
        embed.add_field(name="Users", value=f"Currently there are **{len(self.bot.users)}** users that can use this bot.", inline=True)
        embed.add_field(name="Guilds", value=f"This users are on **{len(self.bot.guilds)}** guilds", inline=True)
        embed.add_field(name="Version", value=f"v{versions.current_version}", inline=False)
        embed.add_field(name="Note", value="Messages and Commands are just counted since the last restart.", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="botinfo", aliases=["binfo", "info"], description="Shows information about the bot.")
    async def _botinfo(self, ctx):
        owner = self.bot.get_user(self.bot.owner_id)

        embed = discord.Embed(title="Botinfo", color=colors.information, description=
                              f"Hey, I'm **{self.bot.user}** and here is some information about me:")
        embed.add_field(name="Client", value=self.bot.user, inline=True)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Version", value=versions.current_version, inline=False)
        embed.add_field(name="Servers", value=f"Currently on **{len(self.bot.guilds)}** servers", inline=True)
        embed.add_field(name="Users", value=f"There's a total of incredible **{len(self.bot.users)}** users!", inline=True)
        embed.add_field(name="Library", value=f"[**discord.py**](https://github.com/Rapptz/discord.py) v**{discord.__version__}**", inline=True)
        embed.add_field(name="System", value="Python v**{0[0]}.{0[1]}. {0[2]}**".format(sys.version_info), inline=True)
        embed.add_field(name="Useful Commands", value="""**Help**: {0}help
            _Help just shows a general help page. For a list of all commands use **{0}commands**._\n
            **Report**: {0}report [user] [proof] [reason]
            _This is just for when a user abuses the bot._\n
            **Support**: {0}support
            If you want to support my development and my developer you can take a look at the support page.\n""".format(config.prefix), inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["uinfo"], description="Get's you information about a specific user.")
    async def _userinfo(self, ctx, user: discord.Member):

        embed = discord.Embed(title="Userinfo", color=colors.information, description=f"Information about **{user.mention}**")
        embed.add_field(name="Client", value=str(user), inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Roles", value=f"**{len(user.roles) - 1}** roles", inline=True)
        embed.add_field(name="Server Join Date", value=f"**{user.joined_at.__format__('%A, %d. %B %Y at %H:%M:%S')}**", inline=True)
        embed.add_field(name="Account Creation Date", value=f"**{user.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')}**", inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["sinfo"], description="Get's you information about a specific server the bot is on.")
    async def _serverinfo(self, ctx):
        guild = ctx.guild
        guildname = guild.name
        embed = discord.Embed(title="Serverinfo", color=colors.information, description=f"Information about **{guildname}**.")
        embed.add_field(name="Owner", value=f"**{guild.owner}** ({guild.owner.id})", inline=True)
        embed.add_field(name="Server-ID", value=guild.id, inline=False)
        embed.add_field(name="Users", value=f"Total: **{guild.member_count}** users\n", inline=True)
        embed.add_field(name="Channels", value=f"""Total: **{len(guild.channels)}** channels
        Voice: **{len(guild.voice_channels)}**
        Text: **{len(guild.text_channels)}**
        Categories: **{len(guild.categories)}**""", inline=True)
        embed.add_field(name="Verification-Level",
                        value=f"The Verification-Level for **{guildname}** is **{guild.verification_level}**.", inline=False)
        embed.add_field(name="Emojis", value=f"**{guildname}** has **{len(guild.emojis)}** different emojis.", inline=False)
        embed.add_field(name="AFK", value=f"Channel: **{guild.afk_channel}**\nTimeout: **{guild.afk_timeout}**", inline=True)
        embed.add_field(name="Default-Channel", value=guild.system_channel, inline=True)
        embed.add_field(name="Server Creation Date",
                        value=f"{guildname} was created  on **{guild.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')}**", inline=False)
        embed.add_field(name="Icon-Url", value=f"[Click here]({guild.icon_url})", inline=True)
        embed.add_field(name="Host Region", value=guild.region, inline=True)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="avatar", description="Get the avatar of a user as picture and link.")
    async def _avatar(self, ctx, user: discord.Member):
        await ctx.send(embed=embeds.one_line(
            title="Avatar", color=colors.information, ctx=ctx,
            message=f"**Link**: {user.avatar_url}\n or [click here]({user.avatar_url})\n\n**Avatar**:"
        ).set_image(url=user.avatar_url))

    @commands.command(name="ping", aliases=["pong", "latency"], description="Get the latency of the bot.")
    async def _ping(self, ctx):
        await ctx.send(embed=embeds.one_line(
            title="Ping", color=colors.information, ctx=ctx,
            message=f"Currently I got a latency of **{round(self.bot.latency * 1000)}**ms:gear:"))

    @commands.command(name="uptime")
    async def _uptime(self, ctx):
        await ctx.send(Counter.uptime())

    @commands.cooldown(1, 10)
    @commands.command(name="github", aliases=["commits"], description="Shows some statistics of the bots github repository")
    async def _github(self, ctx):
        msg = await ctx.send("Fetching information...")

        embed = discord.Embed(title="GitHub", color=colors.misc,
                              description=f"[Click here]({github.repository_url}) to get to the original repository.")
        embed.add_field(name="Stars", value=f"**{config.repository_name}** currently has **{github.stats('stars')}** stars.", inline=True)
        embed.add_field(name="Issues", value=f"Open: **{github.stats('open_issue_count')}** issues.\n"
                             f"Closed: **{github.stats('closed_issue_count')}** issues.\n", inline=True)
        embed.add_field(name="Commits", value=f"There are **{github.stats('commits')}** commits made by Drainyyyy.", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await msg.edit(content=None, embed=embed)

    @commands.group(name="serverlist", aliases=["guildlist", "guilds", "servers"], invoke_without_command=True,
                    description="Returns a list of all servers the bot is on.")
    async def _serverlist(self, ctx):
        embed = discord.Embed(title="Server List", color=colors.information,
                              description=f"To see the latest servers the bot joined use **{config.prefix}serverlist latest**")
        embed.add_field(name="Name", value="\n".join([guild.name for guild in self.bot.guilds]))
        embed.add_field(name="Users", value="\n".join([str(len(guild.members)) for guild in self.bot.guilds]))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @_serverlist.command(name="latest", description="Get a list of the latest 5 servers the bot joined.")
    async def _serverlist_latest(self, ctx):
        embed = discord.Embed(title="Latest Server Joins", color=colors.information,
                              description=f"To see the all servers the bot joined use **{config.prefix}serverlist**")
        embed.add_field(name="Latest Severs", value="**Latest 5**(Since last restart):\n"
                                                    + "\n\n".join(f"**{guild.name}** | **{len(guild.members)}** users" for guild in guild.latest))
        embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
