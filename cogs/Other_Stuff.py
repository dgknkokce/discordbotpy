import discord
import random
from discord.ext import commands

class OtherStuff(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online.")

    #commands
    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        responses = ["As I see it, yes.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don’t count on it.",
                     "It is certain.",
                     "It is decidedly so.",
                     "Most likely.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Outlook good.",
                     "Reply hazy, try again.",
                     "Signs point to yes.",
                     "Very doubtful.",
                     "Without a doubt.",
                     "Yes.",
                     "Yes – definitely.",
                     "You may rely on it."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")







def setup(bot):
    bot.add_cog(OtherStuff(bot))