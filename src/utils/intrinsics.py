import os

import open3d as o3d

from src.definitions import DATA_DIR

_intrinsics = None


def get_intrinsics():
    global _intrinsics
    if _intrinsics is None:
        _intrinsics = o3d.io.read_pinhole_camera_intrinsic(os.path.join(DATA_DIR, 'intrinsic.json'))
    return _intrinsics


def get_focal_length():
    return get_intrinsics().get_focal_length()


def get_principal_point():
    return get_intrinsics().get_principal_point()
