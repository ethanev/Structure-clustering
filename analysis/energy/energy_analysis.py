import os
import ast
import sys
import numpy as np

def read_cent_to_structs(file):
    try: 
	cent_file = open(file)
	line = cent_file.readline()
	for i in range(len(line)):
            if line[i] == '{':
                start = i
            if line[i] == '}':
       		end = i
	cent_file.close()
    except:
	print 'Could not create the centers-to-pdbs dictionary, is the file correct?'
    return eval(line[start:end+1])

def parse_silent(silent_file):
    pdb_to_energy = dict()
    try:
        silent = open(silent_file, 'r')
        for line in silent:
            if line[0:5] == 'SCORE':
                split_line = line.strip().split()
                pdb_to_energy[split_line[-1]] = split_line[1]
        silent.close()
        return pdb_to_energy
    except:
        print 'Are you sure you entered the program arguments in the correct order (silent file, path to centers and path to pdbs)?'

def combine_cents_energies(cent_to_pdb, pdb_to_energy):
    cent_to_pdb_energy = dict()
    for cent in cent_to_pdb:
	cent_to_pdb_energy[cent] = []
        for struct in cent_to_pdb[cent]:
	    cent_to_pdb_energy[cent].append((struct, float(pdb_to_energy[struct])))
    return cent_to_pdb_energy

def find_lowest_energy(cent_to_pdb_energy):
    cent_to_lowest = dict()
    for cent in cent_to_pdb_energy:
	score = 100.00
	best_cent = ''
	for struct in cent_to_pdb_energy[cent]:
	    if struct[1] <= score:
		score = struct[1]
		best_cent = struct[0]
	cent_to_lowest[cent] = (best_cent, score)
    return cent_to_lowest

def find_5_lowest_energies(cent_to_pdb_energy):
    cent_to_lowest = dict()
    for cent in cent_to_pdb_energy:
        cent_to_pdb_energy[cent].sort(key=lambda x: x[1])
        cent_to_lowest[cent] = cent_to_pdb_energy[cent][:5]
    return cent_to_lowest

def get_avg_energy(cent_to_pdb_energy):
    cent_to_avg_e = dict()
    for cent in cent_to_pdb_energy:
	energy_list = []
	for struct in cent_to_pdb_energy[cent]:
	    energy_list.append(struct[1])
	energy_array = np.asarray(energy_list)
	mean_energy = np.mean(energy_array)
	std_energy = np.std(energy_array)
    	cent_to_avg_e[cent] = (mean_energy, std_energy)
    return cent_to_avg_e

def get_cent_size_dict(cent_to_pdbs):
    cent_size = dict()
    for cent in cent_to_pdbs:
	cent_size[cent] = len(cent_to_pdbs[cent])
    return cent_size

def write_csv(avg_energy, lowest_energies, cent_size, path):
    out = open(path + 'cent_loweststruct_lowestenergy.csv', 'w')
    out.write('center, size, average energy, energy std, lowest energy struct 1, structure 1 energy,lowest energy struct 2, structure 2 energy,lowest energy struct 3, structure 3 energy,lowest energy struct 4, structure 4 energy,lowest energy struct 5, structure 5 energy, \n')
    for cent in avg_energy:
	pass
        #out.write(str(cent) + ',' + str(cent_size[cent]) + ',' + str(avg_energy[cent][0]) + ',' + str(avg_energy[cent][1]) + ',' + str(lowest_energies[cent][0][0]) + ',' + str(lowest_energies[cent][0][1]+ ',' + str(lowest_energies[cent][1][0]) + ',' + str(lowest_energies[cent][1][1]))+ ',' + str(lowest_energies[cent][2][0]) + ',' + str(lowest_energies[cent][2][1])+ ',' + str(lowest_energies[cent][3][0]) + ',' + str(lowest_energies[cent][3][1])+ ',' + str(lowest_energies[cent][4][0]) + ',' + str(lowest_energies[cent][4][1]) + '\n')
    out.close()

def write_release_pdb_sh(lowest_energy, silent, path):
    out = open(path[:19]+'release_lowest_structs.sh', 'w')
    out.write('module add c3ddb/rosetta/vmullig_rosetta_24Feb2015 \n')
    out_path = './' + path[19:]
    for cent in lowest_energy:
        out.write('extract_pdbs.linuxgccrelease -in:file:fullatom -in:file:silent %s%s -in:file:tags %s -out:prefix %s & \n' %(path, silent, lowest_energy[cent][0], out_path))
    out.write('wait')
    out.close()

def write_release_5_lowest_pdb_sh(lowest_energies, silent, path):
    out = open(path[:19]+'release_lowest_structs.sh', 'w')
    out.write('module add c3ddb/rosetta/vmullig_rosetta_24Feb2015 \n')
    out_path = './' + path[19:]
    for cent in lowest_energies:
        for struct in lowest_energies[cent]:
            out.write('extract_pdbs.linuxgccrelease -in:file:fullatom -in:file:silent %s%s -in:file:tags %s -out:prefix %s & \n' %(path, silent, struct[0], out_path))
    out.write('wait')
    out.close()

def read_families_file(families_file, path):
    families = dict()
    file = open(path+families_file, 'r')
    family_count = 1
    for line in file:
        family = line.strip().split()
	families[family_count] = family
	family_count += 1
    return families

def main():
    path = '/home/eevans/pymol/8_1_post_clust/'
    silent = 'clustered_MP01_gen8_1.silent'
    cluster_to_count = 'clusters_cent_to_pdb.txt'
   
    pdbs_path = '8_1/'
    cluster_families = '8_1_cluster_families.txt'
    families = read_ramilies_file(cluster_families, path)
    print families


    cent_to_pdbs = read_cent_to_structs(path+cluster_to_count)
    #cluster_to_count = 'final_clustering.txt'
    #cent_to_pdbs = read_cent_to_structs(path+cluster_to_count)

    dict_out = open(path+'final_clustering.txt', 'w')
    dict_out.write(str(cent_to_pdbs))
    dict_out.close()

    struct_to_e_dict = parse_silent(path+silent)

    #Map the energy of a structure to the structure in the cent-to-struct dict
    cent_to_pdb_energy = combine_cents_energies(cent_to_pdbs, struct_to_e_dict)
    #get the lowest energy structure of each cluster
    #cent_to_lowest_energy = find_lowest_energy(cent_to_pdb_energy)
    cent_to_5_lowest = find_5_lowest_energies(cent_to_pdb_energy)
    # make a dictionary that maps the cent to its average energy and standard deviation
    avg_energy_dict = get_avg_energy(cent_to_pdb_energy)
    # make a dictionary that maps the cent to the length of its cluster
    cent_sizes = get_cent_size_dict(cent_to_pdbs)
    # write a csv including the center, its size, energy, std, lowest E struct
#    write_csv(avg_energy_dict, cent_to_lowest_energy, cent_sizes, path)
    write_csv(avg_energy_dict, cent_to_5_lowest, cent_sizes, path)
    # write a executable to release all the lowest energy structres 
#    write_release_pdb_sh(cent_to_lowest_energy, silent, path)
    write_release_5_lowest_pdb_sh(cent_to_5_lowest, silent, path)

if __name__ == '__main__':
    main()

