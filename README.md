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
We describe here how to use our code.
#### Step 1: Download our dataset
Please download our dataset [here](https://drive.google.com/open?id=1FdQCDQNjmB4YNV8yZZZgsnidOumfCNfI).
#### Step 2: Check the completeness of our dataset (Optional)
If you want to be sure that your dataset is complete, use the notebook ```completeness_test.ipynb``` and adapt the path to the different scene folders.
#### Step 3: Hierarchize the dataset
Having all the images into different folders according to the illuminant type is usefull and to do so, run for each scene ```prepare_dataset.py```, here is an example:
```python prepare_dataset.py --folder './data/train/scene_abandonned_city_54/'``` 

Caution: Must be done for all the scenes before Step 4.
#### Step 4: Prepare a dataset for a given experiment
This notebook is used to prepare the dataset for the CycleGAN code and can be used as follows:
* Prepare the dataset for color temperature transfer using the function generate dataset color temperature.
* Prepare the dataset for cardinal direction tranfer using the function generate dataset both.
#### Step 5: Train CycleGAN model
Once the dataset is prepared with Step 4, follow the following instructions to train for image-to-image translation:
* Type ```visdom``` in a terminal to launch a visdom server accessible at [http://localhost:8097](http://localhost:8097).
* Decide the number of GPU to use: ```export CUDA_VISIBLE_DEVICES=0,1``` is to use to train on the two first GPU of your computer.
* Train the model, type ```python train.py -h``` for detailed information, for example:
``` python train.py --dataroot /scratch/barthas/datasets/2500_4500 --cuda --n_cpu 48 --batchSize 8```
#### Step 6: Testing CycleGAN model
Once you trained a model on a given dataset you will want to test on the test samples. To do it you have
to type, for example: 
```python test.py –dataroot /scratch/barthas/datasets/2500_4500 –n cpu 48 –-cuda```
It will also export fakeA and fakeB images, and give you SSIM and PSNR scores.
#### Step 7: Changing color temperature with linear operations
Using the notebook ```white_balance.ipynb```, you can change the color temperature of given images using linear
operations. The python script ```test_linear.py``` allows us to get linear output from our sample test dataset and also obtain SSIM and PSNR scores, for example:
```python .\test_linear.py --dataroot /scratch/barthas/datasets/2500_4500 --temp1 2500 --temp2 4500```

## References
We use [this](https://github.com/aitorzip/PyTorch-CycleGAN) CycleGAN implementation which is inspired of the paper [Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) and the original CycleGAN implementation [junyanz/pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).
