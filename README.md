# Relighting pytorch

Johan Barthas, Ruofan Zhou, Majed El Helou and Sabine Süsstrunk.

This is a Python implementation for the Semester Project [report](https://github.com/cweo/Relighting_pytorch/blob/master/report/Semester_project_report.pdf).

## Codes

### Dependencies
* Python 3.6.10
* PIL
* pandas
* shutil
* torch 1.3.1
* torchvision 0.4.2
* visdom
* SSIM-PIL

To run our Unreal Engine 4 code:
* Unreal Engine 4 4.23.1

### Unreal Engine 4 data generation
To generate datasets yourself using Unreal Engine 4, please download our Unreal Engine 4 project [here](https://drive.google.com/file/d/1-iasuvNbfMIPMf1--qrFl0sGykMx8bNE/view?usp=sharing) and refer to our report's appendix for detailed instructions on how to run it.

### Results
Please find bellow a sample of images generated from the codes.
![thumbnail of result images](https://github.com/cweo/Relighting_pytorch/blob/master/results/thumbnail1/thumbnail1.png "Qualitative analysis of relighting using CycleGAN and linear models")

1st row: 2500K real images generated using Unreal Engine 4, 2nd row: images generated using a CycleGAN model to transfer
from 2500K real images to 4500K, 3rd row: 4500K real images generated using Unreal Engine 4, 4th row: images generated using a linear
model to transfer from 2500K real images to 4500K, 5th row: images generated using a CycleGAN model
to transfer from 2500K real images to 6500K, 6th row: 6500K real images generated using Unreal Engine 4, 7th row: images generated using
a linear model to transfer from 2500K real images to 6500K.

### Running experiments





We base our CycleGAN implementation on https://github.com/aitorzip/PyTorch-CycleGAN. We modified it to make it usable for our dataset.
We also developed tools to prepare our dataset that is available at https://drive.google.com/open?id=1FdQCDQNjmB4YNV8yZZZgsnidOumfCNfI that we generated using Unreal Engine 4.

The report for this project is available here: https://www.overleaf.com/read/fzrzzfvnrghy.
