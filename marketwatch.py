from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

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
ticker_url='https://www.marketwatch.com/'

stockUrl = ['algn', 'poly?countrycode=uk', 'aal?countrycode=uk', 'ibm', 'rrs?countrycode=ca']
symbolNames = ['ALGN', 'POLY', 'AAL', 'IBM', 'RRS']

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)

# headless
options.add_argument('headless')
# options.add_argument("start-maximized")
options.add_argument("disable-infobars")
# options.add_argument("--incognito");
options.add_argument('--disable-gpu')
options.add_argument("--disable-extensions")

options.add_argument("--disable-impl-side-painting")
options.add_argument("--disable-accelerated-2d-canvas'")
options.add_argument("--disable-gpu-sandbox")
# options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")

def getData1(tickername):
    try:
        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

        # if(tickername == "NASDAQ-ALGN"):
        #     tv_url = tv_url + "ALGN/"
        # else if(tickername == "NYSE-IBM"):
        #     tv_url = tv_url + "IBM/"
        # else if(tickername == "")
        url = tv_url + tickername
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

def getData2(tickername):
    try:
        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

        url = tv_url + tickername +"/analystestimates"
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
        rtArray.append(getData1(ticker))
    return rtArray

def realtime2():
    rtArray = list() 
    df = pandas.read_csv('market_ticker.csv')
    for ticker in df["ticker"]:
        rtArray.append(getData2(ticker))
    return rtArray


def getGL():
    realtimeData = list()

    driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)
    driver.get(ticker_url)

    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    page_soup = soup(res, "lxml")
    containers = page_soup.findAll("div", {"class":"element--movers"})
    symbol = containers[0].findAll("span", {"class":"mover__symbol"})
    percent = containers[0].findAll("bg-quote", {"field":"percentChange"})
    for x in range(8):
        realtimeData.append([symbol[x].text, percent[x].text])

    return realtimeData


def getTickerRealTimeData():
    try:
        symbol_list1 = list()
        price_list1 = list()
        change_list1 = list()
        percent_list1 = list()

        symbol_list2 = list()
        price_list2 = list()
        change_list2 = list()
        percent_list2 = list()

        symbol_list3 = list()
        price_list3 = list()
        change_list3 = list()
        percent_list3 = list()

        symbol_list4 = list()
        price_list4 = list()
        change_list4 = list()
        percent_list4 = list()

        symbol_list5 = list()
        price_list5 = list()
        change_list5 = list()
        percent_list5 = list()

        driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
        driver.get(ticker_url)
        driver.implicitly_wait(20)

        while True:
            if EC.presence_of_all_elements_located:
                break
            else:
                continue

        while True:
            try:
                Create = driver.find_element_by_xpath("//ul[@class='tabs']/li[1]/a")
                driver.execute_script("arguments[0].click()", Create);                
                break
            except TimeoutException :
                print("Retrying...")
                continue

        time.sleep(3)
        # driver.implicitly_wait(20)
        res = driver.execute_script("return document.documentElement.outerHTML")
        # driver.quit()

        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("tbody", {"class":"markets__group"})[0]
        symbol = containers.findAll("td", {"class": "symbol"})
        price = containers.findAll("td", {"class": "price"})
        change = containers.findAll("td", {"class": "change"})
        percent = containers.findAll("td", {"class": "percent"})

        for x in range(6):
            symbol_list1.append(symbol[x].text)
            price_list1.append((price[x].text).replace("\n", ""))
            change_list1.append((change[x].text).replace("\n", ""))
            percent_list1.append((percent[x].text).replace("\n", ""))

        usa_ticker = [
            symbol_list1,
            price_list1,
            change_list1,
            percent_list1
        ]

        while True:
            if EC.presence_of_all_elements_located:
                break
            else:
                continue

        while True:
            try:
                Create = driver.find_element_by_xpath("//ul[@class='tabs']/li[2]/a")
                driver.execute_script("arguments[0].click()", Create)                
                break
            except TimeoutException :
                print("Retrying...")
                continue

        time.sleep(3)
        # driver.implicitly_wait(20)
        
        res = driver.execute_script("return document.documentElement.outerHTML")
        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("tbody", {"class":"markets__group"})[0]
        symbol = containers.findAll("td", {"class": "symbol"})
        price = containers.findAll("td", {"class": "price"})
        change = containers.findAll("td", {"class": "change"})
        percent = containers.findAll("td", {"class": "percent"})

        for x in range(6):
            symbol_list2.append(symbol[x].text)
            price_list2.append((price[x].text).replace("\n", ""))
            change_list2.append((change[x].text).replace("\n", ""))
            percent_list2.append((percent[x].text).replace("\n", ""))

        europe_ticker = [
            symbol_list2,
            price_list2,
            change_list2,
            percent_list2
        ]

        while True:
            if EC.presence_of_all_elements_located:
                break
            else:
                continue

        while True:
            try:
                Create = driver.find_element_by_xpath("//ul[@class='tabs']/li[3]/a")
                driver.execute_script("arguments[0].click()", Create)                
                break
            except TimeoutException :
                print("Retrying...")
                continue

        time.sleep(3)
        # driver.implicitly_wait(20)
        
        res = driver.execute_script("return document.documentElement.outerHTML")
        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("tbody", {"class":"markets__group"})[0]
        symbol = containers.findAll("td", {"class": "symbol"})
        price = containers.findAll("td", {"class": "price"})
        change = containers.findAll("td", {"class": "change"})
        percent = containers.findAll("td", {"class": "percent"})

        for x in range(6):
            symbol_list3.append(symbol[x].text)
            price_list3.append((price[x].text).replace("\n", ""))
            change_list3.append((change[x].text).replace("\n", ""))
            percent_list3.append((percent[x].text).replace("\n", ""))

        asia_ticker = [
            symbol_list3,
            price_list3,
            change_list3,
            percent_list3
        ]


        while True:
            if EC.presence_of_all_elements_located:
                break
            else:
                continue

        while True:
            try:
                Create = driver.find_element_by_xpath("//ul[@class='tabs']/li[4]/a")
                driver.execute_script("arguments[0].click()", Create);                
                break
            except TimeoutException :
                print("Retrying...")
                continue

        time.sleep(3)
        # driver.implicitly_wait(20)
        
        res = driver.execute_script("return document.documentElement.outerHTML")
        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("tbody", {"class":"markets__group"})[0]
        symbol = containers.findAll("td", {"class": "symbol"})
        price = containers.findAll("td", {"class": "price"})
        change = containers.findAll("td", {"class": "change"})
        percent = containers.findAll("td", {"class": "percent"})

        for x in range(6):
            symbol_list4.append(symbol[x].text)
            price_list4.append((price[x].text).replace("\n", ""))
            change_list4.append((change[x].text).replace("\n", ""))
            percent_list4.append((percent[x].text).replace("\n", ""))

        fx_ticker = [
            symbol_list4,
            price_list4,
            change_list4,
            percent_list4
        ]

        while True:
            if EC.presence_of_all_elements_located:
                break
            else:
                continue

        while True:
            try:
                Create = driver.find_element_by_xpath("//ul[@class='tabs']/li[7]/a")
                driver.execute_script("arguments[0].click()", Create)             
                break
            except TimeoutException :
                print("Retrying...")
                continue

        time.sleep(3)
        # driver.implicitly_wait(20)
        
        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()
        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("tbody", {"class":"markets__group"})[0]
        symbol = containers.findAll("td", {"class": "symbol"})
        price = containers.findAll("td", {"class": "price"})
        change = containers.findAll("td", {"class": "change"})
        percent = containers.findAll("td", {"class": "percent"})

        for x in range(6):
            symbol_list5.append(symbol[x].text)
            price_list5.append((price[x].text).replace("\n", ""))
            change_list5.append((change[x].text).replace("\n", ""))
            percent_list5.append((percent[x].text).replace("\n", ""))

        crypto_ticker = [
            symbol_list5,
            price_list5,
            change_list5,
            percent_list5
        ]
        
        realtimeData = [
            usa_ticker,
            europe_ticker,
            asia_ticker,
            fx_ticker,
            crypto_ticker
        ]
        
        return realtimeData

    except Exception as ex:
        print(ex)
        pass

def getRealtimeStockData():
    rtArray = [[], [], [], [], []]   
    for i in range(5):
        geturl = tv_url+stockUrl[i]
        print(geturl)
        driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
        driver.get(geturl)

        while True:
            try:
                Create = driver.find_element_by_xpath("//ul[@class='tabs']/li[2]/a")
                driver.execute_script("arguments[0].click()", Create)                
                break
            except TimeoutException :
                print("Retrying...")
                continue
        
        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        page_soup = soup(res, "lxml")
        containers = page_soup.findAll("div", {"class":"stock"})[0]
        status = containers.findAll("small", {"class":"intraday__status"})

        text = status[0].text;

        p=status[0].findAll("span",{"class":"company__ticker"})[0].text
        text=text.replace(p,"")
        p=status[0].findAll("span",{"class":"company__market"})[0].text
        text=text.replace(p,"")
        p=status[0].findAll("span",{"class":"scroll-top"})[0].text
        text=text.replace(p,"")

        marketType = text


        pp = containers.findAll("bg-quote", {"class":"value"})
        price = ""
        changeValue = ""
        changePercent = ""
        if(pp == []):
            pp = containers.findAll("span", {"class":"value"})
            price = pp[0].text

            pp = containers.findAll("span", {"class":"change--point--q"})
            changeValue = pp[0].text

            pp = containers.findAll("span", {"class":"change--percent--q"})
            changePercent = pp[0].text
        else:
            price = pp[0].text

            pp = containers.findAll("bg-quote", {"field":"change"})
            changeValue = pp[0].text

            pp = containers.findAll("bg-quote", {"field":"percentchange"})
            changePercent = pp[0].text

        pp = containers.findAll("td",{"class":"u-semi"})
        preClose = pp[0].text

        pp = containers.findAll("span", {"class":"last-value"})
        volume = pp[0].text.strip()

        pp = containers.findAll("mw-rangebar", {"class":"lowHigh--day"})[0]
        qq = pp.findAll("span", {"class":"low"})
        dayLow = qq[0].text

        pp = containers.findAll("mw-rangebar", {"class":"lowHigh--day"})[0]
        qq = pp.findAll("span", {"class":"high"})
        dayHigh = qq[0].text

        pp = containers.findAll("mw-rangebar", {"class":"lowHigh--year"})[0]
        qq = pp.findAll("span", {"class":"low"})
        weekLow52 = qq[0].text

        pp = containers.findAll("mw-rangebar", {"class":"lowHigh--year"})[0]
        qq = pp.findAll("span", {"class":"high"})
        weekHigh52 = qq[0].text

        pp = containers.findAll("li", {"class":"kv__item"})

        qq = pp[0].findAll("span",{"class":"kv__primary"})
        Open = qq[0].text

        qq = pp[3].findAll("span",{"class":"kv__primary"})
        marketCap = qq[0].text

        qq = pp[4].findAll("span",{"class":"kv__primary"})
        sharesOutstanding = qq[0].text
        
        qq = pp[5].findAll("span",{"class":"kv__primary"})
        publicFloat = qq[0].text
        
        qq = pp[6].findAll("span",{"class":"kv__primary"})
        beta = qq[0].text
        
        qq = pp[7].findAll("span",{"class":"kv__primary"})
        revPerEmployee = qq[0].text
        
        qq = pp[8].findAll("span",{"class":"kv__primary"})
        peRatio = qq[0].text
        
        qq = pp[9].findAll("span",{"class":"kv__primary"})
        eps = qq[0].text
        
        qq = pp[10].findAll("span",{"class":"kv__primary"})
        Yield = qq[0].text
        
        qq = pp[11].findAll("span",{"class":"kv__primary"})
        dividend = qq[0].text
        
        qq = pp[12].findAll("span",{"class":"kv__primary"})
        exDividendDate = qq[0].text
        
        qq = pp[13].findAll("span",{"class":"kv__primary"})
        shortInterest = qq[0].text
        
        qq = pp[14].findAll("span",{"class":"kv__primary"})
        floatShorted = qq[0].text
        
        qq = pp[15].findAll("span",{"class":"kv__primary"})
        averageVolume = qq[0].text


        #PERFORMANCE
        pp = containers.findAll("li", {"class":"ignore-color"})
        week1 = pp[0].text
        month1 = pp[1].text
        month3 = pp[2].text
        ytd = pp[3].text
        year1 = pp[4].text

        rtArray[i] = [
            symbolNames[i],
            marketType,
            price,
            changeValue,
            changePercent,
            Open,
            marketCap,
            sharesOutstanding,
            publicFloat,
            beta,
            revPerEmployee,
            peRatio,
            eps,
            Yield,
            dividend,
            exDividendDate,
            shortInterest,
            floatShorted,
            averageVolume,
            dayLow,
            dayHigh,
            weekLow52,
            weekHigh52,
            week1,
            month1,
            month3,
            ytd,
            year1,
            volume
        ]
        
    return rtArray