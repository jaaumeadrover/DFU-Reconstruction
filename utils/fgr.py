import open3d as o3d
import copy
import numpy as np

import time

def draw_registration_result(source, target, transformation,old_score):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    #source_temp.paint_uniform_color([1, 0.706, 0])
    #target_temp.paint_uniform_color([0, 0.651, 0.929])

    radius_normal = 0.02 * 2
    #print(":: Estimate normal with search radius %.3f." % radius_normal)
    source_temp.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    target_temp.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    result_icp = o3d.pipelines.registration.registration_icp(
        source_temp, target_temp, 0.02, transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())

    # if icp score is better than before
    if result_icp.fitness > 0:
        source_temp.transform(result_icp.transformation)
    else:
        source_temp.transform(transformation)

    print('ICP:'+str(result_icp))
    pcd_combined = source_temp + target_temp
    return pcd_combined, result_icp

def preprocess_point_cloud(pcd, voxel_size):
    #print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd#.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    #print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    #print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def prepare_dataset(voxel_size, path1, path2):
    #print(":: Load two point clouds and disturb initial pose.")
    print(path1)
    print(path2)
    source = o3d.io.read_point_cloud(path1)
    target = o3d.io.read_point_cloud(path2)
    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    #draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh


def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 5#0.5
    #print(":: Apply fast global registration with distance threshold %.3f" \
     #       % distance_threshold)
    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result


def run(src_path, target_path):
    voxel_size = 0.015  # means 1.5cm for the dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = \
            prepare_dataset(voxel_size, src_path, target_path)


    start = time.time()
    result_fast = execute_fast_global_registration(source_down, target_down,
                                                   source_fpfh, target_fpfh,
                                                   voxel_size)
    print("Fast global registration took %.3f sec.\n" % (time.time() - start))
    print(result_fast)
    return draw_registration_result(source_down, target_down, result_fast.transformation, old_score=result_fast)


