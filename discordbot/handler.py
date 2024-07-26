import discord
from io import BytesIO
from common import tarot
from common.tarot import Card, ReadingType, DECKS, MajorMinor, Facing
import shelve
import os
from discord.ext.commands import Context
from discord.ext.pages import Page, Paginator
from typing import List, Tuple


backup = os.path.join(os.path.dirname(__file__), "backup")
color = discord.Colour(0x6B1BF8)
READING_DEFAULTS = {
    "deck": "rider-waite-smith",
    "majorminor": MajorMinor.BOTH,
    "text": True,  # card names and descriptions
    "descriptions": True,  # only shown if text is also true
    "embed": True,
    "image": True,
    "private": False,
    "invert": True,
}


async def handle(
    interaction: discord.Interaction,
    read: ReadingType,
    targetUser: discord.Member | None = None,
):
    try:
        opts = get_opts(interaction)
        await interaction.response.defer(ephemeral=opts["private"])
        messages, files, embeds = build_response(interaction, read, opts, targetUser)
        if len(messages) == 1:
            kwargs: dict = {"content": messages[0]}
            if len(files) > 0:
                kwargs["file"] = files[0]
            if len(embeds) > 0:
                kwargs["embed"] = embeds[0]
            await interaction.followup.send(**kwargs)
        elif opts["embed"]:
            pages: list[Page] = []
            for i in range(0, len(messages)):
                pages.append(
                    Page(
                        files=[files[i]] if len(files) > i else None,
                        embeds=[embeds[i]] if len(embeds) > i else None,
                    )
                )
            paginator = Paginator(pages=pages)
            await paginator.respond(interaction, ephemeral=opts["private"])
        else:
            for i in range(0, len(messages)):
                if files[i]:
                    await interaction.followup.send(
                        content=messages[i], file=files[i], ephemeral=opts["private"]
                    )
                else:
                    await interaction.followup.send(
                        content=messages[i], ephemeral=opts["private"]
                    )
    except Exception as e:
        print(e)
        await interaction.followup.send(
            "Error (if you're seeing this, please let us know!): " + str(e),
            ephemeral=True,
        )


def build_response(
    interaction: discord.Interaction,
    read,
    opts,
    targetUser: discord.Member | None = None,
):
    cards = tarot.draw(
        read.numcards, DECKS[opts["deck"]], opts["invert"], opts["majorminor"]
    )

    MAX_COUNT = 25 if opts["embed"] else 24
    cards = (
        [cards[start : start + MAX_COUNT] for start in range(0, len(cards), MAX_COUNT)]
        if opts["text"]
        else [cards]
    )

    # outputs
    messages: list[str] = []
    files: list[discord.File] = []
    embeds: list[discord.Embed] = []

    for i in range(0, len(cards)):
        message, file, embed = message_and_files(
            cards[i], opts, interaction, read, i, len(cards), MAX_COUNT, targetUser
        )
        messages.append(message)
        if file:
            files.append(file)
        if embed:
            embeds.append(embed)

    return messages, files, embeds


def get_opts(interaction: discord.Interaction):
    opts = READING_DEFAULTS
    gid = str(interaction.guild_id)
    if interaction.user is None:
        raise Exception("No user found")
    uid = str(interaction.user.id)
    with shelve.open(backup, "r") as store:
        if (
            interaction.guild_id is not None
            and gid in store["guilds"]
            and uid in store["guilds"][gid]["users"]
        ):
            opts = store["guilds"][gid]["users"][uid]
        elif uid in store["users"]:
            opts = store["users"][uid]
    return opts


def message_and_files(
    cards: List[Tuple[Card, Facing]],
    opts,
    interaction,
    read,
    count,
    total,
    MAX_COUNT,
    other_user: discord.Member | None = None,
):
    response = tarot.cardtxt(cards)
    who = (
        "<@{}>, here is your reading".format(
            interaction.user.id if other_user is None else other_user.id
        )
        + (" (pg {}/{})".format(count + 1, total) if total > 1 else "")
        + "\n"
    )

    # outputs
    file = None
    message = who
    embed = None

    if opts["image"]:
        im = tarot.cardimg(cards, read.imgfunc)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename=f"image_{count}.png")

    if opts["embed"]:
        embed = discord.Embed(
            title="{} reading for {}".format(
                read.fullname,
                (
                    interaction.user.display_name
                    if other_user is None
                    else other_user.display_name
                ),
            ),
            type="rich",
            color=color,
        )

        if opts["text"]:
            for i, (n, v) in enumerate(response):
                embed.add_field(
                    name="{}) {}".format((count * MAX_COUNT) + i + 1, n),
                    value=v if opts["descriptions"] else "",
                    inline=False,
                )
        if opts["image"]:
            embed.set_image(url=f"attachment://image_{count}.png")
    else:
        if opts["text"]:
            for i, (n, v) in enumerate(response):
                message = (
                    message
                    + "\n**"
                    + str((count * MAX_COUNT) + i + 1)
                    + ") "
                    + n
                    + "**"
                    + ("\n\t" + v if opts["descriptions"] else "")
                )
    return message, file, embed
