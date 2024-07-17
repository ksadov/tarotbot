# attempting to switch to pycord because interactions has annoyed me
import os
from common import layouts
from common.tarot import SIMPLE_READINGS, NCardR, ReadingType
from dotenv import load_dotenv
import discord
from discordbot.components import ReadingSelectorView, AboutView, SettingsView
from discordbot.handler import handle

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
    guild_ids = [int(id) for id in os.getenv("GUILD_IDS").split(",")]
    # guild_ids = None  # uncomment for testing user installs
else:
    token = os.getenv("DISCORD_TOKEN")
    application_id = os.getenv("DISCORD_APPLICATION_ID")
    guild_ids = None

bot = discord.AutoShardedBot(
    debug_guilds=guild_ids, activity=discord.Game("/tarot for a reading")
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
    await handle(ctx, NCardR(numcards))


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
        await handle(ctx, t)


for t in SIMPLE_READINGS:
    addCommand(t)
    help_message += "/{}: {}\n".format(t.id, t.description)
help_message += "/pull [n]: Draw [n] cards\n\n"


def main():
    bot.run(token)


if __name__ == "__main__":
    main()


# TODO: Add optional text input
# add setting to disable descriptions but keep card names
# info about tarot cards and meanings
# playing cards
# oracle cards
# make uploading large images faster
