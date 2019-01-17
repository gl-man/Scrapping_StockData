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

import tradingview as trading
import marketwatch as market
import datetime

hosturl 	= "35.197.135.249"
dbuser 		= "root"
dbpassoword = "password"
dbname 		= "stockprediction"
stock_table_name = ['tbl_align', 'tbl_ibm', 'tbl_aal', 'tbl_poly', 'tbl_rrs']
ticker_table_name = ['ticker_usa', 'ticker_europe', 'ticker_asia', 'ticker_fx', 'ticker_crypto']
realtime_table = "tbl_Realtime"
top_table = "tbl_topStock"

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
            for x in range(2):
                datastr = datastr + "'" + data2[y][x] + "'" + ","
            
            datastr = datastr + "'" + data3[y][0] + "'" + ","
            datastr = datastr + "'" + data3[y][1] + "'" + ","

            datastr = datastr + "'" + "20" + mydatetime + "'"
            
            datastr = "(" + datastr + ")"
            
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
            
            datastr = "(" + datastr + ")"
            
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

            sql = "INSERT INTO "+top_table+" (StockName, ChangePercent) VALUES "+datastr
            mycursor.execute(sql)
            mydb.commit()
            
        mycursor.close()
        mydb.close()
        print("TopGainerLoser SUccesss!")
    except Exception as e: print(e)

def TickerToSql(data):
    try:
        mydb = mysql.connector.connect(
              host      = hosturl,
              user      = dbuser,
              passwd    = dbpassoword,
              database  = dbname
        )
        mycursor = mydb.cursor()
        for i in range(5):
            sql = "DELETE FROM " + ticker_table_name[i] + " WHERE 1=1"
            mycursor.execute(sql)
            mydb.commit()

            for j in range(6):
                datastr = ""                    
                datastr = datastr + "'" + data[i][0][j] + "'" + ","
                datastr = datastr + "'" + data[i][1][j] + "'" + ","
                datastr = datastr + "'" + data[i][2][j] + "'" + ","
                datastr = datastr + "'" + data[i][3][j] + "'"                
                datastr = "(" + datastr + ")"

                sql = "INSERT INTO "+ticker_table_name[i]+" (symbol, price, changevalue, percent) VALUES "+datastr
                mycursor.execute(sql)
                mydb.commit()
            
        mycursor.close()
        mydb.close()
        print("TickerData Saved Successfully!")
    except Exception as e: print(e)

def StockToSql(data):
    try:
        mydb = mysql.connector.connect(
              host      = hosturl,
              user      = dbuser,
              passwd    = dbpassoword,
              database  = dbname
        )
        mycursor = mydb.cursor()
        for i in range(5):

            sql = "DELETE FROM " + stock_table_name[i] + " WHERE 1=1"
            mycursor.execute(sql)
            mydb.commit()

            datastr = ""

            for j in range(28):                                    
                datastr = datastr + "'" + data[i][j] + "'" + ","               
            
            datastr = datastr + "'" + data[i][28] + "'"
            datastr = "(" + datastr + ")"
            
            sql = "INSERT INTO " + stock_table_name[i] + " (symbolName, marketType, price, changeValue, changePercent, open, marketCap, sharesOutstanding, publicFloat, beta, revPerEmployee, peRatio, eps, yield, dividend, exdividendDate, shortInterest, floatShorted, averageVolume, dayLow, dayHigh, weekLow52, weekHigh52, week1, month1, month3, ytd, year1, volume) VALUES " + datastr

            mycursor.execute(sql)
            mydb.commit()
            
        mycursor.close()
        mydb.close()
        print("StockData Saved Successfully!")
    except Exception as e: print(e)


def getData():
    while 1:
        print("Hi")
        start_time = time.time()
        datas1 = trading.realtime()
        datas2 = market.realtime1()
        datas3 = market.realtime2()
        DataToSql(datas1, datas2, datas3)
        execute_time = time.time() - start_time
        if(execute_time > 3600):
            time.sleep(0)
        else:
            time.sleep(3600 - execute_time)

def getRealTimeData():
    while 1:
        start_time = time.time()
        datas = trading.getrealtimedata()
        RealTimeDataToSql(datas)
        execute_time = time.time() - start_time
        if(execute_time > 60):
            time.sleep(0)
        else:
            time.sleep(60 - execute_time)

def getGL():
    while 1:
        start_time = time.time()
        datas = market.getGL()
        GLtoSql(datas)
        execute_time = time.time() - start_time
        time.sleep(1)
        # if(execute_time > 60):
        #     time.sleep(0)
        # else:
        #     time.sleep(60 - execute_time)


def getTopGL():
    while 1:
        start_time = time.time()
        datas = trading.getTopGL()
        # GLtoSql(datas)
        execute_time = time.time() - start_time
        if(execute_time > 60):
            time.sleep(0)
        else:
            time.sleep(60 - execute_time)


def getTickerRealTimeData():
    while 1:
        start_time = time.time()
        datas = market.getTickerRealTimeData()
        TickerToSql(datas)
        execute_time = time.time() - start_time
        print(execute_time)
        time.sleep(1)
        # if(execute_time > 40):
        #     time.sleep(0)
        # else:
        #     time.sleep(40 - execute_time)    



def getStockData():
    while 1:
        start_time = time.time()
        datas = market.getStockData()
        StockToSql(datas)
        execute_time = time.time() - start_time
        print("Stock Scrapping Time:", execute_time)
        time.sleep(1)
        # if(execute_time > 60):
        #     time.sleep(0)
        # else:
        #     time.sleep(60 - execute_time)

def main():
	try:
         # _thread.start_new_thread( getData, () )
         # _thread.start_new_thread( getRealTimeData, () )
         _thread.start_new_thread( getGL, () )
         # _thread.start_new_thread( getTickerRealTimeData, () )
         # _thread.start_new_thread( getTopGL, () ) #to get ticker realtime data
         _thread.start_new_thread( getTickerRealTimeData, () )
         _thread.start_new_thread( getStockData, () )
	except:
		print ("Error: unable to start thread")
	while 1:
		pass
main()