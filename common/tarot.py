import random
from PIL import Image
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


@dataclass
class Card:
    """A class used to represent a tarot card."""

    name: str  # the name of the card
    upright: str  # comma-separated simple meanings for the upright form of the card
    reverse: str  # comma-separated simple meanings for the reversed form of the card
    code: str  # a short string representing the card's suit and rank
    image_path: str  # a string representing the path to the image
    major: bool  # True if the card is major arcana, False if the card is minor arcana


@unique
class DeckType(Enum):
    TAROT = "tarot"
    PLAYING_CARD = "playingcards"


@dataclass
class Deck:
    name: str  # the name of the deck
    type: DeckType
    shortname: (
        str  # a short name for the deck, and also the name of the folder the deck is in
    )
    label: str  # string to display when showing the name of the deck
    is_global: bool  # True if the deck applies to all guilds. False if the deck is only for certain guilds
    all_cards: list[Card]  # A list of the cards in the deck
    major_cards: list[Card]  # A list of only the major cards in the deck
    minor_cards: list[Card]  # A list of only the minor cards in the deck
    guilds: list[
        str
    ]  # A list of guilds ids the deck is allowed in, or [] if is_global is True


DECKS: dict[str, Deck] = {}


def init_decks():
    init_tarot()
    init_playing_cards()


def init_tarot():
    default_tarot_cards: dict[str, Card] = {}
    with open("decks/tarot/default.json", "r") as f:
        json_cards = json.load(f)
        for code, card in json_cards.items():
            default_tarot_cards[code] = Card(
                card["name"],
                card["upright_meaning"],
                card["reversed_meaning"],
                code,
                card["image"],
                card["type"] == "major",
            )

    for deckjson in iglob("decks/tarot/*/deck.json"):
        with open(deckjson, "r") as f:
            deck_data = json.load(f)
            new_cards = copy.deepcopy(default_tarot_cards)
            if "cards" in deck_data:
                # override default cards
                for code, card in deck_data["cards"].items():
                    new_cards[code] = Card(
                        card.get("name")
                        or default_tarot_cards[
                            code
                        ].name,  # only replace if fields are present (keep defaults otherwise)
                        card.get("upright_meaning")
                        or default_tarot_cards[code].upright,
                        card.get("reversed_meaning")
                        or default_tarot_cards[code].reverse,
                        code,
                        card.get("image") or default_tarot_cards[code].image_path,
                        (
                            card.get("type") == "major"
                            or default_tarot_cards[code].major
                        ),
                    )
            for card in new_cards.values():
                card.image_path = path.join(
                    path.dirname(path.abspath(__file__)),
                    "..",
                    "decks",
                    "tarot",
                    deck_data["shortname"],
                    card.image_path,
                )  # add the full path

            new_deck = Deck(
                deck_data["name"],
                DeckType.TAROT,
                deck_data["shortname"],
                deck_data["label"],
                bool(deck_data["global"]),
                list(new_cards.values()),
                list(card for card in new_cards.values() if card.major),
                list(card for card in new_cards.values() if not card.major),
                deck_data["guilds"] or [],
            )
            DECKS[deck_data["shortname"]] = new_deck


def init_playing_cards():
    default_playing_cards: dict[str, Card] = {}
    with open("decks/playingcards/default.json", "r") as f:
        json_cards = json.load(f)
        for code, card in json_cards.items():
            default_playing_cards[code] = Card(
                card["name"],
                card["meaning"],
                card["meaning"],  # playing cards don't have a reversed description
                code,
                card["image"],
                False,  # treat all playing cards as minor arcana
            )
    for deckjson in iglob("decks/playingcards/*/deck.json"):
        with open(deckjson, "r") as f:
            deck_data = json.load(f)
            new_cards = copy.deepcopy(default_playing_cards)
            if "cards" in deck_data:
                # override default cards
                for code, card in deck_data["cards"].items():
                    new_cards[code] = Card(
                        card.get("name")
                        or default_playing_cards[
                            code
                        ].name,  # only replace if fields are present (keep defaults otherwise)
                        card.get("meaning") or default_playing_cards[code].upright,
                        card.get("reversed_meaning")
                        or default_playing_cards[code].reverse,
                        code,
                        card.get("image") or default_playing_cards[code].image_path,
                        (
                            card.get("type") == "major"
                            or default_playing_cards[code].major
                        ),
                    )
            for card in new_cards.values():
                card.image_path = path.join(
                    path.dirname(path.abspath(__file__)),
                    "..",
                    "decks",
                    "playingcards",
                    deck_data["shortname"],
                    card.image_path,
                )  # add the full path

            new_deck = Deck(
                deck_data["name"],
                DeckType.PLAYING_CARD,
                deck_data["shortname"],
                deck_data["label"],
                bool(deck_data["global"]),
                list(new_cards.values()),
                [],  # playing card decks only have all cards
                [],  # playing card decks only have all cards
                deck_data["guilds"] or [],
            )
            DECKS[deck_data["shortname"]] = new_deck


@unique
class MajorMinor(Enum):
    MAJOR_ONLY = "major"
    MINOR_ONLY = "minor"
    BOTH = "both"


@unique
class Facing(Enum):
    UPRIGHT = "upright"
    REVERSED = "reversed"


def draw(
    n: int,
    chosenDeck: str,
    invert=True,
    majorminor: MajorMinor = MajorMinor.BOTH,
) -> list[tuple[Card, Facing]]:
    """Returns a list of n random cards from a full deck of cards, along with the direction the card is facing

    Args:
        n: the number of cards to draw
        chosenDeck: the specific deck to draw from
        invert: If True, cards have a 1/2 chance of being inverted.
                Otherwise, no cards will be inverted.
        major_only: If True, only major arcana cards will be drawn
        minor_only: If True, only minor arcana cards will be drawn

    """
    deck = DECKS[chosenDeck]
    cards = []
    if deck.type == DeckType.TAROT:
        if majorminor == MajorMinor.BOTH:
            cards = deck.all_cards
        elif majorminor == MajorMinor.MAJOR_ONLY:
            cards = deck.major_cards
        elif majorminor == MajorMinor.MINOR_ONLY:
            cards = deck.minor_cards
    elif deck.type == DeckType.PLAYING_CARD:
        cards = deck.all_cards
        invert = False  # don't invert playing cards

    if n < 1 or n > len(cards):
        raise ValueError(f"Number of cards must be between 1 and {len(cards)}")

    hand = random.sample(cards, n)

    return [
        (
            (card, Facing.UPRIGHT)
            if not invert
            else (card, random.choice((Facing.UPRIGHT, Facing.REVERSED)))
        )
        for card in hand
    ]


def cardtxt(cards: list[tuple[Card, Facing]]):
    """Returns a list of tuples containing descriptions of a list of cards."""
    return [
        (
            "{} ({})".format(card.name, facing.value),
            card.upright if facing == Facing.UPRIGHT else card.reverse,
        )
        for card, facing in cards
    ]


def makeImgList(cards: list[tuple[Card, Facing]]):
    """Returns a list of Images corresponding to cards."""
    imgarray = []
    for card, facing in cards:
        newcard = Image.open(card.image_path).convert("RGBA")
        if facing == Facing.REVERSED:
            newcard = newcard.rotate(180, expand=True)
        imgarray.append(newcard)
    return imgarray


def cardimg(
    cardsO: list[tuple[Card, Facing]], imgfunc: layouts.imgfunc_type
) -> Image.Image:
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
