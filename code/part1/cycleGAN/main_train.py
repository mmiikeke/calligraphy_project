import os

outpath = 'output_dense_48086817_pad'
use_dense = True
dataroot = 'data/4808_6817_pad'
os.system(f'python train.py --dataroot {dataroot} --cuda --outpath {outpath}{" --dense" if use_dense else ""}')

outpath = 'output_resnet_48086817_pad'
use_dense = False
dataroot = 'data/4808_6817_pad'
os.system(f'python train.py --dataroot {dataroot} --cuda --outpath {outpath}{" --dense" if use_dense else ""}')