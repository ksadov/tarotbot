import shelve
import os
import common.db as db

backup = os.path.join(os.path.dirname(__file__), "discordbot", "backup2")

db.init()

with shelve.open(backup, "r") as f:
    with db.db.atomic():
        for user in f["users"]:
            u = f["users"][user]
            new = db.Settings(
                userid=user,
                guildid=None,
                deck=u["deck"],
                majorminor=u["majorminor"].value,
                text=u["text"],
                descriptions=u["descriptions"],
                embed=u["embed"],
                image=u["image"],
                private=u["private"],
                invert=u["invert"],
                small_images=False,
            )
            new.save()
        for guild in f["guilds"]:
            for user in f["guilds"][guild]["users"]:
                u = f["guilds"][guild]["users"][user]
                new = db.Settings(
                    userid=user,
                    guildid=guild,
                    deck=u["deck"],
                    majorminor=u["majorminor"].value,
                    text=u["text"],
                    descriptions=u["descriptions"],
                    embed=u["embed"],
                    image=u["image"],
                    private=u["private"],
                    invert=u["invert"],
                    small_images=False,
                )
                new.save()
