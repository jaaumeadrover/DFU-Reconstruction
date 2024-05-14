"""
TITLE: bag_extraction.py
AUTHOR: Jaume Adrover Fernández
DESCRIPTION: script in which we'll basically
preprocess all our dataset, extracting color and depth frames from
.bag files.
CREATION DATE: 05/03/2024
"""
import os

from tqdm import tqdm
from definitions import DATA_DIR
from utils.create_dataset import imagesFromFile
from utils.path import getAllPaths, getVideoInfo, createSomeFolders, getPatientsFolders

# Main loop
for patient in tqdm(getPatientsFolders(), desc='Converting all videos to frames'):
    patient_path = os.path.join(DATA_DIR, patient)  # Get Patient Date
    for date in os.listdir(patient_path):
        paths = getAllPaths(os.path.join(patient_path, date))
        createSomeFolders(list(paths.values())[1:])  # Create color/depth img folders
        for filename in os.listdir(paths['bag']):
            video_path = os.path.join(paths['bag'], filename)  # Get .bag path
            video_info = getVideoInfo(filename)  # Get video info
            imagesFromFile(video_path, paths, video_info)  # Get imgs from recorded sequence
