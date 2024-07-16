import random
from PIL import Image
from typing import List, Dict
from enum import Enum, unique
from os import path, listdir
from . import layouts
from dataclasses import dataclass, field
import json
from glob import iglob
import copy


@dataclass
class ReadingType:
    """Class for representing a type of tarot reading"""

    fullname: str
    id: str
    numcards: int
    description: str
    imgfunc: layouts.imgfunc_type = field(repr=False, compare=False)


OneCardR = ReadingType(
    "One card", "1card", 1, "One card tarot reading", layouts.draw1img
)
ThreeCardR = ReadingType(
    "Three cards", "3card", 3, "Three card tarot reading", layouts.draw3img
)
FiveCardR = ReadingType(
    "Five cards", "5card", 5, "Five card tarot reading", layouts.draw5img
)
CelticR = ReadingType(
    "Celtic Cross", "celtic", 10, "Celtic cross tarot reading", layouts.celticimg
)


def NCardR(numCards):
    return ReadingType(
        "{} cards".format(numCards),
        "ncard",
        numCards,
        "{} card tarot reading".format(numCards),
        layouts.genericimg,
    )


SIMPLE_READINGS = [OneCardR, ThreeCardR, FiveCardR, CelticR]


class Card:
    """A class used to represent a tarot card.

    Attributes:
        name: The name of the card
        upright: Three-word description of a card's upright meaning
        reversed: Three-word description of a card's reversed meaning
        code: A short string representing the card's suit and rank
        major: True if card is major arcana, False if card is minor arcana
        up: True if a card is upright, False if inverted

    """

    def __init__(
        self,
        name: str,
        upright: str,
        reverse: str,
        image_path: str,
        major: bool,
        up=True,
    ):
        self.name = name
        self.upright = upright
        self.reverse = reverse
        self.image_path = image_path
        self.major = major
        self.up = up

    def description(self) -> str:
        """Returns the card name and its meaning, depending on its orientation.

        Example:
            King of Cups (upright): compassion, control, balance

        """
        if self.up:
            descr = self.name + " (upright): " + self.upright
        else:
            descr = self.name + " (reversed): " + self.reverse
        return descr

    def get_name(self) -> str:
        return "{} ({})".format(self.name, "upright" if self.up else "reversed")

    def get_desc(self) -> str:
        if self.up:
            return self.upright
        else:
            return self.reverse


@dataclass
class Deck:
    name: str
    shortname: str
    label: str
    is_global: bool
    cards: List[Card]
    guilds: List[str]


# TODO: remove after updating shelve store
@unique
class Decks(Enum):
    def __new__(cls, shortname, label, longname, global_d=True):
        obj = object.__new__(cls)
        obj._value_ = shortname
        obj.shortname = shortname
        obj.label = label
        obj.longname = longname
        if global_d:
            cls.global_decks = cls.__dict__.get("global_decks", [])
            cls.global_decks.append(obj)
        return obj

    DEFAULT = ("default", "Default", "Default cards")
    SWISS = ("swiss", "Swiss", "IJJ Swiss cards")
    PLANET_SCUM = ("planetscum", "Planet Scum", "Planet Scum Custom Cards", False)
    RIDER_WAITE_SMITH = (
        "rider-waite-smith",
        "Rider-Waite-Smith",
        "Rider-Waite-Smith cards",
    )


DECKS: Dict[str, Deck] = {}

for deckjson in iglob("decks/tarot/*/deck.json"):
    with open(deckjson, "r") as f:
        deck_data = json.load(f)
        new_cards = [
            Card(
                card["name"],
                card["upright_meaning"],
                card["reversed_meaning"],
                path.join(
                    path.dirname(__file__),
                    "..",
                    "decks",
                    "tarot",
                    deck_data["shortname"],
                    card["image"],
                ),
                card["type"] == "major",
            )
            for card in deck_data["cards"]
        ]
        new_deck = Deck(
            deck_data["name"],
            deck_data["shortname"],
            deck_data["label"],
            bool(deck_data["global"]),
            new_cards,
            deck_data["guilds"] or [],
        )
        DECKS[deck_data["shortname"]] = new_deck


@unique
class MajorMinor(Enum):
    MAJOR_ONLY = "major"
    MINOR_ONLY = "minor"
    BOTH = "both"


def make_deck(deck: Deck, majorminor: MajorMinor) -> List[int]:
    """Returns a full deck of tarot cards."""

    if majorminor == MajorMinor.MAJOR_ONLY:
        return [i for i, card in enumerate(deck.cards) if card.major]
    elif majorminor == MajorMinor.MINOR_ONLY:
        return [i for i, card in enumerate(deck.cards) if not card.major]
    else:
        return [i for i, _ in enumerate(deck.cards)]


def draw(
    n: int,
    chosenDeck: Deck = DECKS["rider-waite-smith"],
    invert=True,
    majorminor: MajorMinor = MajorMinor.BOTH,
) -> List[Card]:
    """Returns a list of n random cards from a full deck of cards.

    Args:
        n: the number of cards to draw
        chosenDeck: the specific deck to draw from
        invert: If True, cards have a 1/2 chance of being inverted.
                Otherwise, no cards will be inverted.
        major_only: If True, only major arcana cards will be drawn
        minor_only: If True, only minor arcana cards will be drawn

    """
    deck_indexes = make_deck(chosenDeck, majorminor)
    if n < 1 or n > len(deck_indexes):
        raise ValueError(f"Number of cards must be between 1 and {len(deck_indexes)}")

    hand = [copy.copy(chosenDeck.cards[i]) for i in random.sample(deck_indexes, n)]
    for card in hand:
        if not invert:
            card.up = True
        else:
            if random.choice([True, False]):
                card.up = True
            else:
                card.up = False

    return hand


def cardtxt(cards: List[Card]):
    """Returns a list of tuples containing descriptions of a list of cards."""
    return [(card.get_name(), card.get_desc()) for card in cards]


def makeImgList(cards: List[Card]):
    """Returns a list of Images corresponding to cards."""
    imgarray = []
    for c in cards:
        newcard = Image.open(c.image_path).convert("RGBA")
        if not c.up:
            newcardrev = newcard.rotate(180, expand=1)
            imgarray.append(newcardrev)
        else:
            imgarray.append(newcard)
    return imgarray


def cardimg(cardsO: List[Card], imgfunc: layouts.imgfunc_type) -> Image:
    """Returns an Image of the cards in cards0 in a spread specified by command.

    Args:
        cards0: the cards in the spread
        deck: the deck (set of card images) to use
        command: the spread. Valid spreads are 1card, 3card, 5card, celtic
    """
    cards = makeImgList(cardsO)
    cardwidth = max(map(lambda x: x.width, cards))
    cardheight = max(map(lambda x: x.height, cards))
    img = imgfunc(cards, cardwidth, cardheight)
    return img
