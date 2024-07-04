import os
import open3d as o3d
"""
TITLE: definitions.py
DESCRIPTION: contains all sort of constants that are going to be used during project
implementation.
AUTHOR: Jaume Adrover Fernández
CREATION DATE: 05/03/2024
"""

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
DATA_DIR = os.path.join(ROOT_DIR,'data')

INTRINSICS = o3d.io.read_pinhole_camera_intrinsic(ROOT_DIR + '/data/intrinsic.json')
FX, FY = INTRINSICS.get_focal_length()
CX, CY = INTRINSICS.get_principal_point()
