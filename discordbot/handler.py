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

async def handle(ctx, read: ReadingType):
    await ctx.defer()
    message, file, embed, ephemeral = build_response(ctx.interaction, read)
    await ctx.followup.send(content=message, file=file, embed=embed, ephemeral=ephemeral)

# needed for clicked componenets
async def handle_interaction(interaction, read: ReadingType):
    message, file, embed, ephemeral = build_response(interaction, read)
    await interaction.response.send_message(content=message, file=file, embed=embed, ephemeral=ephemeral)

def build_response(interaction, read):
    opts = READING_DEFAULTS
    gid = str(interaction.guild_id)
    uid = str(interaction.user.id)
    with shelve.open(backup, 'r') as store:
        if gid in store and uid in store[gid]["users"]:
            opts = store[gid]["users"][uid]
    cards = tarot.draw(read.numcards, opts["invert"], opts["majorminor"])
    response = tarot.cardtxt(cards)
    who = "<@{}>, here is your reading\n".format(interaction.user.id)
    file = None
    embed = None
    message = who
    if opts["image"]:
        im = tarot.cardimg(cards, opts["deck"], read.imgfunc)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf,filename="image.png")

    if opts["embed"]:
        embed = discord.Embed(title="{} reading for {}".format(read.fullname, interaction.user.display_name),
                              type="rich",
                              color=color)

        if opts["text"]:
            if read.numcards > 25:
                msg = ""
                for i, (n,v) in enumerate(response):
                    msg += f"{i + 1}) " + n + "\n"
                embed.description = msg
            else:
                for i, (n,v) in enumerate(response):
                    embed.add_field(name='{}) {}'.format(i+1,n), value=v, inline=False)
        if opts["image"]:
            embed.set_image(url="attachment://image.png")
    else:
        if opts["text"]:
            for i, (n,v) in enumerate(response):
                message = (message + "\n**" + str(i+1) + ") " +
                                n + "**\n" + v)
    return message, file, embed, opts["private"]