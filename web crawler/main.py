from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import urllib

import requests
from bs4 import BeautifulSoup

def Get_links():
    chrome.get('https://tm.ncl.edu.tw/overview_index?lang=chn&collection=C_TWrubbing&page=1&page_limit=100')
    result_items = list()

    while len(result_items) == 0:
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        result_items = soup.find_all('div', class_='result_item-list", limit=1)
        time.sleep(1)

    links = list()
    for result_item in result_items:
        children = result_item.find_all('a', href=True, recursive=False)
        if len(children) != 1:
            raise ValueError(f'Error: find link, but there are {len(children)} <a>.')

        links.append(urllib.parse.urljoin(base, children[0].get('href')))
    
    return links

if __name__ == '__main__':
    options = Options()
    options.add_argument('--disable-notifications')

    base = 'https://tm.ncl.edu.tw'

    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    
    links = Get_links()

    


    #print(result_items)
    #print(soup.prettify())