"""
LiquidCrystal LCD library based on PyWiring.
"""

__all__ = ("LiquidCrystal",)

from .values import *
from numpy import uint8
import time

ms = 1./1000
us = 1./1000000
ps = 1./1000000000

def num2boolgen(num):
    for bit in reversed(bin(num)[2:]):
        yield bit == "1"

class LiquidCrystal(object):
    """
    Main LCD class. :py:obj:`ioi` must be a valid PyWiring I/O implementation
    instance. The I/O port must have at least 6 writable I/O pins (bl and
    rw can be left disconnected). You can override the pin numbers passing
    them to the constructor. Unused pins should be overridden with None.
    Currently only 4-bit mode is supported (do people even use 8-bit mode?)

    Defaults:

    ====== ======
    Pin Number
    ====== ======
    en       2
    rw       1
    rs       0
    data4    4
    data5    5
    data6    6
    data7    7
    bl       3
    ====== ======
    """

    def __init__(self, ioi, en=2, rw=1, rs=0, data=[4, 5, 6, 7], bl=3, cols=16, rows=2, charsize=LCD_5x8DOTS):
        if len(data) not in (4, 8):
            raise ValueError("data pins can only be 4 or 8")
        self._ioi = ioi
        self._en = en
        self._rw = rw
        self._rs = rs
        self._dpins = data
        self._bl = bl
        self._bl_sts_mask = 0
        self._displaycontrol = LCD_DISPLAYON | LCD_CURSORON | LCD_BLINKON
        self._displayfunction = LCD_4BITMODE
        self._displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

        if rows > 1:
            self._displayfunction |= LCD_2LINE
        self._rows = rows
        self._cols = cols

        # For some 1 line displays you can select a 10 pixel high font
        if charsize != LCD_5x8DOTS and rows == 1:
            self._displayfunction |= LCD_5x10DOTS
   
        # Values for properties
        self._display = False
        self._backlight = 0
        self._cursor = False
        self._blink = False
        self._ltr = True
        self._autoscroll = False

        # Make all data pins outputs
        for i in self._dpins:
            self._ioi.pin_mode(i, False)

        self._ioi.pin_mode(self._rs, False)
        if self._rw is not None:
            self._ioi.pin_mode(self._rw, False)
        if self._bl is not None:
            self._ioi.pin_mode(self._bl, False)
        self._ioi.pin_mode(self._en, False)

        tow = {} # Avoid multiple digital_writes
        tow[self._rs] = False
        tow[self._en] = False
        if self._rw is not None:
            tow[self._rw] = False
        if self._bl is not None:
            tow[self._bl] = False
        self._ioi.digital_write_bulk(tow)

        # Initialize the display

        # SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
        # according to datasheet, we need at least 40ms after power rises above 2.7V
        # before sending commands. Arduino can turn on way before 4.5V so we'll wait 
        # 50
        self._sleep(100*ms)

        # Put LCD into 4-bit mode
        self.send(0b11)
        self._sleep(4.5*ms) # wait more than 4.1ms

        self.send(0b11)
        self._sleep(150*us)

        self.send(0b11)

        self._sleep(ms)
        self.send(0b10)
      
        self.send(LCD_FUNCTIONSET | self._displayfunction, COMMAND)
        self.send(LCD_DISPLAYCONTROL | self._displaycontrol, COMMAND)
        self._display = True
        self.clear()
        self.send(LCD_ENTRYMODESET | self._displaymode, COMMAND)

        self.backlight = True

    @property
    def backlight(self):
        """
        Set the backlight brightness, if backlight pin was set in the
        constructor. If the pin is a PWM pin, brightness can also be
        adjusted (0-255), otherwise it can only be turned on or off
        (True-False)
        """
        return self._backlight
    @backlight.setter
    def backlight(self, value):
        if self._bl is None:
            return
        self._ioi.analog_write(self._bl, value)
        self._backlight = value

    @property
    def display(self):
        """
        Show or hide content from the display.
        """
        return self._display
    @display.setter
    def display(self, value):
        if value:
            self._displaycontrol |= LCD_DISPLAYON
        else:
            self._displaycontrol &= ~uint8(LCD_DISPLAYON)
        self.send(LCD_DISPLAYCONTROL | self._displaycontrol, COMMAND)
        self._display = value
    
    @property
    def cursor(self):
        """
        Show or hide the cursor (usually an underscore).
        """
        return self._cursor
    @cursor.setter
    def cursor(self, value):
        if value:
            self._displaycontrol |= LCD_CURSORON
        else:
            self._displaycontrol &= ~uint8(LCD_CURSORON)
        self.send(LCD_DISPLAYCONTROL | self._displaycontrol, COMMAND)
        self._cursor = value
    
    @property
    def blink(self):
        """
        Enable or disable cursor blinking (usually a blinking block)
        """
        return self._blink
    @blink.setter
    def blink(self, value):
        if value:
            self._displaycontrol |= LCD_BLINKON
        else:
            self._displaycontrol &= ~uint8(LCD_BLINKON)
        self.send(LCD_DISPLAYCONTROL | self._displaycontrol, COMMAND)
        self._blink = value

    def scroll_display_left(self):
        """
        Scroll the whole display one character to the right. Cursor position
        will be affected, reset with :py:meth:`~LiquidCrystal.home`.
        """
        self.send(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT, COMMAND)

    def scroll_display_right(self):
        """
        Like :py:meth:`~LiquidCrystal.scroll_display_left`, to the right.
        """
        self.send(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT, COMMAND)

    @property
    def ltr(self):
        """
        Write new characters from left to right.
        """
        return self._ltr
    @ltr.setter
    def ltr(self, value):
        if value:
            self._displaymode |= LCD_ENTRYLEFT
        else:
            self._displaymode &= ~uint8(LCD_ENTRYLEFT)
        self.send(LCD_ENTRYMODESET | self._displaymode, COMMAND)
        self._ltr = value

    @property
    def rtl(self):
        """
        Write new characters from right to left.
        """
        return not self._ltr
    @rtl.setter
    def rtl(self, value):
        self.ltr = not value

    def move_cursor_right(self):
        """
        Move the cursor one character to the right.
        """
        self.send(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVERIGHT, COMMAND)

    def move_cursor_left(self):
        """
        Move the cursor one character to the left.
        """
        self.send(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVELEFT, COMMAND)

    @property
    def autoscroll(self):
        """
        This will 'right justify' text from the cursor, if True.
        """
        return self._autoscroll
    @autoscroll.setter
    def autoscroll(self, value):
        if value:
            self._displaymode |= LCD_ENTRYSHIFTINCREMENT
        else:
            self._displaymode &= ~uint8(LCD_ENTRYSHIFTINCREMENT)
        self.send(LCD_ENTRYMODESET | self._displaymode, COMMAND)
        self._autoscroll = value

    def create_char(self, location, char):
        """
        Create a new custom character. Location (0-7) is the character
        position in memory. Char is a sequence of integers. Each integers
        is a binary representation of the character. For example:

        char = [
          0b00000,
          0b01010,
          0b11111,
          0b11111,
          0b01110,
          0b00100,
          0b00000,
          0b00000]

        create_char(0, char)

        The sample character is a heart.

        A character generator can be found at
        http://mikeyancey.com/hamcalc/lcd_characters.php
        """
        location &= 0x7 # we only have 8 locations 0-7
   
        self.send(LCD_SETCGRAMADDR | (location << 3), COMMAND)
        self._sleep(30*us)
   
        for i in char[0:8]:
            self.send(i, DATA)
            self._sleep(40*us)

    def write(self, value):
        """
        Write a raw data byte to the display. Can be used to draw
        non-standard character (check the datasheet for more info)
        or to draw custom characters by passing their location.
        """
        self.send(value, DATA)

    def print_str(self, string):
        """
        Print an ASCII string to the display.
        """
        for c in string:
            self.write(ord(c))

    def clear(self):
        """
        Clear the display and move the cursor home (:py:meth:`~LiquidCrystal.home`).
        """
        self.send(LCD_CLEARDISPLAY, COMMAND)
        self._sleep(HOME_CLEAR_EXEC*us)

    def home(self):
        """
        Move the cursor to the first character. Also resets any display
        scrolls.
        """
        self.send(LCD_RETURNHOME, COMMAND)
        self._sleep(HOME_CLEAR_EXEC*us)

    def set_cursor(self, row, col):
        """
        Move cursor to the desired position. Positions start from 0.
        """
        row_offsets_def = [0x00, 0x40, 0x14, 0x54]
        row_offsets_large = [0x00, 0x40, 0x10, 0x50]
        
        if row >= self._rows:
            row = self._rows - 1

        # 16x4 LCDs have special memory map layout
        if self._cols == 16 and self._rows == 4:
            self.send(LCD_SETDDRAMADDR + (col + row_offsets_large[row]), COMMAND)
        else:
            self.send(LCD_SETDDRAMADDR + (col + row_offsets_def[row]), COMMAND)

    def send(self, value, mode=FOUR_BITS):
        """
        Sends a particular value to the LCD for writing to the LCD or
        as an LCD command.
    
        Users should never call this method.
    
        :py:obj:`value`: Value to send to the LCD.

        :py:obj:`mode`:

        ============================= ============================
        :py:const:`values.DATA`       Write to the LCD CGRAM
        :pyy:const:`values.COMMAND`   Write a command to the LCD
        :pyy:const:`values.FOUR_BITS` Write 4 bits to the LCD
        ============================= ============================
        """
        if mode == FOUR_BITS:
            self.write_bits(value & 0x0F, 4, COMMAND)
        else:
            self.write_bits(value >> 4, 4, mode)
            self.write_bits(value & 0x0F, 4, mode)
        self._sleep(EXEC_TIME*us)

    def pulse_enable(self, tow=None):
        """
        Sends a pulse of 1 us to the Enable pin to execute a command
        or write operation.
        """
        if tow:
            tow[self._en] = True
            self._ioi.digital_write_bulk(tow)
        else:
            self._ioi.digital_write(self._en, True)
        self._sleep(us)
        self._ioi.digital_write(self._en, False)

    def write_bits(self, value, nbits, mode=DATA):
        """
        Write some bits to the display. Value must be an integer,
        nbits is the number of bits to send. If mode == DATA, the
        rs pin will be pulled high before writing.
        """
        tow = {}
        # If an rw pin was specified, pull it low to write
        if self._rw is not None:
            tow[self._rw] = False

        bits = [i for i in num2boolgen(value)][:nbits]
        if len(bits) < nbits:
            bits += [False] * (nbits-len(bits))
        for pin, bit in zip(self._dpins, bits):
            tow[pin] = bit

        # If mode is DATA, pull rs pin high
        tow[self._rs] = mode == DATA

        # Write all pins in one operation
        self.pulse_enable(tow)

    def _sleep(self, t):
        """
        Sleep only if transactions won't take longer than the requested
        time, making writes faster.
        """
        # Don't sleep if read/write transactions take longer than that
        if t > self._ioi.avg_exec_time:
            time.sleep(t - self._ioi.avg_exec_time)