# LiquidCrystal for Python
A Python port of Arduino's LiquidCrystal library that uses PyWiring to access an HD44780-based LCD display through any supported I/O port.

Make sure [PyWiring](https://github.com/Davideddu/python-pywiring) is installed (setuptools installer coming soon for both PyWiring and LiquidCrystal - for now, just make sure it's in your PYTHONPATH).

## Usage
First, get an instance of any PyWiring I/O port that has at least 6 digital outputs. For example, you can use `pywiring.i2c.PCF8574IO` for an I²C I/O port or *"LCD backpack"* based on the PCF8574 (like [this one](http://www.dx.com/p/216865?Utm_rid=14976370&Utm_source=affiliate)), or `pywiring.parport.ParallelIO` for a standard parallel port.

```python
from pywiring import i2c
ioi = i2c.PCF8574IO(1, 0x27)
# 1 is the I²C bus, 0x27 is the I/O port address.
# Read the I/O implementation documentation for further info.
```

Now you only need to pass the I/O implementation instance to `liquidcrystal.LiquidCrystal`. Make sure your pin numbers are correct. Default values are for the [aforementioned LCD backpack](http://www.dx.com/p/216865?Utm_rid=14976370&Utm_source=affiliate). Beware that only 4-bit mode is currently supported. You can set the R/W and the backlight pins (rw and bl) to None if you're not connecting them.

```python
from liquidcrystal import LiquidCrystal
# No argument is required except for the I/O implementation.
# The values shown below are the default ones.
lcd = LiquidCrystal(ioi, en=2, rw=1, rs=0, data=[4, 5, 6, 7], bl=3, cols=16, rows=2)
```

The LCD will be immediately initialized and ready to use.

## Methods

### print_str(`string`)
Prints an ASCII string to the display

### set_cursor(`row`, `col`)
Moves the cursor to the desired location (locations start from 0).

### write(`char`)
Write a custom character to the display. `char` must be an integer between 0 and 255.

### clear()
Clears the display and moves the cursor to the first location. Also resets any display scrolls.

### home()
Moves the cursor to the first location. Also resets any display scrolls.

### create_char(`location`, `char`)
Create a new custom character. Location (0-7) is the character position in memory. Char is a sequence of integers. Each integers is a binary representation of the character. For example:

```python
char = [
  0b00000,
  0b01010,
  0b11111,
  0b11111,
  0b01110,
  0b00100,
  0b00000,
  0b00000]

lcd.create_char(0, char)
```

The sample above character is a heart.

A character generator can be found at http://mikeyancey.com/hamcalc/lcd_characters.php.

### move_cursor_right(), move_cursor_left()
Move the cursor one character to the desired direction.

### scroll_display_right(), scroll_display_left()
Scroll the whole display one character to the desired direction. Cursor position will be affected, reset with `home` or `clear`.

### send(`value`, `mode=values.FOUR_BITS`)
**Note:** you shouldn't need this method at all. Use it only if you know what you're doing.

Send a value to the display. `value` must be an integer between 0 and 255. `mode` can be `values.FOUR_BITS`, `values.DATA` or `values.COMMAND`. In four bit mode, only the lower 4 bits will be sent, with the register select pin low. In data and command mode, the whole byte will be sent, with the rs pin high in data mode or low in command mode.

## Properties
If you don't know what properties are, make sure you read [this](http://itmaybeahack.com/book/python-2.6/html/p03/p03c05_properties.html#properties) and [this](https://en.wikipedia.org/wiki/Property_%28programming%29). Basically, they just act like attributes, but under the hood there's much more going on.

### backlight (default: 255)
Display brightness in a range between 0 and 255. If your I/O port does not support PWM (a.k.a. `analogWrite`), the backlight will be off if set to 0 or False, and on if greater than 0 or True.

### display (default: True)
Show or hide content from the display.

### cursor (default: False)
Show or hide the cursor (usually an underscore).

### blink (default: False)
Enable or disable cursor blinking (usually a blinking block)

### ltr and rtl (default: ltr = True)
Set the character writing direction (left to right, right to left). Note that when one is set to True, the other one is False, and viceversa (they can't both be True, it wouldn't even make sense).

### autoscroll (default: False)
This will 'right justify' text from the cursor, if True.
