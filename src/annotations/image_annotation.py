"""
    TITLE: image_annotation.py
    DESCRIPTION: class that displays a window so user can click in every photo from determined folder in order
    to get ulcer coordinates, that will be stored in annotations.csv.
    AUTHOR: Jaume Adrover Fernández
    CREATION DATE: 12/04/2024
"""
import os
from definitions import DATA_DIR
from utils.image  import ImageAnnotator

if __name__ == "__main__":
    patient = 'p_0001'
    date = '2022-05-19'
    folder_path = os.path.join(DATA_DIR, patient+'/'+date+'/color/') # Write color photos path
    annotator = ImageAnnotator(folder_path)
    annotator.save_annotations_to_csv(os.path.join(DATA_DIR,patient+'/'+date+'/annotations.csv'))
