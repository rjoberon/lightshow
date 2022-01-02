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
# 2022-01-02 (rja)
# - moved functions to demos.py
# 2021-12-30 (rja)
# - initial version

import board
import neopixel
import rotaryio
import demos

# configure hardware here
num_pixels = 8
gpio_neopixel = board.GP20
encoder = rotaryio.IncrementalEncoder(board.GP6, board.GP7)

with neopixel.NeoPixel(gpio_neopixel, num_pixels, auto_write=False) as pixels:
    pixels.brightness = 0.5

    last_position = None
    while True:
        position = encoder.position
        if last_position is None or position != last_position:
            print(position)
            demos.ls_binary(position, num_pixels, pixels, demos.get_rand_col)
            pixels.show()
        last_position = position
