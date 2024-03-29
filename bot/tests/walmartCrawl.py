from selenium import webdriver
from selenium.webdriver.common.by import By
import json,re,time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#import undetected_chromedriver as uc 

from selenium_stealth import stealth



#Walmart has a bot detection
#It has a json_blob containing all the info abt the products in the current page
#Selenium is only used to move between pages, maybe it could be done only by sending a request per page.
# Selinium might be blocked by the bot detection, try using better headers and proxies


def scanSite(driver,data):

        site = driver.find_element(By.XPATH,"//body").get_attribute('outerHTML')
        soup = BeautifulSoup(site, "html.parser")

        #find the data of the page
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    
        if script_tag is not None:
            json_blob = json.loads(script_tag.get_text())
            product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
    
    
        for tile in product_list:

            #make sure the tile is a product
            if not tile['__typename']=="Product": continue

            # Find the price, name ,date and link of the product
            name = tile['name']
            try:                                                                                        
                name=re.findall(r'\b\d{5}\b', name)[0]                          #clean it 
            except Exception as error:
                print(error)
                print("error in : "+name)
    
            price =tile["priceInfo"]["linePrice"]
            price=int(price.replace(".","").replace("$",""))  #clean it
    
            href="https://www.walmart.ca"+tile["canonicalUrl"]
    
            date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date
            inStock=tile["availabilityStatusV2"]
            # Create a dictionary with the scraped data
            product = {
                'name': name,   #Series number
                'price': price, #Price in cents
                'href': href,  #Link to the product
                'date': date,    #Data's date
            }
    
            # Append the dictionary to the list
            data.append(product)
            
        #If there is a next page button, click it and scan the site again
        nextPage = driver.find_element(By.XPATH,"//a[@data-testid()='NextPage']")
        if nextPage:
            actions = ActionChains(driver)#initialize the action chain=
            actions.move_to_element(nextPage).click().perform() 
            time.sleep(3)
            scanSite(driver,data)
            

def crawl():
    
    url ='https://www.walmart.ca/en/search?q=lego'

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("useAutomationExtension", False) 
    

    driver = webdriver.Chrome(options=options) 
    
    data=[]
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    #go to the website
    driver.get(url)
    time.sleep(4)
    #accept cookies
    element = driver.find_element(By.XPATH, "//button[text()='Accept all']")
    actions = ActionChains(driver)#initialize the action chain=
    actions.move_to_element(element).click().perform()
    time.sleep(2)
    #scan the site, if more pages, it recursively calls itself to scan the next page
    scanSite(driver,data)
    driver.quit()
    


    with open('./data/Walmarttest.json', 'w') as outfile:
            json.dump(data, outfile)
            print('Walmart sales data has been scraped and saved to ./data/IndigoCurrent.json')
            outfile.close()
    return data



if __name__ == "__main__":
    crawl()