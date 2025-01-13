import os
from common.tarot import (
    SIMPLE_READINGS,
    NCardR,
    ReadingType,
    OneCardR,
    ThreeCardR,
    init_decks,
)
from dotenv import load_dotenv
import discord
from discordbot.components import ReadingSelectorView, AboutView, SettingsView
from discordbot.handler import handle, handle_8ball
import common.db as db

# TODO update this
help_message = """For support or to request new features, join our discord server. Feedback welcome!\n
Available commands:\n
/tarot: start a reading
/tarotsettings: customize your readings
/tarothelp: view this help\n
"""

load_dotenv()
if os.getenv("TAROT_DEVELOPMENT") == "true":
    token = os.getenv("TEST_TOKEN")
    application_id = os.getenv("TEST_APPLICATION_ID")
    guild_ids = os.getenv("GUILD_IDS")
    if guild_ids is not None:
        guild_ids = [int(id) for id in guild_ids.split(",")]
    # guild_ids = None  # uncomment for testing user installs
else:
    token = os.getenv("DISCORD_TOKEN")
    application_id = os.getenv("DISCORD_APPLICATION_ID")
    guild_ids = None

bot = discord.AutoShardedBot(
    debug_guilds=guild_ids,
    activity=discord.Game("/tarot for a reading. /tarothelp to see all commands"),
)


@bot.event
async def on_ready():
    bot.add_view(ReadingSelectorView())
    print("TarotBot is running")


@bot.slash_command(
    name="tarot",
    description="Start a Tarot reading",
    guild_ids=guild_ids,
    integration_types=(
        {
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
        if guild_ids is None
        else None  # User install options don't work in testing context
    ),
)
async def _tarot(ctx: discord.ApplicationContext):
    await ctx.defer(ephemeral=True)
    await ctx.respond(
        "What type of reading would you like?",
        view=ReadingSelectorView(),
        ephemeral=True,
    )


# this shows up when right clicking a user
@bot.user_command(name="One Card Tarot Reading", guild_ids=guild_ids)
async def _tarot_user_1carrd(ctx: discord.ApplicationContext, member: discord.Member):
    await handle(ctx.interaction, OneCardR, member)


# this shows up when right clicking a user
@bot.user_command(name="Three Card Tarot Reading", guild_ids=guild_ids)
async def _tarot_user_3card(ctx: discord.ApplicationContext, member: discord.Member):
    await handle(ctx.interaction, ThreeCardR, member)


@bot.slash_command(
    name="tarotsettings",
    description="Customize your tarot readings",
    guild_ids=guild_ids,
    integration_types=(
        {
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
        if guild_ids is None
        else None
    ),
)
async def _tarotsettings(ctx: discord.ApplicationContext):
    if ctx.interaction.user is None:
        await ctx.respond(
            "Error. User is None. Please let us know if you see this message"
        )
        return
    await ctx.defer(ephemeral=True)
    await ctx.respond(
        "Customize your tarot readings",
        view=SettingsView(ctx.interaction.guild_id, str(ctx.interaction.user.id)),
        ephemeral=True,
    )


@bot.slash_command(
    name="tarothelp",
    description="Learn about the tarot bot",
    guild_ids=guild_ids,
    integration_types=(
        {
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
        if guild_ids is None
        else None
    ),
)
async def _about(ctx: discord.ApplicationContext):
    await ctx.defer(ephemeral=True)
    await ctx.respond(help_message, view=AboutView(), ephemeral=True)


@bot.slash_command(
    name="pull",
    description="Pull cards from the deck",
    guild_ids=guild_ids,
    integration_types=(
        {
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
        if guild_ids is None
        else None
    ),
)
@discord.option("numcards", description="Number of cards to draw", required=True)
async def _pull(ctx, numcards: int):
    await handle(ctx.interaction, NCardR(numcards))


# TODO: enable when 8ball images are in
# @bot.slash_command(
#     name="8ball",
#     description="Shake the magic 8 ball",
#     guild_ids=guild_ids,
#     integration_types=(
#         {
#             discord.IntegrationType.guild_install,
#             discord.IntegrationType.user_install,
#         }
#         if guild_ids is None
#         else None
#     ),
# )
# async def _shake(ctx):
#     await handle_8ball(ctx.interaction)


def addCommand(t: ReadingType):
    @bot.slash_command(
        name=t.id,
        description=t.description,
        guild_ids=guild_ids,
        integration_types=(
            {
                discord.IntegrationType.guild_install,
                discord.IntegrationType.user_install,
            }
            if guild_ids is None
            else None
        ),
    )
    async def _do_reading(ctx):
        await handle(ctx.interaction, t)


for t in SIMPLE_READINGS:
    addCommand(t)
    help_message += "/{}: {}\n".format(t.id, t.description)
help_message += "/pull [n]: Draw [n] cards\n\n"

help_message += "playing card meanings from https://pathandtarot.com/playing-card-meanings-for-cartomancy/\n\n"


def main():
    db.init()
    init_decks()
    bot.run(token)


if __name__ == "__main__":
    main()


# TODO:
# switch shelve to sql (port backup data)
# add pooling to sql
# info about tarot cards and meanings
# oracle cards
# add as right click option on messages (as the question)
