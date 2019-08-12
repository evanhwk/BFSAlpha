#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen

SC_URL = 'https://www.bookfinder.com/search/isbn/?keywords=9780545010221&currency=AUD&destination=au&mode=basic&classic=off&lang=en&st=sh&ac=qr&submit=&ps=bp'
SC_URL2 = 'https://www.bookfinder.com/search/?ac=sl&st=sl&ref=bf_s2_a3_t1_3&qi=Dt,Us0dzl6NPZWQo3Z1v3F3dWVk_1497963026_1:155:78&bq=author%3Drobin%2520boyd%26title%3Daustralian%2520ugliness'
SC_URL3 = 'https://www.bookfinder.com/search/?ac=sl&st=sl&ref=bf_s2_a1_t1_1&qi=rntS0Q4Oq1rGp5eGDeDkkFlsC3o_1497963026_1:8:1&bq=author%3Dalvin%2520toffler%26title%3Dthird%2520wave'

def init_bookfinder(url):
    """ Init BFS by retreving webpage and scraping

    Args:
        url: URL of the webpage to be scraped

    Returns:
        A BeautifulSoup object representing the scraped webpage
    """

    html = urlopen(url).read()
    soup =  BeautifulSoup(html, 'lxml')
    return soup

def get_book_count(soup):
    """ Get count of used and new books

    Args:
        soup: A BeautifulSoup object representing the scraped webpage

    Returns:
        An array (format : [New, Used]) representing # of books found, New and Used.
    """

    count_arr = [None, None]                                                # [ New, Used ]
    headers = soup.find_all('h3','results-section-heading')             # find h3 headers

    # Get New/Used Book Headers from <h3> in soup
    for hd in headers:
        txt = hd.get_text()                                             # strip html tags
        txt_list = txt.split()                                          # split by spaces
        if (txt_list[0] == 'New' or txt_list[0] == 'Used'):
            count = int(txt_list[-1])                                   # find all nums, skipping first 4 elements
            # if valid count
            if count > 0:
                if txt_list[0] == 'New':
                    count_arr[0] = count
                elif txt_list[0] == 'Used':
                    count_arr[1] = count

    return count_arr                                                    # format: [ New, Used ]

def get_book_prices(soup):
    """ Get the price of both the cheapest new and used book and most expensive new and used book.

    Args:
        soup: A BeautifulSoup object representing the scraped webpage

    Returns:
        An array (format : [New, Used] OR [x]) representing $ of books found, New and Used.
    """

    lowest = []
    highest = []
    tables = soup.find_all('table', 'results-table-Logo')               # find tables

    for table in tables:
        lowest.append(get_low(table))
        highest.append(get_high(table))                                 # len => 1 or 2 / [X] or [New, Used]
    return [ lowest, highest ]                                          # len = 2

def get_low(table):
    """ Get the cheapest price in results-table table

    Args:
        table: A BeautifulSoup object representing the table

    Returns:
        Price of the cheapest book in the table
    """
    # ===========================
    # | 1   |  ...     |   $x.xx| <<<<
    # ---------------------------
    # ...                 ^^^^^^

    p = None
    tr = table.find('tr', 'results-table-first-LogoRow has-data')       # find first table-row
    td = tr.find_all('td')
    if td:
        p = td[-1].get_text()                                           # find last column and convert to text => p

    return p

def get_high(table):
    """ Navigate to the last page (if possible) and get the highest price in results-table table

    Args:
        table: A BeautifulSoup object representing the table

    Returns:
        Price of the cheapest book in the table
    """
    url = None
    # ...
    # ==========================================
    # | <PREV   | (OVERVIEW 1 >>> 2 <<< )| NEXT>
    # ==========================================
    tr = table.find_all('tr', 'results-table-header-row')
    if tr:
        trh = tr[-1]                                                    # find last table-header-row
    a = trh.th.find_all('a')                                            # find all links

    if a:                                                               # if links exist, go to last page link, else assume current page is last page
        url = a[-2].get('href')                                         # find last link and convert to text => url
        html = urlopen(url).read()                                      # run BeautifulSoup
        soup2 =  BeautifulSoup(html, 'lxml')
        table2 = soup2.find('table', 'results-table-Logo')               # find tables
        p = get_high_from_table(table2)
    else:
        p = get_high_from_table(table)

    return [ p, url ]

def get_high_from_table(table):
    """ Get the highest price in results-table table

    Args:
        table: A BeautifulSoup object representing the table

    Returns:
        Price of the cheapest book in the table
    """
    # ...                 VVVVVV
    # ---------------------------
    # | n   |  ...     |   $x.xx| <<<<
    # ===========================

    p = None
    tr = table.find_all('tr', 'has-data')
    if tr:
        trl = tr[-1]
        td = trl.find_all('td')
        if td:
            p = td[-1].get_text()                                    # find last row -> last column and convert to text => p
    return p

soup = init_bookfinder(SC_URL2)
bc = get_book_count(soup)
prices = get_book_prices(soup)

if bc[0] and bc[1]:
    print('New '+str(bc[0])+' '+ str(prices[0][0])+" "+ str(prices[1][0]) )
    print('Used '+str(bc[1])+' '+ str(prices[0][1])+" "+ str(prices[1][1]) )
elif bc[0]:
    print('New '+str(bc[0])+' '+ str(prices[0][0])+" "+ str(prices[1][0]) )
elif bc[1]:
    print('Used '+str(bc[1])+' '+ str(prices[0][0])+" "+ str(prices[1][0]) )
