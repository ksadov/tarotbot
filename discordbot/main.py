# attempting to switch to pycord because interactions has annoyed me
from math import ceil
import os
from common import layouts
from common.tarot import ReadingType
from dotenv import load_dotenv
import discord
from discordbot.components import ReadingSelectorView, AboutView, SettingsView
from discordbot.handler import handle, handle_generic
import discordbot.makeBackupFile

# TODO update this
help_message = """For support or to request new features, join our discord server.
/tarot: start a reading
/tarotsettings: customize your readings
/tarothelp: view this help\n
"""

load_dotenv()
if os.getenv("TAROT_DEVELOPMENT") == "true":
    token = os.getenv('TEST_TOKEN')
    application_id = os.getenv('TEST_APPLICATION_ID')
    guild_ids = [357633267861553162, 410850945229127692]
else:
    token = os.getenv('DISCORD_TOKEN')
    application_id = os.getenv('DISCORD_APPLICATION_ID')
    guild_ids = None

bot = discord.AutoShardedBot(debug_guilds = guild_ids, activity=discord.Game("/tarot for a reading"))

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
    await ctx.respond("Customize your tarot readings", view=SettingsView(str(ctx.interaction.guild_id), str(ctx.interaction.user.id)), ephemeral=True)

@bot.slash_command(name="tarothelp",
             description="Learn about the tarot bot",
             guild_ids=guild_ids)
async def _about(ctx):
    await ctx.respond(help_message, view=AboutView(), ephemeral=True)
    
    
@bot.slash_command(name="pull",
             description="Pull cards from the deck",
             guild_ids=guild_ids)
@discord.option("numcards", description="Number of cards to draw", required=True)
async def _pull(ctx, numcards: int):
    for i in range(0, nummsg):
        try:
            await handle_generic(ctx, numcards, layouts.genericimg, False, "Pull")
        except Exception as e:
            await ctx.followup.send(e, ephemeral=True)

def addCommand(t):
    @bot.slash_command(name=t.id,
                 description=t.description,
                 guild_ids=guild_ids)
    async def _do_reading(ctx):
        await handle(ctx, t)

for t in ReadingType:
    addCommand(t)
    help_message += "/{}: {}\n".format(t.id, t.description)

def main():
    bot.run(token)

if __name__ == '__main__':
    main()
