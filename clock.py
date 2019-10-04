
from __future__ import print_function
import os
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from papirus import Papirus

WHITE = 1
BLACK = 0

CLOCK_FONT_FILE = '/home/pi/weather-pi-data/fonts/Roboto-Black.ttf'

def main(argv):
    """main program - draw and display time and date"""

    papirus = Papirus(rotation = int(argv[0]) if len(sys.argv) > 1 else 0)
    papirus.clear()
    demo(papirus)

def demo(papirus):
    """simple partial update demo - draw a clock"""

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    clock_font_size = int((width - 4)/(8*0.65))      # 8 chars HH:MM:SS
    clock_font = ImageFont.truetype(CLOCK_FONT_FILE, 18)

    # clear the display buffer
    #draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    previous_second = 0
    previous_day = 0

    while True:
        while True:
            now = datetime.today()
            if now.second != previous_second:
                break
            time.sleep(0.1)

        if now.day != previous_day:
            #draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
            previous_day = now.day
        else:
           draw.rectangle((5, 10, width - 5, clock_font_size), fill=WHITE, outline=WHITE)

        draw.text((10, 10), '{h:02d}:{m:02d}:{s:02d}'.format(h=now.hour, m=now.minute, s=now.second), fill=BLACK, font=clock_font)

        # display image on the panel
        papirus.display(image)
        papirus.partial_update()
        previous_second = now.second


if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
