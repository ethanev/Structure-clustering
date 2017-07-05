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


file = 'E_struct_Gen8_1.silent'
path = '/home/eevans/pymol/8_1_all/'
struct_to_e_dict = open_Evstruct_file(file, path)

# define starting structures and clusters
low_e_struct = ['c.4.656_new_cent.pdb.pdb']

# load the top structures
cmd.load(low_e_struct[0])
dist_vs_energy = []
for file in os.listdir(path):
    if file[:-4] != low_e_struct[0][:-4]:
        cmd.load(path+file)
        dist = cmd.align(file[:-4], low_e_struct[0][:-4])
        dist_vs_energy.append((dist[0], float(struct_to_e_dict[file[:-4]]), str(file)))
        cmd.delete(file[:-4])
    else:
        dist_vs_energy.append((float('0.0'), float(struct_to_e_dict[file[:-4]])))
dist_vs_energy.sort(key=lambda tup: tup[0])
print dist_vs_energy[:5]

#out_file = open('Gen8_1-Dist_vs_E.txt', 'w')
#out_file.write(str(dist_vs_energy))
#out_file.close()
