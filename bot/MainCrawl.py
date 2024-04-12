import json,sqlite3
from datetime import datetime
from decimal import Decimal

from scripts.indigoCrawl import isInStock as isInStockIndigo
from scripts.indigoCrawl import crawl as crawlIndigo
from scripts.bestbuyCrawl import crawl as crawlBestBuy
from scripts.toysrusCrawl import crawl as crawlToysRUs
from scripts.legositeCrawl import crawl as crawlLegoSite


def main():
    print("Connecting to DB...")
    conn = sqlite3.connect('LegoLogs.db')
    conn.row_factory = sqlite3.Row #allows access to columns by name
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date
    #initialize list of alerts
    alerts = []
    #get watchlist
    print("Retreiving watchlist...")
    watchlist = cursor.execute('''SELECT * FROM watchlist''').fetchall()
    currentLogs = cursor.execute('''SELECT MAX(log_id) FROM logs ''').fetchone()
    if currentLogs[0] is None:
        currentLogs=0
    else:
        currentLogs=int(currentLogs[0])+1
        
    #execute the indigoIndigo Crawler
    print(currentLogs)
    data = {}
    print("Crawling sites...")
    try:
        print("Crawling Indigo...")
        data["indigoData"],currentLogs = crawlIndigo(0)
    except Exception as e:
        print('Error crawling Indigo: ',e)
    print(currentLogs)
    try:
        print("Crawling BestBuy...")
        data["bestbuyData"],currentLogs = crawlBestBuy(currentLogs)
    except Exception as e:
        print('Error crawling BestBuy: ',e)
    print(currentLogs)
    try:
        print("Crawling ToysRUs...")
        data["toyrusData"],currentLogs = crawlToysRUs(currentLogs)
    except Exception as e:
        print('Error crawling ToysRUs: ',e)
    try:
        print("Crawling LegoSite...")
        data["legositeData"],currentLogs = crawlLegoSite(currentLogs)
    except Exception as e:
        print('Error crawling LegoSite: ',e)
    print(currentLogs)
    
    print("Comparing new Logs to watchlist...")
    #Save the results to the database
    for site in data:
        print(site)
        for item in data[site]:
            print(item)
            cursor.execute('''INSERT INTO logs (log_id,datetime,shop_id,set_num,price,inStock,pickup,ships,link) VALUES (?,?,?,?,?,?,?,?,?)''',
            (item['log_id'],item['date'],1,item['set_num'],Decimal(item['price'])/100,item['inStock'],0,0,item['link']))
            for watch in watchlist:
                if watch['set_num']==item['set_num']: #if the product is in the watchlist
                    if item['price']<=watch['target_price']:  #if good price (watch['price'] is in dollars, item['price'] is in cents)
                        if item['inStock']==1:  #if available
                            cursor.execute('''INSERT INTO hitlist (watchlist_id,log_id) VALUES (?,?)''',(watch['watchlist_id'],item['log_id']))
                            alerts.append(item)
                            print("Found a good deal! ",item['set_num'],item['price'])
    print("Done! Committing changes to DB...")
    conn.commit()
    conn.close()


    #save the alerts to a json file
    if len(alerts) > 0:
        with open('./data/hitlist.json', 'w') as outfile:
            json.dump(alerts, outfile)
            print('We found some good deals! :)')
    else:
        print('No deals today. :(')
    return alerts

if __name__ == "__main__":
    main()