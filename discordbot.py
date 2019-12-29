import os
import tarot
import discord
from dotenv import load_dotenv
from discord.ext import flags, commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN', '/tarotbotenv')

bot = commands.Bot(command_prefix = '!')

class Tarot(commands.Cog):
    """Tarot spread commands."""

    #descriptions of flags for !help command
    flags_description = ("flags:\n--t\n    Text-only spread.\n--n\n    " +
                         "Disable inverted cards.")

    def __init__(self, bot):
        self.bot = bot

    @flags.add_flag("--t", action='store_true', default = False,
                    help="text only mode")
    @flags.add_flag("--n", action='store_false', default = True,
                    help="disable inversion")
    @flags.command(name="1card", brief = "1 card spread",
                   description =
                   "A one-card spread.\n\n" + "\n" + flags_description)
    async def onecard(self, ctx, **flags):
        """1 card spread"""
        cards = tarot.draw(1, flags['n'])
        response = tarot.cardtxt(cards)
        if not flags['t']:
            tarot.cardimg(cards, "1card")
            await ctx.send(file=discord.File("cardimg.png"))
        await ctx.send(response)

    @flags.add_flag("--t", action='store_true', default = False,
                    help="text only mode")
    @flags.add_flag("--n", action='store_false', default = True,
                    help="disable inversion")
    @flags.command(name="3card", brief = "3 card spread",
                   description =
                   "A three-card spread.\n\n" + "\n" + flags_description)
    async def threecard(self, ctx, **flags):
        """3 card spread"""
        cards = tarot.draw(3, flags['n'])
        response = tarot.cardtxt(cards)
        if not flags['t']:
            tarot.cardimg(cards, "3card")
            await ctx.send(file=discord.File("cardimg.png"))
        await ctx.send(response)

    @flags.add_flag("--t", action='store_true', default = False,
                    help="text only mode")
    @flags.add_flag("--n", action='store_false', default = True,
                    help="disable inversion")
    @flags.command(name="5card", brief = "5 card spread",
                   description =
                   "A five-card spread.\n\n" + "\n" + flags_description)
    async def fivecard(self, ctx, **flags):
        """5 card spread"""
        cards = tarot.draw(5, flags['n'])
        response = tarot.cardtxt(cards)
        if not flags['t']:
            tarot.cardimg(cards, "5card")
            await ctx.send(file=discord.File("cardimg.png"))
        await ctx.send(response)

    @flags.add_flag("--t", action='store_true', default = False,
                    help="text only mode")
    @flags.add_flag("--n", action='store_false', default = True,
                    help="disable inversion")
    @flags.command(name="celtic", brief = "Celtic Cross spread",
                   description =
                   "A ten-card Celtic Cross spread.\n\n" + "\n" +
                   flags_description)
    async def celticcross(self, ctx, **flags):
        """celtic cross spread"""
        cards = tarot.draw(10, flags['n'])
        response = tarot.cardtxt(cards)
        if not flags['t']:
            tarot.cardimg(cards, "celtic")
            await ctx.send(file=discord.File("cardimg.png"))
        await ctx.send(response)

bot.add_cog(Tarot(bot))

bot.run(token)
