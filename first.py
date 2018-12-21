#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 19:19:36 2018

@author: Chunyan
"""

from urllib.request import urlopen
import re
import datetime
import time
import mysql.connector
import tradingview as tv
#web_url='https://finance.yahoo.com/quote/ALGN/history?p=ALGN'

print("Hi ! Welcome to yahoo finance Scrappe by Chunyan...")
print("Note : In every minute data will be saved \n  ")


#hosturl="35.245.69.105"
hosturl 	= "35.245.69.105"
dbuser 		= "root"
dbpassoword = "admin123456"
dbname 		= "DataAnalysis"

def realtimedatatomysql(realTimeData):
    try:
        mydb = mysql.connector.connect(
          host 		= hosturl,
          user 		= dbuser,
          passwd 	= dbpassoword,
          database 	= dbname
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO RealTimeData (TickerName, isOpen, CurrentValue, ChangeValue, ChangeInPercent, Volume, LowValue, HighValue, EPS, MktCamp, PE, DividendYield) VALUES (%s,%s,%s, %s,%s, %s,%s, %s,%s,%s, %s, %s)"
        #INSERT INTO `RealTimeData` (`id`, `TickerName`, `isOpen`, `CurrentValue`, `ChangeValue`, `ChangeInPercent`, `Volume`, `LowValue`, `HighValue`, `EPS`, `MktCamp`, `PE`, `ForwardPE`, `Dividend`, `DividendYield`) VALUES (ABS(''), AES_DECRYPT('',''), '', '', '', '', '', '', '', '', '', '', '', '', '')
        # val = (tuple(valuestring))
        # valuestring = []

        lastIndex = len(realTimeData)
        for i in range(0,lastIndex):
        	val = tuple(realTimeData[i])
        	print(val)
        	mycursor.execute(sql, val)
        	mydb.commit()
        mycursor.close()
        mydb.close()
    except Exception as e: print(e) 

def mainfunctin():
    realTimeData = tv.Realtime()
    realtimedatatomysql(realTimeData)
    time.sleep(60)
    mainfunctin()
       
mainfunctin()