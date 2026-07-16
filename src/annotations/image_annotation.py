"""
    TITLE: image_annotation.py
    DESCRIPTION: class that displays a window so user can click in every photo from determined folder in order
    to get ulcer coordinates, that will be stored in annotations.csv.
    AUTHOR: Jaume Adrover Fernández
    CREATION DATE: 12/04/2024
"""
import os
from src.utils.image import ImageAnnotator
from src.utils.path import getPatientPath


def annotate(patient, date):
    csv_path = os.path.join(getPatientPath(patient, date), 'annotations.csv')
    if os.path.exists(csv_path):
        print(f'Annotations already exist at {csv_path}, skipping manual annotation.')
        return
    folder_path = os.path.join(getPatientPath(patient, date), 'color')
    annotator = ImageAnnotator(folder_path)
    annotator.save_annotations_to_csv(csv_path)


if __name__ == "__main__":
    patient = 'p_0001'
    date = '2022-05-19'
    annotate(patient, date)
