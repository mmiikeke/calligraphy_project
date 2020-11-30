from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup

import urllib
import pandas as pd

def Get_links():
    chrome.get('https://tm.ncl.edu.tw/overview_index?lang=chn&collection=C_TWrubbing&page=1&page_limit=100')
    result_items = list()

    while len(result_items) == 0:
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        result_items = soup.find_all('div', class_='result_item-list', limit=1)
        time.sleep(1)

    links = list()
    for result_item in result_items:
        children = result_item.find_all('a', href=True, recursive=False)
        if len(children) != 1:
            raise ValueError(f'Error: find link, but there are {len(children)} links.')

        links.append(urllib.parse.urljoin(base, children[0].get('href')))
    
    return links

def Get_datas(links):
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup.prettify())

        #Get data
        result_items = soup.find_all('div', class_='detail_list')

        for index, result_item in enumerate(result_items):
            title = result_item.find_all('div', class_='detail-th', recursive=False)
            if len(title) != 1:
                raise ValueError(f'Error: find title, but there are {len(title)} titles.')
            title = title[0].getText()

            data = result_item.find_all('div', class_='detail-td', recursive=False)
            if len(data) != 1:
                raise ValueError(f'Error: find data, but there are {len(data)} datas.')
            data = data[0].getText()

            print(f'{index} {title} \t {data}')

            if title in Titles:
                location = Titles.index(title)
                
            #df = pd.DataFrame()

if __name__ == '__main__':
    options = Options()
    options.add_argument('--disable-notifications')

    base = 'https://tm.ncl.edu.tw'

    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    
    Titles = ['index', '碑揭名稱', '碑揭類別', '碑揭原文', 'item_link', 'image_link']

    links = Get_links()
    Get_datas(links)
    



    #print(result_items)
    #print(soup.prettify())