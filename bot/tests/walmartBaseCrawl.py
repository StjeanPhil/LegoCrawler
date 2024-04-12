
from selenium.webdriver.common.by import By
import json,re,time
from bs4 import BeautifulSoup
from datetime import datetime

from seleniumbase import Driver




#Walmart has a bot detection
#It has a json_blob containing all the info abt the products in the current page
#Selenium is only used to move between pages, maybe it could be done only by sending a request per page.
# Selinium might be blocked by the bot detection, try using better headers and proxies

def findnbpages(soup):
    #find the number of pages
    try:
        navBar=soup.find("nav",{"aria-label":"pagination"})
        return int(navBar.find_all("li")[-2].text)
    except Exception as error:
        print("Error in finding the number of pages")
        print(error)
        return 1

def scanSite(driver,data):

    site = driver.get_page_source()
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
        
        try:         
            name = tile['name']                                                                               
            name=re.findall(r'\b\d{5}\b', name)[0]                          #clean it 

            price =tile["priceInfo"]["linePrice"]
            price=int(price.replace(".","").replace("$","").replace(",",""))  #clean it

            href="https://www.walmart.ca"+tile["canonicalUrl"]

            date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date
            #inStock=tile["availabilityStatusV2"]
            # Create a dictionary with the scraped data
            product = {
                'name': name,   #Series number
                'price': price, #Price in cents
                'href': href,  #Link to the product
                'date': date,    #Data's date
            }
        except Exception as error:
            print(error)
            print("error in : "+name)
    
        # Append the dictionary to the list
        data.append(product)
    nbpages=findnbpages(soup)
    return data,nbpages

def crawl():
    
    #url ='https://www.walmart.ca/en/search?q=lego&facet=f_SellerType_en%3AWalmart%7C%7Cf_Availability_en%3AOnline%7C%7Cbrand%3ALEGO&catId=10011_6000205043132'

    url='https://www.walmart.ca/en/search?q=lego&catId=6000205043208&icid=search_page_toys_lego_ninjago_43376_WLGFO8Y423'

    driver=Driver(uc=True) 
    
    data=[]

    try:
             #go to the website
        driver.uc_open_with_reconnect(url,3)
        time.sleep(4)    
        driver.uc_click('button:contains("Accept all")')
        time.sleep(4)

        data,nbpages=scanSite(driver,data)
        for i in range(2,nbpages+1):
            newurl=url+"&page="+str(i)
            driver.uc_open_with_reconnect(newurl,3)
            time.sleep(2)
            data=scanSite(driver,data)

        
    finally:

        driver.quit()



    with open('./data/Walmarttestgo.json', 'w') as outfile:
            json.dump(data, outfile)
            print('Walmart sales data has been scraped and saved to ./data/Walmarttestgo.json')
            outfile.close()
    return data



if __name__ == "__main__":
    crawl()