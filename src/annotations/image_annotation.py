"""
    TITLE: image_annotation.py
    DESCRIPTION: class that displays a window so user can click in every photo from determined folder in order
    to get ulcer coordinates, that will be stored in annotations.csv.
    AUTHOR: Jaume Adrover Fernández
    CREATION DATE: 12/04/2024
"""
import os

import pandas as pd

from src.utils.image import ImageAnnotator
from src.utils.path import getPatientPath


def annotate(patient, date):
    csv_path = os.path.join(getPatientPath(patient, date), 'annotations.csv')
    folder_path = os.path.join(getPatientPath(patient, date), 'color')

    existing_annotations = {}
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        existing_annotations = {row['Filename']: (row['X'], row['Y']) for _, row in df.iterrows()}

    total = len([f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))])
    remaining = total - len(existing_annotations)
    if remaining <= 0:
        print(f'All {total} frames already annotated at {csv_path}, skipping manual annotation.')
        return
    print(f'{len(existing_annotations)}/{total} frames already annotated, {remaining} left to click.')

    annotator = ImageAnnotator(folder_path, existing_annotations)
    annotator.save_annotations_to_csv(csv_path)


if __name__ == "__main__":
    patient = 'p_0001'
    date = '2022-05-19'
    annotate(patient, date)
