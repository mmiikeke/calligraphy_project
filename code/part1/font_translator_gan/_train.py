import os
os.system("python train.py --dataroot .\\datasets\\font --model font_translator_gan --name test_new_dataset --no_dropout --batch_size 128 --style_channel 10")