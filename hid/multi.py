#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Universal HID controller.
#
# Usage: Copy multi.py to /media/rja/CIRCUITPY/code.py
#
# see output on serial console (screen /dev/ttyACM1 115200)
#
# Author: rja
#
# Changes:
# 2022-01-16 (rja)
# - initial version
#
# | pin encoder | function                  | pin Pico |
# |-------------+---------------------------+----------|
# |           A | rotary encoder            | GP14     |
# |           B | rotary encoder            | GP15     |
# |           C | rotary encoder GND        | GND      |
# |           1 | LED red                   | GP21     |
# |           2 | LED green                 | GP20     |
# |           3 | switch                    | GP22     |
# |           4 | LED blue                  | GP19     |
# |           5 | common anode LED & switch | 3.3V     |

import rotaryio
import board
import pwmio
import random
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import adafruit_fancyled.adafruit_fancyled as fancy
from adafruit_debouncer import Debouncer


# configure wiring
# rotary encoder
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
# switch
pin = digitalio.DigitalInOut(board.GP22)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.DOWN
switch = Debouncer(pin)
# LED
rgb = (
    pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=2**16 - 1),
    pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=2**16 - 1),
    pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=2**16 - 1)
)

kbd = Keyboard(usb_hid.devices)
ctl = ConsumerControl(usb_hid.devices)
# red and black button
btnred = digitalio.DigitalInOut(board.GP10)
btnred.switch_to_input(pull=digitalio.Pull.DOWN)
btnblk = digitalio.DigitalInOut(board.GP8)
btnblk.switch_to_input(pull=digitalio.Pull.DOWN)


# helper functions


def set_color(led, rgb):
    """Set LED to rgb using some checks.
       Input colors in range 0..2**8, output colors in range 0..2**16"""
    for i, c in enumerate(rgb):
        val = (255 - min(255, abs(c))) * (2**8 + 1)
        print("  ", c, "→", val)
        led[i].duty_cycle = val


def get_step(value, maxvalue, steps):
    """Split 0...maxvalue into steps-1 parts and return boundary"""
    return int((value % steps) * (maxvalue/(steps - 1)))


# functions mapping encoder positions to LED colors

# used by ls_rgbcmyk
colors = [
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
    return [c*brightness for c in colors[pos % len(colors)]]


def ls_saturation(pos, color=0, steps=9):
    """Loop through saturation of a random color"""
    values = [0, 0, 0]
    values[color] = get_step(pos, 255, steps)
    return values


def ls_random(pos, granularity=4):
    """Random color."""
    return (
        random.randint(1, granularity) * 256//granularity - 1,
        random.randint(1, granularity) * 256//granularity - 1,
        random.randint(1, granularity) * 256//granularity - 1
    )


def ls_binaryrandom(pos):
    """Random color alternating with no color"""
    return ls_random(pos) if pos % 2 == 0 else (0, 0, 0)


def ls_binaryfixed(pos, color=(255, 0, 0)):
    """Fixed color alternating with no color"""
    return color if pos % 2 == 0 else (0, 0, 0)


def ls_hue(pos, steps=33):
    """Loop through hue"""
    hue = get_step(pos, 255, steps)
    return [int(c*255) for c in fancy.CRGB(fancy.CHSV(hue))]


# functions to loop through
funcs = [
    ls_rgbcmyk,
    ls_saturation,
    ls_random,
    ls_binaryrandom,
    ls_binaryfixed,
    ls_hue
]

last_position = None
funci = 0
func = funcs[funci]

while True:
    position = encoder.position
    switch.update()
    # handle rotary encoder
    if last_position is None or position != last_position:
        col = func(position)
        print(position, col)
        set_color(rgb, col)
        if last_position is not None:
            if position > last_position:
                ctl.send(ConsumerControlCode.VOLUME_INCREMENT)
            elif last_position > position:
                ctl.send(ConsumerControlCode.VOLUME_DECREMENT)
    last_position = position

    # handle switch of rotary encoder
    if switch.rose:
        func = funcs[funci]
        print("using", func)
        funci = (funci + 1) % len(funcs)

    # handle black and red button
    if btnred.value:
        print("red button")
        kbd.send(Keycode.ALT, Keycode.A) # mute/unmute
    if btnblk.value:
        print("black button")
        kbd.send(Keycode.ALT, Keycode.Z) # raise/lower hand

    # wait
    time.sleep(0.15)
