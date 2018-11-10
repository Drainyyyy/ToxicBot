import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import context

import cogs
from cogs.commands import admin, help
from cogs.util import perms
from util import presence, important, data

bot = commands.Bot(commands.when_mentioned_or(important.prefix), case_insensitive=True)
bot.remove_command("help")

extensions = [
    "cogs.dblstats",
    "cogs.error",
    "cogs.guild_join",
    "cogs.commands.admin",
    "cogs.commands.debug",
    "cogs.commands.help",
    "cogs.commands.information",
    "cogs.commands.misc",
    "cogs.commands.moderation",
    "cogs.commands.special",
]


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print("Logged in as {0} ({1})".format(bot.user, bot.user.id))
    print("Running on {0} servers".format(len(bot.guilds)))
    change_status = presence.Presence(bot)
    await change_status.change_status()


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    data.msgs += 1
    await bot.process_commands(message)


@bot.event
async def process_commands(message: discord.Message):
    ctx = await bot.get_context(message, cls=context.Context)
    if ctx.command is None:
        if ctx.message.content.startswith(bot.user.mention):
            await ctx.send("Ey... what's up {0}?\nIf you need help do {1}help".format(ctx.author.mention, important.prefix))
    elif admin.disabled:
        if ctx.author.id not in data.owners:
            ctx = await bot.get_context(message, cls=context.Context)
            embed = discord.Embed(title="Error", description="The bot is currently disabled.", color=Color.red())
            embed.set_footer(text="Requested by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
    await bot.invoke(ctx)

for extension in extensions:
    try:
        bot.load_extension(extension)
        print("Successfully loaded {0}".format(extension))
    except Exception as error:
        print("{0} cannot be loaded. [{1}]".format(extension, error))


@bot.command(name="loadcog", aliases=["addcog"])
@perms.is_owner()
async def _loadcog(ctx, extension):
        try:
            bot.load_extension(extension.lower())
            if not extensions.__contains__(extension.lower()):
                extensions.insert(0, extension.lower())
            await ctx.send("``{0}`` has been loaded.".format(extension))
        except Exception:
            await ctx.send("``{0}`` cannot be loaded.".format(extension))


@bot.command(name="reloadcogs", aliases=["reload"])
@perms.is_owner()
async def _reloadcogs(ctx):
    for extension in extensions:
        try:
            bot.unload_extension(extension)
            bot.load_extension(extension)
            await ctx.send("``{0}`` has been reloaded.".format(extension))
        except Exception as error:
            print("{0} cannot be reloaded. [{1}]".format(extension, error))

bot.run(important.token)
