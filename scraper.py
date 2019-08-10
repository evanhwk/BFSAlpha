#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen

SC_URL = 'https://www.bookfinder.com/search/isbn/?keywords=9780545010221&currency=AUD&destination=au&mode=basic&classic=off&lang=en&st=sh&ac=qr&submit=&ps=bp'
SC_URL2 = 'https://www.bookfinder.com/search/?ac=sl&st=sl&ref=bf_s2_a3_t1_3&qi=Dt,Us0dzl6NPZWQo3Z1v3F3dWVk_1497963026_1:155:78&bq=author%3Drobin%2520boyd%26title%3Daustralian%2520ugliness'
SC_URL3 = 'https://www.bookfinder.com/search/?ac=sl&st=sl&ref=bf_s2_a1_t1_1&qi=rntS0Q4Oq1rGp5eGDeDkkFlsC3o_1497963026_1:8:1&bq=author%3Dalvin%2520toffler%26title%3Dthird%2520wave'

def init_bookfinder(url):
    html = urlopen(url).read()
    soup =  BeautifulSoup(html, 'lxml')
    return soup

def get_book_count(soup):

    # [ New, Old ]
    count_arr = [-1, -1]

    # Find h3 headers
    headers = soup.find_all('h3','results-section-heading')

    # Get New/Used Book Header, return array with ['table', 'Max books']
    for hd in headers:
        txt = hd.get_text()
        txt_list = txt.split()
        if (txt_list[0] == 'New' or txt_list[0] == 'Used'):
            # Find all nums, skipping first 4 elements
            count = int(txt_list[-1])

            if count > 0:
                if txt_list[0] == 'New':
                    count_arr[0] = count
                elif txt_list[0] == 'Used':
                    count_arr[1] = count

    return count_arr

def get_cheapest_book(soup):

    price_arr = []
    # find tables
    tables = soup.find_all('table', 'results-table-Logo')

    for table in tables:
        price_arr.append(get_low(table))
    return price_arr

def get_low(table):
    # -----------------------
    # |    |       |   $x.xx| <<<<
    # ---------------------==
    # find table-row
    tr = table.find('tr', 'results-table-first-LogoRow has-data')
    # find last column and convert to text - this is the price
    p = tr.find_all('td')[-1].get_text()

    return p

soup = init_bookfinder(SC_URL)
print(get_book_count(soup))
print(get_cheapest_book(soup))
soup2 = init_bookfinder(SC_URL2)
print(get_book_count(soup2))
print(get_cheapest_book(soup2))
