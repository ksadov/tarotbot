import discord
from tarot import ReadingType, Decks
from handler import handle

class ReadingButton(discord.ui.Button):
    def __init__(self, reading_type: ReadingType):
        super().__init__(
            label=reading_type.fullname,
            style=discord.ButtonStyle.primary,
            custom_id=str(reading_type.id),
        )
        self.reading_type = reading_type

    async def callback(self, interaction: discord.Interaction):
        await handle(interaction, self.reading_type)

class ReadingSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for t in ReadingType:
            self.add_item(ReadingButton(t))


# def createOptions(prefix="", noinvert = False, nomajor = False, nominor = False, notext = False,
#                   noimage = False, noembed = False, private = False):
#     return ActionRow(components = [SelectMenu(
#         options=[# the options in your dropdown
#             SelectOption(label="No Text", value="text", description="Do not show card descriptions", default=notext),
#             SelectOption(label="No Images", value="image", description="Do not show card images", default=noimage),
#             SelectOption(label="No Embed", value="embed", description="Send unembedded message", default=noembed),
#             SelectOption(label="No Inversions", value="invert", description="Only draw upright cards", default=noinvert),
#             SelectOption(label="No Major Arcana", value="major", description="Only draw minor arcana cards", default=nomajor),
#             SelectOption(label="No Minor Arcana", value="minor", description="Only draw major arcana cards", default=nominor),
#             SelectOption(label="Private Reading", value="private", description="Send reading privately", default=private)
#         ],
#         placeholder="Reading Settings",  # the placeholder text to show when no options have been chosen
#         min_values=0,  # the minimum number of options a user must select
#         max_values=7,  # the maximum number of options a user can select
#         custom_id="_tarotoptions"
#     )])

# def createCardSelector(prefix="", selected=Decks.DEFAULT):
#     return ActionRow(
#         SelectMenu(
#             options=[
#                 create_select_option("Default", value="default", description="Default cards", default=(selected==Decks.DEFAULT)),
#                 create_select_option("Swiss", value="swiss", description="IJJ Swiss cards", default=(selected==Decks.SWISS))
#             ],
#             placeholder="Card Type",
#             min_values=1,
#             max_values=1,
#             custom_id=prefix+"_cardtype"
#         )
#     )
class AboutView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.link,
            url="https://discord.gg/xagYSd84ZX",
            label="Discord Link"
        ))
