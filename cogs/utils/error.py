from discord.ext import commands

import config
from utils.message import webhooks, embeds


async def webhook(bot, exception, ctx):
    await webhooks.webhook(url=config.err_wh_url, bot=bot,
                           content=f"**Exception Raw** ```{exception}```",
                           embed=embeds.error(message="Error Report", exception=exception, ctx=ctx))


class ErrorHandling:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandOnCooldown):
            msg = "The command you wanted to use is currently on cooldown."
        elif isinstance(exception, commands.CommandNotFound):
            msg = "It seems like the command you wanted to execute doesn't exist. (Typo?)" \
                  f"\nFor a list of all commands do **{config.prefix}commands** or **[click here]({config.website})**."
        elif isinstance(exception, commands.CheckFailure or commands.MissingPermissions):
            msg = f"You don't have enough permissions to execute this command.\n" \
                f"For some of the commands a special role named **{config.bot_role}** is needed."
        elif isinstance(exception, commands.MissingRequiredArgument):
            msg = "A required argument is missing."
        elif isinstance(exception, commands.BotMissingPermissions):
            msg = "I don't have enough permissions for that."
        elif isinstance(exception, commands.NoPrivateMessage):
            msg = "This command can't be executed in private channel."
        elif isinstance(exception, commands.UserInputError):
            msg = "Your given input was wrong."
        elif isinstance(exception, commands.CommandInvokeError):
            msg = "An error occurred while invoking the command."
            await webhook(self.bot, exception, ctx)
        else:
            msg = "An unknown error occurred.\nThe exception got sent to my dev."
            await webhook(bot=self.bot, exception=exception, ctx=ctx)

        await ctx.send(embed=embeds.error(message=msg, exception=exception, ctx=ctx))


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
