# -*- coding: utf-8 -*-

# LCD Commands
# ---------------------------------------------------------------------------
LCD_CLEARDISPLAY        = 0x01
LCD_RETURNHOME          = 0x02
LCD_ENTRYMODESET        = 0x04
LCD_DISPLAYCONTROL      = 0x08
LCD_CURSORSHIFT         = 0x10
LCD_FUNCTIONSET         = 0x20
LCD_SETCGRAMADDR        = 0x40
LCD_SETDDRAMADDR        = 0x80

# flags for display entry mode
# ---------------------------------------------------------------------------
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off and cursor control
# ---------------------------------------------------------------------------
LCD_DISPLAYON           = 0x04
LCD_CURSORON            = 0x02
LCD_BLINKON             = 0x01

# flags for display/cursor shift
# ---------------------------------------------------------------------------
LCD_DISPLAYMOVE         = 0x08
LCD_CURSORMOVE          = 0x00
LCD_MOVERIGHT           = 0x04
LCD_MOVELEFT            = 0x00

# flags for function set
# ---------------------------------------------------------------------------
LCD_8BITMODE            = 0x10
LCD_4BITMODE            = 0x00
LCD_2LINE               = 0x08
LCD_1LINE               = 0x00
LCD_5x10DOTS            = 0x04
LCD_5x8DOTS             = 0x00

# Define COMMAND and DATA LCD Rs (used by send method).
# ---------------------------------------------------------------------------
COMMAND                 = 0
DATA                    = 1
FOUR_BITS               = 2

# Microseconds
HOME_CLEAR_EXEC         = 2000
EXEC_TIME				= 37