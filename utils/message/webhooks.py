import aiohttp
from discord import Webhook, AsyncWebhookAdapter


async def webhook(url, bot, content=None, embed=None):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        return await webhook.send(username=bot.user.name, avatar_url=bot.user.avatar_url, content=content, embed=embed)
