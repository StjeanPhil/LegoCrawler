import json
#import indigoCrawl
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import re
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def main():
    url="https://www.bestbuy.ca/en-ca/collection/lego-on-sale/130073?path=category%253AToys%252C%2BGames%2B%2526%2BEducation%253Bcategory%253ALEGO%2B%2526%2BBuilding%2BBlocks%253Bcategory%253ALEGO%253Bcurrentoffers0enrchstring%253AOn%2BSale%253BbrandName%253ALEGO%253BsellerName%253ABestBuyCanada"
    #initialize the webdriver
    driver=webdriver.Chrome()
    driver.get(url)

    #let the cookie pop up appear
    time.sleep(2)
    #Accept the cookies
    accceptCookies = driver.find_element(By.ID,'onetrust-accept-btn-handler')
    accceptCookies.click()
    #chillll
    time.sleep(2)

    #initialize the action chain
    actions = ActionChains(driver)

    #Click the "load more" button as much as possible
    while True:
        try:
            loadMoreButton = driver.find_element(By.CLASS_NAME,'loadMore_3AoXT') #find the button
            actions.move_to_element(loadMoreButton).click().perform()            #move the mouse to the button and click
            time.sleep(3)                                                        #give time to load

        except Exception as error:
            print("No more products to load")
            print(error)
            break


    #get the page's HTML after scrolling and loading all the products
    response = driver.find_element(By.XPATH,"//body").get_attribute('outerHTML')
    #Parse the HTML content for the products
    soup = BeautifulSoup(response, 'html.parser')
    tiles = soup.find_all('div', class_='x-productListItem')

    data=[] #list of products

    for tile in tiles:

        # Find the price, name ,link and date

        name = tile.find('div',class_='productItemName_3IZ3c').text.strip() #find it
        try:                                                                #clean it                          
            name=re.findall(r'\b\d{5}\b', name)[0]
        except Exception as error:
            print(error)
            print("error in : "+name)


        price = tile.find('span', {'data-automation':'product-price'}).find('span').text.strip() #find it
        price = int(price.replace(".","").replace("$",""))  #clean it

        href=tile.find('a').get('href')

        date = datetime.now().strftime('%Y-%m-%d')  

        # Create a dictionary with the scraped data
        product = {
            'name': name,   #Series number
            'price': price, #Price in cents
            'href': href,  #Link to the product
            'date': date    #Data's date
        }

        # Append the dictionary to the list
        data.append(product)

    print("data length:")
    print(len(data))
    #save the scraped data to a json file
    with open('./data/BestBuyCurrent.json', 'w') as outfile:
        json.dump(data, outfile)
        print('BestBuy sales data has been scraped and saved to ./data/BestBuyCurrent.json')
        outfile.close()

if __name__ == "__main__":
    main()