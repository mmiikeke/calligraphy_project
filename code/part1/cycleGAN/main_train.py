import os

outpath = 'result/output_dense_48086817_pad'
use_dense = True
batchSize = 16
dataroot = 'data/4808_6817_pad'
os.system(f'python train.py --dataroot {dataroot} --batchSize {batchSize} --cuda --outpath {outpath}{" --dense" if use_dense else ""}')

outpath = 'result/output_resnet_48086817_pad'
use_dense = False
batchSize = 16
dataroot = 'data/4808_6817_pad'
os.system(f'python train.py --dataroot {dataroot} --batchSize {batchSize} --cuda --outpath {outpath}{" --dense" if use_dense else ""}')