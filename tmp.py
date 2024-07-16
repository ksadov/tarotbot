from common import tarot
import json
majors = tarot.make_deck(tarot.MajorMinor.MAJOR_ONLY)
minors = tarot.make_deck(tarot.MajorMinor.MINOR_ONLY)

cards = []
for card in majors:
    cards.append({
            "image": '{}.jpg'.format(card.code),
            "name": card.name,
            "type": "major",
            "upright_meaning": card.upright,
            "reversed_meaning": card.reverse
        })
    
for card in minors:
    cards.append({
            "image": '{}.jpg'.format(card.code),
            "name": card.name,
            "type": "minor",
            "upright_meaning": card.upright,
            "reversed_meaning": card.reverse
        })

print(json.dumps(cards))
