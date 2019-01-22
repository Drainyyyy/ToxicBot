import discord

from utils import channels
from utils.message import colors
import config

latest = []
support = {
    "Website": config.website,
    "Invite": config.invite,
    "GitHub": config.repository_url,
    "Server": config.discord_server,
    "Vote": config.vote,
    "Patreon": config.patreon
           }


class GuildManagement:
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        if len(latest) >= 4:
            latest.pop(4)
        latest.insert(0, guild)
        print(f"[JOIN] Joined [{guild}]")

        embed = discord.Embed(title="Introduction", color=colors.other, description="Hey there.")
        embed.add_field(name="Prefix", value=f"**{config.prefix}** or **mention ({self.bot.user.mention})** - (Currently not editable)")
        embed.add_field(name="Help", value=f"```To get help use \n{config.prefix}help```\nAll relevant infos can be found there.", inline=False)
        embed.add_field(name="Command help",
                        value=f"```To get help  for specific commands use \n{config.prefix}help [command or alias]```", inline=False)
        embed.add_field(name="Command list", value=f"```A list of all commands can be found by using \n{config.prefix}commands```", inline=False)
        embed.add_field(name="Support", value=" | ".join(support),
                        inline=False)
        embed.set_thumbnail(url=guild.icon_url)

        await channels.system_or_first(guild=guild, bot=self.bot).send(embed=embed)

    async def on_guild_leave(self, guild):
        print(f"[LEAVE] Left {guild}")


def setup(bot):
    bot.add_cog(GuildManagement(bot))
