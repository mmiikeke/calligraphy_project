from pathlib import Path
import sys
sys.path.insert(0, str(Path('../../..').resolve()))

import time
import requests
from bs4 import BeautifulSoup
import urllib

import pandas as pd
from utils.tools import download_img, save_csv, save_xlsx 

def Get_font_links():
    font_links = list()

    response = requests.get(base)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())

    result_items = soup.find_all('option')
    for item in result_items:
        if item.get('value').isdigit():
            font_links.append([item.getText(), item.get("value") ,f'http://163.20.160.14/~word/modules/myalbum/viewcat.php?pos=0&cid={item.get("value")}&num={num_per_page}&orderby=dateD'])
    
    print(f'Get {len(font_links)} links')
    #for i in font_links:
    #    print(f'{i[0]}\t{i[1]}\t{i[2]}')

    return font_links


def Get_font_data(cid, csvdir, imagedir):
    font_datas = list()
    link = f'http://163.20.160.14/~word/modules/myalbum/viewcat.php?pos=0&cid={cid}&num={num_per_page}&orderby=dateD'
    counter = 0
    # Iterate different pages
    while True:
        # Get page items
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_items = soup.find_all('img', attrs = {'title' : True})

        # Check if next page is exist
        result_items = soup.find_all('a', class_='xo-pagarrow')
        flag = False
        for item in result_items:
            if item.getText() == '»':
                flag = True
                new_link = urllib.parse.urljoin(base, item.get('href'))
        
        # Check if number of items is correct
        if len(page_items) != num_per_page and flag == True:
            print(f'Warining: I get {len(page_items)} items at {link}')

        for item in page_items:
            data = [None] * len(Titles)
            data[0] = counter
            data[1] = item['title']
            image_link = item['src']
            download_img(image_link, str(imagedir / f'{counter}.png'), show_info=False)
            
            # Final append
            font_datas.append(data)
            counter += 1

        if flag == False:
            break
        link = new_link
        time.sleep(1)
        print(counter)

    df = pd.DataFrame(font_datas)
    save_csv(df, str(csvdir/'data.csv'), header=Titles)
    save_xlsx(df, str(csvdir/'data.xlsx'), header=Titles)

if __name__ == '__main__':
    base = 'http://163.20.160.14/~word/modules/myalbum/index.php'
    num_per_page = 500
    data_savedir = Path('../../../data/part1').resolve()

    data_savedir.mkdir(parents=True, exist_ok=True)
    
    Titles = ['index', 'char']

    font_links = Get_font_links()

    for index, font_link in enumerate(font_links):
        savedir = Path(data_savedir) / font_link[0]
        if savedir.is_dir():
            print(f'{font_link[0]} already exist, {index+1}/{len(font_links)}')
            continue
        print(f'Processing {font_link[0]}, {index+1}/{len(font_links)}')
        (savedir / 'images').mkdir(parents=True, exist_ok=False)
        data = Get_font_data(font_link[1], savedir, savedir / 'images')