from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime
import datetime
import time
import pandas

import bs4
from bs4 import BeautifulSoup as soup
import requests

path_to_chromedriver = "/usr/bin/chromedriver"
balance = {}
profit = 0
tv_url='https://www.marketwatch.com/investing/stock/'

def getData1(web_url, tickername):
    try:
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        options.add_argument('headless')
        options.add_argument('window-size=1200,1100');

        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

        # if(tickername == "NASDAQ-ALGN"):
        #     tv_url = tv_url + "ALGN/"
        # else if(tickername == "NYSE-IBM"):
        #     tv_url = tv_url + "IBM/"
        # else if(tickername == "")
        url = web_url + tickername
        driver.get(url)

        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("span", {"class":"kv__value"})

        Open = containers[0].text[1:-1]

        containers = page_soup.findAll("td", {"class":"u-semi"})
        
        if(tickername == 'poly?countrycode=uk'):
            Close = containers[0].text[1:-1]
        else:
            Close = containers[0].text[1:10]

        realtimeData = [
            Open,
            Close,
            tickername
        ]

        return realtimeData

    except Exception as ex:
        print(ex)
        pass

def getData2(web_url, tickername):
    try:
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        options.add_argument('headless')
        options.add_argument('window-size=1200,1100');

        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

        url = web_url + tickername +"/analystestimates"
        driver.get(url)

        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("table", {"class":"snapshot"})
        if(containers == []):
            Recommendations = ""
            TargetPrice = ''
        else:
            cont = containers[0].findAll("td")
            Recommendations = cont[1].text.strip()
            TargetPrice = cont[3].text.strip()

        realtimeData = [
            Recommendations,
            TargetPrice,
            tickername
        ]

        return realtimeData

    except Exception as ex:
        print(ex)
        pass
        
def realtime1():
    rtArray = list() 
    df = pandas.read_csv('market_ticker.csv')
    for ticker in df["ticker"]:
        rtArray.append(getData1(tv_url, ticker))
    return rtArray

def realtime2():
    rtArray = list() 
    df = pandas.read_csv('market_ticker.csv')
    for ticker1 in df["ticker"]:
        rtArray.append(getData2(tv_url, ticker1))
    return rtArray

def getGL():
    realtimeData = list()
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument('headless')
    options.add_argument('window-size=1200,1100');

    driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

    url = 'https://www.marketwatch.com/'
    driver.get(url)

    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    page_soup = soup(res, "lxml")
    containers = page_soup.findAll("div", {"class":"element--movers"})
    symbol = containers[0].findAll("span", {"class":"mover__symbol"})
    percent = containers[0].findAll("bg-quote", {"field":"percentChange"})
    for x in range(8):
        realtimeData.append([symbol[x].text, percent[x].text])

    return realtimeData
