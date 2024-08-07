import discord
from common.tarot import SIMPLE_READINGS, ReadingType, DECKS, MajorMinor
from discordbot.handler import READING_DEFAULTS, handle
import shelve
import os

backup = os.path.join(os.path.dirname(__file__), "backup")


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
        for t in SIMPLE_READINGS:
            self.add_item(ReadingButton(t))


class DeckSelector(discord.ui.Select):
    def __init__(self, guildid: int | None, userid: str, userdata):
        options = [
            discord.SelectOption(
                label=deck.label,
                value=deck.shortname,
                description=deck.name,
                default=userdata["deck"] == deck.shortname,
            )
            for deck in DECKS.values()
            if deck.is_global or guildid in deck.guilds
        ]
        super().__init__(
            placeholder="Deck Type",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.userid = userid
        self.guildid = guildid

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        with shelve.open(backup, writeback=True) as store:
            if self.guildid is None:
                store["users"][self.userid]["deck"] = DECKS[
                    str(self.values[0])
                ].shortname
            else:
                store["guilds"][str(self.guildid)]["users"][self.userid]["deck"] = (
                    DECKS[str(self.values[0])].shortname
                )
        await interaction.followup.send(
            "New settings have been saved", ephemeral=True, delete_after=2.0
        )


class ReadingSelector(discord.ui.Select):
    def __init__(self, guildid: int | None, userid: str, userdata):
        options = [
            discord.SelectOption(
                label="Show Text",
                value="text",
                description="Show card names and descriptions",
                default=userdata["text"],
            ),
            discord.SelectOption(
                label="Show Descriptions",
                value="descriptions",
                description="Show card descriptions (requires Show Text)",
                default=userdata["descriptions"],
            ),
            discord.SelectOption(
                label="Show Images",
                value="image",
                description="Show card images",
                default=userdata["image"],
            ),
            discord.SelectOption(
                label="Use Embed",
                value="embed",
                description="Display the reading in a nice embed",
                default=userdata["embed"],
            ),
            discord.SelectOption(
                label="Allow Inversions",
                value="invert",
                description="Allow both upright and inverted cards",
                default=userdata["invert"],
            ),
            discord.SelectOption(
                label="Private Reading",
                value="private",
                description="Recieve the reading privately",
                default=userdata["private"],
            ),
        ]
        super().__init__(
            placeholder="Reading Settings",
            min_values=0,
            max_values=len(options),
            options=options,
        )
        self.userid = userid
        self.guildid = guildid

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        with shelve.open(backup, writeback=True) as store:
            if self.guildid is None:
                store["users"][self.userid]["text"] = "text" in self.values
                store["users"][self.userid]["descriptions"] = (
                    "descriptions" in self.values
                )
                store["users"][self.userid]["image"] = "image" in self.values
                store["users"][self.userid]["embed"] = "embed" in self.values
                store["users"][self.userid]["invert"] = "invert" in self.values
                store["users"][self.userid]["private"] = "private" in self.values
            else:
                store["guilds"][str(self.guildid)]["users"][self.userid]["text"] = (
                    "text" in self.values
                )
                store["guilds"][str(self.guildid)]["users"][self.userid][
                    "descriptions"
                ] = ("descriptions" in self.values)
                store["guilds"][str(self.guildid)]["users"][self.userid]["image"] = (
                    "image" in self.values
                )
                store["guilds"][str(self.guildid)]["users"][self.userid]["embed"] = (
                    "embed" in self.values
                )
                store["guilds"][str(self.guildid)]["users"][self.userid]["invert"] = (
                    "invert" in self.values
                )
                store["guilds"][str(self.guildid)]["users"][self.userid]["private"] = (
                    "private" in self.values
                )
        await interaction.followup.send(
            "New settings have been saved", ephemeral=True, delete_after=2.0
        )


class ArcanaSelector(discord.ui.Select):
    def __init__(self, guildid: int | None, userid: str, userdata):
        options = [
            discord.SelectOption(
                label="Major Only",
                value="major",
                description="Only include major arcana cards",
                default=userdata["majorminor"] == MajorMinor.MAJOR_ONLY,
            ),
            discord.SelectOption(
                label="Minor Only",
                value="minor",
                description="Only include minor arcana cards",
                default=userdata["majorminor"] == MajorMinor.MINOR_ONLY,
            ),
            discord.SelectOption(
                label="Both Major and Minor",
                value="both",
                description="Include both major and minor arcana cards",
                default=userdata["majorminor"] == MajorMinor.BOTH,
            ),
        ]
        super().__init__(
            placeholder="Major or Minor Arcana",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.userid = userid
        self.guildid = guildid

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        with shelve.open(backup, writeback=True) as store:
            if self.guildid is None:
                store["users"][self.userid]["majorminor"] = MajorMinor(self.values[0])
            else:
                store["guilds"][str(self.guildid)]["users"][self.userid][
                    "majorminor"
                ] = MajorMinor(self.values[0])
        await interaction.followup.send(
            "New settings have been saved", ephemeral=True, delete_after=2.0
        )


class SettingsView(discord.ui.View):
    def __init__(self, guildid: int | None, userid: str):
        super().__init__()
        with shelve.open(backup, writeback=True) as store:
            if guildid is not None:
                if str(guildid) not in store["guilds"]:
                    # store[guildid] = {"users": {}, "custom_decks": []}
                    store["guilds"][str(guildid)] = {"users": {}}
                if userid not in store["guilds"][str(guildid)]["users"]:
                    store["guilds"][str(guildid)]["users"][userid] = READING_DEFAULTS
                userdata = store["guilds"][str(guildid)]["users"][userid]
            else:
                if userid not in store["users"]:
                    store["users"][userid] = READING_DEFAULTS
                userdata = store["users"][userid]
            # guilddecks = store[guildid]["custom_decks"]
        self.add_item(ReadingSelector(guildid, userid, userdata))
        self.add_item(DeckSelector(guildid, userid, userdata))
        self.add_item(ArcanaSelector(guildid, userid, userdata))


class AboutView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                url="https://discord.gg/xagYSd84ZX",
                label="Discord Link",
            )
        )
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                url="https://ko-fi.com/witchofwonder",
                label="Donation Link",
            )
        )
