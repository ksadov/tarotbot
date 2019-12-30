import os
import tarot
from tarot import ReadingType
import discord
from dotenv import load_dotenv
from discord.ext import flags, commands
from io import BytesIO

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

    async def _handle(self, ctx, cards, type, flags):
        response = tarot.cardtxt(cards)
        embed = discord.Embed(title=type.value, type="rich", color=discord.Color.teal())
        for (n,v) in response:
            embed.add_field(name=n, value=v)
        if not flags['t']:
            im = tarot.cardimg(cards, type)
            with BytesIO() as buf:
                im.save(buf, "PNG")
                buf.seek(0)
            # im.save(buffered, format="PNG")
                file = discord.File(fp=buf,filename="image.png")
            # buffered.close()
                embed.set_image(url="attachment://image.png")
            await ctx.send(file=file, embed=embed)
            # await ctx.send(file=file, embed=embed)
        else:
            await ctx.send(embed=embed)

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
        await self._handle(ctx, cards, ReadingType.ONE, flags)

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
        await self._handle(ctx, cards, ReadingType.THREE, flags)

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
        await self._handle(ctx, cards, ReadingType.FIVE, flags)

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
        await self._handle(ctx, cards, ReadingType.CELTIC, flags)

bot.add_cog(Tarot(bot))

bot.run(token)
