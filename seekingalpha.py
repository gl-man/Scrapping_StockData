# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from time import gmtime, strftime
# import datetime
# import time
# import pandas

# import bs4
# from bs4 import BeautifulSoup as soup
# import requests

# balance = {}
# profit = 0
# tv_url='https://seekingalpha.com/symbol/'
# suffxi_url='/valuation'

# def getData(web_url, tickername):
#     try:
#         options = webdriver.ChromeOptions()
#         prefs = {"profile.default_content_setting_values.notifications" : 2}
#         options.add_experimental_option("prefs",prefs)
#         options.add_argument('headless')
#         options.add_argument('window-size=1200,1100');

#         driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)

#         # if(tickername == "NASDAQ-ALGN"):
#         #     tv_url = tv_url + "ALGN/"
#         # else if(tickername == "NYSE-IBM"):
#         #     tv_url = tv_url + "IBM/"
#         # else if(tickername == "")
#         url = web_url + tickername + suffxi_url
#         driver.get(url)
#         time.sleep(1)

#         res = driver.execute_script("return document.documentElement.outerHTML")
#         driver.quit()
#         time.sleep(1)
#         # html parsing
#         page_soup = soup(res, "lxml")
#         containers = page_soup.findAll("td", {"id":"sum-peRatioFwd"})

#         print(containers)

#         containers = page_soup.findAll("td", {"id":"sum-evEbitda"})
#         print(containers[0].text)
        
#         realtimeData = [
#             "Haha",
#             tickername
#         ]

#         return realtimeData

#     except Exception as ex:
#         print(ex)
#         pass
        
# def realtime():
#     rtArray = list() 
#     df = pandas.read_csv('seek.csv')

#     for ticker in df["ticker"]:
#         print(ticker)
#         rtArray.append(getData(tv_url, ticker))
#     # rtArray.append(getData(tv_url, "NASDAQ-ALGN"))
#     return rtArray

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
tv_url='https://seekingalpha.com/symbol/'
suffxi_url='/valuation'

def getData(web_url, tickername):
    try:
        # path_to_chromedriver = '/usr/lib/chromium-browser/chromedriver'
        path_to_chromedriver = '/usr/bin/chromedriver' # change path as needed
        options = webdriver.ChromeOptions()
        # disable notification
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)

        # headless
        options.add_argument('headless')
        options.add_argument('window-size=1200,1100'); #window size
        browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options) #load chrome driver
        url = web_url + tickername + suffxi_url #search url
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
        ForwardPE = browser.find_element_by_xpath('//*["@id=sum-peRatioFwd"]').text
        EVRatio = browser.find_element_by_xpath('//*["@id=sum-evEbitda"]').text
        print(ForwardPE)
        print(EVRatio)
        browser.close()
        realtimeData = [
            ForwardPE,
            EVRatio,
            TickerName
        ] 

        # time.sleep(60)

        # realtimeData = [
        #     tickername,
        #     isOpen,
        #     CurrentValue,
        #     ChangeValue,
        #     ChangeInPercent,
        #     Volume,
        #     LowValue,
        #     HighValue,
        #     EPS,
        #     MktCap,
        #     PE,
        #     DivYield
        # ]

        return realtimeData

    except Exception as ex:
        print(ex)
        browser.close()
        pass
        
def realtime():
    rtArray = list() 
    df = pandas.read_csv('seek.csv')

    for ticker in df["ticker"]:
        print(ticker)
        rtArray.append(getData(tv_url, ticker))
    # rtArray.append(getData(tv_url, "NASDAQ-ALGN"))
    return rtArray