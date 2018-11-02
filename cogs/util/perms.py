from discord.ext import commands
from discord import role

from util import data


def is_owner():
    def check(ctx):
        return data.owners.__contains__(ctx.message.author.id)
    return commands.check(check)


def is_trusted():
    def check(ctx):
        return data.trusted.__contains__(ctx.message.author.id)
    return commands.check(check)
