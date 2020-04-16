login as: pi
     ┌────────────────────────────────────────────────────────────────────┐
     │                        • MobaXterm 12.1 •                          │
     │            (SSH client, X-server and networking tools)             │
     │                                                                    │
     │ ➤ SSH session to pi@192.168.10.4                                   │
     │   • SSH compression : ✔                                            │
     │   • SSH-browser     : ✔                                            │
     │   • X11-forwarding  : ✔  (remote display is forwarded through SSH) │
     │   • DISPLAY         : ✔  (automatically set on remote server)      │
     │                                                                    │
     │ ➤ For more info, ctrl+click on help or visit our website           │
     └────────────────────────────────────────────────────────────────────┘

Linux papirus 4.19.66+ #1253 Thu Aug 15 11:37:30 BST 2019 armv6l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Apr 14 12:30:55 2020 from 192.168.10.14
pi@papirus:~ $ ls
clock  darkskylib  papi  papirus  PaPiRus  papirus-clock.py  papirus_display  PaPiRusWeather  pihat_weather  Pi-Weather  projects  weatherPapirus  weather-pi-data
pi@papirus:~ $ cd weather-pi-data
pi@papirus:~/weather-pi-data $ ls
blinkt-rain.py  blinkt-uvindex.py  clock2.py  clock.py  config  darksky-dot3k.py  darksky-papirus.py  fonts  papi2.py  papi3.py  papi4.py  papi5.py  papi6.py  papi7.py  papi.py  papirus-clock.py
pi@papirus:~/weather-pi-data $ nano papi6.py
  GNU nano 2.7.4                                                                                   File: papi6.py

from __future__ import print_function

import os
import sys

from papirus import Papirus, PapirusText, PapirusTextPos
from time import sleep

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
import datetime
from datetime import date, timedelta

from darksky import forecast
import textwrap

# set lat/long for location
LOCATION = 37.5396,127.0097 #put your longitude and latittude here in decimal degrees
UNITS = 'auto' #specify the units you want your results in here, see the Dark Sky API docs page for details

# set Darksky API Key
APIKEY= '8aee1d750d1d9085dd42452f730bd6c6' # put your Dark Sky API key here. Get one at https://darksky.net/dev

# For PaPiRus
screen = Papirus()
text = PapirusTextPos(True)

# tempFont = ImageFont.truetype('fonts/Aller_Bd.ttf', 22)
# dayFont = ImageFont.truetype('fonts/Roboto-Black.ttf', 18)
# dateFont = ImageFont.truetype('fonts/Roboto-Bold.ttf', 14)
# font = ImageFont.truetype('fonts/ElecSign.ttf', 10)
# smallFont = ImageFont.truetype('fonts/ElecSign.ttf', 8)
# smallestFont = ImageFont.truetype('fonts/ElecSign.ttf', 7)

def display():
    with forecast (APIKEY, *LOCATION, units=UNITS) as location:
        # today
        currentTemp = location['currently']['temperature']
        upcoming_conditions = location['currently']['summary']
        relativeHumidity = location['currently']['humidity']
        daily_conditions = location['daily']['data'][0]['summary']
        highTemp = location['daily']['data'][0]['temperatureHigh']
        lowTemp = location['daily']['data'][0]['temperatureLow']
        iconDesc = location['currently']['icon']
        # tomorrow
        summary2 = location['daily']['data'][1]['summary']
        iconDesc2 = location['daily']['data'][1]['icon']
        highTemp2 = location['daily']['data'][1]['temperatureHigh']
        lowTemp2 = location['daily']['data'][1]['temperatureLow']

    currentCondFormatted = upcoming_conditions
    temp = '{0:.2f}'.format(currentTemp) + 'C'
    humidity = '{0:.0f}'.format(relativeHumidity*100) + '%'
    tempsToday = 'High ' + '{0:.0f}'.format(highTemp) + ' Low ' + '{0:.0f}'.format(lowTemp)
    tempsTomorrow = 'High ' + '{0:.0f}'.format(highTemp2) + ' Low ' + '{0:.0f}'.format(lowTemp2)

    weekday = date.today()
    day_Name = date.strftime(weekday, '%A')
    day_month_year = date.strftime(weekday, '%Y %b %-d')
    
    weekday2 = datetime.date.today() + datetime.timedelta(days=1)
    day2 = date.strftime(weekday2, '%a')

    try:
        screen.clear()
        print("Summary: "+currentCondFormatted+"\nTemperture: "+temp+" ")
        text.AddText((day_Name) + ' ' + (day_month_year) + '\n' + (temp) + ' ' + (humidity) + '\n' + (tempsToday) + '\n' + (currentCondFormatted) + '\n' + (day2) + ' - ' + (tempsTomorrow) + ' ' + (summary2)$
        # text.AddText((day2) + ' - ' + (tempsTomorrow) + ' ' + (summary2), 0, 60, 10, Id="Lin2", fontPath='/home/pi/weather-pi-data/fonts/ElecSign.ttf')

    except:
        text.UpdateText("Line1", "Connection Error!")

try:
    while True:
        display()
        sleep(300)  # 5 minutes
        text.Clear()
except (KeyboardInterrupt, SystemExit):
    # text.RemoveText("Line2")
    screen.clear()
    text.UpdateText("Line1", "Exiting...\nGoodbye!")
    sleep(2)
    screen.clear()
    os._exit(1)
