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
# | device  | pin    | function                  | Pico |
# |---------+--------+---------------------------+------|
# | LED     | black  | GND                       | GND  |
# | strip   | red    | 5VDC                      | VBUS |
# |         | yellow | DIN                       | GP0  |
# |---------+--------+---------------------------+------|
# | RGB     | A      | rotary encoder            | GP3  |
# | rotary  | B      | rotary encoder            | GP4  |
# | encoder | C      | rotary encoder GND        | GND  |
# |         | 1      | LED red                   | -    |
# |         | 2      | LED green                 | -    |
# |         | 3      | switch                    | -    |
# |         | 4      | LED blue                  | -    |
# |         | 5      | common anode LED & switch | -    |
#
# Author: rja
#
# Changes:
# 2024-01-03 (rja)
# - added selection of different effects using the rotary encoder
# 2023-12-30 (rja)
# - added rotary encoder (which moves the rainbow)
# 2023-12-17 (rja)
# - changed DIN from GP20 to GP0 (1) and added rainbow code :-)
# 2021-12-26 (rja)
# - initial version
#
# Tasks:
# - consider using interrupt-based handling of rotary encoder, for example,
#   https://pypi.org/project/micropython-rotary-encoder/

import time
import board
import neopixel
import rotaryio
import demos


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8
gpio_neopixel = board.GP0

# configure wiring
# rotary encoder
encoder = rotaryio.IncrementalEncoder(board.GP3, board.GP4)
# switch
#pin = digitalio.DigitalInOut(board.GP22)
#pin.direction = digitalio.Direction.INPUT
#pin.pull = digitalio.Pull.DOWN
#switch = Debouncer(pin)
# LED
#rgb = (
#    pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=2**16 - 1),
#    pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=2**16 - 1),
#    pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=2**16 - 1)
#)


effects = [
    demos.ls_position,
    demos.ls_unary,
    demos.ls_binary,
    demos.ls_gray,
    demos.ls_pulse,
    demos.ls_band,
    demos.ls_random
]


with neopixel.NeoPixel(gpio_neopixel, num_pixels, auto_write=False) as pixels:
    pixels.brightness = 0.25

    k = 0                           # running variable for effect
    last_position = None            # last position of rotary encoder

    while True:
        # handle rotary encoder
        position = encoder.position
        if last_position is None or position != last_position:
            print(position)         # position changed → change effect
            effect = effects[position % len(effects)]
            k = 0
        last_position = position

        # handle effect
        effect(k, num_pixels, pixels, demos.col_rand)
        pixels.show()
        if k > 255:
            k = 0
        else:
            k += 1

        time.sleep(0.15)
