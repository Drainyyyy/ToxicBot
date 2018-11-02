import discord
import asyncio
import random

from cogs.util.version_stuff import Version
from util import data, important


class Presence:
    def __init__(self, bot):
        self.bot = bot

    async def change_status(self):
        while True:
            presences = [
                (discord.Status.dnd, discord.ActivityType.watching, "over {0} guilds".format(len(self.bot.guilds))),
                (discord.Status.dnd, discord.ActivityType.listening, "your commands"),
                (discord.Status.dnd, discord.ActivityType.listening, "{0} users | {1} guilds".format(len(self.bot.users), len(self.bot.guilds))),
                (discord.Status.dnd, discord.ActivityType.listening, "{0}help".format(important.prefix)),
                (discord.Status.dnd, discord.ActivityType.playing, "with your data"),
                (discord.Status.dnd, discord.ActivityType.watching, data.website),
                (discord.Status.dnd, discord.ActivityType.watching, "nothing | v{0}".format(Version, important.prefix)),
                (discord.Status.dnd, discord.ActivityType.watching, "my script on {0}".format(data.script_link)),
            ]

            status, activity_type, activity = random.choice(presences)

            await self.bot.change_presence(status=status, activity=discord.Activity(type=activity_type, name=activity))
            await asyncio.sleep(30)
