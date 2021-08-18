import os

outpath = 'result/output_dense_4808_6817_128_pad10_retrain'
use_dense = True
batchSize = 16
dataroot = 'data/4808_6817_128_pad10'
os.system(f'python train.py --dataroot {dataroot} --batchSize {batchSize} --cuda --outpath {outpath}{" --dense" if use_dense else ""}')

"""
outpath = 'result/output_resnet_4808_6817_128_pad10'
use_dense = False
batchSize = 16
dataroot = 'data/4808_6817_128_pad10'
os.system(f'python train.py --dataroot {dataroot} --batchSize {batchSize} --cuda --outpath {outpath}{" --dense" if use_dense else ""}')
"""