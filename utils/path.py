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
