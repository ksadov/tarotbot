import discord
from io import BytesIO
from common import tarot
from common.tarot import ReadingType, Decks, MajorMinor
import shelve
import os


backup = os.path.join(os.path.dirname(__file__), 'backup')
color = discord.Colour(0x6b1bf8)
READING_DEFAULTS = {
    "deck": Decks.DEFAULT,
    "majorminor": MajorMinor.BOTH,
    "text": True,
    "embed": True,
    "image": True,
    "private": True,
    "invert": True,
}

async def handle_generic(interaction: discord.Interaction, numcards, imgfunc, should_inline, reading_type_name):
    opts = READING_DEFAULTS
    gid = str(interaction.guild_id)
    uid = str(interaction.user.id)
    with shelve.open(backup, 'r') as store:
        if gid in store and uid in store[gid]["users"]:
            opts = store[gid]["users"][uid]
    cards = tarot.draw(numcards, opts["invert"], opts["majorminor"])
    response = tarot.cardtxt(cards)
    who = "<@{}>, here is your reading\n".format(interaction.user.id)
    file = None
    embed = None
    message = who
    if opts["image"]:
        im = tarot.cardimg(cards, opts["deck"], imgfunc)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf,filename="image.png")

    if opts["embed"]:
        embed = discord.Embed(title="{} reading for {}".format(reading_type_name, interaction.user.display_name),
                              type="rich",
                              color=color)

        if opts["text"]:
            for i, (n,v) in enumerate(response):
                embed.add_field(name='{}) {}'.format(i+1,n), value=v,
                                    inline=should_inline)
        if opts["image"]:
            embed.set_image(url="attachment://image.png")
    else:
        if opts["text"]:
            for i, (n,v) in enumerate(response):
                message = (message + "\n**" + str(i+1) + ") " +
                                n + "**\n" + v)
    await interaction.response.send_message(content=message, file=file, embed=embed, ephemeral=opts["private"])

async def handle(interaction: discord.Interaction, reading_type: ReadingType):
    await handle_generic(interaction, 
                         reading_type.num, 
                         reading_type.imgfunc, 
                         reading_type in [ReadingType.ONE, ReadingType.THREE], 
                         reading_type.fullname)
