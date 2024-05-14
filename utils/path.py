"""
TITLE: path.py
DATE: 02/03/2024
AUTHOR: Jaume Adrover Fernández
DESCRIPTION: script containing all path manipulation functions such as
getting all bag,color or depth paths,extracting image info etc.
"""

import os

from definitions import ROOT_DIR,DATA_DIR
"""
FUNCTION: getAllPaths
ARGS: 
    ·path: patient main path.
DESCRIPTION: Given a patient_date path, extract bag,color,depth relative locations.. 
"""
def getAllPaths(path):
    paths = {'bag': os.path.join(path, 'bag'),
             'color': os.path.join(path, 'color'),
             'depth': os.path.join(path, 'depth')
             }
    return paths


"""
FUNCTION: getVideoInfo
ARGS: 
    ·path: patient main path.
DESCRIPTION: Given a patient_date path, extract bag, color, depth relative locations. 
"""

def getVideoInfo(src):
    parts = src.split('_')
    num_bag = parts[3].split('.')[0]
    return {'patient': parts[0] + parts[1], 'date': parts[2], 'numBag': num_bag}


"""
FUNCTION: createColDepthImgNames
ARGS: 
    ·src: main path.
    ·frame: video frame number
DESCRIPTION: Given a path, build color/depth paths with according frame number. 
"""
def createColDepthImgNames(src, frame):
    base_name = '_'.join(src.values())
    color = base_name + '_c_' + frame
    depth = base_name + '_d_' + frame
    return {'color': color, 'depth': depth}



"""
FUNCTION: createImageFolders
ARGS: 
    ·src: main path.
DESCRIPTION: Given a path,create folders if needed. 
"""
def createSomeFolders(src):
    for item in src:
        if not os.path.exists(item):
            os.makedirs(item)

def getPatientsFolders():
    return filter(lambda x: x.startswith('p'), os.listdir(DATA_DIR))
def getOrderedFileList(path):
    file_list = os.listdir(path)
    ordered_file_list = [None] * len(file_list)

    for f in file_list:
        frame = int(f.split('_')[1].split('.')[0])
        ordered_file_list[frame] = 'data/pcd/cropped/' + str(f)
    return ordered_file_list

def getPatientPath(patient,date):
    return os.path.join(ROOT_DIR,'data/'+patient +'/'+date)


def getImgFrame(src):
    return int(src.split('_')[4].split('.')[0])

def getFolderImgFrames(path):
    frame_list = []
    for file in os.listdir(path):
        frame_list.append(getImgFrame(file))
    return frame_list