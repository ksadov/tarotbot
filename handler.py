import discord
from io import BytesIO
import tarot
from tarot import ReadingType, Decks
import pysos

# store = shelve.open('backup')
store = pysos.Dict('backup')

color = discord.Colour(0x6b1bf8)
READING_DEFAULTS = {
    "deck": Decks.DEFAULT,
    "notext": False,
    "noembed": False,
    "noimage": False,
    "private": False,
    "noinvert": False,
    "nomajor": False,
    "nominor": False
}

async def handle(interaction: discord.Interaction, reading_type: ReadingType):
    opts = READING_DEFAULTS
    if interaction.user.id in store:
        opts = store[interaction.user.id]
    cards = tarot.draw(reading_type.num, not opts["noinvert"], opts["nominor"], opts["nomajor"])
    response = tarot.cardtxt(cards)
    who = "<@{}>, here is your reading\n".format(interaction.user.id)
    file = None
    embed = None
    message = who
    if not opts["noimage"]:
        im = tarot.cardimg(cards, opts["deck"], reading_type)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            #TODO
            file = discord.File(fp=buf,filename="image.png")

    if not opts["noembed"]:
        embed = discord.Embed(title="{} reading for {}".format(reading_type.fullname, interaction.user.display_name),
                              type="rich",
                              color=color)

        if not opts["notext"]:
            should_inline = reading_type in [ReadingType.ONE, ReadingType.THREE]
            for i, (n,v) in enumerate(response):
                embed.add_field(name='{}) {}'.format(i+1,n), value=v,
                                    inline=should_inline)
        if not opts["noimage"]:
            embed.set_image(url="attachment://image.png")
    else:
        if not opts["notext"]:
            for i, (n,v) in enumerate(response):
                message = (message + "\n**" + str(i+1) + ") " +
                                n + "**\n" + v)
    await interaction.response.send_message(content=message, file=file, embed=embed, ephemeral=opts["private"])
