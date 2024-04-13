from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from datetime import datetime
from decimal import Decimal
#import config
from selenium_stealth import stealth
import json,re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

def crawl(currId) :
    #f= open("./data/LegoSiteCurrent.json","r")
    #data=json.load(f)
    #return data,currId
    url ='https://www.lego.com/en-ca/categories/sales-and-deals?filters.i0.key=categories.id&filters.i0.values.i0=12ba8640-7fb5-4281-991d-ac55c65d8001'
    date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date   
    data=[]

    #initialize the browser
    # Create Chromeoptions instance 
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("useAutomationExtension", False) 
    driver = webdriver.Chrome(options=options) 
    #stealth the browser
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        session_cookie_id="zD6w28nNrWvnOSsyevXIf"
        )
    #open page
    driver.get(url)
    sleep(5)

    #NAVIGATE THE PAGE
    actions = ActionChains(driver)#initialize the action chain=
    goBtn = driver.find_element(By.ID,"age-gate-grown-up-cta")
    if goBtn:
        actions.move_to_element(goBtn).click().perform() 
        time.sleep(3)
    acptBtn =  driver.find_element(By.XPATH,'//button[@data-test="cookie-necessary-button"]')
    if acptBtn:
        actions.move_to_element(acptBtn).click().perform() 
        time.sleep(3)

    #go to all pages to get all product listings
    responses=[]
    while True:
        try:
            listing=driver.find_element(By.ID,"product-listing-grid").get_attribute('outerHTML')
            if listing : 
                responses.append(listing)
            if not driver.find_elements(By.XPATH,'//span[@data-test="pagination-next-disabled"]'):
                goNext=driver.find_element(By.XPATH,'//a[@data-test="pagination-next"]')
                actions.move_to_element(goNext).click().perform()
                time.sleep(5)
            else:
                break
        except Exception as error:
            print(error)
            break   
    #close the browser
    driver.quit()
    #Parse the HTML content of all pages visited for products
    for response in responses:

        soup = BeautifulSoup(response, 'html.parser')
        tiles = soup.find_all("article")    

        #Parse through each product
        for tile in tiles:
            try:        
                # Extract the price
                price_element = tile.find('span', class_='ProductLeaf_discountedPrice__77YmG', attrs={'data-test': 'product-leaf-discounted-price'})
                price = Decimal(price_element.get_text().replace(" CAD","")) if price_element else None

                # Extract the href
                href_element = tile.find('a', attrs={'data-test': 'product-leaf-image-link'})
                href = href_element['href'] if href_element else None

                #Name is the last 5 digits of the href
                name = re.findall(r'\b\d{5}\b', href)[-1] if href else None
                if not name : continue
                
                inStock=(tile.find('a',attrs={'data-test-availability':'K_SOLD_OUT'}) )
                inStock=1 if inStock else 0
                


                # Create a dictionary with the scraped data
                product = {
                    'log_id': currId,   #Unique id for the log
                    'date' : date, # get the current date
                    'shop_id': 3,   #Shop's id
                    'set_num': name,   #Series number
                    'price': price, #Price in cents
                    'link': "https://www.lego.com"+href,  #Link to the product
                    'inStock': inStock, #True if the product is in stock, False otherwise
                    'ships':inStock , # not sure how this work but seems important to add
                    'pickup': 2, #True if the product is in store, False otherwise
                    
                }
                # Append the dictionary to the list
                data.append(product)
                currId+=1

            except Exception as error:
                print(error)


    #save the scraped data to a json file
    with open('./data/LegoSiteCurrent.json', 'w') as outfile:
        json.dump(data, outfile)
        print('LegoSite sales data has been scraped and saved to ./data/LegoSiteCurrent.json')
        outfile.close()
    
    return data,currId

if __name__ == "__main__":
    crawl()
   