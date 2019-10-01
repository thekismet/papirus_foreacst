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
fontsize = 15

#Dark Sky API Key goes here
API_KEY = ""

#Put your location here
LAT = "45.4324893"
LONG = "-122.3778252"

def forecast(idx):

    date = datetime.fromtimestamp(int(data['daily']['data'][idx]['time']))

    day     = calendar.day_name[date.weekday()]
    lo      = data['daily']['data'][idx]['temperatureMin']
    hi      = data['daily']['data'][idx]['temperatureMax']
    cond    = data['daily']['data'][idx]['summary']
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
    text.AddText((day),0,0,20,Id="Line1")
    #Low temp and high temps for the day
    text.AddText(('low:' + str (lo) + ' high:' + str (hi)), 0, 20, fontsize, Id="Line2" ) 
    #Show current temp
    text.AddText(('Currently:' + str (nowtemp)),0,40,fontsize, Id="line3")
    #if there is an alert print it rather than the summary
    #if there is not an alert print the summary
    if warn is not None:
       text.AddText(('' + str (warn)), 0, 60, fontsize, Id="Line4")
    else:
       text.AddText(('' + cond.replace(u'\u2013', '-').encode('utf-8')), 0, 60, fontsize, Id="Line4") 
    
    #write it all out to the dispay
    text.WriteAll()


#get the weather data
url = "https://api.darksky.net/forecast/"+API_KEY+"/"+LAT+","+LONG+"?exclude=[minutely,hourly,flags]&units=us"
response = urllib.urlopen(url)
data = json.loads(response.read())

forecast(0)