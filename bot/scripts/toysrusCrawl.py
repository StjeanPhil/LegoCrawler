import json,re,time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def crawl(currId):
    #f= open("./data/ToysRUsCurrent.json","r")
    #data=json.load(f)
    #return data,currId
    url="https://www.toysrus.ca/en/toysrus/Brands/L/LEGO/See-All-LEGO?prefn1=brandFilter&prefv1=LEGO&prefn2=carSeatNHTSARating&prefv2=TRU"


    
    #initialize the webdriver
    driver=webdriver.Chrome()
    driver.get(url)

    #NAVIGATE THE PAGE
    time.sleep(2) #let the cookie pop up appear
    
    accceptCookies = driver.find_element(By.ID,'onetrust-accept-btn-handler') #Accept the cookies
    accceptCookies.click()
    
    time.sleep(2) #chillll

    actions = ActionChains(driver)#initialize the action chain=
    
    while True: #Click the "load more" button as much as possible

        try:
            loadMoreButton = driver.find_element(By.CLASS_NAME,'b-load_more-button ') #find the button
            actions.move_to_element(loadMoreButton).click().perform()            #move the mouse to the button and click
            time.sleep(6)                                                        #give time to load

        except Exception as error:
            print("No more products to load")
            print(error)
            break

    #get the page's HTML after scrolling and loading all the products
    response = driver.find_element(By.XPATH,"//body").get_attribute('outerHTML')

    #Parse the HTML content for the products
    soup = BeautifulSoup(response, 'html.parser')
    tiles = soup.find_all('div', class_='b-product_tile-inner')

    data=[] #list of products
    date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date
    #Parse through each product
    for tile in tiles:

        # Find the price, name ,link and date
        try:
            title=tile.find('a',class_='b-product_tile-title_link') #find the name
            name = title.text.strip()                     
            try:                                                                                        
                name=re.findall(r'\b\d{5}\b', name)[0]    #clean the name
            except Exception as error:
                print(error)
                #name=title.text.strip()
            

            price = tile.find('span', class_='b-price-value').text.strip() #find it
            price = int(price.replace(".","").replace("$",""))  #clean it
            

            href=title.get('href')  

            if tile.find('div',class_='b-product_shipping_info')['data-availabilitytype']=="instock":
                inStock=1
            else:
                inStock=0
            ships=tile.find_all(class_=['js-homeDelivery',' m-available'])
            ships=1 if ships else 0
            pickup=tile.find_all(class_=['js-freeInStorePickup',' m-available'])
            pickup=1 if pickup else 0


            # Create a dictionary with the scraped data
            product = {
                'log_id': currId,   #Unique id for the log
                'date': date,    #Data's date
                'shop_id': 4,   #Shop's id
                'set_num': name,   #Series number
                'price': price, #Price in cents
                'link': "https://www.toysrus.ca"+href,  #Link to the product
                'inStock':inStock, #True if the product is in stock, False otherwise
                'ships':ships, # not sure how this work but seems important to add
                'pickup':pickup 
   
                

            }

            # Append the dictionary to the list
            data.append(product)
            currId+=1
            

        except Exception as error:
            print(error)
            

    #save the scraped data to a json file
    with open('./data/ToysRUsCurrent.json', 'w') as outfile:
        json.dump(data, outfile)
        print('ToysRUs sales data has been scraped and saved to ./data/ToysRUsCurrent.json')
        outfile.close()
    
    return data,currId


if __name__ == "__main__":
    crawl()