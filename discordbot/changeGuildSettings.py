import shelve
from common.tarot import Decks

# add non-standard deck to the guilds
def addCustomDeck(guildid, deck):
    with shelve.open("backup", writeback=True) as store:
        if guildid not in store:
            store[guildid] = {"users": {}, "custom_decks": []}
        store[guildid]["custom_decks"].append(deck)


#put custom deck into 605900319922061342
if __name__ == "__main__":
    addCustomDeck("605900319922061342", Decks.PLANET_SCUM)
    # test servers. remove these later
    addCustomDeck("357633267861553162", Decks.PLANET_SCUM)
    addCustomDeck("410850945229127692", Decks.PLANET_SCUM)
