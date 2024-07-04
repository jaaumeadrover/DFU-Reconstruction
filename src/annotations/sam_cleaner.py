""""
    CLASS: sam_cleaner.py
    DESCRIPTION: script that given a .csv with ulcer correspondences in (x,y), executes
    SAM model in order to get full leg mask. Then, each mask is multiplied to depth image
    so undesired pixels will have values <=0. This is, in summary, a way to filter depth image by
    segmentating foot.
    AUTHOR: Jaume Adrover Fernández
    CREATION DATE: 14/04/2024
"""
import os
import cv2
import numpy as np
import pandas as pd

from utils.image import getLegMask, searchImgCoords, initSam
from utils.path import getPatientPath, createSomeFolders, getImgFrame, getFolderImgFrames
from tqdm import tqdm

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"



if __name__ == '__main__':
    patient = 'p_0018'
    date    = '2022-05-26'

    # Sam Model
    predictor = initSam()

    # Annotations
    csv_path = os.path.join(getPatientPath(patient, date), 'annotations.csv')
    df = pd.read_csv(csv_path)

    # Color and depth images path
    folder_path = getPatientPath(patient, date)+'/color'
    depth_images_path = getPatientPath(patient, date)+'/depth/raw'
    segm_depth_img_path = getPatientPath(patient, date) + '/depth/segm/'

    # Create segmented photos directory
    createSomeFolders([segm_depth_img_path])

    frame = 0
    # Main Loop
    for f in tqdm(os.listdir(folder_path), desc='Analysing frames...'):
        filename = f                         # Get filename
        depth_filename = f.replace('c','d')  # Get depth filename
        depth_filename = depth_filename.replace('.jpg','.png')

        # Get frame number
        frame = getImgFrame(filename)

        # Check if frame has been done or not
        if frame in getFolderImgFrames(segm_depth_img_path):
            continue

        # Get wound coords from annotations
        cx, cy = searchImgCoords(filename,df)

        # Read image
        image = cv2.imread(os.path.join(folder_path, filename))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Set image to model
        predictor.set_image(image)

        # Sam input params
        input_point = np.array([[cx, cy]])
        input_label = np.array([1])

        # Segment image
        masks, scores, _ = predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )

        # Get SAM predictions
        foot_mask = getLegMask(masks, scores, input_point, input_label, image)    # Get worst SAM mask (full leg)

        # Multiply depth * mask
        depth_image = cv2.imread(os.path.join(depth_images_path, depth_filename), cv2.IMREAD_UNCHANGED)
        segm_depth_img = depth_image * foot_mask

        # Store segmented depth image
        cv2.imwrite(segm_depth_img_path+depth_filename, segm_depth_img)




