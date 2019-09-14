import requests
import certifi
import json
from bs4 import BeautifulSoup

book_path = "https://new.myubam.com/p/7821/alices-adventures-in-wonderland-illustrated-originals-ir"
product = requests.get(book_path, verify=certifi.where()).text

soup = BeautifulSoup(product, features='html.parser')

books = {}

# loop starts here
book_scrape = {}

h1 = soup.find('h1', {'class': 'productname'})
book_scrape['title'] = h1.text.strip()

stats = soup.find('div', {'class': 'product-variant-list'})
stats_table = stats.find('table')
stats_body = stats_table.find('tbody')
stats_rows = stats_table.find_all('tr')[0:2]

headers = []
values = []

for row in stats_rows:
    headers = headers + [th.text.strip() for th in row.find_all('th')]
    values = values + [td.text.strip() for td in row.find_all('td')];

book_scrape['details'] = dict(zip(headers, values))
books.append(book_scrape)

# loop ends here

with open('full_catalogue.json', 'w') as catalog:
    json.dump(books)
