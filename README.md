note: pymol runs in __main__, thus all scripts used with pymol do not use a main() function
# Structure clustering
A multicore PDB file clustering algorithm made for a research compute cluster. It will perform a k-means clustering on raw pdb files. This was chosen because established clustering methods inappropriately clustered more similar structures in different clusters (rosetta clustering for example) 

Usage: 
The entire clustering algorithm is run via singa_batch_full_cluster.sh with no extra arguments.   
  In the current implementation, it requires that you have all of the .pdb files to cluster in their own directory with the path set in       each of the 4 files of the clustering program (update_mean, assign_struct_to_clust, Generate_centers and Generate_data_chunks)

# Analysis - Dendrogram:
Following clustering one should run the cluster_means_2.sh script in addition to placing the final cycle's center-to-cluster_size dictionary in a file (this is used by the dendrogram plotting script and can be done with 'cat clusters_new.txt' and then copying the final dictionary into a new file - leave in dictionary format!). This makes a pickle file that is needed for making a dendrogram.  
Then you can run plot_dendrogram.py (using these two files, the pickle and center-to-size count file) to generate a dendrogram and the input file needed to make a heatmap.

# Analysis - Heatmap:
Take the output file from the dendrogram program and adject the path to this file (in two_structure_distace.py) and the centers for the two structures you want to make a heatmap for.
Run two_structure_distance.sh 
Use the output pickle file for running plot_heatmap.py

# Analysis - Energy and picking best structures:
Energy analysis is controlled by energy_analysis.sh which calls five_struct_energy_analysis and dynamically generates a script to release the best pbds. To use it several things must happen: 

1. Use the heatmap of a self vs. self plot to determine super families. Then make a .txt file with these families like so:

    c.1.000_new_cent,c.2.000_new_cent (This is a single family, no spaces and comma seperated) <br />
    c.4.111_new_cent (A different family) <br />
    c.5.21_new_cent,c.8.190_new_cent (Yet another seperate family) <br />

Alter the path to this file in the five_struct_energy_analysis.py script

2. unlock all pdbs into a folder of your choosing different from the working folder ...alter the 'pdb_path' in five_struct_energy_analysis
    Make sure ONLY .pdb files are in the pdb directory (remove any other files)
 
3. alter all other paths to those related to the sequence of interest. 

Expect output: 
1. A .csv file containing the best structures of each family with average rmsd to other members of the same family and its energy 
2. A .csv file listing the average energies of all clusters with size, and top 5 structures with energies labeled 'cent_loweststruct_lowestenergy.csv'

Note: This document as with the entire repository are still a work in progress!
