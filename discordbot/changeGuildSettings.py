import shelve
from common.tarot import DECKS
import os

backup = os.path.join(os.path.dirname(__file__), 'backup')

# add non-standard deck to the guilds
def addCustomDeck(guildid, deck):
    with shelve.open(backup, writeback=True) as store:
        if guildid not in store:
            store[guildid] = {"users": {}, "custom_decks": []}
        store[guildid]["custom_decks"].append(deck)


#put custom deck into 605900319922061342
if __name__ == "__main__":
    addCustomDeck("605900319922061342", DECKS.PLANET_SCUM)
    # test servers. remove these later
    addCustomDeck("357633267861553162", DECKS.PLANET_SCUM)
    addCustomDeck("410850945229127692", DECKS.PLANET_SCUM)
