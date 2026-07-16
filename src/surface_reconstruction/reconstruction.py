import argparse
import time

import numpy as np
import open3d as o3d


def estimate_normals(pcd, orient_k=100):
    pcd.estimate_normals()
    pcd.orient_normals_consistent_tangent_plane(orient_k)
    return pcd


def ball_pivoting(pcd, radius_multipliers=(5, 10)):
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radii = [avg_dist * m for m in radius_multipliers]

    start = time.time()
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii))
    elapsed = time.time() - start
    return mesh, elapsed


def alpha_shape(pcd, alpha=0.03):
    start = time.time()
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    elapsed = time.time() - start
    return mesh, elapsed


def poisson(pcd, depth=9, density_quantile=0.01):
    start = time.time()
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=depth)
    elapsed = time.time() - start

    vertices_to_remove = densities < np.quantile(densities, density_quantile)
    mesh.remove_vertices_by_mask(vertices_to_remove)
    return mesh, elapsed


def parse_args():
    parser = argparse.ArgumentParser(description='Reconstruct a surface mesh from a point cloud.')
    parser.add_argument('pcd_path', help='Path to the input .pcd file')
    parser.add_argument('--method', choices=['ball_pivoting', 'alpha_shape', 'poisson'], default='poisson')
    parser.add_argument('--alpha', type=float, default=0.03, help='alpha_shape only')
    parser.add_argument('--poisson-depth', type=int, default=9, help='poisson only')
    parser.add_argument('--density-quantile', type=float, default=0.01, help='poisson only')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    pcd = o3d.io.read_point_cloud(args.pcd_path)
    estimate_normals(pcd)
    o3d.visualization.draw_geometries([pcd], point_show_normal=True)

    if args.method == 'ball_pivoting':
        mesh, elapsed = ball_pivoting(pcd)
    elif args.method == 'alpha_shape':
        mesh, elapsed = alpha_shape(pcd, args.alpha)
    else:
        mesh, elapsed = poisson(pcd, args.poisson_depth, args.density_quantile)

    print(f'{args.method} took: {elapsed:.6f} seconds')
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
