from pymol import cmd
import os
import sys


def open_Evstruct_file(file, path):
    try:
	struct_to_e = dict()
        file = open(file)
        for line in file:
	    line = line.strip().split()
	    struct_to_e[line[1]] = line[0]
	file.close()
    except:
        print 'Could not open the file, has it been made?'
	sys.exit(0)
    return struct_to_e


#file = 'E_struct_Gen8_1.silent'
path = '/home/eevans/pymol/H19V_new/'
#struct_to_e_dict = open_Evstruct_file(file, path)

# define starting structures and clusters
low_e_struct = ['c.0.3.pdb.pdb']

# load the top structures
cmd.load(low_e_struct[0])
i = 0
n_in_clust = 0
avg_dist = 0
in_clust_avg = 0
for file in os.listdir(path):
    i += 1
    if file[:-4] != low_e_struct[0][:-4]:
        cmd.load(path+file)
	dist = cmd.align('%s and resi 8-19' %(file[:-4]), '%s and resi 8-19' %(low_e_struct[0][:-4]), cycles=2)
        avg_dist += dist[0]
	if file[:4] == 'c.0.':
	    in_clust_avg += dist[0]
	    n_in_clust += 1
	cmd.delete(file[:-4])
    else:
	pass
avg_dist /= i
in_clust_avg /= n_in_clust
print 'the global average distance: ', avg_dist
print 'total number of structures: ', i
print 'the in cluster average distance: ', in_clust_avg
print 'total number of structures in the cluster: ', n_in_clust
