import pickle
import os
import matplotlib.pylab as plt
import numpy as np

def load_pkl(data_path):
    try:
        data_file = open(data_path, 'r')
        data = pickle.load(data_file)
        data_file.close()
        return data
    except:
        print"Couldn't open the pickle file, please try a different one."

def matrix_energies(data_dict):
    dict_matrix = {}
    for center in data_dict:
        dict_matrix[center] = [float(energy[1]) for energy in data_dict[center]]
    for center in dict_matrix:
        dict_matrix[center] = np.asarray(dict_matrix[center])
    return dict_matrix

def get_center_size(data_matrix):
    return {center : data_matrix[center].shape for center in data_matrix}

def calc_average_energy(data_matrix):
    cluster_avg_energy = {}
    for center in data_matrix:
        cluster_avg_energy[center] = [np.mean(data_matrix[center])]
        cluster_avg_energy[center].append(np.std(data_matrix[center]))
    return cluster_avg_energy

def get_lowest_energies(data_dict):
    '''
    Finds the lowest energy pose in the cluster, uses the original dictionary!
    Does not use the np matrix version since that lost info about the structure.
    '''
    cluster_lowest_e = {}
    for center in data_dict:
        data_dict[center] = sorted(data_dict[center], key=lambda x: float(x[1]))
        lowest = data_dict[center][:100]
        cluster_lowest_e[center] = lowest
    return cluster_lowest_e

def summarize_data(cluster_sizes_dict, total_avg_energy_dict, low_energy_structures_dict):
    out_file = open('MP16_cluster-energy_analysis.csv', 'w')
    out_file.write('center,cluster size, average energy, energy standard deviation, lowest energy structure, lowest energy, \n')
    for center in total_avg_energy_dict:
        size = cluster_sizes_dict[center]
        average_energy = np.around(total_avg_energy_dict[center][0], decimals=2)
        energy_std = total_avg_energy_dict[center][1]
        lowest_energy_struct = low_energy_structures_dict[center][0][0]
        lowest_energy = low_energy_structures_dict[center][0][1]
        out_file.write(str(center)+','+str(size)[1:-3]+','+str(average_energy)+','+str(energy_std)+','+str(lowest_energy_struct)+','+str(lowest_energy)+'\n')
    out_file.close()

def main():
    pkl_path = 'MP16_center_energies.pkl'
    data = load_pkl(pkl_path) #unpickle data
    center_matrix = matrix_energies(data) # turn the data into a dictionary of center:[np array of energies]
    center_size = get_center_size(center_matrix) # calculate the size of clusters to compare with dendrogram
    center_total_avg_e = calc_average_energy(center_matrix) #get dictionary of center : average energy
    cluster_low_e_poses = get_lowest_energies(data) # get dictiionary of center : 10 lowest energy structures and energie
    summarize_data(center_size, center_total_avg_e, cluster_low_e_poses)

#get average energy and standard deviation of lowest 100

if __name__ == "__main__":
    main()