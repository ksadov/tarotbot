import random
from PIL import Image

eightball_states = []


def shake() -> tuple[Image.Image, str]:
    return random.choice(eightball_states)
