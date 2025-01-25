import discord
from io import BytesIO
from common import tarot, eightball, oblique_strategies
from common.tarot import Card, ReadingType, MajorMinor, Facing
import common.db as db
import os
from discord.ext.commands import Context
from discord.ext.pages import Page, Paginator
from typing import List, Tuple

color = discord.Colour(0x6B1BF8)


async def handle(
    interaction: discord.Interaction,
    read: ReadingType,
    targetUser: discord.Member | None = None,
):
    try:
        opts = get_opts(interaction)
        await interaction.response.defer(ephemeral=opts.private)
        messages, files, embeds = build_response(interaction, read, opts, targetUser)
        if len(messages) == 1:
            kwargs: dict = {"content": messages[0]}
            if len(files) > 0:
                kwargs["file"] = files[0]
            if len(embeds) > 0:
                kwargs["embed"] = embeds[0]
            await interaction.followup.send(**kwargs)
        elif opts.embed:
            pages: list[Page] = []
            for i in range(0, len(messages)):
                pages.append(
                    Page(
                        files=[files[i]] if len(files) > i else None,
                        embeds=[embeds[i]] if len(embeds) > i else None,
                    )
                )
            paginator = Paginator(pages=pages)
            await paginator.respond(interaction, ephemeral=opts.private)
        else:
            for i in range(0, len(messages)):
                if files[i]:
                    await interaction.followup.send(
                        content=messages[i], file=files[i], ephemeral=opts.private
                    )
                else:
                    await interaction.followup.send(
                        content=messages[i], ephemeral=opts.private
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
        read.numcards, opts.deck, opts.invert, MajorMinor(opts.majorminor)
    )

    MAX_COUNT = 25 if opts.embed else 24
    cards = (
        [cards[start : start + MAX_COUNT] for start in range(0, len(cards), MAX_COUNT)]
        if opts.text
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
    gid = str(interaction.guild_id)
    if interaction.user is None:
        raise Exception("No user found")
    uid = str(interaction.user.id)
    return db.get(uid, gid)


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

    if opts.image:
        im = tarot.cardimg(cards, read.imgfunc)
        with BytesIO() as buf:
            if opts.small_images:
                im = im.reduce(2)
            im.save(buf, "PNG", optimize=True)
            buf.seek(0)
            file = discord.File(fp=buf, filename=f"image_{count}.png")

    if opts.embed:
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

        if opts.text:
            for i, (n, v) in enumerate(response):
                embed.add_field(
                    name="{}) {}".format((count * MAX_COUNT) + i + 1, n),
                    value=v if opts.descriptions else "",
                    inline=False,
                )
        if opts.image:
            embed.set_image(url=f"attachment://image_{count}.png")
    else:
        if opts.text:
            for i, (n, v) in enumerate(response):
                message = (
                    message
                    + "\n**"
                    + str((count * MAX_COUNT) + i + 1)
                    + ") "
                    + n
                    + "**"
                    + ("\n\t" + v if opts.descriptions else "")
                )
    return message, file, embed


async def handle_8ball(
    interaction,
    other_user: discord.Member | None = None,
):
    try:
        opts = get_opts(interaction)
        await interaction.response.defer(ephemeral=opts.private)
        image, description = eightball.shake()
        message = (
            "<@{}>, here is your reading".format(
                interaction.user.id if other_user is None else other_user.id
            )
            + "\n"
        )
        file = None
        embed = None
        if opts.image:
            with BytesIO() as buf:
                image.save(buf, "PNG", optimize=True)
                buf.seek(0)
                file = discord.File(fp=buf, filename=f"8ball_image.png")

        if opts.embed:
            embed = discord.Embed(
                title="The 8-ball shakes for {}".format(
                    interaction.user.display_name
                    if other_user is None
                    else other_user.display_name
                ),
                type="rich",
                color=color,
            )

            if opts.text:
                embed.add_field(
                    name="{}".format(description),
                    value="",
                    inline=False,
                )
            if opts.image:
                embed.set_image(url=f"attachment://8ball_image.png")
        else:
            if opts.text:
                message = message + "\n**" + description
        kwargs: dict = {
            "content": message,
            "file": file,
            "embed": embed,
            "ephemeral": opts.private,
        }
        await interaction.followup.send(**kwargs)
    except Exception as e:
        print(e)
        await interaction.followup.send(
            "Error (if you're seeing this, please let us know!): " + str(e),
            ephemeral=True,
        )


async def handle_oblique(
    interaction,
    other_user: discord.Member | None = None,
):
    try:
        opts = get_opts(interaction)
        await interaction.response.defer(ephemeral=opts.private)
        strategy = oblique_strategies.oblique()
        message = (
            "<@{}>, here is your reading".format(
                interaction.user.id if other_user is None else other_user.id
            )
            + "\n"
        )
        embed = None
        if opts.embed:
            embed = discord.Embed(
                title="An Oblique Strategy for {}".format(
                    interaction.user.display_name
                    if other_user is None
                    else other_user.display_name
                ),
                type="rich",
                color=color,
            )
            embed.add_field(
                name="{}".format(strategy),
                value="",
                inline=False,
            )
        else:
            message = message + "\n" + strategy
        kwargs: dict = {
            "content": message,
            "embed": embed,
            "ephemeral": opts.private,
        }
        await interaction.followup.send(**kwargs)
    except Exception as e:
        print(e)
        await interaction.followup.send(
            "Error (if you're seeing this, please let us know!): " + str(e),
            ephemeral=True,
        )
