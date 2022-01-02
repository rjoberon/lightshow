#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Emulates a NeoPixel strip.
#
# Usage: ./emulator.py
#
# Author: rja
#
# Changes:
# 2021-12-31 (rja)
# - initial version

import sys
import sdl2.ext
import demos


class NeoPixelEmulator():

    led_size = 40
    gap_size = 2

    def __init__(self, size):
        self.data = [(0, 0, 0) for i in range(size)]

        # init SDL window
        sdl2.ext.init()
        width = len(self.data) * (self.led_size + self.gap_size) + self.gap_size
        height = self.led_size + 2*self.gap_size
        self.window = sdl2.ext.Window("NeoPixel Emulator", size=(width, height))
        self.surface = self.window.get_surface()
        sdl2.ext.fill(self.surface, 0)
        self.window.show()

    def show(self):
        x = self.gap_size
        for col in self.data:
            self._draw_square(x, col)
            x += self.led_size + self.gap_size

    def _draw_square(self, x, col):
        rect = [x, self.gap_size, self.led_size, self.led_size]
        color = sdl2.ext.Color(col[0], col[1], col[2])
        sdl2.ext.fill(self.surface, color, rect)

    def __repr__(self):
        return str(self.data)

    def run(self, func, getcolor):
        running = True
        position = 0
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_LEFT:
                        position -= 1
                        self.set(position, func, getcolor)
                    elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                        position += +1
                        self.set(position, func, getcolor)
                    elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        running = False
                        break
            self.window.refresh()
        sdl2.ext.quit()
        return 0

    def set(self, pos, func, getcolor):
        func(pos, len(self.data), self.data, getcolor)
        self.show()


if __name__ == '__main__':
    npe = NeoPixelEmulator(8)
    sys.exit(npe.run(demos.ls_binary, demos.get_const_col))
