import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path('../../..').resolve()))

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

from myutils.tools import get_files_path

model_weight_path = Path('result/output_dense_4808_6817_128_pad10_retrain').resolve()
test = True
use_dense = True
generate_result_image = True
data_path = Path('data/4808_6817_128_pad10').resolve()
total_result_images = 10
generator_A2B = model_weight_path / '199_netG_A2B.pth'
generator_B2A = model_weight_path / '199_netG_B2A.pth'

if test:
    """ Generate A to B """
    print('\n\n======================')
    print('   Generate A to B')
    print('======================\n\n')
    in_path = data_path
    out_path = model_weight_path / 'fake' / 'test'
    os.system(f'python test2.py --dataroot {str(in_path)} --out_path {str(out_path)} --generator_A2B {str(generator_A2B)} --generator_B2A {str(generator_B2A)} --cuda{" --dense" if use_dense else ""}')

    """ Generate A to B to A """
    print('\n\n======================')
    print(' Generate A to B to A')
    print('======================\n\n')
    in_path = model_weight_path / 'fake'
    out_path = model_weight_path / 'cycle_fake' / 'test'
    os.system(f'python test2.py --dataroot {str(in_path)} --out_path {str(out_path)} --generator_A2B {str(generator_A2B)} --generator_B2A {str(generator_B2A)} --cuda{" --dense" if use_dense else ""}')

def save_multiple_img(images, savepath, rows = 1, cols=1):
    figure, ax = plt.subplots(nrows=rows,ncols=cols,figsize=(18, 2))
    for ind,image in enumerate(images):
        ax[ind].imshow(image, cmap='gray')
        #ax[ind].set_title(result_images_titles[ind])
        #ax.ravel()[ind].set_axis_off()
        ax[ind].get_xaxis().set_visible(False)
        ax[ind].get_yaxis().set_visible(False)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f'{savepath}')

if generate_result_image:

    """ Generate result images A and B """
    
    print('\n\n============================')
    print('Generate result image A and B')
    print('============================\n\n')
    path = data_path / 'test' / 'A'
    path_list = get_files_path(str(path), '.png')
    savepath = model_weight_path / 'A.png'
    images = [mpimg.imread(i) for i in path_list]
    save_multiple_img(images, str(savepath), 1, total_result_images)

    path = data_path / 'test' / 'B'
    path_list = get_files_path(str(path), '.png')
    savepath = model_weight_path / 'B.png'
    images = [mpimg.imread(i) for i in path_list]
    save_multiple_img(images, str(savepath), 1, total_result_images)
    
    
    """ Generate result images A to B """
    print('\n\n============================')
    print('Generate result image A to B')
    print('============================\n\n')
    path = model_weight_path / 'fake' / 'test' / 'A'
    path_list = get_files_path(str(path), '.png')
    savepath = model_weight_path / 'fakeA.png'
    images = [mpimg.imread(i) for i in path_list]
    save_multiple_img(images, str(savepath), 1, total_result_images)

    path = model_weight_path / 'fake' / 'test' / 'B'
    path_list = get_files_path(str(path), '.png')
    savepath = model_weight_path / 'fakeB.png'
    images = [mpimg.imread(i) for i in path_list]
    save_multiple_img(images, str(savepath), 1, total_result_images)

    """ Generate result images A to B to A """
    print('\n\n=================================')
    print('Generate result image A to B to A')
    print('=================================\n\n')
    path = model_weight_path / 'cycle_fake' / 'test' / 'A'
    path_list = get_files_path(str(path), '.png')
    savepath = model_weight_path / 'cycle_fakeA.png'
    images = [mpimg.imread(i) for i in path_list]
    save_multiple_img(images, str(savepath), 1, total_result_images)

    path = model_weight_path / 'cycle_fake' / 'test' / 'B'
    path_list = get_files_path(str(path), '.png')
    savepath = model_weight_path / 'cycle_fakeB.png'
    images = [mpimg.imread(i) for i in path_list]
    save_multiple_img(images, str(savepath), 1, total_result_images)

