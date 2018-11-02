import sys
import traceback

import discord
from discord import Color
from discord.ext import commands

from util import data, important


class ErrorHandling:

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title='Error', description="It seems like the command you wanted to execute doesn't exist.", color=Color.red())
            embed.add_field(name="Command list", value="If you want to see a list of all commands [click here]({0})"
                            .format(data.website), inline=False)
            embed.add_field(name="Error message", value="```{0}```".format(error), inline=False)
            embed.set_footer(text="Error triggered by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.NoPrivateMessage):
            description = "The command you wanted to execute can't be executed in private channel."

        elif isinstance(error, commands.DisabledCommand):
            description = "The command you wanted to execute is currently disabled."

        elif isinstance(error, commands.CommandInvokeError):
            description = "An error occurred while invoking the command."

        elif isinstance(error, commands.CheckFailure):
            description = "It seems like you don't have enough permissions for this command."

        elif isinstance(error, commands.BotMissingPermissions):
            description = "The bot doesn't have enough permissions for this command."

        elif isinstance(error, commands.MissingRequiredArgument):
            description = "A required argument is missing."

        elif isinstance(error, commands.MissingPermissions):
            description = "You are missing permissions to execute this command."

        elif isinstance(error, commands.CommandOnCooldown):
            description = "The command you wanted to execute is currently on cooldown for you."

        else:
            description = "An unknown error occured"

        embed = discord.Embed(title="Error", description=description, color=Color.red())
        embed.add_field(name="Error message", value="```{0}```".format(error), inline=False)
        embed.set_footer(text="Error triggered by {0}".format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
