import shelve
import os

backup = os.path.join(os.path.dirname(__file__), "discordbot", "backup")
newbackup = os.path.join(os.path.dirname(__file__), "discordbot", "newbackup")


# add non-standard deck to the guilds
def addCustomDeck(guildid, deck):
    with shelve.open(backup, writeback=True) as store:
        if guildid not in store:
            store[guildid] = {"users": {}, "custom_decks": []}
        store[guildid]["custom_decks"].append(deck)


if __name__ == "__main__":
    with shelve.open(backup, "r") as store:
        with shelve.open(newbackup, writeback=True) as newstore:
            newstore["guilds"] = {}
            newstore["users"] = {}
            for guild in store:
                newdata = store[guild]
                del newdata["custom_decks"]
                for user in newdata["users"]:
                    if type(newdata["users"][user]["deck"]) != str:
                        newdata["users"][user]["deck"] = newdata["users"][user][
                            "deck"
                        ].shortname
                newstore["guilds"][guild] = newdata
    os.replace(newbackup, backup)


for user in f["users"]:
    if f["users"][user]["deck"] == "default":
        print("whoops")
        f["users"][user]["deck"] = "rider-waite-smith"
