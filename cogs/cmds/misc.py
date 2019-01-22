import random
import string
from datetime import datetime

import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import context

import config
from utils import formatter
from utils.message import embeds, colors

afk = {}


async def is_afk(user, message):
    if user.id in afk:
        afk_for = formatter.timedelta(datetime.now() - afk[user.id]["afk_time"])
        embed = discord.Embed(title="AFK", color=colors.misc, description=f"{user.mention} has returned from being AFK.")
        embed.add_field(name="Reason was", value=f"```{afk[user.id]['reason']}```", inline=False)
        embed.add_field(name="AFK for", value=afk_for)
        embed.set_footer(text=f"Requested by {user}", icon_url=user.avatar_url)
        await message.channel.send(embed=embed)
        afk.pop(user.id)
        pass
    for mention in message.mentions:
        if mention.id in afk:
            afk_for = formatter.timedelta(datetime.now() - afk[user.id]["afk_time"])
            embed = discord.Embed(title="AFK", color=colors.misc, description=f"{mention.mention} is currently AFK.")
            embed.add_field(name="Reason was", value=f"```{afk[user.id]['reason']}```", inline=False)
            embed.add_field(name="AFK for", value=afk_for)
            embed.set_footer(text=f"Requested by {user}", icon_url=user.avatar_url)
            await message.channel.send(embed=embed)
        pass


class Miscellaneous:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        ctx = await self.bot.get_context(message, cls=context.Context)
        hit = ["Hit!", "I guess you never miss!"]
        miss = ["Missed!", "I guess you never miss! Only this time you did..."]
        if message.content.lower().startswith("hit or miss"):
            await ctx.send(random.choice(hit + miss))
        await is_afk(user=ctx.author, message=message)

    @commands.command(name="google", aliases=["lmgtfy"], description="Let me google that for you!")
    async def _google(self, ctx, *, query):
        await ctx.send(embed=embeds.one_line(
            title="Google", color=colors.misc, ctx=ctx,
            message=f"To see the result for **{query}**: [click here](http://lmgtfy.com/?q={query.replace(' ', '+')})"))

    @commands.command(name="8ball", aliases=["yesno"], description="Let the magical 8ball answer questions for you!")
    async def _8ball(self, ctx, *, question):
        answers = ["I don't think so...", "That's not possible at all.", "No way!", "Of course!", "YES!!!11!", "Yup ma friend!"]
        answer = random.choice(answers)
        await ctx.send(embed=embeds.one_line(
            title="8ball", color=colors.misc, ctx=ctx,
            message=f"""Let the magical 8ball answer your questions! Feel free to ask what you want!\n
            **Your question was**: ```{question}```
            **My answer is**:```{answer}```"""))

    @commands.has_role(name=config.bot_role)
    @commands.command(name="say", aliases=["embed"], description="Let the bot say what you want but with an embed.")
    async def _say(self, ctx, *, text):
        embed = discord.Embed(color=colors.misc, description=text)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="afk", description="Show others that you are afk and why.")
    async def _afk(self, ctx, *, reason="No reason submitted."):
        if ctx.author.id not in afk:
            embed = discord.Embed(title="AFK", color=Color.orange(), description=f"{ctx.author.mention} has gone AFK.")
            embed.add_field(name="Reason", value=f"```{reason}```")
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            afk[ctx.author.id] = {"reason": reason, "afk_time": datetime.now()}

    @commands.command(name="passwordgen", aliases=["pwgen", "passwordgenerator", "pwgenerator"],
                      description="Generates a completely random password for you.")
    async def _pwgen(self, ctx, length: int):
        chars = string.ascii_letters + string.digits + string.punctuation

        if length >= 8 and not length >= 95 and not length < 8:
            password = "".join(random.sample(chars, length))
            password_embed = embeds.one_line(title="Password Generator", color=colors.misc, ctx=ctx,
                                    message=f"**Here's your password**: {password}")
            await ctx.send("Password got sent per direct message!")
            await ctx.author.send(embed=password_embed)
        else:
            raise commands.UserInputError("The length must be between 8 and 94.")

    @commands.command(name="coinflip", aliases=["flipcoin"], description="Flips a coin for you.")
    async def _coinflip(self, ctx, coins: int = 1):

        if 1 <= coins <= 1000:
            heads = 0
            tails = 0
            for flip in range(coins):
                coin = random.randint(1, 2)
                if coin == 1:
                    heads += 1
                else:
                    tails += 1
            message = f"You flipped **{heads}** heads and **{tails}** tails."
        elif coins == 1:
            def out(cflip):
                messages = [f"Its... **{cflip}**!", f"You flipped... **{cflip}**"]
                return random.choice(messages)
            flip = random.choice["heads", "tails"]
            message = random.choice(out(flip))
        else:
            raise commands.UserInputError("You can only flip one up to 1000 coins.")

        await ctx.send(embed=embeds.one_line(title="Coinflip", color=colors.misc, ctx=ctx, message=message))

    @commands.cooldown(1, 10)
    @commands.command(name="mail", alises=["poke"], description="Let the bot be your messenger.")
    async def _mail(self, ctx, user: discord.Member, *, message):
        if user == ctx.author:
            await ctx.send(f"You can't message yourself, **{ctx.author}**")
            return
        embed = discord.Embed(title="Mail", color=colors.misc, description=f"New mail from **{ctx.author}**!")
        embed.add_field(name="Message", value=message, inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await user.send(embed=embed)
        await ctx.send(f"Message sent to **{user}**.")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
