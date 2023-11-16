import discord
from io import BytesIO
from common import tarot
from common.tarot import Card, ReadingType, Decks, MajorMinor
import shelve
import os
from discord.ext.commands import Context
from discord.ext.pages import Page, Paginator


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

async def handle(ctx: Context, read: ReadingType):
    try:
        opts = get_opts(ctx.interaction)
        interaction: discord.Interaction = ctx.interaction
        await ctx.defer(ephemeral=opts['private'])
        messages, files, embeds = build_response(ctx.interaction, read, opts)
        if len(messages) == 1:
            message = messages[0]
            file = files[0]
            embed = embeds[0]
            if file:
                await interaction.followup.send(content=message, file=file, embed=embed)
            else:
                await interaction.followup.send(content=message, embed=embed)
        elif opts['embed']:
            pages: list[Page] = []
            for i in range(0, len(messages)):
                if files[i]:
                    pages.append(Page(files=[files[i]], embeds=[embeds[i]]))
                else:
                    pages.append(Page(embeds=[embeds[i]]))
            paginator = Paginator(pages=pages)
            await paginator.respond(interaction, ephemeral=opts['private'])
        else:
            for i in range(0, len(messages)):
                if files[i]:
                    await interaction.followup.send(content=messages[i], file=files[i], ephemeral=opts['private'])
                else:
                    await interaction.followup.send(content=messages[i], ephemeral=opts['private'])
    except Exception as e:
        await interaction.followup.send("(if you're seeing this, please let us know!): " + str(e), ephemeral=True)


# needed for clicked componenets
async def handle_interaction(interaction, read: ReadingType):
    await interaction.response.defer()
    opts = get_opts(interaction)
    messages, files, embeds = build_response(interaction, read, opts)
    message = messages[0]
    file = files[0]
    embed = embeds[0]
    if file:
        await interaction.followup.send(content=message, file=file, embed=embed, ephemeral=opts['private'])
    else:
        await interaction.followup.send(content=message, embed=embed, ephemeral=opts['private'])

def build_response(interaction, read, opts):
    cards = tarot.draw(read.numcards, opts["invert"], opts["majorminor"])
    
    MAX_COUNT = 25 if opts["embed"] else 24
    cards = [cards[start:start + MAX_COUNT] for start in range(0,len(cards),MAX_COUNT)] if opts['text'] else [cards]

    # outputs
    messages: list[str] = []
    files: list[discord.File] = []
    embeds: list[discord.Embed] = []

    for i in range(0, len(cards)):
        message, file, embed = message_and_files(cards[i], opts, interaction, read, i, len(cards), MAX_COUNT)
        messages.append(message)
        files.append(file)
        embeds.append(embed)

    return messages, files, embeds

def get_opts(interaction):
    opts = READING_DEFAULTS
    gid = str(interaction.guild_id)
    uid = str(interaction.user.id)
    with shelve.open(backup, 'r') as store:
        if gid in store and uid in store[gid]["users"]:
            opts = store[gid]["users"][uid]
    return opts


def message_and_files(cards: list[Card], opts, interaction, read, count, total, MAX_COUNT):
    response = tarot.cardtxt(cards)
    who = (
        "<@{}>, here is your reading".format(interaction.user.id) 
           + (" (pg {}/{})".format(count+1, total) if total > 1 else "") 
           + "\n"
           )
    
    # outputs
    file = None
    message = who
    embed = None

    if opts["image"]:
        im = tarot.cardimg(cards, opts["deck"], read.imgfunc)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf,filename=f"image_{count}.png")
            

    if opts["embed"]:
        embed = discord.Embed(title="{} reading for {}".format(read.fullname, interaction.user.display_name),
                              type="rich",
                              color=color)

        if opts["text"]:
            for i, (n,v) in enumerate(response):
                    embed.add_field(name='{}) {}'.format((count * MAX_COUNT) + i+1,n), value=v, inline=False)
        if opts["image"]:
            embed.set_image(url=f"attachment://image_{count}.png")
    else:
        if opts["text"]:
            for i, (n,v) in enumerate(response):
                message = (message + "\n**" + str((count * MAX_COUNT) + i+1) + ") " +
                                n + "**\n" + v)
    return message, file, embed