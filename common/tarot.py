import random
from PIL import Image
from typing import List
from enum import Enum, unique
from os import path
from . import layouts

class ReadingType():
     def __init__(self, fullname: str, id: str, numcards: int, description: str, imgfunc):
        self.fullname = fullname
        self.id = id
        self.num = numcards
        self.description = description
        self.imgfunc = imgfunc

class OneCardR(ReadingType):
     def __init__(self):
          super().__init__("One card", "1card", 1, "One card tarot reading", layouts.draw1img)

class ThreeCardR(ReadingType):
     def __init__(self):
          super().__init__("Three cards", "3card", 3, "Three card tarot reading", layouts.draw3img)

class FiveCardR(ReadingType):
     def __init__(self):
          super().__init__("Five cards", "5card", 5, "Five card tarot reading", layouts.draw5img)

class CelticR(ReadingType):
     def __init__(self):
          super().__init__("Celtic Cross", "celtic", 10, "Celtic cross tarot reading", layouts.celticimg)

class NCardR(ReadingType):
     def __init__(self, numCards):
          super().__init__("{} cards".format(numCards), "ncard", numCards, "{} card tarot reading".format(numCards), layouts.genericimg)

READING_TYPE_ENUM: list[ReadingType] = [OneCardR(), ThreeCardR(), FiveCardR(), CelticR()]

@unique
class Decks(Enum):
    def __new__(cls, shortname, label, longname, global_d = True):
        obj = object.__new__(cls)
        obj._value_ = shortname
        obj.shortname = shortname
        obj.label = label
        obj.longname = longname
        if global_d:
            cls.global_decks = cls.__dict__.get('global_decks', [])
            cls.global_decks.append(obj)
        return obj

    DEFAULT = ("default", "Default", "Default cards")
    SWISS = ("swiss", "Swiss", "IJJ Swiss cards")
    PLANET_SCUM = ("planetscum", "Planet Scum", "Planet Scum Custom Cards", False)

@unique
class MajorMinor(Enum):
    MAJOR_ONLY = "major"
    MINOR_ONLY = "minor"
    BOTH = "both"

class Card:
    """A class used to represent a tarot card.

    Attributes:
        name: The name of the card
        upright: Three-word description of a card's upright meaning
        reversed: Three-word description of a card's reversed meaning
        code: A short string representing the card's suit and rank
        up: True if a card is upright, False if inverted

    """

    def __init__(self, name: str, upright: str,
                 reverse: str, code: str, up=True):
        self.name = name
        self.upright = upright
        self.reverse = reverse
        self.code = code
        self.up = True

    def description(self) -> str:
        """Returns the card name and its meaning, depending on its orientation.

        Example:
            King of Cups (upright): compassion, control, balance

        """
        if (self.up):
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

def make_deck(majorminor: MajorMinor) -> List[Card]:
    """Returns a full deck of tarot cards."""
    major = [
        Card("The World",
             "fulfillment, harmony, completion",
             "incompletion, no closure", "21M"),
        Card("Judgement",
             "reflection, reckoning, awakening",
             "lack of self awareness, doubt, self loathing", "20M"),
        Card("The Sun",
             "joy, success, celebration, positivity",
             "negativity, depression, sadness", "19M"),
        Card("The Moon",
             "unconscious, illusions, intuition",
             "confusion, fear, misinterpretation", "18M"),
        Card("The Star",
             "hope, faith, rejuvenation",
             "faithlessness, discouragement, insecurity", "17M"),
        Card("The Tower",
             "sudden upheaval, broken pride, disaster",
             "disaster avoided, delayed disaster, fear of suffering", "16M"),
        Card("The Devil",
             "addiction, materialism, playfulness",
             "freedom, release, restoring control", "15M"),
        Card("Temperance",
             "middle path, patience, finding meaning",
             "extremes, excess, lack of balance", "14M"),
        Card("Death",
             "end of cycle, beginnings, change, metamorphosis",
             "fear of change, holding on, stagnation, decay", "13M"),
        Card("The Hanged Man",
             "sacrifice, release, martyrdom",
             "stalling, needless sacrifice, fear of sacrifice", "12M"),
        Card("Justice",
             "cause and effect, clarity, truth",
             "dishonesty, unaccountability, unfairness", "11M"),
        Card("The Wheel of Fortune",
             "change, cycles, inevitable fate",
             "no control, clinging to control, bad luck", "10M"),
        Card("The Hermit",
             "contemplation, search for truth, inner guidance",
             "loneliness, isolation, lost your way", "9M"),
        Card("Strength",
             "inner strength, bravery, compassion, focus",
             "self doubt, weakness, insecurity", "8M"),
        Card("The Chariot",
             "direction, control, willpower",
             "lack of control, lack of direction, aggression", "7M"),
        Card("The Lovers",
             "partnerships, duality, union",
             "loss of balance, one-sidedness, disharmony", "6M"),
        Card("The Hierophant",
             "tradition, conformity, morality, ethics",
             "rebellion, subversiveness, new approaches", "5M"),
        Card("The Emperor",
             "authority, structure, control, fatherhood",
             "tyranny, rigidity, coldness", "4M"),
        Card("The Empress",
             "motherhood, fertility, nature",
             "dependence, smothering, emptiness, nosiness", "3M"),
        Card("The High Priestess",
             "intuitive, unconscious, inner voice",
             "lack of center, lost inner voice, repressed feelings", "2M"),
        Card("The Magician",
             "willpower, desire, creation, manifestation",
             "trickery, illusions, out of touch", "1M"),
        Card("The Fool",
             "innocence, new beginnings, free spirit",
             "recklessness, taken advantage of, inconsideration", "0M")
    ]
    minor = [
        Card("Seven of Wands",
             "perseverance, defensive, maintaining control",
             "give up, destroyed confidence, overwhelmed", "7W"),
        Card("Four of Wands",
             "community, home, celebration",
             "lack of support, transience, home conflicts", "4W"),
        Card("Ace of Wands",
             "creation, willpower, inspiration, desire",
             "lack of energy, lack of passion, boredom", "AW"),
        Card("Ten of Wands",
             "accomplishment, responsibility, burden",
             "inability to delegate, overstressed, burnt out", "10W"),
        Card("Nine of Wands",
             "resilience, grit, last stand",
             "exhaustion, fatigue, questioning motivations", "9W"),
        Card("Eight of Wands",
             "rapid action, movement, quick decisions",
             "panic, waiting, slowdown", "8W"),
        Card("Six of Wands",
             "victory, success, public reward",
             "excess pride, lack of recognition, punishment", "6W"),
        Card("Five of Wands",
             "competition, rivalry, conflict",
             "avoiding conflict, respecting differences", "5W"),
        Card("Three of Wands",
             "looking ahead, expansion, rapid growth",
             "obstacles, delays, frustration", "3W"),
        Card("Two of Wands",
             "planning, making decisions, leaving home",
             "fear of change, playing safe, bad planning", "2W"),
        Card("Page of Wands",
             "exploration, excitement, freedom",
             "lack of direction, procrastination, creating conflict", "PW"),
        Card("Queen of Wands",
             "courage, determination, joy",
             "selfishness, jealousy, insecurities", "QW"),
        Card("King of Wands",
             "big picture, leader, overcoming challenges",
             "impulsive, overbearing, unachievable expectations", "KW"),
        Card("Knight of Wands",
             "action, adventure, fearlessness",
             "anger, impulsiveness, recklessness", "KNW"),
        Card("King of Cups",
             "compassion, control, balance",
             "coldness, moodiness, bad advice", "KC"),
        Card("Queen of Cups",
             "compassion, calm, comfort",
             "martyrdom, insecurity, dependence", "QC"),
        Card("Knight of Cups",
             "following the heart, idealist, romantic",
             "moodiness, disappointment", "KNC"),
        Card("Page of Cups",
             "happy surprise, dreamer, sensitivity",
             "emotional immaturity, insecurity, disappointment", "PC"),
        Card("Ten of Cups",
             "inner happiness, fulfillment, dreams coming true",
             "shattered dreams, broken family, domestic disharmony", "10C"),
        Card("Nine of Cups",
             "satisfaction, emotional stability, luxury",
             "lack of inner joy, smugness, dissatisfaction", "9C"),
        Card("Eight of Cups",
             "walking away, disillusionment, leaving behind",
             "avoidance, fear of change, fear of loss", "8C"),
        Card("Seven of Cups",
             "searching for purpose, choices, daydreaming",
             "lack of purpose, diversion, confusion", "7C"),
        Card("Six of Cups",
             "familiarity, happy memories, healing",
             "moving forward, leaving home, independence", "6C"),
        Card("Five of Cups",
             "loss, grief, self-pity",
             "acceptance, moving on, finding peace", "5C"),
        Card("Four of Cups",
             "apathy, contemplation, disconnectedness",
             "sudden awareness, choosing happiness, acceptance", "4C"),
        Card("Three of Cups",
             "friendship, community, happiness",
             "overindulgence, gossip, isolation", "3C"),
        Card("Two of Cups",
             "unity, partnership, connection",
             "imbalance, broken communication, tension", "2C"),
        Card("Ace of Cups",
             "new feelings, spirituality, intuition",
             "emotional loss, blocked creativity, emptiness", "AC"),
        Card("King of Swords",
             "head over heart, discipline, truth",
             "manipulative, cruel, weakness", "KS"),
        Card("Knight of Swords",
             "action, impulsiveness, defending beliefs",
        "no direction, disregard for consequences, unpredictability", "KNS"),
        Card("Queen of Swords",
             "complexity, perceptiveness, clear mindedness",
             "cold hearted, cruel, bitterness", "QS"),
        Card("Page of Swords",
             "curiosity, restlessness, mental energy",
             "deception, manipulation, all talk", "PS"),
        Card("Ten of Swords",
             "failure, collapse, defeat",
             "can't get worse, only upwards, inevitable end", "10S"),
        Card("Nine of Swords",
             "anxiety, hopelessness, trauma",
             "hope, reaching out, despair", "9S"),
        Card("Eight of Swords",
             "imprisonment, entrapment, self-victimization",
             "self acceptance, new perspective, freedom", "8S"),
        Card("Seven of Swords",
             "deception, trickery, tactics and strategy",
             "coming clean, rethinking approach, deception", "7S"),
        Card("Six of Swords",
             "transition, leaving behind, moving on",
             "emotional baggage, unresolved issues, resisting transition", "6S"),
        Card("Five of Swords",
             "unbridled ambition, win at all costs, sneakiness",
             "lingering resentment, desire to reconcile, forgiveness", "5S"),
        Card("Three of Swords",
             "heartbreak, suffering, grief",
             "recovery, forgiveness, moving on", "3S"),
        Card("Four of Swords",
             "rest, restoration, contemplation",
             "restlessness, burnout, stress", "4S"),
        Card("Two of Swords",
             "difficult choices, indecision, stalemate",
             "lesser of two evils, no right choice, confusion", "2S"),
        Card("Ace of Swords",
             "breakthrough, clarity, sharp mind",
             "confusion, brutality, chaos", "AS"),
        Card("King of Pentacles",
             "abundance, prosperity, security",
             "greed, indulgence, sensuality", "KP"),
        Card("Queen of Pentacles",
             "practicality, creature comforts, financial security",
             "self-centeredness, jealousy, smothering", "QP"),
        Card("Knight of Pentacles",
             "efficiency, hard work, responsibility",
             "laziness, obsessiveness, work without reward", "KNP"),
        Card("Page of Pentacles",
             "ambition, desire, diligence",
             "lack of commitment, greediness, laziness", "PP"),
        Card("Ten of Pentacles",
             "legacy, culmination, inheritance",
             "fleeting success, lack of stability, lack of resources", "10P"),
        Card("Nine of Pentacles",
             "fruits of labor, rewards, luxury",
             "reckless spending, living beyond means, false success", "9P"),
        Card("Eight of Pentacles",
             "apprenticeship, passion, high standards",
             "lack of passion, uninspired, no motivation", "8P"),
        Card("Seven of Pentacles",
             "hard work, perseverance, diligence",
             "work without results, distractions, lack of rewards", "7P"),
        Card("Six of Pentacles",
             "charity, generosity, sharing",
             "strings attached, stinginess, power and domination", "6P"),
        Card("Five of Pentacles",
             "need, poverty, insecurity",
             "recovery, charity, improvement", "5P"),
        Card("Four of Pentacles",
             "conservation, frugality, security",
             "greediness, stinginess, possessiveness", "4P"),
        Card("Three of Pentacles",
             "teamwork, collaboration, building",
             "lack of teamwork, disorganized, group conflict", "3P"),
        Card("Two of Pentacles",
             "balancing decisions, priorities, adapting to change",
             "loss of balance, disorganized, overwhelmed", "2P"),
        Card("Ace of Pentacles",
             "opportunity, prosperity, new venture",
             "lost opportunity, missed chance, bad investment", "AP")
        ]
    if majorminor == MajorMinor.MAJOR_ONLY:
        return major
    elif majorminor == MajorMinor.MINOR_ONLY:
        return minor
    else:
        return major + minor

def draw(n: int, invert=True, majorminor: MajorMinor = MajorMinor.BOTH) -> List[Card]:
    """Returns a list of n random cards from a full deck of cards.

        Args:
            n: the number of cards to draw
            invert: If True, cards have a 1/5 chance of being inverted.
                    Otherwise, no cards will be inverted.
            major_only: If True, only major arcana cards will be drawn
            minor_only: If True, only minor arcana cards will be drawn

    """
    deck = make_deck(majorminor)
    if n < 1 or n > len(deck):
        raise ValueError(f"Number of cards must be between 1 and {len(deck)}")

    hand = []
    for i in range(n):
        mycard = deck[random.randrange(len(deck))]
        if invert and (random.randrange(2) == 0):
            mycard.up = False
        deck.remove(mycard)
        hand.append(mycard)
    return hand

def cardtxt(cards: List[Card]):
    """Returns a list of tuples containing descriptions of a list of cards."""
    return list(map(lambda card: (card.get_name(), card.get_desc()), cards))

def makeImgList (cards: List[Card], deck: Decks):
    """Returns a list of Images corresponding to cards."""
    imgarray = []
    for c in cards:
        newcard = Image.open(path.join(path.dirname(__file__),"..","decks",deck.shortname,c.code + ".jpg")).convert("RGBA")
        if not c.up:
            newcardrev = newcard.rotate(180, expand = 1)
            imgarray.append(newcardrev)
        else:
            imgarray.append(newcard)
    return (imgarray)



def cardimg(cardsO: List[Card], deck: Decks, imgfunc) -> Image:
    """Returns an Image of the cards in cards0 in a spread specified by command.

        Args:
            cards0: the cards in the spread
            command: the spread. Valid spreads are 1card, 3card, 5card, celtic
    """
    cards = makeImgList(cardsO, deck)
    cardwidth = max(map(lambda x: x.width, cards))
    cardheight = max(map(lambda x: x.height, cards))
    img = imgfunc(cards, cardwidth, cardheight)
    return img
