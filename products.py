import requests
import certifi
import json
import os
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import IPython.utils.tests.test_module_paths

with open('product_links.json') as product_links:
    products = list(json.load(product_links))

books = {}

for book_path in products:
    try:
        # loop starts here
        book_id = book_path[book_path.index('/p') + 3:book_path.rfind('/')]

        if os.path.exists('./products/' + book_id + '.json'):
            print('Skipping', book_id, 'because it already exists.')
            continue

        product = requests.get(book_path, verify=certifi.where()).text

        soup = BeautifulSoup(product, features='html.parser')

        book_scrape = {}

        # get title
        h1 = soup.find('h1', {'class': 'productname'})
        book_scrape['title'] = h1.text.strip()

        # get price, hardback/softback, etc
        stats = soup.find('div', {'class': 'product-variant-list'})
        stats_table = stats.find('table')
        stats_body = stats_table.find('tbody')
        stats_rows = stats_table.find_all('tr')[0:2]

        headers = []
        values = []

        for row in stats_rows:
            headers = headers + [th.text.strip().lower() for th in row.find_all('th')]
            values = values + [td.text.strip() for td in row.find_all('td')];

        book_scrape.update(dict(zip(headers, values)))

        book_scrape['overview'] = soup.find('div', {'id': 'tabs-1'}).text.strip()

        # get table details
        try:
            productspec_page = requests.get("https://new.myubam.com/ProductTab/ProductSpecifications/" + book_id, verify=certifi.where()).text
            productspec = BeautifulSoup(productspec_page, features='html.parser')

            spectab = productspec.find('table')
            for tr in spectab.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) > 0 and len(tds[0].text.strip()) > 0:
                    key = tds[0].text.strip().lower()
                    book_scrape[key] = tds[1].text.strip()
        except:
            pass

        try:
            os.mkdir('./products')
        except:
            pass

        book_scrape['timestamp'] = datetime.now().isoformat()
        with open('./products/' + book_id + '.json', 'w') as catalog:
            json.dump(book_scrape, catalog)
            print("wrote", book_id + '.json')
        sleep(5)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Error for product", book_id)

# loop ends here

