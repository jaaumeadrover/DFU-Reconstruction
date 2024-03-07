"""
TITLE: dataPreprocessing
DATE: 05/03/2024
AUTHOR: Jaume Adrover Fernández
DESCRIPTION: script in which we'll basically
preprocess all our dataset, extracting color and depth frames from
.bag files.
"""
import os

import cv2
from tqdm import tqdm
from utils.create_dataset import imagesFromFile
from utils.path import getAllPaths, getImageInfo
from definitions import ROOT_DIR

data_path = ROOT_DIR + '/data/'

for patient in tqdm(os.listdir(data_path), desc='Converting all videos to frames'):
    patient_path = os.path.join(data_path, patient)
    for date in os.listdir(patient_path):
         paths = getAllPaths(os.path.join(patient_path,date))
         for filename in os.listdir(paths['bag']):
             img_path = os.path.join(paths['bag'], filename) # Get img path
             img_info = getImageInfo(filename)               # Get img info
             imagesFromFile(img_path, paths, img_info)




