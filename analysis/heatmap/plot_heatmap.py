import numpy as np
import matplotlib.pyplot as plt
import pickle


def get_distance_data(path_to_data):
    try:
        data_file = open(path_to_data, 'r')
        data = pickle.load(data_file)
        cent_1_label = pickle.load(data_file)
        cents_1 = pickle.load(data_file)
        cent_2_label = pickle.load(data_file)
        cents_2 = pickle.load(data_file)
        return data, cents_1, cents_2, cent_1_label, cent_2_label
    except:
        print 'please try a different distances file, could not open the one entered.'

def main():
    path = 'distances_81to9_14.pkl'
    distance_matrix, cents_1, cents_2, cent_1_label, cent_2_label = get_distance_data(path)
    plt.imshow(distance_matrix, cmap='terrain', interpolation='nearest') #seismic, PuOr, RdGy, ocean, terrain
    plt.colorbar()
    ax = plt.gca()
    plt.yticks(range(len(cents_1)))
    plt.ylabel(cent_1_label)
    plt.xticks(range(len(cents_2)))
    plt.xlabel(cent_2_label)
    ax.set_xticklabels(cents_2, rotation='vertical')
    ax.set_yticklabels(cents_1)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
