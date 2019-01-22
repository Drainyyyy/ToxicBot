import asyncio
import typing

import asyncpg
import discord
from discord.ext import commands

import config
from utils import versions, emojis, github, perms
from utils.db import profile
from utils.db.profile import Profile
from utils.message import embeds, colors, webhooks


class Special:
    def __init__(self, bot):
        self.bot = bot
        self.devmsgs = {}

    @commands.command(name="changelogs", aliases=["changes", "version"],
                      description="Shows the changes from a version you want.\n If you give no version the changes of the latest version are shown")
    async def _change_logs(self, ctx, version=versions.current_version):
        await ctx.send(
            embed=embeds.one_line(
                title=f"Changelog from version **{version}**", message=f"{versions.changes(version)}",
                color=colors.special, ctx=ctx))

    @commands.group(name="devmsg", aliases=["devmessage"], invoke_without_command=True,
                    description=f"This command is to request features and stuff. To report bugs use the {config.prefix}bugreport command.")
    async def _devmsg(self, ctx):
        await ctx.send(f"For help use **{config.prefix}help devmsg**")

    @commands.cooldown(1, 10)
    @_devmsg.command(name="send", description="Sends the message you want to my dev.")
    async def _devmsg_send(self, ctx, *, text):
        message_id = format(len(self.devmsgs), "08d")
        embed = discord.Embed(title="Dev Message", color=colors.special, description=f"ID: **{message_id}**")
        embed.add_field(name="Message", value=text, inline=False)
        embed.set_footer(text=f"Sent by {ctx.author}", icon_url=ctx.author.avatar_url)
        await webhooks.webhook(url=config.notif_wh_url, bot=self.bot, embed=embed)
        await ctx.send(embed=embeds.one_line(title="Dev Message", color=colors.special, ctx=ctx,
                                             message="Message has successfully been sent."))
        self.devmsgs[message_id] = {"author_id": ctx.author.id, "text": text}

    @commands.cooldown(1, 10)
    @perms.trusted()
    @_devmsg.command(name="reply", aliases=["respond", "answer"], description="Answer a user that has sent a message to a dev.")
    async def _devmsg_respond(self, ctx, message_id, *, text):
        embed = discord.Embed(title="Dev Message", color=colors.special, description="This would be your message. Send?")
        embed.add_field(name="Your message", value=self.devmsgs[message_id]["text"], inline=False)
        embed.add_field(name="Reply", value=text, inline=False)
        embed.set_footer(text=f"Replied by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emojis.check_mark)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emojis.check_mark

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content="Your time ran out. Try again!")
        else:
            embed.description = "Reply to your message."
            user = self.bot.get_user(self.devmsgs[message_id]["author_id"])
            await user.send(embed=embed)
            await ctx.send(f"Successfully sent the reply to **{user}**.")

    @commands.cooldown(1, 30)
    @commands.bot_has_permissions(add_reactions=True)
    @commands.command(name="bugreport", aliases=["bug"], description="Here you can report a bug.")
    async def _bug(self, ctx, *, description):
        embed = discord.Embed(title="Bug Report", color=colors.special)
        embed.add_field(name="Requirements", value=f"""Before you report your bug, try to complete the following checklist:
        **1.** Which feature is bugging?
        **2.** What is bugging? ( + detailed description of the bug)
        **3.** How can I reproduce the bug?
        **3.** [Check here]({config.repository_url}issues) if matching bug reports already exist. (If so just don't click the reaction)
        \nIf your bugreport doesn't match this checklist just send another one. If it does than click the reaction below.""", inline=False)
        embed.add_field(name="Your Report", value=f"**Now check your report again**:```{description}```")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emojis.check_mark)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emojis.check_mark

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content="Your time ran out. Try again!")
        else:
            github.post_issue(author=ctx.author, author_id=ctx.author.id, content=description)
            await ctx.send("Successfully sent the bugreport.")

    @commands.group(name="profile", description="Make a profile of yourself.", invoke_without_command=True)
    async def _profile(self, ctx):
        await ctx.send(f"For help use **{config.prefix}help profile.**")

    @_profile.command(name="create", description="Create a profile of yourself.")
    async def _profile_create(self, ctx, *, description_of_yourself):
        if ctx.author.id in profile.profiles:
            raise commands.UserInputError("You already got a profile.")
        if len(description_of_yourself) > 500:
            raise commands.UserInputError("Your description must can maximal be 500 chars.")
        try:
            await Profile.insert(Profile(self.bot), ctx.author.id, description_of_yourself)
            embed = discord.Embed(title="Profile", color=colors.special, description=f"Your profile has been created like this.")
            embed.add_field(name="Client", value=f"{ctx.author.mention} (**{ctx.author}** ID: {ctx.author.id})", inline=False)
            embed.add_field(name="Description", value=f"```{description_of_yourself}```", inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Created by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        except Exception:
            raise commands.UserInputError(f"You already got a profile. To delete it use {config.prefix}profile delete.")

    @_profile.command(name="view", description="View the profile of other users.")
    async def _profile_view(self, ctx, user: typing.Union[discord.Member, int]):
        if isinstance(user, int):
            uid = int
        elif isinstance(user, discord.Member):
            uid = user.id
        else:
            raise commands.UserInputError("User must be mentioned or given by the id.")

        try:
            profile_of = self.bot.get_user(uid)
            description = await Profile.get(Profile(self.bot), profile_of.id)
        except Exception:
            raise commands.UserInputError("Either the user or the profile doesn't exist.")

        embed = discord.Embed(title=profile_of.name, color=colors.special, description=f"Viewing profile of **{profile_of}**.")
        embed.add_field(name="Client", value=f"{profile_of.mention} (**{profile_of}** ID: {profile_of.id})", inline=False)
        embed.add_field(name="Description of him/her", value=f"```{description}```", inline=False)
        embed.set_thumbnail(url=profile_of.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @_profile.command(name="delete", description="Delete your profile")
    async def _profile_delete(self, ctx):
        if ctx.author.id not in profile.profiles:
            raise commands.UserInputError("You don't got a profile.")
        embed = discord.Embed(title="Profile", color=colors.special, description=f"Do you really want to delete your profile?")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emojis.check_mark)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emojis.check_mark

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content="Your time ran out. Try again!")
        else:
            await Profile.delete(Profile(self.bot), ctx.author.id)
            await ctx.send(f"Successfully deleted the profile of **{ctx.author.mention}**")


def setup(bot):
    bot.add_cog(Special(bot))
