import datetime
import time


class Counter:
    def __init__(self, bot):
        self.bot = bot
    messages = 0
    commands = 0
    completed_commands = 0
    failed_commands = 0

    start_time = time.time()

    @staticmethod
    async def on_message(message):
        Counter.messages += 1

    @staticmethod
    async def on_command_completion(ctx):
        Counter.completed_commands += 1

    @staticmethod
    async def on_command_error(ctx, error):
        Counter.failed_commands += 1

    @staticmethod
    async def on_command(ctx):
        Counter.commands += 1

    @staticmethod
    def uptime():
        difference = int(round(time.time() - Counter.start_time))
        uptime = datetime.timedelta(seconds=difference)
        return str(uptime)


def setup(bot):
    bot.add_cog(Counter(bot))
