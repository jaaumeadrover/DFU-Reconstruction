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
from utils.path import getAllPaths, getVideoInfo, createImageFolders
from definitions import ROOT_DIR

data_path = ROOT_DIR + '/data/'

for patient in tqdm(os.listdir(data_path), desc='Converting all videos to frames'):
    patient_path = os.path.join(data_path, patient)
    for date in os.listdir(patient_path):
         paths = getAllPaths(os.path.join(patient_path, date))
         createImageFolders(list(paths.values())[1:])
         for filename in os.listdir(paths['bag']):
             video_path = os.path.join(paths['bag'], filename)   # Get img path
             video_info = getVideoInfo(filename)               # Get img info
             imagesFromFile(video_path, paths, video_info)       # Get imgs from video




