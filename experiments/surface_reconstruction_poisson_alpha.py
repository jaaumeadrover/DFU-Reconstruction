import time

import numpy as np
import open3d as o3d

# Read Point Cloud
pcd = o3d.io.read_point_cloud("pcd_51.pcd")

o3d.visualization.draw_geometries([pcd])

# Estimate Normals
pcd.estimate_normals()
pcd.orient_normals_consistent_tangent_plane(100)
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

# Alpha Shapes
alpha = 0.03  # This value may need adjustment
start_time = time.time()
mesh_alpha = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
alpha_time = time.time() - start_time
o3d.visualization.draw_geometries([mesh_alpha], mesh_show_back_face=True)
print('Alpha shapes took: '+str(alpha_time))

# Poisson Surface Reconstruction
start_time = time.time()
poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
poisson_time = time.time() - start_time
print('Poisson took: '+str(poisson_time))
# Remove low-density vertices to clean the mesh
vertices_to_remove = densities < np.quantile(densities, 0.01)
poisson_mesh.remove_vertices_by_mask(vertices_to_remove)
o3d.visualization.draw_geometries([poisson_mesh], mesh_show_back_face=True)

# Print execution times
print(f"Alpha Shapes Execution Time: {alpha_time:.6f} seconds")
print(f"Poisson Surface Reconstruction Execution Time: {poisson_time:.6f} seconds")
