import os
import tarot
from tarot import ReadingType
import discord
from dotenv import load_dotenv
from discord.ext import flags, commands
from io import BytesIO

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 't!')

#flags
FLAGS = {
	"text_only": {
		"flag": "--t",
		"letter": "t",
		"action": "store_true",
		"default": False,
		"help": "text only mode"
	},
	"no_inversions": {
		"flag": "--n",
		"letter": "n",
		"action": "store_false",
		"default": True,
		"help": "disable inversion"
	},
	"major_only": {
		"flag": "--M",
		"letter": "M",
		"action": "store_true",
		"default": False,
		"help": "only draw major arcana cards"
	},
	"minor_only": {
		"flag": "--m",
		"letter": "m",
		"action": "store_true",
		"default": False,
		"help": "only draw minor arcana cards"
	},
	"no_embed": {
		"flag": "--e",
		"letter": "e",
		"action": "store_false",
		"default": True,
		"help": "disable embed"
	},
	"image_only": {
		"flag": "--i",
		"letter": "i",
		"action": "store_true",
		"default": False,
		"help": "disable text"
	}
}

def add_flags(*flagList):
	def f(func):
		newf = func
		for flag in flagList:
			dec = flags.add_flag(FLAGS[flag]["flag"], action=FLAGS[flag]["action"],
					default=FLAGS[flag]["default"], help=FLAGS[flag]["help"])
			newf = dec(func)
		return newf
	return f

class Tarot(commands.Cog):
    """Tarot spread commands."""

    #descriptions of flags for !help command
    flags_description = ("flags:\n--t\n    Text-only spread.\n--n\n    " +
                         "Disable inverted cards.\n"+
                         "--M\n\tOnly draw major arcana cards\n" +
                         "--m\n\tOnly draw minor arcana cards\n" +
                         "Disable inverted cards.\n--e\n    " +
                         "Send unembedded response.\n--i\n    " +
                         "Image-only spread.")

    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.purple()
        # self.color = discord.Color.from_rgb(107,46,244)

    async def _handle(self, ctx, cards, type, flags):
        response = tarot.cardtxt(cards)
        #textonly disabled
        if not flags['t']:
            im = tarot.cardimg(cards, type)
            with BytesIO() as buf:
                im.save(buf, "PNG")
                buf.seek(0)
                file = discord.File(fp=buf,filename="image.png")
        #embeds enabled
        if flags['e']:
            embed = discord.Embed(title=type.value, type="rich",
                                  color=self.color)
            #imageonly disabled
            if not flags['i']:
                should_inline = type in [ReadingType.ONE, ReadingType.THREE]
                for i, (n,v) in enumerate(response):
                    embed.add_field(name='{}) {}'.format(i+1,n), value=v,
                                    inline=should_inline)
            #textonly disabled
            if not flags['t']:
                embed.set_image(url="attachment://image.png")
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(embed=embed)
        #embeds disabled
        else:
            responsetext = ""
            for i, (n,v) in enumerate(response):
                responsetext = (responsetext + "\n**" + str(i+1) + ") " +
                                n + "**\n" + v)
            #textonly disabled
            if not flags['t']:
                await ctx.send(file=file)
            #imageonly disabled
            if not flags['i']:
                await ctx.send(responsetext)

    @add_flags("text_only", "no_inversions", "major_only", "minor_only", "no_embed", "image_only")
    @flags.command(name="1card", brief = "1 card spread",
                   description = flags_description)
    async def onecard(self, ctx, **flags):
        """A one-card spread."""
        cards = tarot.draw(1, flags[FLAGS["no_inversions"]["letter"]], flags[FLAGS["major_only"]["letter"]], flags[FLAGS["minor_only"]["letter"]])
        await self._handle(ctx, cards, ReadingType.ONE, flags)

    @add_flags("text_only", "no_inversions", "major_only", "minor_only", "no_embed", "image_only")
    @flags.command(name="3card", brief = "3 card spread",
                   description = flags_description)
    async def threecard(self, ctx, **flags):
        """A three-card spread."""
        cards = tarot.draw(3, flags[FLAGS["no_inversions"]["letter"]], flags[FLAGS["major_only"]["letter"]], flags[FLAGS["minor_only"]["letter"]])
        await self._handle(ctx, cards, ReadingType.THREE, flags)

    @add_flags("text_only", "no_inversions", "major_only", "minor_only", "no_embed", "image_only")
    @flags.command(name="5card", brief = "5 card spread",
                   description = flags_description)
    async def fivecard(self, ctx, **flags):
        """A five-card spread."""
        cards = tarot.draw(5, flags[FLAGS["no_inversions"]["letter"]], flags[FLAGS["major_only"]["letter"]], flags[FLAGS["minor_only"]["letter"]])
        await self._handle(ctx, cards, ReadingType.FIVE, flags)

    @add_flags("text_only", "no_inversions", "major_only", "minor_only", "no_embed", "image_only")
    @flags.command(name="celtic", brief = "Celtic Cross spread",
                   description = flags_description)
    async def celticcross(self, ctx, **flags):
        """A ten-card Celtic Cross spread."""
        cards = tarot.draw(10, flags[FLAGS["no_inversions"]["letter"]], flags[FLAGS["major_only"]["letter"]], flags[FLAGS["minor_only"]["letter"]])
        await self._handle(ctx, cards, ReadingType.CELTIC, flags)

bot.add_cog(Tarot(bot))

bot.run(token)
