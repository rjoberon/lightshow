#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo of NeoPixel strip on Raspberry Pi Pico
#
# Preparation: copy neopixel.mpy from bundle (https://circuitpython.org/libraries) to /media/rja/CIRCUITPY/lib/
#
# Usage: Copy neopixel.py to /media/rja/CIRCUITPY/code.py
#
# Source: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/neopixel-leds
#
# Wiring:
# GND (black)  → GND  (3)
# 5VDC (red)   → VBUS (40)
# DIN (yellow) → GP20 (26)
#
# Author: rja
#
# Changes:
# 2021-12-26 (rja)
# - initial version


"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import board
import neopixel
import time

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8

pixels = neopixel.NeoPixel(board.GP20, num_pixels)
pixels.brightness = 0.5

while True:
    # pixels.fill((1, 1, 1))
    for i in range(8):
        pixels[i] = (0, 0, 0)
    time.sleep(3)
