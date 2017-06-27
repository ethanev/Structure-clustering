from pymol import cmd
import os
import numpy as np

def cluster_centers(centers_to_num, center_list, distance):
    '''
    Function is used to do a find the distances between all pairs of centers to get an overall clustering of structures.
    '''
    closest_dict = {center:[] for center in center_list}
    distances = np.zeros((len(center_list),len(center_list)))
    center_groups = dict()
    # assign each structure to best cluster center
    for center1 in center_list:
        closest_distance = 10000.0
        for center2 in center_list:
            if center1 != center2:
                dist = cmd.align(center2, center1)
                if dist[0] < closest_distance:
                    closest_dict[center1] = str(center2)
                    closest_distance = dist[0]
                distances[centers_to_num[center2]][centers_to_num[center1]] = dist[0]
    return distances, centers_to_num, closest_dict

    #file_coords = cmd.get_coords(file)
    #cluster_centers[best_struct].append(file)
    #print file_coords.shape,cluster_coords[best_struct].shape, file, best_struct
    #cluster_coords[best_struct] = np.add(file_coords, cluster_coords[best_struct])

def load_data():
    #path to data
    path = '/home/eevans/pymol/Gen3/'
    #file name list and file-to-number dict
    centers_to_num = dict()
    center_list_full = os.listdir(path)
    center_list = []
    for center in center_list_full:
        center_list.append(center[:-4])
    #load cluster centers and make lookup dictionary
    for file, num in zip(center_list, range(len(center_list))):
        centers_to_num[str(file)] = num
        cmd.load(path+file+'.pdb')
    return centers_to_num, center_list


centers_to_num, center_list = load_data()
distance = 2.0
distances, centers_to_num, closest_dict = cluster_centers(centers_to_num, center_list, distance)

print distances
print centers_to_num
print closest_dict
