from selenium import webdriver
from selenium.webdriver.common.by import By
import json,re,time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import requests as request
url="https://www.walmart.ca/en/search?q=lego&facet=f_SellerType_en%3AWalmart%7C%7Cf_Availability_en%3AOnline%7C%7Cbrand%3ALEGO&catId=10011_6000205043132&page=21"
response = request.get(url)
site=response.content
soup = BeautifulSoup(site, "html.parser")
data=[]
#find the data of the page
print(site)
script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
if script_tag is not None:
    json_blob = json.loads(script_tag.get_text())
    product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
for tile in product_list:
    #make sure the tile is a product
    if not tile['__typename']=="Product": continue
    # Find the price, name ,date and link of the product
    name = tile['name']
    print(name)
    try:                                                                                        
        name=re.findall(r'\b\d{5}\b', name)[0]                          #clean it 
    except Exception as error:
        print(error)
        print("error in : "+name)
    price =tile["priceInfo"]["linePrice"]
    price=int(price.replace(".","").replace("$",""))  #clean it
    href="https://www.walmart.ca"+tile["canonicalUrl"]
    date = datetime.now().strftime('%Y-%m-%d-%H')  # get the current date
    
    # Create a dictionary with the scraped data
    product = {
        'name': name,   #Series number
        'price': price, #Price in cents
        'href': href,  #Link to the product
        'date': date,    #Data's date
    }
    # Append the dictionary to the list
    data.append(product)
with open('./data/WalmartTest.json', 'w') as outfile:
    json.dump(data, outfile)
    print('Walmart sales data has been scraped and saved to ./data/IndigoCurrent.json')
    outfile.close()
    