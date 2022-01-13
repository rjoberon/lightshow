#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Zoom buttons for mute/unmute and raise/lower hand.
#
# Usage: cp to CIRCUITPY/code.py
#
# See: https://support.zoom.us/hc/en-us/articles/205683899-hot-keys-and-keyboard-for-zoom
#
# Based on: https://github.com/MakeMagazinDE/Pico_Tastatur/blob/main/src/Drei_Tasten.py
#
# Author: rja
#
# Changes:
# 2022-01-13 (rja)
# - initial version

import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

btnred = digitalio.DigitalInOut(board.GP16)
btnred.switch_to_input(pull=digitalio.Pull.DOWN)
btnblk = digitalio.DigitalInOut(board.GP17)
btnblk.switch_to_input(pull=digitalio.Pull.DOWN)

while True:
    if btnred.value:
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.A) # mute/unmute
        time.sleep(0.2)
    if btnblk.value:
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.Y) # raise/lower hand
        time.sleep(0.2)
