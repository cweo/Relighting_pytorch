import argparse
import sys
import os

from PIL import Image
from math import log10
import numpy as np
import glob

from utils import change_temp
from color_temp import temperature_to_rgb
from SSIM_PIL import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument('--temp1', type=int, default=2500, help='original color temperature')
parser.add_argument('--temp2', type=int, default=4500, help='new color temperature')
parser.add_argument('--dataroot', type=str, default='datasets/horse2zebra/', help='root directory of the dataset')
parser.add_argument('--size', type=int, default=256, help='size of the data (squared assumed)')
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
        old_min = 0
        old_max = 255
        new_min = 0
        new_max = 1
        convert_RGB_2_float = lambda array: array*(new_max - new_min)/(old_max-old_min)
    
        mse_A = ((convert_RGB_2_float(np.array(real_A)) - convert_RGB_2_float(np.array(fake_A)))**2).mean()
        psnr_A = 10 * log10(1 / mse_A)
        #print(mse_A, " || ", psnr_A)
        avg_psnr_A += psnr_A

        mse_B = ((convert_RGB_2_float(np.array(real_B)) - convert_RGB_2_float(np.array(fake_B)))**2).mean()
        psnr_B = 10 * log10(1 / mse_B)
        avg_psnr_B += psnr_B

        sys.stdout.write('\rGenerated images %04d of %04d \n' % (i+1, len(files_A)))


    print("===> Avg. SSIM fake_A: {:.4f}".format(ssim_fake_A / len(files_A)))
    print("===> Avg. SSIM fake_B: {:.4f}".format(ssim_fake_B / len(files_A)))
    print("===> Avg. PSNR fake_A: {:.4f} dB".format(avg_psnr_A / len(files_A)))
    print("===> Avg. PSNR fake_B: {:.4f} dB".format(avg_psnr_B / len(files_A)))

    sys.stdout.write('\n')
    ###################################
