from dotenv import load_dotenv
import discord
import os

load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print("bot is running")
    print(len(bot.guilds))

bot.run(os.getenv('DISCORD_TOKEN'))