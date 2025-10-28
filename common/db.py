import peewee
from peewee_aio import Manager, AIOModel, fields
from common.tarot import MajorMinor

# db = SqliteDatabase("settings.db")
db = Manager("aiosqlite:///settings.db")


@db.register
class Settings(AIOModel):
    userid = fields.CharField()
    guildid = fields.CharField(null=True)
    deck = fields.CharField(default="rider-waite-smith")
    majorminor = fields.CharField(
        default=MajorMinor.BOTH.value, choices=[(a.value, a.name) for a in MajorMinor]
    )
    text = fields.BooleanField(default=True)
    descriptions = fields.BooleanField(default=True)
    embed = fields.BooleanField(default=True)
    image = fields.BooleanField(default=True)
    private = fields.BooleanField(default=False)
    invert = fields.BooleanField(default=True)
    small_images = fields.BooleanField(default=False)


async def get(userid, guildid=None):
    async with db:
        async with db.connection():
            return (await Settings.get_or_create(userid=userid, guildid=guildid))[0]


async def update(
    dbobj,
    *,
    deck=None,
    majorminor=None,
    text=None,
    descriptions=None,
    embed=None,
    image=None,
    private=None,
    invert=None,
    small_images=None,
):
    async with db:
        async with db.connection():
            if deck is not None:
                dbobj.deck = deck
            if majorminor is not None:
                dbobj.majorminor = majorminor
            if text is not None:
                dbobj.text = text
            if descriptions is not None:
                dbobj.descriptions = descriptions
            if embed is not None:
                dbobj.embed = embed
            if image is not None:
                dbobj.image = image
            if private is not None:
                dbobj.private = private
            if invert is not None:
                dbobj.invert = invert
            if small_images is not None:
                dbobj.small_images = small_images
            await dbobj.save()


async def init():
    async with db:
        async with db.connection():
            await Settings.create_table()
