#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 19:19:36 2018

@author: Chunyan
"""

from urllib.request import urlopen
import re
from datetime import datetime
import time
import mysql.connector
import _thread
from queue import Queue

import seekingalpha as seek # Captcha
import tradingview as trading
import marketwatch as market
import datetime
#web_url='https://finance.yahoo.com/quote/ALGN/history?p=ALGN'


#hosturl="35.245.69.105"
hosturl 	= "35.245.69.105"
dbuser 		= "root"
dbpassoword = "admin123456"
dbname 		= "Stock_Prediction"
table_name = ['tbl_ALIGN', 'tbl_IBM', 'tbl_AAL', 'tbl_POLY', 'tbl_RRS']
realtime_table = "tbl_Realtime"
top_table = "tbl_TopGL"

def compare(date1, date2):
    if(date1==""):
        return true
    else:
        date1 = datetime.strptime (date1, '%b %d, %Y')
        date2 = datetime.strptime (date2, '%b %d, %Y')
        return date1 < date2

def DataToSql(data1, data2, data3):
    try:
        mydb = mysql.connector.connect(
              host      = hosturl,
              user      = dbuser,
              passwd    = dbpassoword,
              database  = dbname
        )
        mycursor = mydb.cursor()
        mydatetime = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
        for y in range(5):            
            datastr = ""
            for x in range(26):
                datastr = datastr + "'" + data1[y][x] + "'" + ","
            # datastr = datastr + "'"+ data1[table_index][25] +"'"
            for x in range(2):
                datastr = datastr + "'" + data2[y][x] + "'" + ","
            
            datastr = datastr + "'" + data3[y][0] + "'" + ","
            datastr = datastr + "'" + data3[y][1] + "'" + ","

            datastr = datastr + "'" + "20" + mydatetime + "'"
            # print("20"+datetime.datetime.now().strftime("%y-%m-%d %H:%M")) 
            
            datastr = "(" + datastr + ")"

            # print(datastr)
            
            sql = "INSERT INTO "+table_name[y]+" (MarketCapitalisation, PBPrictoBookRatio, QuickRatio, CurrentRatio, DEDebttoEquityRatio, ReturnonAssets, ReturnonEquity, ReturnonInvestedCapital, NetMargin, GrossMargin, OperatingMargin, PreTaxMargin, Volume, DayRangeLow, DayRangeHigh, PE, Beta, Dividend, DividendYield, WeekRangeLow52, WeekRangeHigh52, Price, Low, High, ChangeValue, ChangePercent, Open, Close, Recommendations, TargetPrice, Date) VALUES "+datastr
            mycursor.execute(sql)
            mydb.commit()
        mycursor.close()
        mydb.close()
        print("Stock Success")
            
    except Exception as e: print(e)


def RealTimeDataToSql(data):
    try:
        mydb = mysql.connector.connect(
              host      = hosturl,
              user      = dbuser,
              passwd    = dbpassoword,
              database  = dbname
        )
        mycursor = mydb.cursor()
        mydatetime = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
        for y in range(5):            
            datastr = ""
            for x in range(12):
                datastr = datastr + "'" + data[y][x] + "'" + ","

            datastr = datastr + "'" + "20" + mydatetime + "'"
            # print("20"+datetime.datetime.now().strftime("%y-%m-%d %H:%M")) 
            
            datastr = "(" + datastr + ")"

            # print(datastr)
            
            sql = "INSERT INTO "+realtime_table+" (Status, Price, ChangeValue, ChangePercent, Volume, Low, High, EPS, PE, DivYield, MarketCapitalization, Stockname,  Date) VALUES "+datastr
            mycursor.execute(sql)
            mydb.commit()

        mycursor.close()
        mydb.close()
        print("Realtime SUccesssss")
    except Exception as e: print(e)

def GLtoSql(data):
    try:
        mydb = mysql.connector.connect(
              host      = hosturl,
              user      = dbuser,
              passwd    = dbpassoword,
              database  = dbname
        )
        mycursor = mydb.cursor()
        sql = "DELETE FROM " + top_table + " WHERE 1=1"
        mycursor.execute(sql)
        mydb.commit()
        for x in range(8):
            datastr = ""
            
            datastr = datastr + "'" + data[x][0] + "'" + ","
            datastr = datastr + "'" + data[x][1] + "'"
            
            datastr = "(" + datastr + ")"

            sql = "INSERT INTO "+top_table+" (Tickername, ChangePercent) VALUES "+datastr
            mycursor.execute(sql)
            mydb.commit()
            
        mycursor.close()
        mydb.close()
        print("TopGainerLoser SUccesssss")
    except Exception as e: print(e)

# GET DATA VIA SCRAPPING

def getData():
    while 1:
        print("Hi")
        start_time = time.time()
        datas1 = trading.realtime()
        datas2 = market.realtime1()
        datas3 = market.realtime2()
        DataToSql(datas1, datas2, datas3)
        time.sleep(3500)

def getRealTimeData():
    while 1:
        datas = trading.getrealtimedata()
        
        RealTimeDataToSql(datas)
        time.sleep(30)

def getGL():
    while 1:
        start_time = time.time()
        datas = market.getGL()
        GLtoSql(datas)
        time.sleep(30)

def main():
	try:
         _thread.start_new_thread( getData, () )
         _thread.start_new_thread( getRealTimeData, () )
         _thread.start_new_thread( getGL, () )
	except:
		print ("Error: unable to start thread")
	while 1:
		pass
main()