from math import ceil, sqrt
from PIL import Image, ImageDraw

def draw1img (cards, cardwidth: int, cardheight: int) -> Image:
    """Returns an Image representing a 1-card spread.

        Args:
            cards (List[Image]): 1-item list containing the card in the spread
            cardwidth: the width of the card image
            cardheight: the height of the card image

    """
    image_border = 20
    total_width = (cardwidth + 2*image_border)
    total_height = (cardheight + 2*image_border)
    img = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    img.paste(cards[0], (image_border, image_border))
    return img

def draw3img (cards, cardwidth: int, cardheight: int) -> Image:
    """Returns an Image representing a 3-card spread.

        Args:
            cards (List[Image]): 3-item list containing the cards in the spread
            cardwidth: the width of the card image
            cardheight: the height of the card image

    """
    image_border = 20
    total_width = (3*cardwidth + 4*image_border)
    total_height = (cardheight + 2*image_border)
    img = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    img.paste(cards[0], (image_border, image_border))
    img.paste(cards[1], (2*image_border + cardwidth, image_border))
    img.paste(cards[2], (3*image_border + 2*cardwidth, image_border))
    return img

def draw5img (cards, cardwidth: int, cardheight: int) -> Image:
    """Returns an Image representing a 5-card spread.

        Args:
            cards (List[Image]): 5-item list containing the cards in the spread
            cardwidth: the width of the card image
            cardheight: the height of the card image

    """
    image_border = 20
    total_width = (3*cardwidth + 4*image_border)
    total_height = (3*cardheight + 4*image_border)
    img = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    img.paste(cards[0], (2*image_border + cardwidth, image_border))
    img.paste(cards[1], (2*image_border + cardwidth,
                         2*image_border + cardheight))
    img.paste(cards[2], (2*image_border + cardwidth,
                         3*image_border + 2*cardheight))
    img.paste(cards[3], (image_border, 2*image_border + cardheight))
    img.paste(cards[4], (3*image_border + 2*cardwidth,
                         2*image_border + cardheight))
    return img

def celticimg (cards, cardwidth: int, cardheight: int) -> Image:
    """Returns an Image representing a Celtic Cross spread.

        Args:
            cards (List[Image]): 10-item list containing the cards in the spread
            cardwidth: the width of the card image
            cardheight: the height of the card image

    """
    image_border = 20
    column1 = image_border
    column2 = 7*image_border + cardwidth
    column1_5 = (column2 + cardwidth//2) - (cardheight//2)
    column3 = column2 + cardwidth + 6*image_border
    column4 = column3 + cardwidth + 4*image_border
    row1 = image_border
    row2 = row1 + cardheight + image_border
    row1_5 = (row1 + row2)//2
    row3 = row2 + cardheight + image_border
    row2_5 = (row2 + row3)//2
    row4 = row3 + cardheight + image_border
    row3_5 = (row3 + row4)//2
    total_width = column4 + cardwidth + image_border
    total_height = row4 + cardheight + image_border
    img = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    img.paste(cards[0], (column2, row2_5))
    img.paste(cards[2], (column2, row1_5))
    img.paste(cards[3], (column2, row3_5))
    img.paste(cards[4], (column1, row2_5))
    img.paste(cards[5], (column3, row2_5))
    img.paste(cards[6], (column4, row4), cards[6])
    img.paste(cards[7], (column4, row3), cards[7])
    img.paste(cards[8], (column4, row2))
    img.paste(cards[9], (column4, row1))
    card2 = cards[1].rotate(90, expand = 1)
    img.paste(card2, (column1_5, row2_5 + 2*image_border))
    return img

def genericimg (cards, cardwidth: int, cardheight: int) -> Image:
    """Returns an Image representing a 5-card spread.

        Args:
            cards (List[Image]): list containing the cards in the spread
            cardwidth: the width of the card image
            cardheight: the height of the card image

    """
    image_border = 20
    ratio = (9*cardwidth + 2*image_border) / (16*cardheight + 2*image_border)
    rows = ceil(sqrt(len(cards)*ratio))
    cols = ceil(len(cards) / rows)
    total_width = (cols*(cardwidth + image_border) - image_border)
    total_height = (rows*(cardheight + image_border) - image_border)
    
    img = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    for i in range(0, rows):
        for j in range(0, cols):
            cardnum = i*cols + j
            if cardnum >= len(cards):
                break
            img.paste(cards[i*cols + j], (j*(image_border + cardwidth), i*(image_border + cardheight)))
    return img