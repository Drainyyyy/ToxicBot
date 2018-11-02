import dbl
import asyncio

from util import important


class DblApi:

    def __init__(self, bot):
        self.bot = bot
        self.token = important.prefix
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):

        while True:
            print("attempting to post server count")
            try:
                await self.dblpy.post_server_count()
                print("posted server count ({})".format(len(self.bot.guilds)))
            except Exception as e:
                print("Failed to post server count\n{}: {}".format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(bot):
    bot.add_cog(DblApi(bot))
