import pandas as pd
import numpy as np


from data_exploration import load_and_get_unique_elements
# Inbound data:

file_path_inb = 'Inbound_ARG.xlsx'
data_inb = pd.read_excel(file_path_inb)

def generate_source_station(data_inb):

    unique_origin = load_and_get_unique_elements(file_path_inb, 2)

    origin_dict = {og: index for index, og in enumerate(unique_origin)}

    origin_lat = np.zeros(len(unique_origin))
    origin_long = np.zeros(len(unique_origin))

    for index, row in data_inb.iterrows():

        # niz je row.items()
    
        i = origin_dict[row["Origin"]]
        
        if origin_lat[i] == 0:
            origin_lat[i] = row["Origin Latitude"]

        # print(origin_lat[i])

        if origin_long[i] == 0:
            origin_long[i] = row["Origin Longitude"]


    return origin_lat, origin_long


def gen_dist(data_inb):

    unique_origin = load_and_get_unique_elements(file_path_inb, 2)

    origin_dict = {og: index for index, og in enumerate(unique_origin)}

    origin_dist = np.zeros(len(unique_origin))
    

    for index, row in data_inb.iterrows():

        # niz je row.items()
    
        i = origin_dict[row["Origin"]]
        
        if origin_dist[i] == 0:
            origin_dist[i] = row["Distance [km]"]

        

    return origin_dist



def get_origin(file_path_inb):
    unique_origin = load_and_get_unique_elements(file_path_inb, 2)
    origin_dict = {og: index for index, og in enumerate(unique_origin)}
    return unique_origin, origin_dict



if __name__ == '__main__':
    origin_lat, origin_long = generate_source_station(data_inb)
    
    

        

        


    