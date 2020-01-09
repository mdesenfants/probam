import requests
from bs4 import BeautifulSoup
from time import sleep
import json
from os import path
import certifi

base_url = 'https://new.myubam.com'

urls = [base_url]
products = set()
visited = set()

if path.exists('product_links.json'):
    with open('product_links.json', 'r') as infile:
        products = json.load(infile)
        print(len(products), "products listed. Delete product_links.json to reset.")
else:
    for url in urls:
        if url in visited:
            continue

        print("Visiting:", url)
        res = requests.get(url, verify=certifi.where())
        soup = BeautifulSoup(res.text, features='html.parser')

        visited.add(url)

        for link in soup.find_all('a', href=True):
            href = link['href']
            if len(href) > 1 and href[0] == '/':
                href = base_url + href

            if '/p/' in href:
                products.add(href)
            elif '/c/' in href:
                urls.append(href)
        
        sleep(5) # don't DDOS the poor folks

    with open('product_links.json', 'w') as outfile:
        json.dump([p for p in products], outfile)

    with open('visisted_links.json', 'w') as outfile:
        json.dump([v for v in visited], outfile)
