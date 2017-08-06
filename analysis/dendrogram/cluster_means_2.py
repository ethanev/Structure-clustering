from pymol import cmd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform
import pickle

def cluster_centers():
    '''
    Function is used to do a find the distances between all pairs of centers to get an overall clustering of structures.
    '''
    #path to data
    path = '/home/eevans/pymol/MP01-C_cents/'
    #load cluster centers
    centers_to_num = dict()
    center_list_full = os.listdir(path)
    center_list = []
    for center in center_list_full:
        center_list.append(center[:-4])
    closest_dict = {center:[] for center in center_list}
    for file, num in zip(center_list, range(40)):
        centers_to_num[str(file)] = num
        cmd.load(path+file+'.pdb')
    distances = np.zeros((len(center_list),len(center_list)))
    # assign each structure to best cluster center
    for center1 in center_list:
        closest_distance = 10000.0
        for center2 in center_list:
            if center1 != center2:
                dist = cmd.align('%s and resi 6-21' %(center2), '%s and resi 6-21' %(center1), cycles=2)
                if dist[0] < closest_distance:
                    closest_dict[center1] = str(center2)
                    closest_distance = dist[0]
                distances[centers_to_num[center2]][centers_to_num[center1]] = dist[0]
    return distances, centers_to_num, closest_dict

        #file_coords = cmd.get_coords(file)
        #cluster_centers[best_struct].append(file)
#       print file_coords.shape,cluster_coords[best_struct].shape, file, best_struct
        #cluster_coords[best_struct] = np.add(file_coords, cluster_coords[best_struct])

distances, centers_to_num, closest_dict = cluster_centers()
#heatmap = plt.pcolor(distances)
#savefig('test.png')
distances = np.around(distances, decimals=1)
distance_upper = squareform(distances)
distances_file = open('distances_new_MP01-C.pkl' ,'w')
pickle.dump(distance_upper, distances_file)
pickle.dump(centers_to_num, distances_file)
distances_file.close()

print centers_to_num
print closest_dict

