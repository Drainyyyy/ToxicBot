import asyncio
import pathlib

import discord
from discord.ext import commands

import config
from utils import versions, channels, emojis, perms
from utils.db import blacklist
from utils.db.blacklist import Blacklist
from utils.db.db import Database
from utils.db.trust import Trust
from utils.message import embeds, colors, webhooks

cog_list = []

for cog in [file.stem for file in pathlib.Path("cogs/utils").glob('*.py')]:
    if cog.startswith("__"):
        continue

    cog_list.append(f"cogs.utils.{cog}")

for cog in [file.stem for file in pathlib.Path("cogs/cmds").glob('*.py')]:
    if cog.startswith("__"):
        continue

    cog_list.append(f"cogs.cmds.{cog}")


class Administration(commands.Cog, name="Administration"):
    def __init__(self, bot):
        self.bot = bot

    @perms.trusted()
    @commands.command(name="cversfile", aliases=["createversionfile", "createversfile", "cvfile"], description="Create a file for a version.")
    async def _create_version_file(self, ctx, version=versions.current_version, amount: int = 1):
        await ctx.send(embed=embeds.one_line(
                title="Version File", message=versions.create_version_file(version, amount),
                color=colors.admin, ctx=ctx)
        )

    @commands.is_owner()
    @commands.command(name="reload", aliases=["reloadcogs"], description="Reload all commands and utils.")
    async def _reload(self, ctx):
        passed = []
        failed = {}
        for extension in cog_list:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
                passed.append(f"``{extension}``")
            except Exception as error:
                failed[extension] = error

        try:
            await Database.updatedb(Database(self.bot))
            passed.append("``Database``")
        except Exception as error:
            failed["Database"] = error

        if passed is not None:
            await ctx.send(f"Successfully loaded {', '.join(passed)}")
        if failed is not None:
            for fail in failed:
                await ctx.send(f"Failed loading **{fail}**. Error:```{failed[fail]}```")

    @commands.is_owner()
    @commands.command(name="sendall", description="Send a message to all guilds the bot is on")
    async def _sendall(self, ctx, title, *, text):
        embed = discord.Embed(title="Send to all", color=colors.admin,
                              description=f"Do you want to send this message to **{len(self.bot.guilds)}** guilds?")
        embed.add_field(name="Your message", value=f"**{title}**\n\n{text}", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emojis.check_mark)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emojis.check_mark

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=120.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            send_embed = discord.Embed(title=title, color=colors.admin, description=text)
            send_embed.set_footer(text=f"Sent by {ctx.author}", icon_url=ctx.author.avatar_url)
            sending = await ctx.send("Sending message...")
            for guild in self.bot.guilds:
                await channels.system_or_first(guild, self.bot).send(embed=send_embed)
            await sending.edit(
                content=f"Your message has been sent to **{len(self.bot.guilds)}** guilds with a total of **{len(self.bot.users)}** users.")

    @perms.trusted()
    @commands.command(name="check", description="Check on what servers a user is (and the bot ofc)")
    async def _server_check(self, ctx, user_id: int):
        user_guilds = []
        try:
            user = self.bot.get_user(user_id)
        except Exception:
            raise commands.UserInputError("This user is on no server the bot is on.")
        for guild in self.bot.guilds:
            if user in guild.members:
                user_guilds.append(f"``{guild.name}({guild.id})``")
        embed = discord.Embed(title="Check", color=colors.admin, description=f"Check for **{user}**")
        embed.add_field(name="Servers", value=f"This user is on **{len(user_guilds)}** guilds where the bot is on.", inline=False)
        embed.add_field(name="Server-list", value="\n".join(user_guilds), inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="leave", aliases=["leaveserver"], description="Leaves servers,")
    async def _leave(self, ctx, server_id: int, *, reason=None):
        try:
            guild = self.bot.get_guild(server_id)
        except Exception:
            raise commands.UserInputError(f"The bot is on server with the id '{server_id}'")
        embed = discord.Embed(title="Leave", color=colors.admin, description=f"Do you really want me to leave **{guild.name}**({guild.id})?")
        if reason is not None:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Arranged by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emojis.check_mark)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emojis.check_mark

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content="Your time ran out. Try again!")
        else:
            if reason is not None:
                send_embed = discord.Embed(title="Leave", color=colors.admin, description="Leaving your guild.")
                send_embed.add_field(name="Reason", value=reason, inline=False)
                send_embed.set_footer(text=f"Arranged by {ctx.author}", icon_url=ctx.author.avatar_url)
                await channels.system_or_first(guild, self.bot).send(embed=send_embed)
            await guild.leave()
            await ctx.send("Successfully left the server.")

    @perms.trusted()
    @commands.command(name="echo", aliases=["devsay"], description="The bot says exactly what you want him to say.")
    async def _devsay(self, ctx, *, text):
        await ctx.send(text)

    @commands.group(name="trust", description="Trust a user special permissions for the bot.", invoke_without_command=True)
    async def _trust(self, ctx):
        await ctx.send(f"For help use **{config.prefix}help trust.**")

    @commands.is_owner()
    @_trust.command(name="add", description="Add a user to the trusts.")
    async def _trust_add(self, ctx, uid: int, perm_level: int = 1):
        await Trust.trust(Trust(self.bot), uid, perm_level)
        user = self.bot.get_user(uid)
        embed = discord.Embed(title="Trust", color=colors.admin, description=f"Trusting **{user}**")
        embed.add_field(name="UID", value=f"{uid}", inline=True)
        embed.add_field(name="Permissions level", value=f"{perm_level}", inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"Trusted by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
        await webhooks.webhook(url=config.notif_wh_url, bot=self.bot, embed=embed)
        await user.send(embed=embed)

    @commands.is_owner()
    @_trust.command(name="remove", description="Remove a user from the trusted people.")
    async def _trust_remove(self, ctx, uid: int, *, reason="No reason submitted."):
        await Trust.untrust(Trust(self.bot), uid)
        user = self.bot.get_user(uid)
        embed = discord.Embed(title="Trust", color=colors.admin, description=f"Unrusting **{user}**")
        embed.add_field(name="UID", value=f"{uid}", inline=True)
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"Untrusted by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
        await webhooks.webhook(url=config.notif_wh_url, bot=self.bot, embed=embed)
        await user.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="updatedb", aliases=["reloaddb"], description="Update the database data.")
    async def _updatedb(self, ctx):
        msg = await ctx.send("Reloading database.")
        try:
            await Database.updatedb(Database(self.bot))
            await msg.edit(content="Database got reloaded.")
        except Exception as error:
            await msg.edit(content="An error occurred.")
            raise commands.CommandInvokeError(f"[DB] Couldn't reload the database.\n[{error}]")

    @commands.group(name="blacklist", description="When a user is on the blacklist he is unable to use the bot anymore.", invoke_without_command=True)
    async def _blacklist(self, ctx):
        await ctx.send(f"For help use **{config.prefix}help blacklist.**")

    @perms.trusted()
    @_blacklist.command(name="add", description="Adds a user to the blacklist.")
    async def _blacklist_add(self, ctx, victim_uid: int, *, reason):
        if victim_uid in blacklist.blacklisted:
            raise commands.UserInputError("This user is already on the blacklist.")
        victim = self.bot.get_user(victim_uid)

        await Blacklist.insert(Blacklist(self.bot), victim.id, reason, ctx.author.id)

        embed = discord.Embed(title="Blacklist", color=colors.admin, description=f"Blacklisting **{victim}**")
        embed.add_field(name="Victim", value=f"{victim.mention} (**{victim}** ID: {victim.id})", inline=True)
        embed.add_field(name="Executor", value=f"{ctx.author.mention} (**{ctx.author}** ID: {ctx.author.id})", inline=True)
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.add_field(name="Ban ID", value=str(victim_uid), inline=True)
        embed.set_thumbnail(url=victim.avatar_url)
        embed.set_footer(text=f"To get information about blacklist use {config.prefix}blacklist info. | Blacklisted by {ctx.author}",
                         icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
        await webhooks.webhook(url=config.notif_wh_url, bot=self.bot, embed=embed)
        await victim.send(embed=embed)

    @perms.trusted()
    @_blacklist.command(name="remove", description="Remove a user from the blacklist.")
    async def _blacklist_remove(self, ctx, victim_uid: int):
        record = await Blacklist.get_all(Blacklist(self.bot), victim_uid)
        if victim_uid not in blacklist.blacklisted:
            raise commands.UserInputError("This user is not on the blacklisted.")
        victim = self.bot.get_user(victim_uid)
        banned_by = self.bot.get_user(record["executor_id"])
        embed = discord.Embed(title="Blacklist", color=colors.admin, description=f"Removing **{victim}** from the blacklist.")
        embed.add_field(name="Victim", value=f"{victim.mention} (**{victim}** ID: {victim.id})", inline=True)
        embed.add_field(name="Executor", value=f"{ctx.author.mention} (**{ctx.author}** ID: {ctx.author.id})", inline=True)
        embed.add_field(name="Banned by", value=f"{banned_by.mention} (**{banned_by}** ID:{banned_by.id})", inline=True)
        embed.add_field(name="Banned for", value=f"```{record['reason']}```", inline=False)
        embed.set_thumbnail(url=victim.avatar_url)
        embed.set_footer(text=f"To get information about blacklist use {config.prefix}blacklist info. | Blacklisted by {ctx.author}",
                         icon_url=ctx.author.avatar_url)

        await Blacklist.remove(Blacklist(self.bot), victim_uid)

        await ctx.send(embed=embed)
        await webhooks.webhook(url=config.notif_wh_url, bot=self.bot, embed=embed)
        await victim.send(embed=embed)

    @_blacklist.command(name="info", description="Get information about what blacklist is.")
    async def _blacklist_info(self, ctx):
        infos = {"What's this blacklist for?": """This Blacklist is a list for users that abused this bot.
        They are getting listed and are from that point on no longer able to use this bot.""",
                 "What to do when banned?": f"""If you are banned you must join the bots support server ({config.discord_server}).
                 There's no other option at the moment.""",
                 "I got banned for nothing!": """If you think you got banned without any reason just join our support server.
                 We got logs about who got blacklisted when etc.""",
                 "How can I get informations about my ban?": f"""Just use {config.prefix}blacklist view [ban id/your id]"""}

        embed = discord.Embed(title="Blacklist", color=colors.admin, description="A help page for the blacklist command.")
        for info in infos:
            embed.add_field(name=info, value=infos[info], inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @_blacklist.command(name="view", aliases=["baninfo"], description="Get information about your ban.")
    async def _blacklist_baninfo(self, ctx, ban_id: int):
        if ban_id not in blacklist.blacklisted:
            raise commands.UserInputError("This user isn't blacklisted.")
        elif not perms.nc_trusted(ctx, ban_id) and ctx.author.id is not ban_id:
            raise commands.CheckFailure("You don't have permissions for viewing this ban.")

        victim = self.bot.get_user(ban_id)
        record = await Blacklist.get_all(Blacklist(self.bot), victim.id)
        executor_id = record["executor_id"]
        executor = self.bot.get_user(executor_id)
        reason = record["reason"]

        embed = discord.Embed(title="Blacklist", color=colors.admin, description=f"Viewing ban for **{victim}**.")
        embed.add_field(name="Victim", value=f"{victim.mention} (**{victim}** ID: {victim.id})", inline=True)
        embed.add_field(name="Executor", value=f"{executor.mention} (**{executor}** ID: {executor.id})", inline=True)
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.add_field(name="Ban ID", value=str(ban_id), inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.author.send(embed=embed)
        await ctx.send("Take a look at your DMs.")

    @commands.is_owner()
    @commands.command(name="shutdown", aliases=["stop"], description="Shut down the bot.")
    async def _shutdown(self, ctx, *, reason="No reason submitted."):
        embed = embeds.one_line(title="Shutdown", color=colors.special, ctx=ctx,
                                message=f"Shutdown initiated by {ctx.author.mention} (**{ctx.author}** ID: {ctx.author.id}).```{reason}```")
        await ctx.send(embed=embed)
        await webhooks.webhook(url=config.notif_wh_url, bot=self.bot, embed=embed)
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Administration(bot))
