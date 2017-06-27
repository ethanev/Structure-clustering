from pymol import cmd
import os


# path = 'C:/Users/ethan/Documents/MIT/Pentelute Lab/Miniprotein project/Miniprotein Analysis/Ab initio cluster analysis/pdbs/'
path = '/home/eevans/pymol/test/'

# define the threshold distance
distance = 4

# define starting structures and clusters 
top_clusters = ['c.13.0.pdb.pdb']
clusters = {file[:-4]:[] for file in top_clusters}

# load the top structures
for file in top_clusters:
    cmd.load(path+file)

i = 0
for file in os.listdir(path):
    i+=1
    if i % 100 == 0:
        print 'step: ', i
	print 'length of clusters: ', len(clusters)
        for clust in clusters:
            if len(clusters[clust]) >= 20:
                print 'large cluster: ', len(clusters[clust]), clust
    if file not in top_clusters:
        cmd.load(path+file)
	print 'coords: ', len(cmd.get_coords(file[:-4]))
        dist_list = []
        for cluster_cent in clusters: 
#            dist = cmd.align(file[:-4],cluster_cent)
            dist = cmd.align(file[:-4], cluster_cent)
            dist_list.append((dist[0],cluster_cent))
        dist_list = sorted(dist_list, key=lambda x: x[0])
        if float(dist_list[0][0]) < distance:
            clusters[str(dist_list[0][1])].append(file[:-4])
            cmd.delete(str(file[:-4]))
        else:
	    top_clusters.append(file)
            clusters[file[:-4]] = []
for clust in clusters:
    if len(clust) > 1000:
        print clust, len(clust)

print 'DONE WITH 1ST CLUSTERING'

for file in os.listdir(path):
    if file not in top_clusters:
        cmd.load(path+file)
        dist_list = []
        for cluster_cent in clusters:
            dist = cmd.align(file[:-4],cluster_cent)
            dist_list.append((dist[0],cluster_cent))
        dist_list = sorted(dist_list, key=lambda x: x[0])
        if float(dist_list[0][0]) < distance:
            clusters[str(dist_list[0][1])].append(file[:-4])
            cmd.delete(str(file[:-4]))
        else:
            top_clusters.append(file)
            clusters[file[:-4]] = []

for clust in clusters:
    if len(clust) > 1000:
        print clust, len(clust)

print 'DONE WITH 2nd CLUSTERING'

for file in os.listdir(path):
    if file not in top_clusters:
        cmd.load(path+file)
        dist_list = []
        for cluster_cent in clusters:
            dist = cmd.align(file[:-4],cluster_cent)
            dist_list.append((dist[0],cluster_cent))
        dist_list = sorted(dist_list, key=lambda x: x[0])
        if float(dist_list[0][0]) < distance:
            clusters[str(dist_list[0][1])].append(file[:-4])
            cmd.delete(str(file[:-4]))
        else:
            top_clusters.append(file)
            clusters[file[:-4]] = []

for clust in clusters:
    if len(clust) > 1000:
        print clust


print 'DONE WITH 3rd CLUSTERING'

for file in os.listdir(path):
    if file not in top_clusters:
        cmd.load(path+file)
        dist_list = []
        for cluster_cent in clusters:
            dist = cmd.align(file[:-4],cluster_cent)
            dist_list.append((dist[0],cluster_cent))
        dist_list = sorted(dist_list, key=lambda x: x[0])
        if float(dist_list[0][0]) < distance:
            clusters[str(dist_list[0][1])].append(file[:-4])
            cmd.delete(str(file[:-4]))
        else:
            top_clusters.append(file)
            clusters[file[:-4]] = []

for clust in clusters:
    if len(clust) > 1000:
        print clust


