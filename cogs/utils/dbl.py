import dbl

import asyncio

from discord.ext import commands

import config


class DiscordBotsOrgAPI(commands.Cog, name="DiscordBotsOrgAPI"):
    """
    Handles interactions with the discordbots.org API
    Modified example from https://discordbots.org/api/docs
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = config.dbl_token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            print('[DBLAPI] attempting to post server count')
            try:
                await self.dblpy.post_guild_count()
                print('[DBLAPI] posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                print('[DBLAPI] Failed to post server count | {}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
