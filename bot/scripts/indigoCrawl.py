import requests
import json
from decimal import *
from bs4 import BeautifulSoup
from datetime import datetime

def crawl(currId):
    #f= open("./data/IndigoCurrent.json","r")
    #data=json.load(f)
    #return data,currId
    # Make a request to the website
    # Define the URL
    url="https://www.indigo.ca/en-ca/indigo-kids-baby/sale/kids-toys/lego-sets-on-sale/?start=0&sz=500"
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with class "searchProductTiles"
    tiles = soup.find_all('div', class_='product-tile')

    # Create a list to store the scraped data
    data = []

    # Loop through each tile
    for tile in tiles:
        # Find the price, name ,date and link of the product
        name = tile.find('h3').text.strip()[-5:]
        #check that all char in c are digits
        if not name.isdigit():continue
        
        price = Decimal(tile.find('span', class_='sale-true').text.strip()[1:])
        href=tile.find('a').get('href')
        date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date

        # Create a dictionary with the scraped data
        product = {
            'log_id': currId,   #Unique id for the log
            'date': date,    #Data's date
            'shop_id': 1,   #Shop's id
            'set_num': int(name),   #Series number
            'price': price, #Price in cents
            'link': 'https://www.indigo.ca'+href,  #Link to the product
            
        }
        product['inStock']=(1 if isInStock(product)else 0)
        product['ships']=(1 if product['inStock'] else 0)
        product['pickup']='2' #we are not actually checking if the product is available for pickup
        
        # Append the dictionary to the list
        data.append(product)
        currId+=1

    #save the scraped data to a json file
    with open('./data/IndigoCurrent.json', 'w') as outfile:
        json.dump(data, outfile)
        print('Indigo sales data has been scraped and saved to ./data/IndigoCurrent.json')
        outfile.close()
    return data,currId

#INDIGO DOES NOT HAVE STOCK IN THE SEARCH PAGE, STOCK IS ONLY CHECKED IF THE PRODUCT IS IN THE WATCHLIST
def isInStock(p):
    # Define the URL    
    #url="https://www.indigo.ca/en-ca/search?q="+p["name"]+"+lego"
    url=p["link"]
    response = requests.get(url,timeout=4)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the "add to cart" button
    symbol = soup.find(class_='add-to-cart')
    #check if the "add to cart" button is disabled
    if symbol.get('disabled') !="":
        return True
    return False    

if __name__ == "__main__":
    crawl()