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
import tradingview as tv
import yahoofinancial as yahoo
import _thread
from queue import Queue
#web_url='https://finance.yahoo.com/quote/ALGN/history?p=ALGN'

print("Hi ! Welcome to yahoo finance Scrappe by Chunyan...")
print("Note : In every minute data will be saved \n  ")


#hosturl="35.245.69.105"
hosturl 	= "35.245.69.105"
dbuser 		= "root"
dbpassoword = "admin123456"
dbname 		= "DataAnalysis"

def compare(date1, date2):
    if(date1==""):
        return true
    else:
        date1 = datetime.strptime (date1, '%b %d, %Y')
        date2 = datetime.strptime (date2, '%b %d, %Y')
        return date1 < date2

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
        lastIndex = len(realTimeData)
        for i in range(0,lastIndex):
        	val = tuple(realTimeData[i])
        	# print(val)
        	mycursor.execute(sql, val)
        	mydb.commit()
        mycursor.close()
        mydb.close()
    except Exception as e: print(e) 

def historicaldatatomysql(data, tbname):
    try:
        mydb = mysql.connector.connect(
          host 		= hosturl,
          user 		= dbuser,
          passwd 	= dbpassoword,
          database 	= dbname
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO " + tbname + " (DateStamp, Open, High, Low, Close, Adj_Close, Volume) VALUES (%s, %s,%s,%s, %s,%s, %s)"
        sql1 = "SELECT * FROM " + tbname + " ORDER BY id DESC LIMIT 1"
        print(sql)
        mycursor.execute(sql1)
        temp = mycursor.fetchall()
        isEmpty = mycursor.rowcount
        print(isEmpty)
        print(type(isEmpty))
        # print("--------LatestOne---------")
        # print(temp)
        # print("--------------------------")
        # lastIndex = len(data)
        for record in data:
            # print("*******************")
            # print(record)
            # print("*******************")
            val = tuple(record)
            print("*************************")
            print(val)
            print(val[0])
            print("*************************")
            if isEmpty==0:
                print("insert")
                mycursor.execute(sql, val)
            elif compare(temp[0][1], val[0]):
                mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        print("InsertDB completed")
    except Exception as e: print(e) 

def getRealTime():
	while 1:
		print("RealTime")
		realTimeData = tv.realtime()
		print(realTimeData)
		realtimedatatomysql(realTimeData)
		time.sleep(60)

def getHistory():
    tbnamelist = ['tb_history_ALIGN', 'tb_history_IBM', 'tb_history_Anglo', 'tb_history_Polymetal', 'tb_history_Randgold']
    while 1:
        print('History')
        datas=yahoo.getHistoryData()
        print("########################")
        print(datas)
        print("########################")
        index = 0
        for data in datas:
            print("insert one company start")
            print(data)
            historicaldatatomysql(data,tbnamelist[index])
            index=index+1
            time.sleep(2)
            print("insert one company complete")
        print("all company completed")
        time.sleep(3600)

def main():
	# t1 = threading.Thread(target = getRealTime)
	# t1.daemon = True
	# t2 = threading.Thread(target = getHistory)
	# t2.daemon = True
	# t1.start()
	# t2.start()
	try:
		# _thread.start_new_thread( getRealTime, () )
		_thread.start_new_thread( getHistory, () )
	except:
		print ("Error: unable to start thread")
	while 1:
		pass
main()