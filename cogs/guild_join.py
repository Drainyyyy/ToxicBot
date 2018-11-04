import sys

import discord
from discord import Color
from cogs.util import version_stuff
from util import important, data


class Guild_Join:
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        print("Joined '{0}'".format(guild.name))
        drainyyy = self.bot.get_user(249221746006163467)
        if guild.system_channel not in guild.text_channels:
            channel = guild.text_channels[0]
        else:
            channel = guild.system_channel

        embed = discord.Embed(title="Introducing me", description="Hey I'm {}.\nHere is some general information about me".format(self.bot.user)
                              , color=Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Prefix", value=important.prefix, inline=False)
        embed.add_field(name="Help", value="For help do **{}help**".format(important.prefix), inline=True)
        embed.add_field(name="Information", value="For information do **{}info**".format(important.prefix), inline=True)
        embed.add_field(name="Owner", value=drainyyy, inline=True)
        embed.add_field(name="Version", value="v**{}**".format(version_stuff.version), inline=True)
        embed.add_field(name="Library", value="**[discord.py](https://github.com/Rapptz/discord.py)** v**{}**"
                        .format(discord.__version__), inline=True)
        embed.add_field(name="System", value="Python version: **{0[0]}.{0[1]}.{0[2]}**".format(sys.version_info), inline=True)
        embed.add_field(name="Support", value="| [Patreon]({}) | [Server]({}) | [Github]({}) | [Website]({}) | [Invite]({}) | [Vote]({}) |"
                        .format(data.patreon, data.my_server, data.github, data.website, data.invite_link, data.dbl_vote), inline=False)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Guild_Join(bot))
