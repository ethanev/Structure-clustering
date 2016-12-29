import numpy as np
import pickle
from multiprocessing import cpu_count
from pymol import cmd

def print_list(list):
    string = ''
    for item in list:
        string = string + item + ','
    print string.strip(',')

def dict_add(dict1, dict2):
    added = dict()
    for ele in dict1:
        if ele not in dict2:
            added[ele] = dict1[ele]
        else:
            added[ele] = np.add(dict1[ele], dict2[ele])
    for ele in dict2:
        if ele not in dict1:
            added[ele] = dict2[ele]
    return added

def average_dict(dict, size_dict):
    for ele in dict:
        dict[ele] = dict[ele]/float(size_dict[ele])
    return dict

def calc_dist_update_mean(new_coord_dict):
    path = '/home/eevans/pymol/test/'
    dist_sum = 0
    new_centers = []
    for file in new_coord_dict:
	cmd.load(path+file+'.pdb')
	old_coords = cmd.get_coords(file)
	new_coords = new_coord_dict[file]
	dist = np.linalg.norm(new_coords-old_coords)
        dist_sum += dist

	#save the new mean structures
        cmd.load_coords(new_coords,file)
	if str(file)[-9:] == '_new_cent':
	    cmd.save(path+str(file)+'.pdb', file)
            txt_name = str(file)
	else:
	    cmd.save(path+str(file)[:-4]+'_new_cent.pdb', file)
	    txt_name = str(file)[:-4]+'_new_cent'
	new_centers.append(txt_name)
    distance_file = open('distances.txt', 'a')
    distance_file.write(str(dist_sum)+'\n')
    distance_file.close()

    distance_file = open('latest_distance.txt', 'w')
    distance_file.write(str(int(dist_sum)))
    distance_file.close()
    return dist_sum, new_centers
# define the number of chunks of data
#num_of_chunks = cpu_count() 
num_of_chunks = 64 # used for debugging

# open the file with the pickled data
f = open('temp', 'r')

# load data and get the average cluster center
combined = dict()
cluster_lengths = dict()
for i in range(num_of_chunks):
    data = pickle.load(f)
    data_cluster = pickle.load(f)
    cluster_lengths = dict_add(data_cluster, cluster_lengths)
   # print 'adding in: ', data_cluster, '\n' 
   # print 'combined: ', cluster_lengths, '\n' 
    combined = dict_add(data, combined) 
combined = average_dict(combined, cluster_lengths)
f.close()
dist_cent_changed, new_centers = calc_dist_update_mean(combined)
print_list(new_centers)
#print cluster_lengths
#print combined

out = open('clusters_new.txt', 'a')
out.write(str(cluster_lengths))
out.close()

