"""


"""

import open3d as o3d

from definitions import INTRINSICS

"""
Function:
Description:

"""
def buildPcd(color_path,depth_path):
    color_raw = o3d.io.read_image(color_path)
    depth_raw = o3d.io.read_image(depth_path)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw, convert_rgb_to_intensity=False)

    return o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, INTRINSICS)


def getBestPcdIndex(pcd,score):
    index = score.index(max(score))
    return pcd[index], index