import json

from scripts.indigoCrawl import isInStock as isInStockIndigo
from scripts.indigoCrawl import crawl as crawlIndigo
from scripts.bestbuyCrawl import crawl as crawlBestBuy
from scripts.toysrusCrawl import crawl as crawlToysRUs
from scripts.legositeCrawl import crawl as crawlLegoSite

def main():

    #initialize list of alerts
    alerts = []
    #get watchlist
    watchlist = json.loads(open('./data/watchlist.json').read())
    #execute the indigoIndigo Crawler
    indigoData =crawlIndigo()
    bestbuyData =crawlBestBuy()
    toyrusData =crawlToysRUs()
    legostieData= crawlLegoSite()
    #compare price of products with watchlist
    for watch in watchlist:
        #Indigo 
        #DOES NOT HAVE STOCK IN THE SEARCH PAGE, STOCK IS ONLY CHECKED IF THE PRODUCT IS IN THE WATCHLIST
        for item in indigoData:
            if item['name'] == watch['name']:
                if int(item['price']) < int(watch['price']):
                    product=item
                    product['store']='Indigo'
                    #if the product is in stock, add it to the alerts
                    if isInStockIndigo(product):
                        product['inStock']=True
                        alerts.append(product)
        #BestBuy
        #Has both store and online stock in the search page
        for item in bestbuyData:
            if item['name'] == watch['name']:
                if int(item['price']) < int(watch['price']):
                    if item['inStock'] == True or item['inStore'] == True:
                        product=item
                        product['store']='BestBuy'
                        alerts.append(product)
        #ToysRUs
        for item in toyrusData:
            if item['name'] == watch['name']:
                if int(item['price']) < int(watch['price']):
                    if item['inStock'] == True or item['available'] == "Pickup Only":
                        product=item
                        product['store']='ToysRUs'

                        alerts.append(product)
        #LegoSite
        for item in legostieData:
            if item['name'] == watch['name']:
                if int(item['price']) < int(watch['price']):
                    product=item
                    product['store']='LegoSite'
                    alerts.append(product)

    #save the alerts to a json file
    if len(alerts) > 0:
        with open('./data/hitlist.json', 'w') as outfile:
            json.dump(alerts, outfile)
            print('We found some good deals! :)')
            
    else:
        print('No deals today. :(')
    return(alerts)

if __name__ == "__main__":
    main()