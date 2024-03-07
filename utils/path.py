"""

"""
import os

"""
Given a patient_date path, extract bag,color,depth relative locations.
"""
def getAllPaths(path):
    paths = {'bag': os.path.join(path, 'bag'),
             'color': os.path.join(path, 'color'),
             'depth': os.path.join(path, 'depth')
             }
    return paths

def getImageInfo(src):
    parts  = src.split('_')
    num_bag = parts[3].split('.')[0]
    return {'patient': parts[0]+parts[1], 'date': parts[2], 'numBag': num_bag}
def createColDepthImgNames(src, frame):
    base_name = '_'.join(src.values())
    color = base_name +'_c_' + frame
    depth = base_name +'_d_' + frame
    return {'color': color, 'depth': depth}
