#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Use the pico as MIDI input device.
#
# Usage: cp to CIRCUITPY/code.py
#
# Author: rja
#
# Useful resources:
# - https://blog.4dcu.be/diy/2021/05/20/MIDIpad.html
# - https://in-thread.sonic-pi.net/t/using-pitch-change-and-control-change-from-midi-controller-roli-lightblock/435/7
# - https://sites.uci.edu/camp2014/2014/04/30/managing-midi-pitchbend-messages/
# - https://docs.circuitpython.org/projects/midi/en/latest/api.html
# - https://blog.4dcu.be/diy/2021/05/20/MIDIpad.html

# TODO:
# - use button debouncer? see multi.py or https://github.com/CrazyRobMiles/PICO-MIDI-Crackers-Controller/blob/main/code/CrackersController.py
#
# Changes:
# 2023-01-17 (rja)
# - initial version

import board
import digitalio
import rotaryio
import time
import usb_midi
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
# from adafruit_midi.control_change import ControlChange

note_mapping = [
        ["C3", "C2"], # red
        ["D3", "D2"], # black
        ["E3", "E2"],
        ["F3", "F2"],
        ["G3", "G2"],
        ["A3", "A2"],
        ["B3", "B2"],
        ["C4", "C3"],
        ["G2", "G1"]
    ]

# set up MIDI device
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

print("set up MIDI device")

# set up buttons
button_pins = [
    board.GP10, # red
    board.GP8   # black
]
buttons = [digitalio.DigitalInOut(bp) for bp in button_pins]
for btn in buttons:
    btn.switch_to_input(pull=digitalio.Pull.DOWN)

# button and trigger states
pressed_buttons = [False for _ in button_pins]
triggered_buttons = [False for _ in button_pins]

# set up rotary encoder
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
encoder_last_pos = 0

bend = 8192 # range: 0 ... 16383 with 8192 no bend
bend_step = 683

# main loop
while True:

    # handle rotary encoder
    encoder_pos = encoder.position
    if encoder_pos != encoder_last_pos:
        print("encoder:", encoder_pos, encoder_last_pos)
        if encoder_pos > encoder_last_pos:
            bend = min(16383, bend + bend_step)
        elif encoder_pos < encoder_last_pos:
            bend = max(0, bend - bend_step)
        print("bending:", bend)
        midi.send(PitchBend(bend))
    encoder_last_pos = encoder_pos

    # set all pressed buttons to True
    for ix, btn in enumerate(buttons):
        pressed_buttons[ix] = btn.value

    for ix, (pk, tk) in enumerate(zip(pressed_buttons, triggered_buttons)):
        if pk and not tk:
            print("note %d started" % ix)
            midi.send([NoteOn(a, 60) for a in note_mapping[ix]])
            triggered_buttons[ix] = True
        elif not pk and tk:
            print("note %d stopped" % ix)
            triggered_buttons[ix] = False
            midi.send([NoteOff(a, 0) for a in note_mapping[ix]])

    time.sleep(0.01)
