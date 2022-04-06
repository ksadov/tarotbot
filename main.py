# attempting to switch to pycord because interactions has annoyed me
import os
from tarot import ReadingType
from dotenv import load_dotenv
import discord
from components import ReadingSelectorView, AboutView
from handler import handle

# TODO update this
help_message = """For support or to request new features, join our discord server.
/tarot: start a reading
/tarothelp: view this help
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

bot = discord.Bot(debug_guilds = guild_ids)

@bot.event
async def on_ready():
    bot.add_view(ReadingSelectorView())
    print("TarotBot is running")

@bot.slash_command(name="tarot",
             description="Start a Tarot reading",
             guild_ids=guild_ids)
async def _tarot(ctx):
    await ctx.respond("What type of reading would you like?", view=ReadingSelectorView(), ephemeral=True) #flags=64

@bot.slash_command(name="tarotsettings",
             description="Customize your tarot readings",
             guild_ids=guild_ids)
async def _tarotsettings(ctx):
    opts = READING_DEFAULTS
    if ctx.user.id in store:
        opts = store[ctx.user.id]
    await ctx.respond("Customize your tarot readings", components=settings_components(opts), ephemeral=True)

@bot.slash_command(name="tarothelp",
             description="Learn about the tarot bot",
             guild_ids=guild_ids)
async def _about(ctx):
    await ctx.respond(help_message, view=AboutView(), ephemeral=True)


def addCommand(t):
    @bot.slash_command(name=t.id,
                 description=t.description,
                 guild_ids=guild_ids)
    async def _do_reading(ctx):
        await handle(ctx.interaction, t)

for t in ReadingType:
    addCommand(t)
    help_message += "/{}: {}\n".format(t.id, t.description)

bot.run(token)

# store.close()
