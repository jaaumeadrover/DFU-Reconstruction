import open3d as o3d
import trimesh
import numpy as np
import time

# Read Point Cloud
pcd = o3d.io.read_point_cloud("pcd_51.pcd")

# Estimate Normals
pcd.estimate_normals()
pcd.orient_normals_consistent_tangent_plane(100)
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

# estimate radius for rolling ball
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 5 * avg_dist

# Ball pivoting
start = time.time()
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
           pcd,
           o3d.utility.DoubleVector([radius, radius * 2]))

bpa_time = time.time()-start

print('Ball Pivoting Algorithm took: '+str(bpa_time))

# Without hole filling
o3d.visualization.draw_geometries([mesh])
tmesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
tmesh = tmesh.fill_holes(99).to_legacy()

# With hole filling (no difference noticed)
o3d.visualization.draw_geometries([tmesh])

# o3d.io.write_triangle_mesh('mesh.ply',tmesh)

# create the triangular mesh with the vertices and faces from open3d
tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),
                          vertex_normals=np.asarray(mesh.vertex_normals))

trimesh.convex.is_convex(tri_mesh)

o3d.visualization.draw_geometries([mesh])
