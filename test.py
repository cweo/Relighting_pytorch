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

from models import Generator
from datasets import ImageDataset
from utils import get_concat_h
import pytorch_ssim

parser = argparse.ArgumentParser()
parser.add_argument('--batchSize', type=int, default=1, help='size of the batches')
parser.add_argument('--dataroot', type=str, default='datasets/horse2zebra/', help='root directory of the dataset')
parser.add_argument('--input_nc', type=int, default=3, help='number of channels of input data')
parser.add_argument('--output_nc', type=int, default=3, help='number of channels of output data')
parser.add_argument('--size', type=int, default=256, help='size of the data (squared assumed)')
parser.add_argument('--cuda', action='store_true', help='use GPU computation')
parser.add_argument('--n_cpu', type=int, default=8, help='number of cpu threads to use during batch generation')
parser.add_argument('--generator_A2B', type=str, default='output/netG_A2B.pth', help='A2B generator checkpoint file')
parser.add_argument('--generator_B2A', type=str, default='output/netG_B2A.pth', help='B2A generator checkpoint file')
opt = parser.parse_args()
print(opt)
if __name__== '__main__':
    if torch.cuda.is_available() and not opt.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")

    ###### Definition of variables ######
    # Networks
    netG_A2B = Generator(opt.input_nc, opt.output_nc)
    netG_B2A = Generator(opt.output_nc, opt.input_nc)

    # Multi GPU
    if torch.cuda.device_count() >= 1 and opt.cuda:
            # export CUDA_VISIBLE_DEVICES=0,1 to use only 2 gpus
            print("Let's use", torch.cuda.device_count(), "GPUs!")
            netG_A2B = torch.nn.DataParallel(netG_A2B)
            netG_B2A = torch.nn.DataParallel(netG_B2A)

    if opt.cuda:
        netG_A2B.cuda()
        netG_B2A.cuda()

    # Load state dicts
    netG_A2B.load_state_dict(torch.load(opt.generator_A2B))
    netG_B2A.load_state_dict(torch.load(opt.generator_B2A))

    # Set model's test mode
    netG_A2B.eval()
    netG_B2A.eval()

    # Inputs & targets memory allocation
    Tensor = torch.cuda.FloatTensor if opt.cuda else torch.Tensor
    input_A = Tensor(opt.batchSize, opt.input_nc, opt.size, opt.size)
    input_B = Tensor(opt.batchSize, opt.output_nc, opt.size, opt.size)

    # Dataset loader
    transforms_ = [ transforms.Resize(opt.size, Image.BICUBIC),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5)) ]
    dataloader = DataLoader(ImageDataset(opt.dataroot, transforms_=transforms_, mode='test'), 
                            batch_size=opt.batchSize, shuffle=False, num_workers=opt.n_cpu)
    ###################################

    ###### Testing######

    # Create output dirs if they don't exist
    if not os.path.exists('output/A'):
        os.makedirs('output/A')
    if not os.path.exists('output/B'):
        os.makedirs('output/B')

    ssim_fake_A = 0
    ssim_fake_B = 0
    avg_psnr_A = 0
    avg_psnr_B = 0

    criterion = torch.nn.MSELoss()

    for i, batch in enumerate(dataloader):
        # Set model input
        real_A = Variable(input_A.copy_(batch['A']))
        real_B = Variable(input_B.copy_(batch['B']))

        # Generate output
        fake_B = netG_A2B(real_A)
        fake_A = netG_B2A(real_B)

        # Save concatenate image
        #save_image(0.5*(fake_A.data + 1.0), 'output/A/%04d.png' % (i+1))
        #save_image(0.5*(fake_B.data + 1.0), 'output/B/%04d.png' % (i+1))

        #Evaluate ssim
        ssim_fake_A += pytorch_ssim.ssim(real_A.data, fake_A.data)
        ssim_fake_B += pytorch_ssim.ssim(real_B.data, fake_B.data)

        # Evaluate PSNR
        mse_A = criterion(fake_A.data, real_A.data)
        psnr_A = 10 * log10(1 / mse_A.item())
        avg_psnr_A += psnr_A

        mse_B = criterion(fake_B.data, real_B.data)
        psnr_B = 10 * log10(1 / mse_B.item())
        avg_psnr_B += psnr_B

        sys.stdout.write('\rGenerated images %04d of %04d \n' % (i+1, len(dataloader)))


    print("===> Avg. SSIM fake_A: {:.4f}".format(ssim_fake_A / len(dataloader)))
    print("===> Avg. SSIM fake_B: {:.4f}".format(ssim_fake_B / len(dataloader)))
    print("===> Avg. PSNR fake_A: {:.4f} dB".format(avg_psnr_A / len(dataloader)))
    print("===> Avg. PSNR fake_B: {:.4f} dB".format(avg_psnr_B / len(dataloader)))

    sys.stdout.write('\n')
    ###################################
