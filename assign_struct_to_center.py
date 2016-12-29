import os
import numpy as np
from pymol import cmd
import argparse
import pickle

def parse_in():
    '''
    Read in the input clusters and data from the rand_center_split_Data.py program
    and make a distionary for clusters and a list for the data to read through
    '''
    parser = argparse.ArgumentParser(description='read in the data chunk and cluster centers')
    parser.add_argument('cluster_centers', help='list of cluster centers')
    parser.add_argument('data', help='list of data to be clustered')
    args = parser.parse_args()
    cluster_centers = {ele:[] for ele in args.cluster_centers.split(',')}
    data = args.data.split(',')
    return cluster_centers, data

def assign_struct_to_center(cluster_centers, data):
    '''
    Function is used to assign each structure to a cluster center and update the centers mean coords
    returns:
        1. a dictionary of cluster mapped to all the structures in it
        2. a dictionary of cluster mapped to its average coordinates
    '''
    #path to data
    path = '/home/eevans/pymol/test/'
    #load cluster centers
    cluster_coords = dict()
    for file in cluster_centers:
        cmd.load(path+file+'.pdb')
	cluster_coords[file] = cmd.get_coords(file) - cmd.get_coords(file) # used to zero out the coords and just initiallize a data structure of the correct size
    # assign each structure to best cluster center
    for file in data:
	cmd.load(path+file+'.pdb')
	if file in cluster_centers:
            cluster_centers[file].append(file)
            cluster_coords[file] += cmd.get_coords(file)
	else:
            best_dist = 10000.0
            best_struct = None
            for center in cluster_centers:
	        dist = cmd.align(file, center)
                if dist[0] < best_dist:
                    best_dist = dist[0]
                    best_struct = center
		    file_coords = cmd.get_coords(file)
	    cluster_centers[best_struct].append(file)
#	    print file_coords.shape,cluster_coords[best_struct].shape, file, best_struct
            cluster_coords[best_struct] = np.add(file_coords, cluster_coords[best_struct])
            cmd.delete(file)
#    for center in cluster_coords:
#        cluster_coords[center] = cluster_coords[center] / len(cluster_centers[center])
#   	 cmd.load_coords(cluster_coords[center], center)
#	 cmd.save(path+center[:-4]+'_center.pdb', center)
    return cluster_centers, cluster_coords

def get_cluster_sizes(cluster_dict):
    cluster_sizes = dict()
    for ele in cluster_dict:
        cluster_sizes[ele] = len(cluster_dict[ele])
    return cluster_sizes

np.set_printoptions(threshold=np.inf)
centers, data = parse_in()
clusters, cluster_coords = assign_struct_to_center(centers, data)
cluster_sizes = get_cluster_sizes(clusters)
print cluster_sizes
#for cluster in cluster_coords:
#    print cluster
#    print cluster_coords[cluster]

coords_size = open('temp' ,'a')
pickle.dump(cluster_coords, coords_size)
pickle.dump(cluster_sizes, coords_size)
coords_size.close()

