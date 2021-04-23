import os
import pandas as pd
import requests

def get_files_path(root_path, end_string, interrupt = True):
    filepath_list = list()
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(end_string):
                filepath_list.append(os.path.join(root, file))
    
    if (interrupt and len(filepath_list) == 0):
        raise ValueError('Error: Can\'t find any ' + end_string + ' file in ' + root_path)

    return filepath_list

def download_img(link, savepath, warning = True, show_info=True):
    dirpath = os.path.dirname(savepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    if os.path.isfile(savepath):
        print('Warning: Image file already exists! ' + savepath)

    img = requests.get(link)

    if show_info:
        print('Save file: ' + savepath)

    with open(savepath, "wb") as file:
        file.write(img.content)

def save_csv(df, savepath, index = False, header = False, warning = True, show_info=True):
    dirpath = os.path.dirname(savepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    if os.path.isfile(savepath):
        print('Warning: Csv file already exists! ' + savepath)

    if show_info:
        print('Save file: ' + savepath)
    df.to_csv(savepath, index=index, header=header)


def save_xlsx(df, savepath, index = False, header = False, warning = True, show_info=True):
    dirpath = os.path.dirname(savepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    if os.path.isfile(savepath):
        print('Warning: Csv file already exists! ' + savepath)

    if show_info:
        print('Save file: ' + savepath)
    df.to_excel(savepath, index=index, header=header)