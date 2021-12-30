#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Usage: Copy to /media/rja/CIRCUITPY/code.py
#
# Author: rja
#
# Docs:
# - NeoPixel: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
# - Rotary:
#
# Changes:
# 2021-12-30 (rja)
# - initial version

import board
import neopixel
import rotaryio
from random import randint

num_pixels = 8
encoder = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
pixels = neopixel.NeoPixel(board.GP20, num_pixels, auto_write=False)

pixels.brightness = 0.5

hv = 64
mv = 32

cols = [
    (hv,  0,   0),   # red
    (0,  hv,   0),   # green
    (0,   0,  hv),   # blue
    (mv, mv,   0),
    (mv,  0,  mv),
    (0,  mv,  mv)
]


def get_rand_col(onoff):
    if onoff != 0:
        return cols[randint(0, len(cols)-1)]
    return (0, 0, 0)


def set_pixel_as_int(n, pixels):
    """Sets the pixels to show n % 2^8."""
    for i, j in enumerate("{0:{fill}8b}".format(n % 2**8, fill='0')):
        #pixels[i] = (int(j)*100, 0, 0)
        pixels[i] = get_rand_col(int(j))
    pixels.show()


last_position = None
while True:
    position = encoder.position
    if last_position is None or position != last_position:
        print(position)
        set_pixel_as_int(position, pixels)
    last_position = position
