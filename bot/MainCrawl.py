import json,sqlite3
from datetime import datetime
from decimal import Decimal
from utils.discordBot import sendDiscordAlert

from scripts.indigoCrawl import crawl as crawlIndigo
from scripts.bestbuyCrawl import crawl as crawlBestBuy
from scripts.toysrusCrawl import crawl as crawlToysRUs
from scripts.legositeCrawl import crawl as crawlLegoSite
#add log to end of file
def log(msg):
    with open('./data/log.txt', 'a') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - '+msg+'\n')

def main():
    log("Starting MainCrawl.py")
    log("Connecting to DB...")    
    conn = sqlite3.connect('LegoLogs.db')
    conn.row_factory = sqlite3.Row #allows access to columns by name
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date
    #initialize list of alerts
    alerts = []
    #get watchlist
    log("Retreiving watchlist...")
    watchlist = cursor.execute('''SELECT * FROM watchlist''').fetchall()
    currentLogs = cursor.execute('''SELECT MAX(log_id) FROM logs ''').fetchone()
    if currentLogs[0] is None:
        currentLogs=0
    else:
        currentLogs=int(currentLogs[0])+1
        
    #execute the indigoIndigo Crawler
    
    data = {}
    log("Crawling sites...")
    try:
        log("Crawling Indigo...")
        data["indigoData"],currentLogs = crawlIndigo(0)
    except Exception as e:
        log('Error crawling Indigo: ',e)
    log(currentLogs)
    try:
        log("Crawling BestBuy...")
        data["bestbuyData"],currentLogs = crawlBestBuy(currentLogs)
    except Exception as e:
        log('Error crawling BestBuy: ',e)
    log(currentLogs)
    try:
        log("Crawling ToysRUs...")
        data["toyrusData"],currentLogs = crawlToysRUs(currentLogs)
    except Exception as e:
        log('Error crawling ToysRUs: ',e)
    try:
        log("Crawling LegoSite...")
        data["legositeData"],currentLogs = crawlLegoSite(currentLogs)
    except Exception as e:
        log('Error crawling LegoSite: ',e)
    log(currentLogs)
    
    log("Comparing new Logs to watchlist...")
    #Save the results to the database
    for site in data:
        print(site)
        for item in data[site]:
            print(item)
            cursor.execute('''INSERT INTO logs (log_id,datetime,shop_id,set_num,price,inStock,pickup,ships,link) VALUES (?,?,?,?,?,?,?,?,?)''',
            (item['log_id'],item['date'],item['shop_id'],item['set_num'],Decimal(item['price']),item['inStock'],0,0,item['link']))
            for watch in watchlist:
                if watch['set_num']==item['set_num']: #if the product is in the watchlist
                    if item['price']<=watch['target_price']:  #if good price (watch['price'] is in dollars, item['price'] is in cents)
                        if item['inStock']==1:  #if available
                            cursor.execute('''INSERT INTO hitlist (watchlist_id,log_id) VALUES (?,?)''',(watch['watchlist_id'],item['log_id']))
                            alert=item
                            alert["target_price"]=watch["target_price"]
                            alert["watchlist_id"]=watch["watchlist_id"]

                            alert["shop"]=cursor.execute('''SELECT name FROM shops WHERE shop_id=(?)''',str(item['shop_id'])).fetchone()[0]
                            alert["name"]=cursor.execute('''SELECT name FROM products WHERE set_num=(?)''',str(item['set_num'])).fetchone()[0]
                            alerts.append(alert)
                            log("Found a good deal! ",item['set_num'],Decimal(item['price']))
    log("Done! Committing changes to DB...")
    conn.commit()
    conn.close()


    #save the alerts to a json file
    if len(alerts) > 0:
        log("Sending "+len(alerts)+" alerts to dicord")
        with open('./data/hitlist.json', 'w') as outfile:
            json.dump(alerts, outfile)
            print('We found some good deals! :)')
        for alert in alerts:
            #send a discord alert 
            sendDiscordAlert(alert)

    else:
        print('No deals today. :(')
    return alerts

if __name__ == "__main__":
    main()