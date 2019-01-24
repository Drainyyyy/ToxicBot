import asyncio
import random

import discord

import config


class Presence:
    def __init__(self, bot):
        self.bot = bot
        self.presences = [
            (discord.Status.dnd, discord.ActivityType.watching, f" over {len(self.bot.guilds)} servers!"),
            (discord.Status.dnd, discord.ActivityType.listening, f" {config.prefix}help | {config.prefix}commands"),
            (discord.Status.dnd, discord.ActivityType.watching, f" over {len(self.bot.guilds)} servers with a total of {len(self.bot.users)} users"),
            (discord.Status.dnd, discord.ActivityType.playing, " with shitcode"),
            (discord.Status.dnd, discord.ActivityType.listening, " you."),
            (discord.Status.dnd, discord.ActivityType.playing, " mention me!"),
            ]

    async def start_status(self):
        while True:

            status, activity_type, activity = random.choice(self.presences)

            await self.bot.change_presence(status=status, activity=discord.Activity(type=activity_type, name=activity))
            await asyncio.sleep(30)
