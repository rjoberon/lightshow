#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo functions for lightshow.
#
# Usage: import as a module
#
# Author: rja
#
# Changes:
# 2022-01-02 (rja)
# - initial version

from random import randint

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


def get_rand_col():
    return colors[randint(0, len(colors)-1)]


def get_const_col():
    return colors[0] # red


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
