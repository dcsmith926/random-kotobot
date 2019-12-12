"""
Functions for randomly generating the Twitter header image.
It's a very naive approach that just tries to fit random words
into random positions in the image without overlapping other words.
It loops forever, doing this until NUM_WORDS have been successfully inserted into the image. 
"""

from math import sqrt
import os
import random
from PIL import Image, ImageDraw, ImageFont
from jmdict import JMDict

HEADER_WIDTH = 1500
HEADER_HEIGHT = 500
HEADER_BG_COLOR = (163, 0, 255, 252)
HEADER_MODE = 'RGBA'
HEADER_PATH = 'header.png'

FONT_PATH = 'font/SoukouMincho/SoukouMincho.ttf'
FONT_SIZE = 72

NUM_WORDS = 25 
MAX_TRY_FIT_WORD = 100 

TEXT_FILL_COLOR = (255, 255, 255, 252) 
TEXT_STROKE_COLOR = (255, 0, 255, 252)
TEXT_STROKE_SIZE = 2

def random_coords(min_x, max_x, min_y, max_y):
    x = random.randint(int(min_x), int(max_x))
    y = random.randint(int(min_y), int(max_y))
    return (x, y)

def rect_overlap(rect1, rect2):

    x1_t, y1_t = rect1[0]
    x1_b, y1_b = rect1[1]

    x2_t, y2_t = rect2[0]
    x2_b, y2_b = rect2[1]

    if x1_b < x2_t or x2_b < x1_t:
        return False

    if y1_b < y2_t or y2_b < y1_t:
        return False

    return True

def too_close(text_position, text_size, used_areas, allowed_overlap=-10):

    text_x, text_y = text_position
    text_width, text_height = text_size

    # top left corner and bottom right corner
    text_rect = (
        (text_x + allowed_overlap, text_y + allowed_overlap),
        (text_x + text_width - allowed_overlap, text_y + text_height - allowed_overlap),
    ) 

    for position, size in used_areas:

        a_x, a_y = position
        a_width, a_height = size

        a_rect = (
            (a_x + allowed_overlap, a_y + allowed_overlap),
            (a_x + a_width - allowed_overlap, a_y + a_height - allowed_overlap),
        )

        if rect_overlap(text_rect, a_rect):
            return True
    
    return False

def find_good_position(text_size, used_areas):

    text_width, text_height = text_size

    # how far the text can overflow edge of image
    overflow_x = text_width / 2
    overflow_y = text_height / 2

    min_x = 0 - overflow_x
    max_x = HEADER_WIDTH + overflow_x

    min_y = 0 - overflow_y 
    max_y = HEADER_HEIGHT + overflow_y

    tries = 0
    while tries < MAX_TRY_FIT_WORD:
        text_position = random_coords(min_x, max_x, min_y, max_y)
        if not too_close(text_position, text_size, used_areas):
            break
        tries += 1
    
    # tried all we can, return None
    if tries >= MAX_TRY_FIT_WORD:
        return None
    # found a good position, so return it
    else:
        return text_position

def draw_text(draw, text, position, font, fill_color, stroke_size=0, stroke_color=None):

    x, y = position

    # a hacky way to draw text with stroke is to draw the text using the stroke color
    # multiple times at various offsets from the actual position,
    # and then draw the text using the fill color at the actual position
    if stroke_size > 0:
        for i in range(stroke_size + 1):
            draw.text((x, y + i), text, font=font, fill=stroke_color)
            draw.text((x, y - i), text, font=font, fill=stroke_color)
            draw.text((x + i, y), text, font=font, fill=stroke_color)
            draw.text((x - i, y), text, font=font, fill=stroke_color)
            draw.text((x + i, y + i), text, font=font, fill=stroke_color)
            draw.text((x + i, y - i), text, font=font, fill=stroke_color)
            draw.text((x - i, y + i), text, font=font, fill=stroke_color)
            draw.text((x - i, y - i), text, font=font, fill=stroke_color)

    draw.text(position, text, font=font, fill=fill_color)

def generate_header():

    im = Image.new(HEADER_MODE, (HEADER_WIDTH, HEADER_HEIGHT), HEADER_BG_COLOR)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join(os.path.curdir, FONT_PATH), size=FONT_SIZE)

    jm = JMDict()

    used_areas = []

    for i in range(NUM_WORDS):

        while True:

            # get a random word, and its size
            text = str(jm.random_entry())
            text_size = font.getsize(text)

            # try to find a good position for the word in our image
            # will return None if no good position found after a max number of attempts
            text_position = find_good_position(text_size, used_areas)

            # if found a good position, break out of loop
            if not text_position is None:
                break

        # append the position and size to our list of used areas
        used_areas.append((
            text_position,
            text_size,
        ))

        # draw the text at the position
        draw_text(draw, text, text_position, font, TEXT_FILL_COLOR, TEXT_STROKE_SIZE, TEXT_STROKE_COLOR)

    with open(HEADER_PATH, 'wb') as f:
        im.save(f)