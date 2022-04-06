import interactions
from interactions import Embed, EmbedField, EmbedImageStruct, Attachment
import os
import tarot
from tarot import ReadingType, Decks
from dotenv import load_dotenv
from io import BytesIO
from components import createComponents, default_components, about_components, settings_components, start_reading_components
# import shelve
import pysos

# store = shelve.open('backup')
store = pysos.Dict('backup')

# TODO update this
help_message = """For support or to request new features, join our discord server.
/tarot: start a reading
/tarothelp: view this help
/1card: one card reading
/3card: three card reading
/5card: five card reading
/celtic: celtic cross reading
"""

load_dotenv()
if os.getenv("TAROT_DEVELOPMENT"):
    token = os.getenv('TEST_TOKEN')
    application_id = os.getenv('TEST_APPLICATION_ID')
    guild_ids = [357633267861553162, 410850945229127692]
else:
    token = os.getenv('DISCORD_TOKEN')
    application_id = os.getenv('DISCORD_APPLICATION_ID')
    guild_ids = None

bot = interactions.Client(token=token, disable_sync=True)
# bot.load("interactions.ext.enhanced")

@bot.event
async def on_ready():
    print("TarotBot is running")

@bot.command(name="tarot",
             description="Start a Tarot reading",
             scope=guild_ids)
async def _tarot(ctx):
    await ctx.send("What type of reading would you like?", components=default_components, ephemeral=True) #flags=64

@bot.command(name="tarotsettings",
             description="Customize your tarot readings",
             scope=guild_ids)
async def _tarotsettings(ctx):
    opts = READING_DEFAULTS
    if ctx.user.id in store:
        opts = store[ctx.user.id]
    await ctx.send("Customize your tarot readings", components=settings_components(opts), ephemeral=True)

@bot.command(name="tarothelp",
             description="Learn about the tarot bot",
             scope=guild_ids)
async def _about(ctx):
    await ctx.send(help_message, components=about_components, ephemeral=True)

@bot.command(name="1card",
             description="One card tarot reading",
             scope=guild_ids)
async def _1card(ctx):
    await _handle(ctx, ReadingType.ONE)

@bot.command(name="3card",
             description="Three card tarot reading",
             scope=guild_ids)
async def _3card(ctx):
    await _handle(ctx, ReadingType.THREE)

@bot.command(name="5card",
             description="Five card tarot reading",
             scope=guild_ids)
async def _5card(ctx):
    await _handle(ctx, ReadingType.FIVE)

@bot.command(name="celtic",
             description="Celtic cross card tarot reading",
             scope=guild_ids)
async def _5card(ctx):
    await _handle(ctx, ReadingType.CELTIC)

color = 0x6b1bf8
READING_DEFAULTS = {
    "deck": Decks.DEFAULT,
    "notext": False,
    "noembed": False,
    "noimage": True,
    "private": False,
    "noinvert": False,
    "nomajor": False,
    "nominor": False
}

async def _handle(ctx, type):
    opts = READING_DEFAULTS
    if ctx.author.user.id in store:
        opts = store[ctx.author.user.id]
    cards = tarot.draw(type.num, not opts["noinvert"], opts["nominor"], opts["nomajor"])
    response = tarot.cardtxt(cards)
    who = "<@{}>, here is your reading\n".format(ctx.author.user.id)
    file = None
    embed = None
    message = who
    if not opts["noimage"]:
        im = tarot.cardimg(cards, opts["deck"], type)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            #TODO
            file = interactions.File(fp=buf,filename="image.png")

    if not opts["noembed"]:
        embed = Embed(title="{} reading for {}".format(type.fullname, ctx.author.nick), type="rich",
                              color=color)

        if not opts["notext"]:
            should_inline = type in [ReadingType.ONE, ReadingType.THREE]
            embed.fields = []
            for i, (n,v) in enumerate(response):
                embed.fields.append(EmbedField(name='{}) {}'.format(i+1,n), value=v,
                                    inline=should_inline))
        if not opts["noimage"]:
            embed.image = EmbedImageStruct(url="attachment://image.png")
    else:
        if not opts["notext"]:
            for i, (n,v) in enumerate(response):
                message = (message + "\n**" + str(i+1) + ") " +
                                n + "**\n" + v)

    await ctx.send(content=message, file=file, embeds=embed, ephemeral=opts["private"])

@bot.event
async def on_component(ctx):
    print(ctx);
# @bot.component(button)
# async def button_response(ctx):
#     print("someone clicked the button! :O")

bot.start()

# store.close()
