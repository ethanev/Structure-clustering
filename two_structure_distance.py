from pymol import cmd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform
import pickle
import ast

def load_pdbs(path):
    centers_to_num = dict()
    center_list_full = os.listdir(path)
    center_list = []
    for center in center_list_full:
        center_list.append(center[:-4])
    for file, num in zip(center_list, range(len(center_list_full))):
        centers_to_num[str(file)] = num
        cmd.load(path+file+'.pdb')
    return center_list

def get_cluster_order_data(path_to_ordered_cluster_data):
    try:
        size_file = open(path_to_ordered_cluster_data, 'r')
        data = size_file.read()
        ordered_data_list_full = ast.literal_eval(data)
        ordered_data_list = [ele.split()[0][:-1] for ele in ordered_data_list_full]
        return ordered_data_list, ordered_data_list_full
    except:
        print 'please try a different cluster size file, could not open the file.'

def cluster_centers():
    '''
    Function is used to do a find the distances between all pairs of centers to get an overall clustering of structures.
    '''
    #load the centers in the proper order
    dend_ordered_cents_1 = 'Gen3_cluster_sizes_dend_order.txt'
    ordered_cents_1, ordered_cents_1_full = get_cluster_order_data(dend_ordered_cents_1)
    cent_1_label = dend_ordered_cents_1[:-29]
    dend_ordered_cents_2 = 'Gen8_1_cluster_sizes_dend_order.txt'
    ordered_cents_2, ordered_cents_2_full = get_cluster_order_data(dend_ordered_cents_2)
    cent_2_label = dend_ordered_cents_2[:-29]


    #load the PDBs
    path_1 = '/home/eevans/pymol/Gen3/'
    path_2 = '/home/eevans/pymol/8_1/'
    center_list_1 = load_pdbs(path_1)
    center_list_2 = load_pdbs(path_2)

    distances = np.zeros((len(center_list_1),len(center_list_2)))
    # assign each structure to best cluster center
    i = 0
    for center1 in ordered_cents_1:
        j = 0
        for center2 in ordered_cents_2:
            dist = cmd.align('%s and resi 5-20' %(center2), '%s and resi 5-20' %(center1), cycles=2)
            distances[i][j] = dist[0]
            j += 1
        i += 1
    return distances, ordered_cents_1_full, ordered_cents_2_full, cent_1_label, cent_2_label

distances, ordered_cents_1, ordered_cents_2,cent_1_label,cent_2_label = cluster_centers()
#heatmap = plt.pcolor(distances)
#savefig('test.png')
distances = np.around(distances, decimals=3)
distances_file = open('distances_81to3.pkl' ,'w')
pickle.dump(distances, distances_file)
pickle.dump(cent_1_label, distances_file)
pickle.dump(ordered_cents_1, distances_file)
pickle.dump(cent_2_label, distances_file)
pickle.dump(ordered_cents_2, distances_file)
distances_file.close()
