import requests
from bs4 import BeautifulSoup
url="https://www.indigo.ca/en-ca/black-panther-76215/673419361859.html"

#url="https://www.indigo.ca/en-ca/search?q="+product["name"]+"+lego"
response = requests.get(url)
# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
# Find all elements with class "searchProductTiles"
symbol = soup.find(class_='add-to-cart')
#check if the element is disabled

if symbol.get('disabled')!="" : print(symbol)