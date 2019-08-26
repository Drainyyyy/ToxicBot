import asyncio
import pathlib

import asyncpg
import discord
from discord.ext import commands
from discord.ext.commands import context

import config
from utils.presence import Presence
from utils.db import blacklist
from utils.db.db import Database
from utils.message import embeds, colors

cog_list = []

for cog in [file.stem for file in pathlib.Path("cogs/utils").glob("*.py")]:
    if cog.startswith("__"):
        continue

    cog_list.append(f"cogs.utils.{cog}")

for cog in [file.stem for file in pathlib.Path("cogs/cmds").glob("*.py")]:
    if cog.startswith("__"):
        continue

    cog_list.append(f"cogs.cmds.{cog}")


async def run():

    db_login = {"user": config.db_user, "password": config.db_password, "database": config.db_name, "host": config.db_host}
    db = await asyncpg.create_pool(**db_login)

    print("[DB] Logged in.")

    await db.execute("CREATE TABLE IF NOT EXISTS blacklist(uid bigint PRIMARY KEY, reason varchar(2000), executor_id bigint)")
    await db.execute("CREATE TABLE IF NOT EXISTS guild_channels(gid bigint PRIMARY KEY, log_cid bigint)")
    await db.execute("CREATE TABLE IF NOT EXISTS trust(uid bigint PRIMARY KEY, perm_level int)")
    await db.execute("CREATE TABLE IF NOT EXISTS profile(uid bigint PRIMARY KEY, description varchar(500))")

    bot = Bot(db=db)
    bot.remove_command("help")

    try:
        await bot.start(config.bot_token)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()
    except ConnectionResetError or OSError:
        await bot.logout()
        await db.close()
        await asyncio.sleep(60)
        await run()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or(config.prefix), case_insensitive=True, owner_id=config.owner_id)
        self.db = kwargs.pop("db")

    async def on_ready(self):
        await self.wait_until_ready()

        print(f"Logged in as {self.user} ({self.user.id})")
        print(f"Running on {len(self.guilds)} guilds with a total of {len(self.users)} users.")

        for ext in cog_list:
            try:
                self.load_extension(ext)
                print(f"[Cogs] Loaded '{ext}'")
            except ImportError as error:
                print(f"[Cogs] Cannot load '{ext}' [{error}]")

        #   Load database stuff into cache
        await Database.updatedb(Database(self))

        #   Start presence
        status_changer = Presence(self)
        await status_changer.start_status()

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=context.Context)
        if message.author.bot:
            return
        if ctx.author.id in blacklist.blacklisted:
            if message.content.startswith(f"{config.prefix}blacklist") or message.content.startswith(f"{config.prefix}help"):
                await self.process_commands(message)
                return
            else:
                await ctx.send(embed=embeds.one_line(title=None, color=colors.admin, ctx=ctx, message="⛔You are currently blacklisted.")
                               .set_footer(text=f"For information just use {config.prefix}blacklist info | "
                               f"To get all blacklist commands use {config.prefix}help blacklist | Triggered by {ctx.author}",
                                           icon_url=ctx.author.avatar_url))
                return
        await self.process_commands(message)

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message, cls=context.Context)
        if ctx.command is None:
            if ctx.message.content.startswith(self.user.mention):
                await ctx.send(embed=embeds.one_line(
                    title="Introducing me!",
                    message=f"Hey there! I'm **{self.user}**.\n"
                    f"Currently I'm on **{len(self.guilds)}** servers with a total of **{len(self.users)}** users.\n"
                    f"My help command is **{config.prefix}help** and for a list of all commands do **{config.prefix}commands**.",
                    color=colors.other,
                    ctx=ctx
                ))
        await self.invoke(ctx)


asyncio.get_event_loop().run_until_complete(run())
