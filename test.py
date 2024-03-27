import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import re

import time

import webdriver_manager
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

url= "https://www.walmart.ca/en/browse/toys/lego/10011_6000205043132?icid=landing%2Fcp_page_toys_shop_all_lego_18944_EU28ISZ2DN&facet=f_SellerType_en%3AWalmart%7C%7Cbrand%3ALEGO%7C%7Cf_Availability_en%3AOnline"
    #url_root= "https://www.walmart.ca"
driver = webdriver.Chrome()
driver.get(url)
#NAVIGATE THE PAGE
time.sleep(5) #let the cookie pop up appear

try:
    accceptCookies = driver.find_element('button',{'arial-label':'acceptAll button'}) #Accept the cookies
    accceptCookies.click()
except Exception as error:
    print("No cookies to accept")
    print(error)
time.sleep(2) #chillll
actions = ActionChains(driver)#initialize the action chain=

actions.scroll_by_amount(0, 1000).perform()
#
#accceptCookies = driver.find_element(By.ID,'onetrust-accept-btn-handler') #Accept the cookies
#accceptCookies.click()
#
#time.sleep(2) #chillll
#actions = ActionChains(driver)#initialize the action chain=
#
#while True: #Click the "load more" button as much as possible
#    try:
#        loadMoreButton = driver.find_element(By.CLASS_NAME,'loadMore_3AoXT') #find the button
#        actions.move_to_element(loadMoreButton).click().perform()            #move the mouse to the button and click
#        time.sleep(3)                                                        #give time to load
#    except Exception as error:
#        print("No more products to load")
#        print(error)
#        break
##get the page's HTML after scrolling and loading all the products
#response = driver.find_element(By.XPATH,"//body").get_attribute('outerHTML')
##Parse the HTML content for the products
#soup = BeautifulSoup(response, 'html.parser')
#tiles = soup.find_all('div', class_='x-productListItem')
#data=[] #list of products
##Parse through each product
#for tile in tiles:
#
#