import os
import pandas as pd
import requests

def download_img(link, savepath, warning = True):
    dirpath = os.path.dirname(savepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    if os.path.isfile(savepath):
        print('Warning: Image file already exists! ' + savepath)

    img = requests.get(link)

    print('Save file: ' + savepath)

    with open(savepath, "wb") as file:
        file.write(img.content)

def save_csv(df, savepath, index = False, header = False, warning = True):
    dirpath = os.path.dirname(savepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    if os.path.isfile(savepath):
        print('Warning: Csv file already exists! ' + savepath)

    print('Save file: ' + savepath)
    df.to_csv(savepath, index=index, header=header)