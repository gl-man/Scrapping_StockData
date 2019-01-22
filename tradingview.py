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

path_to_chromedriver = '/usr/bin/chromedriver'

balance = {}
profit = 0
tv_url='https://www.tradingview.com'

default_url = 'https://www.tradingview.com/symbols/'
stock_url = ['NASDAQ-ALGN', 'LSE-POLY', 'LSE-AAL', 'SIX-IBM', 'TSXV-RRS']
stockNames = ['ALGN', 'POLY', 'AAL', 'IBM', 'RRS']

top_gainer_url = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"
top_loser_url = "https://www.tradingview.com/markets/stocks-usa/market-movers-losers/"

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
# options.add_experimental_option("prefs",prefs)
options.add_argument('headless')
# options.add_argument('window-size=1200,1100')
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

def getData(web_url, tickername):
    try:
        browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options) #load chrome driver
        url = web_url + '/symbols/' + tickername

        browser.get(url)
        browser.implicitly_wait(20)

        TickerName = tickername
        MarketCapitalization = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]').text
                
        if(MarketCapitalization == "" or MarketCapitalization == "—" or MarketCapitalization == "_"):
            while 1:
                browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
                browser.get(url)
                browser.implicitly_wait(20)
                MarketCapitalization = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]').text
                
                if(MarketCapitalization != "_" and MarketCapitalization != "" and MarketCapitalization != "—"):
                    break

                   
        PricetoBookRatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[10]/span[2]').text
        QuickRatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/span[2]').text
        CurrentRatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/span[2]').text
        DERatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/span[2]').text
        ReturnonAssets = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/span[2]').text
        ReturnonEquity = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[3]/span[2]').text
        ReturnonInvestedCapital = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[4]/span[2]').text
        NetMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]').text
        GrossMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[3]/span[2]').text
        OperatingMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[4]/span[2]').text
        PreTaxMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[5]/span[2]').text
        YearBeta = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/span[2]').text
        DividendsPaid =  browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/span[2]').text
        DividendsYield =  browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/span[2]').text
        WeekRangeHigh52 = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/span[2]').text
        WeekRangeLow52 = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[5]/span[2]').text        

        # Volume = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[3]/span').text
        DayRangeLow = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[4]/span[1]').text
        DayRangeHigh = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[4]/span[3]').text
        PE = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[7]/span').text

        # ChangeValue = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[4]').text
        # ChangePercent = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[5]').text
        # isFalling = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[3]').get_attribute("class")
            
        # if(isFalling.find("tv-symbol-header-quote__trend-arrow--growing") == -1):     #check if the price is falling
        #     ChangeValue = "-"+ChangeValue
        #     ChangePercent = "-"+ChangePercent
        Volume      = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[3]/span').text
        Price = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[1]').text
        Low = DayRangeLow
        High = DayRangeHigh

        ChangeValue = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[4]').text
        ChangePercent = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[5]').text
        ChangePercent = ChangePercent[1:-1]
        isFalling = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[3]').get_attribute("class")
        # isFalling = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[3]').get_attribute("class")
            
        if(isFalling.find("tv-symbol-header-quote__trend-arrow--growing") == -1):     #check if the price is falling
            ChangeValue = "-"+ChangeValue
            ChangePercent = "-"+ChangePercent
        # if(isFalling.find("tv-symbol-header-quote__trend-arrow--falling")):     #check if the price is falling
        #     ChangeValue = "-"+ChangeValue
        #     ChangePercent = "-"+ChangePercent
        browser.close()
        realtimeData = [
            MarketCapitalization,
            PricetoBookRatio,
            QuickRatio,
            CurrentRatio,
            DERatio,
            ReturnonAssets,
            ReturnonEquity,
            ReturnonInvestedCapital,
            NetMargin,
            GrossMargin,
            OperatingMargin,
            PreTaxMargin,
            Volume,        
            DayRangeLow,
            DayRangeHigh,
            PE,
            YearBeta,
            DividendsPaid,
            DividendsYield,
            WeekRangeLow52,
            WeekRangeHigh52,
            Price,
            Low,
            High,
            ChangeValue,
            ChangePercent,
            TickerName
        ]

        return realtimeData

    except Exception as ex:
        print(ex)
        browser.close()
        pass



def getRealTimeData1(web_url, tickername):
    try:
        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

        url = web_url + '/symbols/' + tickername
        driver.get(url)

        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        page_soup = soup(res, "lxml")

        containers = page_soup.findAll("div", {"class":"tv-symbol-header-row"})

        MarketCapitalization = "AA"
        MarketCapitalization = containers[0].findAll("span", {"class":"js-symbol-market-cap"})[0].text

        while 1:
            if(containers[0].findAll("div", {"class":"tv-symbol-header-quote__market-stat"}) == ""  or containers[0].findAll("div", {"class":"tv-symbol-header-quote__market-stat"}) == []):
                driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)
                url = web_url + '/symbols/' + tickername
                driver.get(url)

                res = driver.execute_script("return document.documentElement.outerHTML")
                driver.quit()
                page_soup = soup(res, "lxml")
                containers = page_soup.findAll("div", {"class":"tv-symbol-header-row"})
            else:
                break;

        isOpen = containers[0].findAll("div", {"class":"tv-symbol-header-quote__market-stat"})[0].text     

        if(isOpen == "Market Closed"):
            isOpen = "close"
        else:
            isOpen = "open"

        isFalling = containers[0].findAll("span", {"class":"tv-symbol-header-quote__trend-arrow--falling"}) 

        Price = containers[0].findAll("span", {"class":"js-symbol-last"})[0].text 

        ChangeValue = containers[0].findAll("span", {"class":"js-symbol-change"})[0].text
        ChangePercent = containers[0].findAll("span", {"class":"js-symbol-change-pt"})[0].text
        ChangePercent = ChangePercent[1:-1]

        if(isFalling != []):
            ChangeValue = "-"+ChangeValue
            ChangePercent = "-"+ChangePercent

        Volume = containers[0].findAll("span", {"class":"js-symbol-volume"})[0].text

        Open = containers[0].findAll("span", {"class":"js-symbol-open"})[0].text
        Close = containers[0].findAll("span", {"class":"js-symbol-prev-close"})[0].text

        Low = containers[0].findAll("span", {"class":"js-symbol-header__range-price-l"})[0].text
        High = containers[0].findAll("span", {"class":"js-symbol-header__range-price-r"})[0].text

        EPS = containers[0].findAll("span", {"class":"js-symbol-eps"})[0].text

        PE = containers[0].findAll("span", {"class":"js-symbol-pe"})[0].text

        DivYield = containers[0].findAll("span", {"class":"js-symbol-dividends"})[0].text
        
        TickerName = tickername

        realtimeData = [
            isOpen,
            Price,
            ChangeValue,
            ChangePercent,
            Volume,
            Low,
            High,
            EPS,
            PE,
            DivYield,
            MarketCapitalization,
            TickerName
        ]

        print(realtimeData)

        return realtimeData

    except Exception as ex:
        print(ex)
        pass

def getRealTimeData(web_url, tickername):
    try:
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        options.add_argument('headless')
        options.add_argument('window-size=1200,1100');

        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

        url = web_url + '/symbols/' + tickername
        driver.get(url)

        res = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        page_soup = soup(res, "lxml")

        containers = page_soup.findAll("div", {"class":"tv-symbol-header-row"})

        MarketCapitalization = containers[0].findAll("span", {"class":"js-symbol-market-cap"})[0].text

        isOpen = containers[0].findAll("div", {"class":"js-symbol-header__last-title"})[0].text

        if(isOpen == "Market Closed"):
            isOpen = "close"
        else:
            isOpen = "open"

        isFalling = containers[0].findAll("span", {"class":"tv-symbol-header-quote__trend-arrow--falling"}) 

        Price = containers[0].findAll("span", {"class":"js-symbol-last"})[0].text 

        ChangeValue = containers[0].findAll("span", {"class":"js-symbol-change"})[0].text
        ChangePercent = containers[0].findAll("span", {"class":"js-symbol-change-pt"})[0].text
        ChangePercent = ChangePercent[1:-1]

        if(isFalling != []):
            ChangeValue = "-"+ChangeValue
            ChangePercent = "-"+ChangePercent

        Volume = containers[0].findAll("span", {"class":"js-symbol-volume"})[0].text

        Open = containers[0].findAll("span", {"class":"js-symbol-open"})[0].text
        Close = containers[0].findAll("span", {"class":"js-symbol-prev-close"})[0].text

        Low = containers[0].findAll("span", {"class":"js-symbol-header__range-price-l"})[0].text
        High = containers[0].findAll("span", {"class":"js-symbol-header__range-price-r"})[0].text

        EPS = containers[0].findAll("span", {"class":"js-symbol-eps"})[0].text

        PE = containers[0].findAll("span", {"class":"js-symbol-pe"})[0].text

        DivYield = containers[0].findAll("span", {"class":"js-symbol-dividends"})[0].text
        
        TickerName = tickername
        
        realtimeData = [
            isOpen,
            Price,
            ChangeValue,
            ChangePercent,
            Volume,
            Low,
            High,
            EPS,
            PE,
            DivYield,
            MarketCapitalization,
            TickerName
        ]

        print(realtimeData)

        return realtimeData

    except Exception as ex:
        print(ex)
        pass
        
def realtime():
    rtArray = list() 
    df = pandas.read_csv('tickerlist.csv')

    for ticker in df["ticker"]:
        rtArray.append(getData(tv_url, ticker))
    return rtArray

def getrealtimedata():
    rtArray = list() 
    df = pandas.read_csv('tickerlist.csv')

    for ticker in df["ticker"]:
        rtArray.append(getRealTimeData(tv_url, ticker))
    return rtArray

def getStockData():
    rtArray = list()

    for i in range(5):
        MarketCapitalization = ""

        new_url = default_url + stock_url[i]

        browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options) #load chrome driver
        print(new_url)
        browser.get(new_url)
        browser.implicitly_wait(20)
                   
        PricetoBookRatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[10]/span[2]').text
        QuickRatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/span[2]').text
        CurrentRatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/span[2]').text
        DERatio = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/span[2]').text
        ReturnonAssets = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/span[2]').text
        ReturnonEquity = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[3]/span[2]').text
        ReturnonInvestedCapital = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[4]/span[2]').text
        NetMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]').text
        GrossMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[3]/span[2]').text
        OperatingMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[4]/span[2]').text
        PreTaxMargin = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[5]/span[2]').text
        # YearBeta = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/span[2]').text
        # DividendsPaid =  browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/span[2]').text
        # DividendsYield =  browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/span[2]').text
        # WeekRangeHigh52 = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/span[2]').text
        # WeekRangeLow52 = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[5]/span[2]').text        

        # # Volume = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[3]/span').text
        # DayRangeLow = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[4]/span[1]').text
        # DayRangeHigh = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[4]/span[3]').text
        # PE = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div/div[2]/div[7]/span').text

        # # ChangeValue = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[4]').text
        # # ChangePercent = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[5]').text
        # # isFalling = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[3]').get_attribute("class")
            
        # # if(isFalling.find("tv-symbol-header-quote__trend-arrow--growing") == -1):     #check if the price is falling
        # #     ChangeValue = "-"+ChangeValue
        # #     ChangePercent = "-"+ChangePercent
        # Volume      = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[3]/span').text
        # Price = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[1]').text
        # Low = DayRangeLow
        # High = DayRangeHigh

        # ChangeValue = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[4]').text
        # ChangePercent = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[5]').text
        # ChangePercent = ChangePercent[1:-1]
        # isFalling = browser.find_element_by_xpath('//*["@id=js-category-content"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span[3]').get_attribute("class")
        # # isFalling = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[3]').get_attribute("class")
            
        # if(isFalling.find("tv-symbol-header-quote__trend-arrow--growing") == -1):     #check if the price is falling
        #     ChangeValue = "-"+ChangeValue
        #     ChangePercent = "-"+ChangePercent
        # # if(isFalling.find("tv-symbol-header-quote__trend-arrow--falling")):     #check if the price is falling
        # #     ChangeValue = "-"+ChangeValue
        # #     ChangePercent = "-"+ChangePercent
        browser.close()
        # realtimeData = [
        #     # MarketCapitalization,
        #     PricetoBookRatio,
        #     QuickRatio,
        #     CurrentRatio,
        #     DERatio,
        #     ReturnonAssets,
        #     ReturnonEquity,
        #     ReturnonInvestedCapital,
        #     NetMargin,
        #     GrossMargin,
        #     OperatingMargin,
        #     PreTaxMargin,
        #     # Volume,        
        #     # DayRangeLow,
        #     # DayRangeHigh,
        #     # PE,
        #     # YearBeta,
        #     # DividendsPaid,
        #     # DividendsYield,
        #     # WeekRangeLow52,
        #     # WeekRangeHigh52,
        #     # Price,
        #     # Low,
        #     # High,
        #     # ChangeValue,
        #     # ChangePercent,
        #     stockNames[i]
        # ]
        realtimeData = [
            PricetoBookRatio,
            QuickRatio,
            CurrentRatio,
            DERatio,
            ReturnonAssets,
            ReturnonEquity,
            ReturnonInvestedCapital,
            NetMargin,
            GrossMargin,
            OperatingMargin,
            PreTaxMargin,
            stockNames[i]
        ]
        rtArray.append(realtimeData)

    return rtArray