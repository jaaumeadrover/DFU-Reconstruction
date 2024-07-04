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

# # Create the triangular mesh with the vertices and faces from Open3D
# tri_mesh_alpha = trimesh.Trimesh(np.asarray(mesh_alpha.vertices), np.asarray(mesh_alpha.triangles),
#                                  vertex_normals=np.asarray(mesh_alpha.vertex_normals))
# tri_mesh_poisson = trimesh.Trimesh(np.asarray(poisson_mesh.vertices), np.asarray(poisson_mesh.triangles),
#                                    vertex_normals=np.asarray(poisson_mesh.vertex_normals))
#
# # Visualize final meshes
# o3d.visualization.draw_geometries([mesh_alpha], mesh_show_back_face=True)
# o3d.visualization.draw_geometries([poisson_mesh], mesh_show_back_face=True)

# Optionally save meshes
# o3d.io.write_triangle_mesh('alpha_shape_mesh.ply', mesh_alpha)
# o3d.io.write_triangle_mesh('poisson_mesh.ply', poisson_mesh)

# Print execution times
print(f"Alpha Shapes Execution Time: {alpha_time:.6f} seconds")
print(f"Poisson Surface Reconstruction Execution Time: {poisson_time:.6f} seconds")
