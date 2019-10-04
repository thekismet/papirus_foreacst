#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script will get the current weather forecast from     #
# Dark Sky and display a variety of stats on PiSupply's      #
# PaPiRus, including temperature, humidity, and the chance   #
# of rain.                                                   #
# Created by Wesley Archer (@raspberrycoulis)                #

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
import calendar

import datetime
from datetime import date, timedelta

from ConfigParser import ConfigParser

# Import details from config file to save typing
config = ConfigParser()
config.read('config/config.ini')
api_key = config.get('darksky', 'key')
latitude = config.get('darksky', 'latitude')
longitude = config.get('darksky', 'longitude')
units = config.get('darksky', 'units')

# For PaPiRus
screen = Papirus()
text = PapirusTextPos(True)
# text = PapirusText()

try:
    import darksky
except ImportError:
    exit("This script requires the Dark Sky Python API Wrapper\nInstall with: git clone https://github.com/raspberrycoulis/dark-sky-python.git\nThen run sudo python setup.py install in the directory")

def display():
    forecast = darksky.Forecast(api_key, latitude, longitude, units=units)
    current = forecast.currently
    daily = forecast.daily
    summary = current.summary
    summary = str(summary)
    temp = current.temperature
    temp = str(temp)
    humidity = current.humidity*100
    humidity = str(humidity)
    rain = current.precipProbability*100
    rain = str(rain)

    weekday = date.today()
    day_Name = date.strftime(weekday, '%A')
    day_month_year = date.strftime(weekday, '%Y %b %-d')

    try:
        screen.clear()
        print("Summary: "+summary+"\nTemperture: "+temp+" C\nHumidity: "+humidity+"%\nRain: "+rain+"%")
        text.AddText((day_Name) + ', ' + (day_month_year) + '\n' + (summary), 0, 0, 18, Id="Line1", fontPath='/home/pi/weather-pi-data/fonts/Roboto-Black.ttf')
        # text.AddText((day_Name) + ', ' + (day_month_year) + '\n' + (summary), 0, 0, 18, Id="Line1", fontPath='/home/pi/weather-pi-data/fonts/Roboto-Black.ttf')
        # text.AddText((summary), 0, 18, 14, Id="Line2", fontPath='/home/pi/weather-pi-data/fonts/Roboto-Bold.ttf')
        text.AddText('T: '+ (temp) + 'C ' + 'H: ' + (humidity) + '% R: ' + (rain) +'%', 0, 36, 14, Id="Line3", fontPath='/home/pi/weather-pi-data/fonts/Roboto-Bold.ttf')
        # text.write(""+summary+"\nTemp: "+temp+" C\nHumidity: "+humidity+"%\nRain: "+rain+"%", 18, fontPath='/home/pi/weather-pi-data/fonts/Roboto-Black.ttf', maxLines = 10)
    except:
        text.UpdateText("Line1", "Connection Error!")
        # text.write("Connection Error!", 18, fontPath='/home/pi/weather-pi-data/fonts/Roboto-Black.ttf', maxLines = 10)

try:
    while True:
        display()
        sleep(300)  # 5 minutes
        text.Clear()
except (KeyboardInterrupt, SystemExit):
    text.RemoveText("Line2")
    text.RemoveText("Line3")
    screen.clear()
    text.UpdateText("Line1", "Exiting...\nGoodbye!")
    # text.write("Exiting...\nGoodbye!", 18, fontPath='/home/pi/weather-pi-data/fonts/Roboto-Black.ttf', maxLines = 10)
    sleep(2)
    screen.clear()
    os._exit(1)

