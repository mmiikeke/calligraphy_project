from pathlib import Path
import sys
sys.path.insert(0, str(Path('..').resolve()))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import urllib

import pandas as pd
from utils.tools import download_img, save_csv 

def Get_item_links():
    item_links = list()

    # 21 pages
    for i in range(21):
        chrome.get(f'https://tm.ncl.edu.tw/overview_index?lang=chn&collection=C_TWrubbing&page={i+1}&page_limit=100')

        result_items = list()
        while len(result_items) == 0:
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            result_items = soup.find_all('div', class_='result_item-list', limit=200)
            time.sleep(0.2)
        
        for result_item in result_items:
            children = result_item.find_all('a', href=True, recursive=False)
            if len(children) != 1:
                raise ValueError(f'Error: find link, but there are {len(children)} links.')

            item_links.append(urllib.parse.urljoin(base, children[0].get('href')))
    
    return item_links

def Get_image(soup, link_index):
    image_item = soup.find_all('div', class_='popup-gallery')
    if len(image_item) == 0:
        print(f'Error: find image item, but there are {len(image_item)} image items.')
        return None
    elif len(image_item) > 1:
        raise ValueError(f'Error: find image item, but there are {len(image_item)} image items.')

    image_item = image_item[0].find_all('a', href=True, recursive=False)
    if len(image_item) == 0:
        print(f'Error: find image item, but there are {len(image_item)} image items.')
        return None
    elif len(image_item) > 1:
        raise ValueError(f'Error: find image item, but there are {len(image_item)} image items.')

    image_link = urllib.parse.urljoin(base, image_item[0].get('href'))

    download_img(image_link, str(image_savedir / f'{link_index}.jpg'))

    return image_link

def Get_item_datas(links, start = 0):
    item_datas = list()

    for link_index, link in enumerate(links):
        print(f'Get page: {link_index}/{len(links)-1}.')

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup.prettify())

        result_items = soup.find_all('div', class_='detail_list')

        locations = list()

        # Get Title
        for index, result_item in enumerate(result_items):
            th = result_item.find_all('div', class_='detail-th', recursive=False)
            if len(th) != 1:
                raise ValueError(f'Error: find title, but there are {len(th)} titles.')
            th = th[0].getText()

            if th in Titles:
                locations.append(Titles.index(th))
            else:
                Titles.append(th)
                locations.append(len(Titles)-1)
                print(f'Find new title: |{th}|, total len = {len(Titles)}.')
        time.sleep(0.1)

        # Get Data
        data = [None] * len(Titles)
        for index, result_item in enumerate(result_items):     
            td = result_item.find_all('div', class_='detail-td', recursive=False)
            if len(td) != 1:
                raise ValueError(f'Error: find data, but there are {len(td)} datas.')
            td = td[0].getText()

            data[locations[index]] = td
        time.sleep(0.1)

        # Get image
        image_link = Get_image(soup, link_index)
        time.sleep(0.1)

        # Fill other field
        data[0] = link_index
        data[4] = link
        data[5] = image_link

        # Final append
        item_datas.append(data)


    return item_datas

if __name__ == '__main__':
    options = Options()
    options.add_argument('--disable-notifications')

    base = 'https://tm.ncl.edu.tw'
    image_savedir = Path('../../../data/part2/images').resolve()
    csv_savepath = Path('../../../data/part2/data.csv').resolve()

    image_savedir.mkdir(parents=True, exist_ok=True)
    csv_savepath.parent.mkdir(parents=True, exist_ok=True)

    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    
    Titles = ['index', '碑碣名稱', '碑碣類別', '碑碣原文', 'item_link', 'image_link']

    links = Get_item_links()
    datas = Get_item_datas(links)
    df = pd.DataFrame(datas)
    save_csv(df, str(csv_savepath), header=Titles)