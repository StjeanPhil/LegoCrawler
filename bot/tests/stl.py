from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
#import config
from selenium_stealth import stealth
import json
from bs4 import BeautifulSoup

def main() :
    url ='https://www.lego.com/en-ca/categories/sales-and-deals?filters.i0.key=categories.id&filters.i0.values.i0=12ba8640-7fb5-4281-991d-ac55c65d8001'

    #url ="https://bot.incolumitas.com"
    #url="https://bot.sannysoft.com/"
    #initialize the browser
    # Create Chromeoptions instance 
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
        fix_hairline=True
        )
    #go to the website
    data=[]
    #for i in range():
    url_pages=url#+"/?page="+str(i)
    driver.get(url_pages)
    sleep(5)
    # Find the script element with id "__NEXT_DATA__"

    site = driver.find_element(By.XPATH,"//body").get_attribute('outerHTML')
    soup = BeautifulSoup(site, "html.parser")
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    
    if script_tag is not None:
        json_blob = json.loads(script_tag.get_text())
        product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
        data.append(product_list)

    driver.quit()
    print(script_tag)
    print(data)
    


if __name__ == "__main__":
    main()