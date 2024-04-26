"""
TITLE: clean_bbox
DATE: 05/04/2024
AUTHOR: Jaume Adrover Fernández
DESCRIPTION: script that basically generates a 3D bounding box, having on its 
center the main ulcer. Then, all points cloud are cropped so they only have an 
area of 50x50x50 cm from the main wound.
"""

import open3d as o3d
import numpy as np
import os
import pandas as pd
from tqdm import tqdm
from definitions import ROOT_DIR
from utils.tools_3d import buildPcd
import cv2
from definitions import intrinsics

fx, fy = intrinsics.get_focal_length()
cx, cy = intrinsics.get_principal_point()

def searchImgCoords(filename,df):
    # substitute c for d
    print(filename)
    row = df.loc[df['Filename'] == filename]
    print(row)
    cx, cy = row.iloc()[0]['X'], row.iloc()[0]['Y']
    return cx, cy


file_list = os.listdir('data/color/')
ordered_file_list = [None] * len(file_list)
csv_path = 'D:\\FootWoundsSegmentation\\src\\annotations\\annotations.csv'
df = pd.read_csv(csv_path)
print(df)

for f in file_list:
    frame = int(f.split('_')[4].split('.')[0])
    ordered_file_list[frame] = f

print(ordered_file_list)
i=0
for f in ordered_file_list:
    color_file = f
    depth_file = color_file.replace('c', 'd')
    color_file = 'data/color/' + color_file
    depth_file = 'data/depth/' + depth_file
    pcd = buildPcd(color_file,depth_file)
    #o3d.visualization.draw_geometries([pcd])
    d_cx,d_cy = searchImgCoords(f, df)
    print(d_cx)
    print(d_cy)
    depth_value = cv2.imread(depth_file,cv2.IMREAD_UNCHANGED)[d_cy, d_cx]
    print(depth_value)
    z = depth_value*0.001
    center = [(d_cx-cx)*z/fx,(d_cy-cy)*z/fy,z]
    print(center)
    bbox = o3d.geometry.OrientedBoundingBox(center=center, extent=[0.6, 0.6, 0.6],
                                         R=np.identity(3))
    o3d.visualization.draw_geometries([pcd,bbox])
    pcd = pcd.crop(bbox)
    pcd = pcd.voxel_down_sample(voxel_size=0.02)
    # o3d.visualization.draw_geometries([pcd,bbox])
    o3d.io.write_point_cloud('data/pcd/cropped/pcd_'+str(i)+'.pcd',pcd)
    i = i+1



#for every photo
    # color
    # depth
    # wound_coords =
    # depth_value = depth[x][y]
    # center = [(), (), ()]