"""
TITLE: definitions.py
DESCRIPTION: contains all sort of constants that are going to be used during project
implementation.
AUTHOR: Jaume Adrover Fernández
CREATION DATE: 05/03/2024
"""
import os
import open3d as o3d

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
intrinsics = o3d.io.read_pinhole_camera_intrinsic(ROOT_DIR+'/data/intrinsics.json')