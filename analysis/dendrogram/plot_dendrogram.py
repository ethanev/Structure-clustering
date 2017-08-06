import pickle
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import ast

def get_distance_data(path_to_data):
    try:
        data_file = open(path_to_data, 'r')
        data = pickle.load(data_file)
        print data
        cent_to_num = pickle.load(data_file)
        print cent_to_num
        cent_to_num_items = sorted(cent_to_num.items(), key=lambda tup: tup[1])
        cent_to_num = [center[0] for center in cent_to_num_items]
        return data, cent_to_num
    except:
        print 'please try a different distances file, could not open the one entered.'

def get_cluster_size_data(path_to_size_data):
    try:
        size_file = open(path_to_size_data, 'r')
        data = size_file.read()
        data_dict = ast.literal_eval(data)
        return data_dict
    except:
        print 'please try a different cluster size file, could not open the file.'

def prep_data(path_to_data, path_to_size_data):
    '''
    opens and returns the two data files in the proper form for clustering!

    :param path_to_data: string name of the data file
    :param path_to_size_data: string name of the data file
    
    :return: the distances np array (1D) form of the upper triangular matrix of distances and the size labeled clusters
    '''
    cluster_sizes = get_cluster_size_data(path_to_size_data)
    data, cent_to_num = get_distance_data(path_to_data)
    cent_to_num_plus_size = [cent +': ' + str(cluster_sizes[cent]) for cent in cent_to_num]
    return data, cent_to_num_plus_size

def main():
    # get the data, requires a pickled file from the python script: cluster_means_2.py
    # also requires a .txt file with a string representation of the FINAL center sizes dictionary from the
    # update_mean.py script generated during clustering.
    path_to_data = 'distancesMP25.pkl'
    path_to_size_data = 'MP25_cluster_sizes.txt'
    data, cent_to_num_plus_size = prep_data(path_to_data, path_to_size_data)

    #perform the data linkage analysis and the create the dendrogram with proper labels
    pre_dend_data_linkage = linkage(data, method='average')
    plt.figure()
    dend = dendrogram(pre_dend_data_linkage, labels=cent_to_num_plus_size) # orientation='left')

    #get data to do sequence-to-sequence comparison
    cluster_order = dend['ivl']
    out_clust_order_FILE = open(path_to_size_data[:-4]+'_dend_order.txt', 'w')
    out_clust_order_FILE.write(str(cluster_order))
    out_clust_order_FILE.close()

    #making the plot look pretty
    plt.rcParams['lines.linewidth'] = 2 # thicken up the dendrogram lines to look better!
    ax = plt.gca()
    ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation='vertical') #rotate the x labels to be vertical
    ax.tick_params(axis='x', which='major', labelsize=12)
    ax.set_ylabel('distance')
    ax.tick_params(axis='y', which='major', labelsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
