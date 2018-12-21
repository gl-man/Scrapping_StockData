from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime
import datetime
import time
import pandas

balance = {}
profit = 0
tv_url='https://www.tradingview.com'
tags=('','ideas', 'components', 'technicals')

def getTradingData(web_url, tickername):
    try:
        path_to_chromedriver = '/usr/lib/chromium-browser/chromedriver' # change path as needed
        options = webdriver.ChromeOptions()
        # disable notification
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)

        # headless
        options.add_argument('headless')
        options.add_argument('window-size=1200,1100'); #window size
        browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options) #load chrome driver
        url = web_url + '/symbols/' + tickername #search url
        # print('************URL*****************')
        # print(url)
        # print('********************************')
        browser.get(url)     #request send and get html page
        # browser.maximize_window()
        # browser.implicitly_wait(60) # wait for loading elements in 60 seconds.
        time.sleep(1.5) # sleep 1.5s

        #TickerName
        TickerName = tickername
        #isOpen
        isOpen = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/div').text;
        if(isOpen == "Market Open"):
            isOpen = "open"
        else:
            isOpen = "close"
        #CurrentValue
        CurrentValue    = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[1]').text; # Open or Close Value
        #ChangeValue and ChangeInPercent
        isFalling       = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[3]').get_attribute("class")
        ChangeValue     = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[4]').text
        ChangeInPercent = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[1]/div[1]/span[5]').text
        ChangeInPercent = ChangeInPercent[1:-1]
            
        if(isFalling.find("tv-symbol-header-quote__trend-arrow--falling")):     #check if the price is falling
            ChangeValue = "-"+ChangeValue
            ChangeInPercent = "-"+ChangeInPercent

        Volume      = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[3]/span').text
        LowValue    = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[4]/span[1]').text
        HighValue   = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[4]/span[3]').text
        EPS         = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[5]/span').text
        MktCap      = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[6]/span').text
        PE          = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[7]/span').text
        # ForwardPE   = 
        DivYield    = browser.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div/div[2]/div[8]/span').text
    

        browser.close()

        # time.sleep(60)

        realtimeData = [
            tickername,
            isOpen,
            CurrentValue,
            ChangeValue,
            ChangeInPercent,
            Volume,
            LowValue,
            HighValue,
            EPS,
            MktCap,
            PE,
            DivYield
        ]

        return realtimeData

    except Exception as ex:
        print(ex)
        browser.close()
        pass
        
def Realtime():
    rtArray = list() 
    df = pandas.read_csv('tickerlist.csv')

    for ticker in df["ticker"]:
        print(ticker)
        rtArray.append(getTradingData(tv_url, ticker))
       
    return rtArray