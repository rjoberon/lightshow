#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo for simple rotary encoder with LED on Raspberry Pi Pico.
# (rotates through red, green, blue, yellow, magenta, cyan, white)
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
import digitalio

encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
rgb = (
    digitalio.DigitalInOut(board.GP21),
    digitalio.DigitalInOut(board.GP20),
    digitalio.DigitalInOut(board.GP19)
)

for c in rgb:
    c.direction = digitalio.Direction.OUTPUT

states = [
    (False, False, False),
    (True, False, False),
    (False, True, False),
    (False, False, True),
    (True, True, False),
    (True, False, True),
    (False, True, True),
    (True, True, True)
]


last_position = None
while True:
    position = encoder.position
    if last_position is None or position != last_position:
        state = states[position % len(states)]
        print(position, state)
        for i, c in enumerate(rgb):
            c.value = state[i]
    last_position = position
