# Structure clustering
A multicore PDB file clustering algorithm made for a research compute cluster. It will perform a k-means clustering on raw pdb files. This was chosen because established clustering methods inappropriately clustered more similar structures in different clusters (rosetta clustering for example) 

Usage: 
The entire clustering algorithm is run via full_cluster.sh with no extra arguments. 

In the current implementation, it requires that you have all of the .pdb files to cluster in their own directory with the path set in each of the 4 files of the clustering program (update_mean, assign_struct_to_clust, Generate_centers and Generate_data_chunks)

Note: This document as with the entire repository are still a work in progress!
