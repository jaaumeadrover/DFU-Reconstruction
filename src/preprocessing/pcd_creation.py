"""
    TITLE: pcd_creation.py
    DESCRIPTION: script that basically generates a 3D bounding box, having on its
    center the main ulcer. Then, all points cloud are cropped so they only have an
    area of 45x45x45 cm from the main wound.
    AUTHOR: Jaume Adrover Fernández
    DATE: 05/04/2024
"""

import cv2
import numpy as np
import open3d as o3d
import pandas as pd

from tqdm import tqdm
from definitions import CX, CY, FX, FY
from utils.image import searchImgCoords
from utils.path import getSortedList, getPatientPath, createSomeFolders
from utils.tools_3d import buildPcd

if __name__ == '__main__':
    patient = 'p_0018'
    date = '2022-05-26'

    path = getPatientPath(patient,date)

    # Get sorted file list by frame number
    file_list = getSortedList(path+'/color/')

    # Get patient annotations for wound coords (cx,cy)
    csv_path = path + '/annotations.csv'
    df = pd.read_csv(csv_path)

    # Create PointCloud patient folder
    pcd_path = path+'/pcd/single/'
    createSomeFolders([pcd_path])

    # Main Loop
    i = 0
    for f in tqdm(file_list, desc='Cropping all PointClouds...'):
        color_file = f
        depth_file = color_file.replace('c', 'd')

        # Color/Depth Image paths
        color_file = path + '/color/' + color_file
        depth_file = path + '/depth/segm/' + depth_file

        # Build PointCloud
        pcd = buildPcd(color_file, depth_file)

        # Search for wound coordinates
        d_cx, d_cy = searchImgCoords(f, df)

        # Get wound pixel depth value
        depth_value = cv2.imread(depth_file, cv2.IMREAD_UNCHANGED)[d_cy, d_cx]

        # Calculate center coordinate 2D -> 3D
        z = depth_value*0.001
        center = [(d_cx-CX)*z/FX, (d_cy-CY)*z/FY, z]

        # Build 3D Bounding Box with center in the wound pixel
        bbox = o3d.geometry.OrientedBoundingBox(center=center, extent=[0.45, 0.45, 0.45], R=np.identity(3))

        pcd = pcd.crop(bbox)
        pcd = pcd.voxel_down_sample(voxel_size=0.01)

        # Uncomment if wanted to see pcd + bounding box
        o3d.visualization.draw_geometries([pcd,bbox])

        o3d.io.write_point_cloud(pcd_path+'pcd_'+str(i)+'.pcd', pcd)
        i = i+1
