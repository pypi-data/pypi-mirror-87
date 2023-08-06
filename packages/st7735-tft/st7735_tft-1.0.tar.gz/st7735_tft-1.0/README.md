# ST7735 TFT
This python library is to interface with LCD displays based on the ST7735 chip.  
It is based on [ST7735 by Pimoroni](https://github.com/pimoroni/st7735-python), but made to be faster when only updating a section of the screen.
- Only updates the pixels that have changed since the last screen update
- Can use `pigpio` or `RPi.GPIO` libraries

