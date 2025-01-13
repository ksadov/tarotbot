from peewee import *
from common.tarot import MajorMinor

db = SqliteDatabase("settings.db")


class Settings(Model):
    userid = CharField()
    guildid = CharField(null=True)
    deck = CharField(default="rider-waite-smith")
    majorminor = CharField(
        default=MajorMinor.BOTH.value, choices=[(a.value, a.name) for a in MajorMinor]
    )
    text = BooleanField(default=True)
    descriptions = BooleanField(default=True)
    embed = BooleanField(default=True)
    image = BooleanField(default=True)
    private = BooleanField(default=False)
    invert = BooleanField(default=True)
    small_images = BooleanField(default=False)

    class Meta:
        database = db


def get(userid, guildid=None):
    with db:
        return Settings.get_or_create(userid=userid, guildid=guildid)[0]


def update(
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
    with db:
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
        dbobj.save()


def init():
    with db:
        db.create_tables([Settings])
