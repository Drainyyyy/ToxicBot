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

        embed = discord.Embed(title="Introducing me", description="Hey I'm {0}.\nHere is some general information about me".format(self.bot.user)
                              , color=Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Prefix", value=important.prefix, inline=False)
        embed.add_field(name="Help", value="{0}help".format(important.prefix), inline=True)
        embed.add_field(name="Owner", value=drainyyy, inline=True)
        embed.add_field(name="Version", value=version_stuff.version, inline=True)
        embed.add_field(name="Library", value="[discord.py](https://github.com/Rapptz/discord.py)\ndiscord.py version: {1}\n"
                                              "Python version: {0[0]}.{0[1]}.{0[2]}".format(sys.version_info, discord.__version__), inline=False)
        embed.add_field(name="Support", value="[Our Discord server](https://discord.gg/7hwqtSD)"
                                              " - Here you can give me suggestions of new commands (you can also use the devmsg command)."
                                              "\n[Vote](https://discordbots.org/bot/497000115194822661/vote)"
                                              " - Every vote helps."
                                              "\n[Website]({0})"
                                              " - It's possible that the website is sometimes little bit buggy."
                                              "\n[Invite]({1})"
                                              " - Invite me to other servers so our community can grow up faster."
                        .format(data.website, data.invite_link), inline=False)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Guild_Join(bot))
