from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime
import datetime
import time
import pandas
from bs4 import BeautifulSoup as soup
import lxml

yahoo_url='https://finance.yahoo.com'

def getData(web_url, company):
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
        url = web_url + '/quote/' + company + '/history?p=' + company #search url
        #https://finance.yahoo.com/quote/ALGN/history?p=ALGN
        # print('************URL*****************')
        print(url)
        # print('********************************')
        browser.get(url)     #request send and get html page
        # browser.maximize_window()
        # browser.implicitly_wait(60) # wait for loading elements in 60 seconds.
        time.sleep(1.5) # sleep 1.5s

        # html = browser.page_source
        # bs = soup(html, 'lxml')
        table   = browser.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table').get_attribute('innerHTML')
        # companyname = browser.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').text
        bs = soup(table, 'lxml')
        containers = bs.findAll("tr", {"class":"BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)"}) #BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)
        result = list()
        for container in reversed(containers):
            # print("#####\n")
            # print(container)
            # itemList = [companyname] #add company name at the first of line
            itemList = list()
            items = container.findAll("td") #find td tags, items is list of td tags
            for item in items: #item is one td tag
                itemList.append(item.span.text)
            result.append(itemList)
        browser.close()
        return result
    except Exception as ex:
        print(ex)
        browser.close()
        pass
        
def getHistoryData():
    rtArray = list() 
    df = pandas.read_csv('companylist.csv')
    for company in df["company"]:
        # print(company)
        item = getData(yahoo_url, company)
        rtArray.append(item)
        break
    # print(rtArray[1])
    return rtArray
# getHistoryData()