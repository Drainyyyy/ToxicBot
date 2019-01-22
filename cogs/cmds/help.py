import discord
from discord.ext import commands
from utils.message import colors
from config import prefix
import config

helps = {
    "Report": f"""If a user abuses the bot you can report him/her with the report command.
    _Note: After 3 reports the user is getting automatically banned._
    ```{prefix}report [user] [proof] [reason]```
    You can also access your reports. To see all report commands use the specific help command for report.""",
    "Blacklisted/Banned": f"""If you are blacklisted, there's no way to change it back except you join our discord and send an unban request there.
    Here's a link to the discord: ```{config.discord_server}```""",
    "Bugs": f"When you found a bug just send it to me with the bug-report command.```{prefix}bug [description of the bug]```"
}

cog_utils = []


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.cogs = self.bot.cogs
        self.cogs.pop("Counter")
        self.cogs.pop("ErrorHandling")
        self.cogs.pop("GuildManagement")
        self.cogs.pop("Debug")
        self.cogs.pop("DiscordBotsOrgAPI")

    @commands.command(name="commands", aliases=["cmds", "cmdlist", "commandlist"], description="Returns a list of all commands.")
    async def _command_list(self, ctx):
        embed = discord.Embed(title="Commands", color=colors.special,
                              description=f"To get help for a specific command use **{prefix}help [command]**")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        for cog in self.cogs:
            cmds = "``" + "``, ``".join(map(str, list(self.bot.get_cog_commands(cog)))) + "``"
            embed.add_field(name=cog, value=cmds, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="help", description="A simple help command.")
    async def _help(self, ctx, *, keyword=None):
        if keyword is None:

            embed = discord.Embed(title="Help", color=colors.special,
                                  description=f"""This is a general help page.
                                              To get help for a specific command use **{prefix}help [command]**.
                                              For a list of all commands use **{prefix}commands**.""")
            embed.set_footer(text=f"To get help for a specific command just use {prefix}help [command] | Requested by {ctx.author}",
                             icon_url=ctx.author.avatar_url)
            for field in helps:
                embed.add_field(name=field, value=helps[field], inline=True)
            await ctx.send(embed=embed)

        elif keyword in self.bot.all_commands:
            cmd = self.bot.get_command(keyword)
            embed = discord.Embed(title="Help", color=colors.other, description=f"A list of all commands can be found with **{prefix}commands**.")
            embed.add_field(name=cmd.name, value=f"""
                **Description:** {cmd.description}
                **Aliases:** {", ".join(cmd.aliases)}
                **Usage:** {prefix}{cmd.name} {" ".join(["[" + param  + "]" for param in dict(cmd.clean_params)])}
                """, inline=True)
            try:
                embed.add_field(name="Subcommands",
                                value="\n".join(f"{prefix}{cmd} **{subcmd.name}** "
                                f"{' '.join(['[' + param  + ']' for param in dict(subcmd.clean_params)])}" for subcmd in cmd.commands), inline=False)
            except Exception:
                pass
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            raise commands.CommandNotFound(f"Couldn't find '{keyword}'.")


def setup(bot):
    bot.add_cog(Help(bot))
