from discord import Embed

from utils.message import colors


def error(message, exception, ctx):
    embed = Embed(title="Error", color=colors.error, description=message)
    embed.add_field(name="Command", value=ctx.message.content, inline=False)
    embed.add_field(name="Exception", value=f"```{exception}```", inline=False)
    embed.set_footer(text=f"Triggered by {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
    return embed


def one_line(title, message, color, ctx):
    embed = Embed(title=title, color=color, description=message)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    return embed
