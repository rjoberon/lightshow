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
# | device  | pin    | function                  | Pico  |
# |---------+--------+---------------------------+-------|
# | LED     | black  | GND                       | GND   |
# | strip   | red    | 5VDC                      | VBUS  |
# |         | yellow | DIN                       | GP0   |
# |---------+--------+---------------------------+-------|
# | RGB     | A      | rotary encoder            | GP3   |
# | rotary  | B      | rotary encoder            | GP4   |
# | encoder | C      | rotary encoder GND        | GND   |
# |         | 1      | LED red                   | -     |
# |         | 2      | LED green                 | -     |
# |         | 3      | switch                    | GP2   |
# |         | 4      | LED blue                  | -     |
# |         | 5      | common anode LED & switch | 3.3V  |
# |---------+--------+---------------------------+-------|
# | EC11    | A      | rotary encoder            | GP10  |
# | rotary  | B      | rotary encoder            | GP11  |
# | encoder | C      | GND                       | GND   |
# |         | D      | GND                       | GND   |
# |         | E      | switch                    | GP12  |
#
# Author: rja
#
# Changes:
# 2024-01-13 (rja)
# - connected switches and 2nd rotary encoder
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
import rotaryio
import digitalio
from adafruit_debouncer import Debouncer


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8
gpio_neopixel = board.GP0

# configure wiring

# rotary encoder with switch and RGB LED
# rotary encoder
encoder1 = rotaryio.IncrementalEncoder(board.GP3, board.GP4)
# switch
pin1 = digitalio.DigitalInOut(board.GP2)
pin1.direction = digitalio.Direction.INPUT
pin1.pull = digitalio.Pull.DOWN
switch1 = Debouncer(pin1)
# LED
#rgb = (
#    pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=2**16 - 1),
#    pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=2**16 - 1),
#    pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=2**16 - 1)
#)

# rotary encoder with switch
# rotary encoder
encoder2 = rotaryio.IncrementalEncoder(board.GP11, board.GP10)
# switch
pin2 = digitalio.DigitalInOut(board.GP12)
pin2.direction = digitalio.Direction.INPUT
pin2.pull = digitalio.Pull.UP
switch2 = Debouncer(pin2)


last_pos1 = None                # last position of rotary encoder 1
last_pos2 = None                # last position of rotary encoder 2

while True:
    # handle rotary encoder1 (speed or stepping)
    pos1 = encoder1.position
    if last_pos1 is None or pos1 != last_pos1:
        print("encoder 1:", last_pos1, "→", pos1)
    last_pos1 = pos1

    # handle switch1
    switch1.update()
    # handle switch of rotary encoder
    if switch1.rose:
        print("switch 1")

    # handle switch2
    switch2.update()
    # handle switch of rotary encoder
    if switch2.rose:
        print("switch 2")

    # handle rotary encoder2 (effect)
    pos2 = encoder2.position
    if last_pos2 is None or pos2 != last_pos2:
        print("encoder 2:", last_pos2, "→", pos2)
    last_pos2 = pos2

    time.sleep(0.05)                          # wait
