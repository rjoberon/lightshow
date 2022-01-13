#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo for simple rotary encoder on Raspberry Pi Pico
#
# Usage: Copy rotarytest.py to /media/rja/CIRCUITPY/code.py
#
# see output on serial console (screen /dev/ttyACM1 115200)
# Source: https://learn.adafruit.com/rotary-encoder/circuitpython
#
# Author: rja
#
# Changes:
# 2021-12-26 (rja)
# - initial version

# A → D9  (GP6)
# B → D10 (GP7)
# C → GND (e.g., D8)


import rotaryio
import board

encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
last_position = None

while True:
    position = encoder.position
    if last_position is None or position != last_position:
        print(position)
    last_position = position
