import discord
from common.tarot import SIMPLE_READINGS, ReadingType, DECKS, MajorMinor
import common.db as db
from discordbot.handler import handle
import asyncio


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
    def __init__(self, dbuser):
        options = [
            discord.SelectOption(
                label=deck.label,
                value=deck.shortname,
                description=deck.name,
                default=dbuser.deck == deck.shortname,
            )
            for deck in DECKS.values()
            if deck.is_global or dbuser.guildid in deck.guilds
        ]
        super().__init__(
            placeholder="Deck Type",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.dbuser = dbuser

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await db.update(self.dbuser, deck=DECKS[str(self.values[0])].shortname)
        await interaction.followup.send(
            "New settings have been saved", ephemeral=True, delete_after=2.0
        )


class ReadingSelector(discord.ui.Select):
    def __init__(self, dbuser):
        options = [
            discord.SelectOption(
                label="Show Text",
                value="text",
                description="Show card names and descriptions",
                default=dbuser.text,
            ),
            discord.SelectOption(
                label="Show Descriptions",
                value="descriptions",
                description="Show card descriptions (requires Show Text)",
                default=dbuser.descriptions,
            ),
            discord.SelectOption(
                label="Show Images",
                value="image",
                description="Show card images",
                default=dbuser.image,
            ),
            discord.SelectOption(
                label="Use Embed",
                value="embed",
                description="Display the reading in a nice embed",
                default=dbuser.embed,
            ),
            discord.SelectOption(
                label="Allow Inversions",
                value="invert",
                description="Allow both upright and inverted cards",
                default=dbuser.invert,
            ),
            discord.SelectOption(
                label="Private Reading",
                value="private",
                description="Recieve the reading privately",
                default=dbuser.private,
            ),
            discord.SelectOption(
                label="Small File Size",
                value="small_images",
                description="Generate smaller images (save on bandwidth)",
                default=dbuser.small_images,
            ),
        ]
        super().__init__(
            placeholder="Reading Settings",
            min_values=0,
            max_values=len(options),
            options=options,
        )
        self.dbuser = dbuser

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await db.update(
            self.dbuser,
            text="text" in self.values,
            descriptions="descriptions" in self.values,
            image="image" in self.values,
            embed="embed" in self.values,
            invert="invert" in self.values,
            private="private" in self.values,
            small_images="small_images" in self.values,
        )
        await interaction.followup.send(
            "New settings have been saved", ephemeral=True, delete_after=2.0
        )


class ArcanaSelector(discord.ui.Select):
    def __init__(self, dbuser):
        options = [
            discord.SelectOption(
                label="Major Only",
                value="major",
                description="Only include major arcana cards",
                default=dbuser.majorminor == MajorMinor.MAJOR_ONLY.value,
            ),
            discord.SelectOption(
                label="Minor Only",
                value="minor",
                description="Only include minor arcana cards",
                default=dbuser.majorminor == MajorMinor.MINOR_ONLY.value,
            ),
            discord.SelectOption(
                label="Both Major and Minor",
                value="both",
                description="Include both major and minor arcana cards",
                default=dbuser.majorminor == MajorMinor.BOTH.value,
            ),
        ]
        super().__init__(
            placeholder="Major or Minor Arcana",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.dbuser = dbuser

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await db.update(self.dbuser, majorminor=MajorMinor(self.values[0]).value)
        await interaction.followup.send(
            "New settings have been saved", ephemeral=True, delete_after=2.0
        )


class SettingsView(discord.ui.View):
    def __init__(self, guildid: int | None, userid: str):
        super().__init__()

    @classmethod
    async def create(cls, guildid: int | None, userid: str):
        view = cls(guildid, userid)
        dbuser = await db.get(userid, str(guildid))
        view.add_item(ReadingSelector(dbuser))
        view.add_item(DeckSelector(dbuser))
        view.add_item(ArcanaSelector(dbuser))
        return view


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
