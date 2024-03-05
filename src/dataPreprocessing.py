#####################################################
##               Read bag from file                ##
#####################################################
import os

import cv2
import tqdm
from utils.create_dataset import imagesfromfile
from utils.path import getAllPaths
from definitions import ROOT_DIR

data_path = ROOT_DIR + '/data/'

#for all patients
for patient in os.listdir(data_path):
    patient_path = os.path.join(data_path, patient)
    #for every taken video of each patient
    for date in os.listdir(patient_path):
         paths = getAllPaths(os.path.join(patient_path,date))
         for filename in os.listdir(paths['bag']):
             img_path = os.path.join(paths['bag'],filename)
             imagesfromfile(img_path,paths['color'])




# cd.imagesfromfile('1.bag','../data/hola.png')