import argparse
import sys
import os

import torchvision.transforms as transforms
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from torch.autograd import Variable
import torch
from PIL import Image
from math import log10
import numpy as np
import glob

from utils import change_temp
from color_temp import temperature_to_rgb
from models import Generator
from datasets import ImageDataset
from utils import get_concat_h
import pytorch_ssim
from utils import tensor2image
from SSIM_PIL import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument('--batchSize', type=int, default=1, help='size of the batches')
parser.add_argument('--temp1', type=int, default=2500, help='original color temperature')
parser.add_argument('--temp2', type=int, default=4500, help='new color temperature')
parser.add_argument('--dataroot', type=str, default='datasets/horse2zebra/', help='root directory of the dataset')
parser.add_argument('--input_nc', type=int, default=3, help='number of channels of input data')
parser.add_argument('--output_nc', type=int, default=3, help='number of channels of output data')
parser.add_argument('--size', type=int, default=256, help='size of the data (squared assumed)')
parser.add_argument('--cuda', action='store_true', help='use GPU computation')
parser.add_argument('--n_cpu', type=int, default=8, help='number of cpu threads to use during batch generation')
opt = parser.parse_args()
print(opt)

if __name__== '__main__':
   
    ###### Testing######

    # Create output dirs if they don't exist
    if not os.path.exists('output/A_linear'):
        os.makedirs('output/A_linear')
    if not os.path.exists('output/B_linear'):
        os.makedirs('output/B_linear')

    ssim_fake_A = 0
    ssim_fake_B = 0
    avg_psnr_A = 0
    avg_psnr_B = 0

    files_A = glob.glob(os.path.join(opt.dataroot, 'test/A/*.png'))
    files_B = glob.glob(os.path.join(opt.dataroot, 'test/B/*.png'))
        
    for i, (image_path1, image_path2) in enumerate(zip(files_A, files_B)):
        # Set model input
        real_A = Image.open(image_path1).convert('RGB').resize((opt.size, opt.size), Image.BICUBIC)
        real_B = Image.open(image_path2).convert('RGB').resize((opt.size, opt.size), Image.BICUBIC)
        # Generate output
        fake_A = change_temp(real_B, opt.temp2, opt.temp1)
        fake_B = change_temp(real_A, opt.temp1, opt.temp2)
        
        # Save concatenate image
        fake_A.save('output/A_linear/%04d.png' % (i+1))
        fake_B.save('output/B_linear/%04d.png' % (i+1))
        
        #Evaluate ssim
        ssim_fake_A += compare_ssim(real_A, fake_A)
        ssim_fake_B += compare_ssim(real_B, fake_B)

        # Evaluate PSNR
        mse_A = np.square(np.array(real_A) - np.array(fake_A)).mean(axis=None)
        psnr_A = 10 * log10(1 / mse_A)
        avg_psnr_A += psnr_A

        mse_B = np.square(np.array(real_B) - np.array(fake_B)).mean(axis=None)
        psnr_B = 10 * log10(1 / mse_B)
        avg_psnr_B += psnr_B

        sys.stdout.write('\rGenerated images %04d of %04d \n' % (i+1, len(files_A)))


    print("===> Avg. SSIM fake_A: {:.4f}".format(ssim_fake_A / len(files_A)))
    print("===> Avg. SSIM fake_B: {:.4f}".format(ssim_fake_B / len(files_A)))
    print("===> Avg. PSNR fake_A: {:.4f} dB".format(avg_psnr_A / len(files_A)))
    print("===> Avg. PSNR fake_B: {:.4f} dB".format(avg_psnr_B / len(files_A)))

    sys.stdout.write('\n')
    ###################################
