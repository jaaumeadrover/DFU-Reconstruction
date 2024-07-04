import os.path
import open3d as o3d

from definitions import ROOT_DIR,DATA_DIR

i=1
def update_function(vis):
    global i

    # Read Point Cloud
    print('Displaying pcd: ' + str(i))
    #path =os.path.join(DATA_DIR, 'p_0001/2022-05-19/pcd/unified/pcd_'+str(i)+'.pcd') # os.path.join(ROOT_DIR, 'data/p_0001/2022-05-19/pcd/pcd_'+str(i)+'.pcd')
    path = os.path.join(DATA_DIR, 'p_0001/2022-05-19/pcd/unified/combined/pcd_' + str(
        i) + '.pcd')  # os.path.join(ROOT_DIR, 'data/p_0001/2022-05-19/pcd/pcd_'+str(i)+'.pcd')
    # Read Point cloud
    cloud_v2 = o3d.io.read_point_cloud(path)
    cloud.points = cloud_v2.points
    cloud.colors = cloud_v2.colors

    # Update geometry
    vis.update_geometry(cloud)
    i = i+1

    # Update renderer and handle events
    vis.update_renderer()
    vis.poll_events()
    vis.run()


# Create a VisualizerWithKeyCallback object
vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()

# Register the key callback function - pressing 'a' allows you to switch to next pcd
vis.register_key_callback(65, update_function)

# Read First Point Cloud
cloud = o3d.geometry.PointCloud()

path = os.path.join(ROOT_DIR, 'data/p_0018/2022-05-26/pcd/single/pcd_5.pcd')
path2 = os.path.join(ROOT_DIR, 'data/p_0018/2022-05-26/pcd/single/pcd_6.pcd')

cloud.points = o3d.io.read_point_cloud(path).points
cloud = o3d.io.read_point_cloud(path)
cloud2 = o3d.io.read_point_cloud(path2)

cloud = cloud + cloud2

# Add geometry to the scene
vis.add_geometry(cloud)

# Run the visualizer
vis.run()

# Destroy the visualizer window
vis.destroy_window()
