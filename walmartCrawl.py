import json
#import indigoCrawl
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import re

import time



def main():

    url_root= "https://www.walmart.ca/en/browse/toys/lego/10011_6000205043132?icid=landing%2Fcp_page_toys_shop_all_lego_18944_EU28ISZ2DN&facet=f_SellerType_en%3AWalmart%7C%7Cbrand%3ALEGO%7C%7Cf_Availability_en%3AOnline"
    #url_root= "https://www.walmart.ca"
    
    ua = UserAgent()
    #call the UserAgent as ua
    userAgent = ua.random
    # make it random
    headers = {"User-Agent": userAgent} 
    working= True
    page=0
    #list of products
    data=[]
    while working:
        working=False
        page+=1
        #url=url_root+"&page="+str(page)+"&affinityOverride=default"
        #url=url_root+"&affinityOverride=default"
        url=url_root
        soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
        print(soup)
        tiles = soup.body.find_all('div', {'data-testid': 'list-view'})
        print(len(tiles))

        
        
        for tile in tiles:
            #working=True
            try:
                price=int(tile.find('span',class_='w_q67L').contents[0].split('$')[1].replace('.','').replace(',',''))
                name=tile.find('span',{'data-automation-id':'product-title'}).contents[0]
                name=re.findall(r'\b\d{5}\b', name)[0]
                #date = datetime.now().strftime('%Y-%m-%d')  # get the current date
                #find the "a" element of the sibling element of tile

                href =tile.find_previous_sibling('a').get('href')
                #print(href)

                # Create a dictionary with the scraped data
                product = {
                    'name': name,   #Series number
                    'price': price, #Price in cents
                #    'date': date,    #Data's date
                    'link': href
                }
                # Append the dictionary to the list
                data.append(product)
            except:
                continue
            
        print(len(data))

            
        #save the scraped data to a json file
    print(len(data))
    with open('./data/WalmartCurrent.json', 'w') as outfile:
        json.dump(data, outfile)
        print('Walmart sales data has been scraped and saved to ./data/WalmartCurrent.json')
        outfile.close()






if __name__ == "__main__":
    main()

    