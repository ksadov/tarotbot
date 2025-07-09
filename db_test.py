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


if __name__ == "__main__":
    with db:
        print(Settings.select().where(Settings.embed == False).count())
