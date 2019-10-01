#!/usr/bin/python
# Weather forecast for Raspberry Pi W with PaPiRus hat.
# Retrieves data from DarkSky.net's API, prints current conditions and
# Adapted from Adafruit Industries Python-Thermal-Printer forecast.py
# https://github.com/adafruit/Python-Thermal-Printer/blob/master/forecast.py  
# MIT license.
# 

from __future__ import print_function
from datetime import date
from datetime import datetime
from papirus import PapirusTextPos
import calendar
import urllib, json

text = PapirusTextPos(False)
fontsize = 10

#Dark Sky API Key goes here
API_KEY = "XXX"

#Put your location here
LAT = "37.5396"
LONG = "127.0097"

def forecast(idx):

    date = datetime.fromtimestamp(int(data['daily']['data'][idx]['time']))

    day     = calendar.day_name[date.weekday()]
    lo      = data['daily']['data'][idx]['temperatureMin']
    hi      = data['daily']['data'][idx]['temperatureMax']
    cond    = data['currently']['summary']
    nowtemp = data['currently']['temperature'] 

    #if there is a weather alert for the area get the title to print later.
    if 'alerts' in data:
	warn = data['alerts'][idx]['title'] 
    else:
        warn = None

#    uncomment these to print outputs to local shell/session    
#    print(day)
#    print('low :' + str(lo) )
#    print('high:' + str(hi))
#    print('' + cond.replace(u'\u2013', '-').encode('utf-8')) # take care of pesky unicode dash
#    print('current temp: ' + str(nowtemp))
#    if there is an alert print it rather than the summary
#    if warn is not None:
#       print('alerts: ' + str(warn)) 
#    else:
#       print('Summary: ' + cond.replace(u'\u2013', '-').encode('utf-8'))

    #The follow preapres the data to send to Papirus hat
    #Show Day 
    text.AddText((day), 0, 0, 18, Id="Line1", fontPath='/home/pi/PaPiRusWeather/fonts/Roboto-Bold.ttf')
    #Low temp and high temps for the day
    text.AddText(('low:' + str (lo) + ' high:' + str (hi)), 0, 30, fontsize, Id="Line2", fontPath='/home/pi/PaPiRusWeather/fonts/ElecSign.ttf') 
    #Show current temp
    text.AddText(('Currently:' + str (nowtemp)), 0, 40, fontsize, Id="line3",fontPath='/home/pi/PaPiRusWeather/fonts/ElecSign.ttf')
    #if there is an alert print it rather than the summary
    #if there is not an alert print the summary
    if warn is not None:
       text.AddText(('' + str (warn)), 0, 50, fontsize, Id="Line4", fontPath='/home/pi/PaPiRusWeather/fonts/ElecSign.ttf')
    else:
       text.AddText(('' + cond.replace(u'\u2013', '-').encode('utf-8')), 0, 50, fontsize, Id="Line4", fontPath='/home/pi/PaPiRusWeather/fonts/ElecSign.ttf') 
    
    #write it all out to the dispay
    text.WriteAll()


#get the weather data
url = "https://api.darksky.net/forecast/"+API_KEY+"/"+LAT+","+LONG+"?exclude=[minutely,hourly,flags]&units=auto"
response = urllib.urlopen(url)
data = json.loads(response.read())

forecast(0)
