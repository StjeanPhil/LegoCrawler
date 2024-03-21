import requests
import json
from decimal import *
from bs4 import BeautifulSoup
from datetime import datetime

def main():
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
        name = tile.find('h3').text.strip()[-5:]
        #check that all char in c are digits
        if not name.isdigit():continue
        # Find the price, name and date
        price = int(tile.find('span', class_='sale-true').text.strip()[1:].replace(".",""))
        date = datetime.now().strftime('%Y-%m-%d')  # get the current date

        # Create a dictionary with the scraped data
        product = {
            'name': name,   #Series number
            'price': price, #Price in cents
            'date': date    #Data's date
        }

        # Append the dictionary to the list
        data.append(product)

    #save the scraped data to a json file
    with open('./data/IndigoCurrent.json', 'w') as outfile:
        json.dump(data, outfile)
        print('Indigo sales data has been scraped and saved to ./data/IndigoCurrent.json')
        outfile.close()

if __name__ == "__main__":
    main()