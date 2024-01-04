#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo functions for lightshow.
#
# Usage: import as a module
#
# Arguments:
# - k: arbitrary integer (= rotary encoder position)
# - n: number of pixels (LEDs)
# - pixels: NeoPixel
# - getcolor: color function
#
# Author: rja
#
# Changes:
# 2024-01-04 (rja)
# - added ls_sine
# - added workaround for missing rainbowio library
# 2024-01-03 (rja)
# - added ls_rainbow
# 2022-01-03 (rja)
# - repaired scalar assignment for list slices
# - added ls_gray, ls_pulse, ls_random
# 2022-01-02 (rja)
# - initial version

from random import randint, getrandbits
from math import sin

try:
    from rainbowio import colorwheel
except ImportError:
    def colorwheel(c):
        print("WARNING: rainbowio not found, using constant color")
        return (128, 0, 0)


# color configuration
hv = 255
mv = 128

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


def col_rand():
    return colors[randint(0, len(colors)-1)]


def col_const():
    return colors[0] # red


def ls_position(k, n, pixels, getcolor):
    """0: [        ]
       1: [O       ]
       2: [ O      ]
       3: [  O     ]
       4: [   O    ]
       ...
       n: [       O]
    """
    for i in range(n):
        pixels[i] = getcolor() if i == (k - 1) % n else OFF


def ls_unary(k, n, pixels, getcolor):
    """0: [        ]
       1: [O       ]
       2: [OO      ]
       3: [OOO     ]
       4: [OOOO    ]
       ...
       n: [OOOOOOOO]
    """
    for i in range(n):
        pixels[i] = getcolor() if i < k % (n + 1) else OFF


def ls_binary(k, n, pixels, getcolor):
    """0: [        ]
       1: [       O]
       2: [      O ]
       3: [      OO]
       4: [     O  ]
       ...
       n: [OOOOOOOO]
    """
    for i, j in enumerate("{0:{fill}8b}".format(k % 2**n, fill='0')):
        pixels[i] = getcolor() if j == '1' else OFF


def ls_gray(k, n, pixels, getcolor):
    """0: [        ]
       1: [       O]
       2: [      OO]
       3: [      O ]
       4: [     OO ]
       ...
       n: [OOOOOOOO]
    """
    kk = k % 2**n
    for i, j in enumerate("{0:{fill}8b}".format(kk ^ (kk >> 1), fill='0')):
        pixels[i] = getcolor() if j == '1' else OFF


def ls_pulse(k, n, pixels, getcolor):
    """0: [        ]
       1: [   OO   ]
       2: [  OOOO  ]
       ...
       4: [OOOOOOOO]
       ...
       6: [  OOOO  ]
       7: [   OO   ]
       8: [        ]
       9: [   OO   ]
       ...
    """
    off = abs(n//2 - ((k - 1) % n))
    for i in range(n):
        pixels[i] = getcolor() if i >= off and i < n - off else OFF


# TODO
def ls_band(k, n, pixels, getcolor):
    """0: [        ]  1 4 0
       1: [   OO   ]  2 3 1
       2: [  O  O  ]  3 2 2
       ...            4 1 3
       4: [O      O]  5 2 4
       ...            6 3 5
       6: [  O  O  ]  7 4 6
       7: [   OO   ]  8 3 7
       8: [        ]
       9: [   OO   ]
       ...
    """
    off = abs(n//2 - ((k - 1) % (n - 1)))
    # print(k, off)
    for i in range(n):
        pixels[i] = getcolor() if i == off or i == n - off else OFF


def ls_sine(k, n, pixels, getcolor):
    """Sine wave"""
    # The constant 40 fixes the speed/resolution.
    on = int((1 + sin(((2*3.1415926)/40) * (k % 40)))/2 * n)
    for i in range(n):
        pixels[i] = getcolor() if i == on else OFF


def ls_random(k, n, pixels, getcolor):
    for i, j in enumerate("{0:{fill}8b}".format(getrandbits(n), fill='0')):
        pixels[i] = getcolor() if j == '1' else OFF


def ls_rainbow(k, n, pixels, getcolor):
    """A rainbow starting at k."""
    # FIXME: document/explain constants
    for i in range(n):
        pixel_index = (i * 256 // n) + k
        pixels[i] = colorwheel(pixel_index & 255)
