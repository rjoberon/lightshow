#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo for simple rotary encoder with LED on Raspberry Pi Pico.
#
# Usage: Copy rotaryledtest.py to /media/rja/CIRCUITPY/code.py
#
# see output on serial console (screen /dev/ttyACM1 115200)
# Source: https://learn.adafruit.com/rotary-encoder/circuitpython
#
# Author: rja
#
# Changes:
# 2022-01-09 (rja)
# - initial version
#
# | pin RE | function                  | pin Pico       |
# |--------+---------------------------+----------------|
# |      A | rotary encoder            | D9  (GP6)      |
# |      B | rotary encoder            | D10 (GP7)      |
# |      C | rotary encoder GND        | GND (e.g., D8) |
# |      1 | LED red                   | GP21           |
# |      2 | LED green                 | GP20           |
# |      3 | switch                    |                |
# |      4 | LED blue                  | GP19        |
# |      5 | common anode LED & switch | 3.3V           |

import rotaryio
import board
import pwmio
import random
#import adafruit_fancyled.adafruit_fancyled as fancy

# configure wiring
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
OFF = 2**16 - 1
ON  = 0
rgb = (
    pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=OFF),
    pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=OFF),
    pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=OFF)
)
RED = 0
GREEN = 1
BLUE = 2


def set_color(led, rgb):
    """Set LED to rgb using some checks. colors in range 0..255"""
    for i, c in enumerate(rgb):
        val = (255 - min(255, abs(c))) * (2**8 + 1)
        print("  ", c, "→", val)
        led[i].duty_cycle = val


# functions mapping encoder positions to LED colors

# used by rgbcmyk
states = [
    (0, 0, 0), # off
    (1, 0, 0), # red
    (0, 1, 0), # green
    (0, 0, 1), # blue
    (1, 1, 0), # yellow
    (1, 0, 1), # magenta
    (0, 1, 1), # cyan
    (1, 1, 1)  # white
]


def ls_rgbcmyk(pos, brightness=255):
    """Loop through red, green, blue, yellow, magenta, cyan, white"""
    return [c*brightness for c in states[pos % len(states)]]


def ls_saturation(pos, color=RED, steps=9):
    """Loop through saturation of a random color"""
    values = [0, 0, 0]
    values[color] = int((pos % steps) * (255/(steps - 1)))
    return values


def ls_hue(pos):
    """Rotate through hue"""
    pass


# functions to loop through
funcs = [ls_rgbcmyk]
funcs = [ls_saturation]

last_position = None
funci = 0

while True:
    position = encoder.position
    if last_position is None or position != last_position:
        func = funcs[funci]
        col = func(position)
        print(position, col)
        set_color(rgb, col)
    last_position = position
