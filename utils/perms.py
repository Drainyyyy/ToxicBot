from discord.ext import commands

import config
from utils.db import trust


def trusted():
    async def predicate(ctx):
        return ctx.author.id in trust.trusted or commands.is_owner()
    return commands.check(predicate)


#   nc means non check
def trust_or_owner(uid):
    return uid in trust.trusted or uid == config.owner_id


def nc_trusted(ctx, compare: int = None):
    #   compare is eg for blacklist that users that got less permissions than the author are not returning true
    if ctx.author.id == config.owner_id:
        return True
    elif compare is not None:
        print("Compare not none")
        if compare in trust.trusted:
            print("compare in trusted")
            return trust.trusted[ctx.author.id] >= trust.trusted[compare]
        else:
            return trust_or_owner(ctx.author.id)
    else:
        return trust_or_owner(ctx.author.id)
