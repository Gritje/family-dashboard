#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
# https://github.com/rm-hull/luma.led_matrix/blob/master/LICENSE.rst
# MIT License

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.render import canvas
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class LedMatrix():
    
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, width=32, height=8, block_orientation=90, blocks_arranged_in_reverse_order=False)
        print("Created device")
                
    def updateLedDisplay(self, msg):             
        with canvas(self.device) as draw:
            text(draw, (3, 0), msg, fill="white", font=proportional(TINY_FONT))

if __name__ == "__main__":
    led = LedMatrix()
    led.updateLedDisplay("test")