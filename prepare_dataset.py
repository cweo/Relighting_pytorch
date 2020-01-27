import numpy as np
import pandas as pd
import os
import shutil
import argparse

# Use example: python .\prepare_dataset.py --folder './data/train/scene_abandonned_city_54/'

parser = argparse.ArgumentParser(description='Explode the dataset folder into sub directories for each illuminant.')
parser.add_argument('--folder', type=str, help='Dataset folder path.', required=True)

args = parser.parse_args()


folder_path = args.folder
files = []
for i in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path,i)) and 'dataset' in i:
        files.append(i)

dataset = pd.read_csv(os.path.join(folder_path, files[0]))
dataset.head()

color_temperatures = [2500 + 1000*k for k in range(5)]
locations = {'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W'}

for temperature in color_temperatures:
    temperature_path = os.path.join(folder_path, str(temperature))
    os.mkdir(temperature_path)
    for location in locations:
        os.mkdir(os.path.join(temperature_path, location))

        
for temperature in color_temperatures:
    for location in locations:
        condition = (dataset[location] == 1) & (dataset['illuminant'] == temperature) 
        dataset[condition].to_csv(os.path.join(folder_path, str(temperature), location, 'dataset_'+str(temperature)+'_'+location+'.csv'))
        for index, row in dataset[condition].iterrows():
            image_name = row['rendered_image'].split('.')[0]
            for i in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path,i)) and (image_name == i.split('_')[0] or image_name == i.split('.')[0]):
                    file_path = os.path.join(folder_path, i)
                    new_path = os.path.join(folder_path, str(temperature), location, i)
                    shutil.move(file_path, new_path)