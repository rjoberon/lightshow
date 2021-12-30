#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Usage: Copy to /media/rja/CIRCUITPY/code.py
#
# Author: rja
#
# Docs:
# - NeoPixel: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
# - Rotary: https://circuitpython.readthedocs.io/en/latest/shared-bindings/rotaryio/
#           https://github.com/adafruit/circuitpython/tree/main/shared-bindings/rotaryio
#
# Ideas + Next Steps:
# - refactoring
# - implement ls_spectrum
# - use button to choose from available functions
# - check for interrupt-driven reading of rotary encoder
#
# Changes:
# 2021-12-30 (rja)
# - initial version

import board
import neopixel
import rotaryio
from random import randint

# configure hardware here
num_pixels = 8
gpio_neopixel = board.GP20
encoder = rotaryio.IncrementalEncoder(board.GP6, board.GP7)

# color configuration
hv = 64
mv = 32

colors = [
    (hv,  0,   0),   # red
    (0,  hv,   0),   # green
    (0,   0,  hv),   # blue
    (mv, mv,   0),   # yellow
    (mv,  0,  mv),   # magenta
    (0,  mv,  mv),   # cyan
    (hv, mv,   0)    # orange?
]
OFF = (0, 0, 0)


def get_rand_col():
    return colors[randint(0, len(colors)-1)]


# functions that convert encoder positions to neopixel configurations


def ls_binary(k, n, pixels, getcolor):
    """0: [        ]
       1: [O       ]
       2: [ O      ]
       3: [OO      ]
       4: [  O     ]
       ...
       n: [OOOOOOOO]
    """
    for i, j in enumerate("{0:{fill}8b}".format(k % 2**n, fill='0')):
        if j == '1':
            pixels[i] = getcolor()
        else:
            pixels[i] = OFF


def ls_unary(k, n, pixels, getcolor):
    """0: [        ]
       1: [O       ]
       2: [OO      ]
       3: [OOO     ]
       ...
       n: [OOOOOOOO]
    """
    pixels[:k] = getcolor()
    pixels[k:] = OFF


def ls_position(k, n, pixels, getcolor):
    """0: [        ]
       1: [O       ]
       2: [ O      ]
       3: [  O     ]
       ...
       n: [       O]
    """
    pixels[:] = OFF
    pixels[k % n] = getcolor()


def ls_spectrum(k, n, pixels, getcolor):
    """Scroll through the spectrum of light."""
    pass


with neopixel.NeoPixel(gpio_neopixel, num_pixels, auto_write=False) as pixels:
    pixels.brightness = 0.5

    last_position = None
    while True:
        position = encoder.position
        if last_position is None or position != last_position:
            print(position)
            ls_binary(position, num_pixels, pixels, get_rand_col)
            pixels.show()
        last_position = position
