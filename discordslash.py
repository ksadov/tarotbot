import os
import tarot
from tarot import ReadingType, Decks
import discord
from dotenv import load_dotenv
from io import BytesIO
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option
from discord_slash.model import ButtonStyle

DEV_BUILD = False

load_dotenv()

if DEV_BUILD:
    token = os.getenv('TEST_TOKEN')
    application_id = os.getenv('TEST_APPLICATION_ID')
    guild_ids = [357633267861553162, 410850945229127692]
else:
    token = os.getenv('DISCORD_TOKEN')
    application_id = os.getenv('DISCORD_APPLICATION_ID')
    guild_ids = None

client = discord.Client(activity=discord.Game("switching to slash commands"))
slash = SlashCommand(client, sync_commands=True)

# uncomment to enable global commands


def createButtons(prefix=""):
    return create_actionrow(
        create_button(
            style=ButtonStyle.blurple,
            label="1 card",
            custom_id=prefix+"_1card"
        ),
        create_button(
            style=ButtonStyle.blurple,
            label="3 card",
            custom_id=prefix+"_3card"
        ),
        create_button(
            style=ButtonStyle.blurple,
            label="5 card",
            custom_id=prefix+"_5card"
        ),
        create_button(
            style=ButtonStyle.blurple,
            label="Celtic Cross",
            custom_id=prefix+"_celticcross"
        )
    )

def createOptions(prefix="", noinvert = False, nomajor = False, nominor = False, notext = False,
                  noimage = False, noembed = False, private = False):
    return create_actionrow(create_select(
        options=[# the options in your dropdown
            create_select_option("No Text", value="text", description="Do not show card descriptions", default=notext),
            create_select_option("No Images", value="image", description="Do not show card images", default=noimage),
            create_select_option("No Embed", value="embed", description="Send unembedded message", default=noembed),
            create_select_option("No Inversions", value="invert", description="Only draw upright cards", default=noinvert),
            create_select_option("No Major Arcana", value="major", description="Only draw minor arcana cards", default=nomajor),
            create_select_option("No Minor Arcana", value="minor", description="Only draw major arcana cards", default=nominor),
            create_select_option("Private Reading", value="private", description="Send reading privately", default=private)
        ],
        placeholder="Reading Settings",  # the placeholder text to show when no options have been chosen
        min_values=0,  # the minimum number of options a user must select
        max_values=7,  # the maximum number of options a user can select
        custom_id="_tarotoptions"
    ))

def createCardSelector(prefix="", selected=Decks.DEFAULT):
    return create_actionrow(
        create_select(
            options=[
                create_select_option("Default", value="default", description="Default cards", default=(selected==Decks.DEFAULT)),
                create_select_option("Swiss", value="swiss", description="IJJ Swiss cards", default=(selected==Decks.SWISS))
            ],
            placeholder="Card Type",
            min_values=1,
            max_values=1,
            custom_id=prefix+"_cardtype"
        )
    )

deckMap = {Decks.DEFAULT: "", Decks.SWISS:"_*s*"}

def createComponents(noinvert = False, nomajor = False, nominor = False, notext = False,
                  noimage = False, noembed = False, private = False, deck=Decks.DEFAULT):
    prefix = ""
    prefix += "_i" if noinvert else ""
    prefix += "_M" if nomajor else ""
    prefix += "_m" if nominor else ""
    prefix += "_t" if notext else ""
    prefix += "_im" if noimage else ""
    prefix += "_e" if noembed else ""
    prefix += "_p" if private else ""
    prefix += deckMap[deck]
    b = createButtons(prefix)
    c = createCardSelector(prefix, deck)
    o = createOptions(prefix, noinvert, nomajor, nominor, notext, noimage, noembed, private)
    return [o,c,b]

default_components = createComponents()
about_components = [create_actionrow(
    create_button(
        style=ButtonStyle.URL,
        url="https://discord.com/api/oauth2/authorize?client_id=659747523354689549&scope=applications.commands",
        label="Add to server"
    ),
    create_button(
        style=ButtonStyle.URL,
        url="https://discord.gg/xagYSd84ZX",
        label="Discord Link"
    )
)]
color = discord.Color.purple()
async def _handle(ctx, cards, deck, type, notext, noimage, noembed, private):
    response = tarot.cardtxt(cards)
    who = "Reading for " + ctx.author.mention + "\n"
    if not noimage:
        im = tarot.cardimg(cards, deck, type)
        with BytesIO() as buf:
            im.save(buf, "PNG")
            buf.seek(0)
            file = discord.File(fp=buf,filename="image.png")
    if not noembed:
        embed = discord.Embed(title=type.value + " reading for " +ctx.author.display_name, type="rich",
                              color=color)

        if not notext:
            should_inline = type in [ReadingType.ONE, ReadingType.THREE]
            for i, (n,v) in enumerate(response):
                embed.add_field(name='{}) {}'.format(i+1,n), value=v,
                                inline=should_inline)
        if not noimage:
            embed.set_image(url="attachment://image.png")
            await ctx.send(file=file, embed=embed, hidden=private)
        else:
            await ctx.send(embed=embed, hidden=private)
    else:
        responsetext = ""
        for i, (n,v) in enumerate(response):
            responsetext = (responsetext + "\n**" + str(i+1) + ") " +
                            n + "**\n" + v)
        if not noimage and not notext:
            await ctx.send(who + responsetext, file=file, hidden=private)
        elif not notext:
            await ctx.send(who + responsetext, hidden=private)
        elif not noimage:
            await ctx.send(who, file=file, hidden=private)

@client.event
async def on_ready():
    print("Ready!")

#TEMPORARY HELP. REMOVE THIS
#if recieves message that starts with t!help
#send help message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('t!help'):
        await message.channel.send('This bot is switching to slash commands. if /tarot does not work, please re-add the bot:', components=about_components)



@slash.slash(name="tarot",
             description="Start a Tarot reading",
             guild_ids=guild_ids)
async def _tarot(ctx):
    await ctx.send("What type of reading would you like?", components=default_components, hidden=True) #flags=64

@slash.slash(name="tarothelp",
             description="Learn about the tarot bot",
             guild_ids=guild_ids)
async def _about(ctx):
    await ctx.send("For support or to request new features, join our discord server.", components=about_components, hidden=True)

# @slash.component_callback()
# async def _tarotoptions(ctx):
#     await ctx.send("not implemented")
    #TODO: check compatibility of options

@client.event
async def on_component(ctx):
    noinvert = "_i_" in ctx.custom_id
    nomajor = "_M_" in ctx.custom_id
    nominor = "_m_" in ctx.custom_id
    notext = "_t_" in ctx.custom_id
    noimage= "_im_" in ctx.custom_id
    noembed = "_e_" in ctx.custom_id
    private = "_p_" in ctx.custom_id
    deck = Decks.DEFAULT
    if "*s*" in ctx.custom_id:
        deck = Decks.SWISS

    if "_tarotoptions" in ctx.custom_id:
        noinvert = "invert" in ctx.selected_options
        nomajor = "major" in ctx.selected_options
        nominor = "minor" in ctx.selected_options
        notext = "text" in ctx.selected_options
        noimage = "image" in ctx.selected_options
        noembed = "embed" in ctx.selected_options
        private = "private" in ctx.selected_options
        if nomajor and nominor:
            pass
        if notext and noimage:
            pass
        await ctx.edit_origin(components = createComponents(noinvert,nomajor,nominor,notext,noimage,noembed,private,deck))
    elif "_cardtype" in ctx.custom_id:
        if "swiss" in ctx.selected_options:
            deck = Decks.SWISS
        else:
            deck = Decks.DEFAULT
        await ctx.edit_origin(components = createComponents(noinvert,nomajor,nominor,notext,noimage,noembed,private,deck))
    else:
        numCards = 0
        readingType = None
        if "_1card" in ctx.custom_id:
            numCards = 1
            readingType = ReadingType.ONE
        elif "_3card" in ctx.custom_id:
            numCards = 3
            readingType = ReadingType.THREE
        elif "_5card" in ctx.custom_id:
            numCards = 5
            readingType = ReadingType.FIVE
        elif "_celticcross" in ctx.custom_id:
            numCards = 10
            readingType = ReadingType.CELTIC
        else:
            #TODO: error
            pass
        cards = tarot.draw(numCards, not noinvert, nominor, nomajor)
        await _handle(ctx, cards, deck, readingType, notext, noimage, noembed, private)


client.run(token)

## TODO:
# check compatibility of options
# help command with guide for celtic cross
# delete component message and give error if invalid request sent
