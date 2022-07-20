import time
import syglass as sy
import trimesh
import numpy as np
import pyvista as pv

#              ________________________________________________              #
#/=============|  Surface-to-Surface Colocalization Example   |=============\#
#|             ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾             |#
#|  Compares the distance between meshes and pairs them based on a          |#
#|  distance threshold.                                                     |#
#|                                                                          |#
#|  Note that for now the project must NOT be opened in syGlass when this   |#
#|  script runs. This can later be built into a syGlass plugin, which will  |#
#|  not suffer from this issue.                                             |#
#|                                                                          |#
#\==========================================================================/#

# constants: modify as needed before running the script
EXPERIMENT_NAME = 'default'
PROJECT_PATH = 'C:/Users/emmak/Downloads/new_data/33074_8kHz.syg'
MESH_PATH = 'C:/Users/emmak/Downloads/new_data/'
DISTANCE_THRESHOLD = 50

if __name__ == '__main__':
    # get the project object, meshes
    project = sy.get_project(PROJECT_PATH)
    mesh_names = project.impl.GetMeshNamesAndSizes(EXPERIMENT_NAME)
    voxel_dimensions = project.get_voxel_dimensions()
    pv_read_meshes = []
    project_meshes = []
    mean_distances_unsorted = []
    blacklist_meshes = []
    pairs = []
    orphaned = []
    sorted_dists = []
    centers_list = []

    # iterate through list of meshes
    for mesh_name in mesh_names:
        print('\nProcessing mesh: ' + mesh_name)
        project.impl.ExportMeshOBJs(EXPERIMENT_NAME, mesh_name, MESH_PATH + '/' + mesh_name)
       
        # meshes take a second to export—here we wait for them
        while project.impl.GetMeshIOPercentage() != 100.0:
            time.sleep(0.1)
       
        # pyvista reads each mesh
        pv_read_meshes.append(pv.read(MESH_PATH + '/' + mesh_name))
        project_meshes.append(mesh_name)

    # compare all meshes
    i = 0
    k = 1
    while i < len(pv_read_meshes):
        while k < len(pv_read_meshes):
            closest_cells, closest_points = pv_read_meshes[k].find_closest_cell(pv_read_meshes[i].points, return_closest_point = True)
            d_exact = np.linalg.norm(pv_read_meshes[i].points - closest_points, axis = 1)
            mean_dist = np.mean(d_exact)
            mean_distances_unsorted.append((project_meshes[i], project_meshes[k], mean_dist))
            k = k + 1
        i = i + 1
        k = i + 1
    
    # sort and then pair meshes
    sorted_dists = sorted(mean_distances_unsorted, key=lambda i: i[-1])
    for sorted_dist in sorted_dists:
        if (blacklist_meshes.count(sorted_dist[0]) == 0 and blacklist_meshes.count(sorted_dist[1]) == 0):
            if sorted_dist[2] <= DISTANCE_THRESHOLD:
                pairs.append(sorted_dist)
                project.set_surface_color(sorted_dist[0], (255, 0, 0, 1) , EXPERIMENT_NAME)
                project.set_surface_color(sorted_dist[1], (0, 255, 0, 1) , EXPERIMENT_NAME)
                blacklist_meshes.append(sorted_dist[0])
                blacklist_meshes.append(sorted_dist[1])
                mesh1 = trimesh.load_mesh(MESH_PATH + '/' + sorted_dist[0])
                mesh2 = trimesh.load_mesh(MESH_PATH + '/' + sorted_dist[1])
                xyz_center_points1 = mesh1.center_mass
                zyx_center_points1 = [xyz_center_points1[2] / voxel_dimensions[0], xyz_center_points1[1] / voxel_dimensions[1], xyz_center_points1[0] / voxel_dimensions[2]]
                xyz_center_points2 = mesh2.center_mass
                zyx_center_points2 = [xyz_center_points2[2] / voxel_dimensions[0], xyz_center_points2[1] / voxel_dimensions[1], xyz_center_points2[0] / voxel_dimensions[2]]
                center_mass_points = [zyx_center_points1, zyx_center_points2]
                centers_list.append(center_mass_points)
    # create distance measurements
    centers_array = np.array(centers_list)
    project.set_distance_measurements(centers_array, EXPERIMENT_NAME)

# check for orphaned meshes
    for mesh in project_meshes:
        if blacklist_meshes.count(mesh) == 0:
            orphaned.append(mesh)
            project.set_surface_color(mesh, (0, 0, 255, 1) , EXPERIMENT_NAME)
    print("Pairs: " + str(pairs))
    print("Orphaned: " + str(orphaned))
