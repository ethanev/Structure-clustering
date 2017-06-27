import os
import random
from multiprocessing import cpu_count

def print_list(list):
    string = ''
    for item in list:
        string = string + item + ','
    print string.strip(',')

#path to data
path = '/home/eevans/pymol/9_15/'

##### obtain the cluster centers randomly
# define how many clusters you want
clusters = 40

#create a dictionary container for the cluster centers
cluster_centers = dict()
center_values = []

#list of structures to be clustered
structures = os.listdir(path)

#randomly determine the cluster centers
for i in range(clusters):
    i += 1
    selected = False
    while not selected:
        value = random.randrange(0,len(structures))
        if value not in center_values:
            center_values.append(value)
            selected = True
for num in center_values:
    cluster_centers[structures[num][:-4]] = []
print_list(cluster_centers.keys())
#print '#### Done with cluster centers ####'
##### Chunk the data into pieces of the desired size
##### Goal: take as input the number of CPUs and break into this many chunks
# number of chunks
num_chunks = cpu_count()
# alter number of chunks is simply user defined to run on cluster
# num_chunks = 40

# size of data per chunk
data_chunk_size = len(structures) / num_chunks #this is an int, will make the last chunk take the remainder of data later

# split the data up and print the output to be read
chunk_dict = dict()
for i in range(num_chunks):
    chunk_dict[str(i)] = []
#chunk_dict = {str(i):[] for i in range(0,num_chunks)}
for i in range(num_chunks):
    for l in range(data_chunk_size):
        chunk_dict[str(i)].append(structures.pop())
while len(structures) != 0:
    chunk_dict[str(0)].append(structures.pop())
#for chunk in chunk_dict:
#    print_list(chunk_dict[chunk])
#print '#### done printing chunked data'






