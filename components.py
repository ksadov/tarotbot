import discord
from tarot import ReadingType, Decks, MajorMinor
from handler import handle, READING_DEFAULTS
import shelve

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

class DeckSelector(discord.ui.Select):
    def __init__(self, guildid: str, userid: str, userdata, guilddecks):
        options = [
            discord.SelectOption(
                label=deck.label,
                value=deck.shortname,
                description=deck.longname,
                default=userdata["deck"] == deck
            ) for deck in guilddecks
        ]
        super().__init__(
            placeholder = "Deck Type",
            min_values = 1,
            max_values = 1,
            options = options,
        )
        self.userid = userid
        self.guildid = guildid

    async def callback(self, interaction: discord.Interaction):
        with shelve.open("backup", writeback=True) as store:
            store[self.guildid]["users"][self.userid]["deck"] = Decks(self.values[0])
        await interaction.response.send_message("New settings have been saved", ephemeral=True, delete_after=2.0)

class ReadingSelector(discord.ui.Select):
    def __init__(self, guildid: str, userid: str, userdata):
        options = [
            discord.SelectOption(
                label="Show Text",
                value="text",
                description="Show card descriptions",
                default=userdata["text"]
            ),
            discord.SelectOption(
                label="Show Images",
                value="images",
                description="Show card images",
                default=userdata["image"]
            ),
            discord.SelectOption(
                label="Use Embed",
                value="embed",
                description="Display the reading in a nice embed",
                default=userdata["embed"]
            ),
            discord.SelectOption(
                label="Allow Inversions",
                value="invert",
                description="Allow both upright and inverted cards",
                default=userdata["invert"]
            ),
            discord.SelectOption(
                label="Private Reading",
                value="private",
                description="Recieve the reading privately",
                default=userdata["private"]
            )
        ]
        super().__init__(
            placeholder = "Reading Settings",
            min_values = 0,
            max_values = len(options),
            options = options,
        )
        self.userid = userid
        self.guildid = guildid

    async def callback(self, interaction: discord.Interaction):
        with shelve.open("backup", writeback=True) as store:
            store[self.guildid]["users"][self.userid]["text"] = "text" in self.values
            store[self.guildid]["users"][self.userid]["images"] = "images" in self.values
            store[self.guildid]["users"][self.userid]["embed"] = "embed" in self.values
            store[self.guildid]["users"][self.userid]["invert"] = "invert" in self.values
            store[self.guildid]["users"][self.userid]["private"] = "private" in self.values
        await interaction.response.send_message("New settings have been saved", ephemeral=True, delete_after=2.0)


class ArcanaSelector(discord.ui.Select):
    def __init__(self, guildid: str, userid: str, userdata):
        options = [
            discord.SelectOption(
                label="Major Only",
                value="major",
                description="Only include major arcana cards",
                default=userdata["majorminor"] == MajorMinor.MAJOR_ONLY
            ),
            discord.SelectOption(
                label="Minor Only",
                value="minor",
                description="Only include minor arcana cards",
                default=userdata["majorminor"] == MajorMinor.MINOR_ONLY
            ),
            discord.SelectOption(
                label="Both Major and Minor",
                value="both",
                description="Include both major and minor arcana cards",
                default=userdata["majorminor"] == MajorMinor.BOTH
            )
        ]
        super().__init__(
            placeholder = "Major or Minor Arcana",
            min_values = 1,
            max_values = 1,
            options = options,
        )
        self.userid = userid
        self.guildid = guildid

    async def callback(self, interaction: discord.Interaction):
        with shelve.open("backup", writeback=True) as store:
            store[self.guildid]["users"][self.userid]["majorminor"] = MajorMinor(self.values[0])
        await interaction.response.send_message("New settings have been saved", ephemeral=True, delete_after=2.0)

class SettingsView(discord.ui.View):
    def __init__(self, guildid: str, userid: str):
        super().__init__()
        with shelve.open("backup", writeback=True) as store:
            if guildid not in store:
                store[guildid] = {"users": {}, "decks": Decks.global_decks()}
            if userid not in store[guildid]["users"]:
                store[guildid]["users"][userid] = READING_DEFAULTS
            userdata = store[guildid]["users"][userid]
            guilddecks = store[guildid]["decks"]
        self.add_item(ReadingSelector(guildid, userid, userdata))
        self.add_item(DeckSelector(guildid, userid, userdata, guilddecks))
        self.add_item(ArcanaSelector(guildid, userid, userdata))


class AboutView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.link,
            url="https://discord.gg/xagYSd84ZX",
            label="Discord Link"
        ))
