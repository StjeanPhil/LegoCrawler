import json
import indigoCrawl
import requests
from bs4 import BeautifulSoup


#Tests if the product is in stock. Return true/false
def isInStock(p):
    # Define the URL    
    url="https://www.indigo.ca/en-ca/search?q="+p["name"]+"+lego"
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the "add to cart" button
    symbol = soup.find(class_='add-to-cart')
    #check if the "add to cart" button is disabled
    if symbol.get('disabled') !="":
        return True
    return False

def main():

    #initialize list of alerts
    alerts = []

    #get wathclist
    watchlist = json.loads(open('watchlist.json').read())


    #execute the indigoIndigo Crawler
    exec(open('indigoCrawl.py').read())
    #Get the result from the crawler
    indigoData =json.loads(open('./data/IndigoCurrent.json').read())


    #compare price of products with watchlist
    for item in indigoData:
        for watch in watchlist:
            if item['name'] == watch['name']:
                if int(item['price']) < int(watch['price']):
                    product= {
                        'name': item['name'],
                        'price': item['price'],
                        'site': 'Indigo'
                    }
                    #if the product is in stock, add it to the alerts
                    if isInStock(product):alerts.append(product)

    #save the alerts to a json file
    if len(alerts) > 0:
        with open('IndigoCurrent.json', 'w') as outfile:
            json.dump(alerts, outfile)
            print('We found some good deals! :)')
    else:
        print('No deals today. :(')

if __name__ == "__main__":
    main()