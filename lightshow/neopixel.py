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
# 2023-12-17 (rja)
# - changed DIN from GP20 to GP0 (1) and added rainbow code :-)
# 2021-12-26 (rja)
# - initial version


"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import time
import board
import neopixel
from rainbowio import colorwheel

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8

pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = 0.5

def rainbow(speed):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(speed)

while True:
    rainbow(0)
