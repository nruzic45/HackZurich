
import pandas as pd
import numpy as np
import math

from inbound import generate_source_station, get_origin, gen_dist



class CityGraph:
    def __init__(self):
        self.graph = {}  # Using a dictionary to store the graph data

    def add_city(self, city_name):
        """
        Add a city to the graph.
        """
        if city_name not in self.graph:
            self.graph[city_name] = []

    def add_connection(self, city1, city2):
        """
        Add a connection (edge) between two cities.
        """
        if city1 in self.graph and city2 in self.graph:
            self.graph[city1].append(city2)
            self.graph[city2].append(city1)  # Assuming the connection is bidirectional

    def get_connections(self, city_name):
        """
        Get a list of cities connected to the given city.
        """
        if city_name in self.graph:
            return self.graph[city_name]
        else:
            return []

    def __str__(self):
        return str(self.graph)
    
def load_and_get_unique_elements(file_path, column_number):
    try:
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Check if the specified column number is valid
        if column_number < 0 or column_number >= df.shape[1]:
            raise ValueError("Invalid column number")

        # Extract the specified column
        column_data = df.iloc[:, column_number]

        # Get unique elements from the column and convert them to a list
        unique_elements = column_data.unique().tolist()

        return unique_elements
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return str(e)

# Test functions

file_path = "Outbound_ARG.xlsx"  
column_number = 6 

unique_elements = load_and_get_unique_elements(file_path, column_number)


#-------------------------------------------------------------------------------------------


file_path = "Outbound_ARG.xlsx"  

input_cities = [('MENDOZA',40), ('GODOY CRUZ',13), ('VILLA CONSTITUCION',24), ('CURUZU CUATIA',50), ('MUNRO',30)]

data = pd.read_excel(file_path)

unique_cities = load_and_get_unique_elements(file_path, 11)
unique_cementare = load_and_get_unique_elements(file_path, 2)  
unique_routes = load_and_get_unique_elements(file_path, 9)

city_dict = {city: index for index, city in enumerate(unique_cities)}

cementare_dict = {cem: index for index, cem in enumerate(unique_cementare)}

route_dict = {rt: index for index, rt in enumerate(unique_routes)}

# --------------------------------------------------------------------------------------------

def generate_graph_mat_basic(data):


    mat = np.ones((len(unique_cities), len(unique_cementare)))*10000


    # Iterate through rows and print their contents
    for index, row in data.iterrows():

        # niz je row.items()

        i = city_dict[row["City"]]
        j = cementare_dict[row["Plant Name"]]

        value_to_check = row["Distance [km]"]

        if mat[i][j] > value_to_check:
            mat[i][j] = value_to_check 


    for i in range(0,len(unique_cities)):
        for j in range(0, len(unique_cementare)):
           if mat[i][j] == 10000:
            mat[i][j] = 0 

    return mat

def generate_graph_mat_routes(data):


    mat = np.ones((len(unique_cities), len(unique_cementare)))*10000


    # Iterate through rows and print their contents
    for index, row in data.iterrows():

        # niz je row.items()

        i = city_dict[row["City"]]
        j = cementare_dict[row["Plant Name"]]

        value_to_check = row["Distance [km]"]
        route_to_add = route_dict[row["Route ID"]]

        if mat[i][j] > value_to_check:
            mat[i][j] = route_to_add 


    for i in range(0,len(unique_cities)):
        for j in range(0, len(unique_cementare)):
           if mat[i][j] == 10000:
            mat[i][j] = 0

    return mat


def generate_mat_with_corr(mat_basic,mat):

    mat_corr = []

    for i in range(0,len(mat[0])):
        j = i 
        for j in range(i, len[0]):
            if mat[i].any() == mat[j].any():
                continue
            else:
                for k in range(mat[i]):
                    if mat[i][k] == mat[j][k]:
                        mat_basic[i][j] = mat_basic[j][j]      
                    
                mat_corr[i][j] = mat_basic[i][j]



def get_mat(input,mat):

    for ind, city in enumerate(input):        
        print(city[0])
        print(mat[city_dict[city[0]]])



def generate_city_list(data):

    city_lat = np.zeros(len(unique_cities))
    city_long = np.zeros(len(unique_cities))

    for index, row in data.iterrows():

        # niz je row.items()
    
        i = city_dict[row["City"]]
        
        if city_lat[i] == 0:
            city_lat[i] = row["Plant Latitude"]

        # print(origin_lat[i])

        if city_long[i] == 0:
            city_long[i] = row["Plant Longitude"]

        

    return city_lat, city_long



#---
file_path_inb = 'Inbound_ARG.xlsx'
data_inb = pd.read_excel(file_path_inb)
#---


def spherical_to_euclidean(longitude, latitude, radius=6371.0):
    
    # Convert degrees to radians
    lon_rad = math.radians(longitude)
    lat_rad = math.radians(latitude)
    
    # Calculate Euclidean coordinates
    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.cos(lat_rad) * math.sin(lon_rad)
    z = radius * math.sin(lat_rad)
    
    return x,y

def euc(x1,y1,x2,y2):
    x1_euc, y1_euc = spherical_to_euclidean(x1,y1)
    x2_euc, y2_euc = spherical_to_euclidean(x2,y2)
    return np.sqrt((y2_euc-y1_euc)*(y2_euc-y1_euc) + (x2_euc-x1_euc)*(x2_euc-x1_euc))

def min_euc(city_lat_1, city_long_1,origin_lat,origin_long):
    min = 1000000
    source = 0
    for i in range(0,len(origin_lat)):
        dist = euc(city_lat_1, city_long_1, origin_lat[i], origin_long[i])
        if dist<min:
            min = dist
            source = i

    return min, source

def calc_euc_city(data, data_inb):
    city_lat, city_long = generate_city_list(data)
    origin_lat, origin_long = generate_source_station(data_inb)

    euclid_distances = np.zeros(len(unique_cities))
    sources_closest = np.zeros(len(unique_cities))
    for city in unique_cities:
        min, ind_source = min_euc(city_lat[city_dict[city]], city_long[city_dict[city]], origin_lat, origin_long)
        euclid_distances[city_dict[city]] = min
        sources_closest[city_dict[city]] = ind_source

    return euclid_distances, sources_closest


def outbound_optimize(data,_input):
    
    i = city_dict[_input[0]]
    mat = generate_graph_mat_basic(data)
    
    factory = mat[i]
    min = 100000
    outbound_i = 0
    for j in range(0,len(factory)):
        if factory[j] < min:
            min = factory[j]
            outbound_i = j

    return unique_cementare[outbound_i], min


def outbound_optimize_array(input_arr):
    
    factories = []

    for i in range(0,len(input_arr)):
        factory, min = outbound_optimize(data, input_arr[i])
        factories.append(factory)
    
    return factories

def calculate_ring_percent(data,data_inb,euclid,source_closest,town):

    i = source_closest[city_dict[town]]
    i = int(i)
    _, value_out = outbound_optimize(data, (town, 0))
    euclid_value = euclid[city_dict[town]]

    all_dist = gen_dist(data_inb)
    dist_source_value = all_dist[i]

    sum = value_out + dist_source_value + euclid_value
    percent = euclid_value/sum

    return percent
    
    

def inbound_optimize(data,data_inb,input):
    euclid_distances, source_closest = calc_euc_city(data, data_inb)
    i = city_dict[input[0]]
    return source_closest[i]


def inbound_optimize_array(input_arr):
    unique_origin, origin_dict = get_origin(file_path_inb)
    euclid_distances, source_closest = calc_euc_city(data, data_inb)
    
    sources = []
    percents = []
    for i in range(0, len(input_arr)):
        j = city_dict[input_arr[i][0]]
        j = int(j)
        percent = calculate_ring_percent(data,data_inb,euclid_distances,source_closest,unique_cities[j]) * 100
        sources.append(unique_origin[int(source_closest[j])])
        percents.append(percent)


    return sources, percents
    



if __name__ == "__main__":
    # mat = generate_graph_mat_basic(data)
    # mat_route = generate_graph_mat_routes(data)
    # get_mat(input_cities, mat)

    #print(mat_route)
    #print((mat-mat_route*10000)>0)
    #print(mat.any() == mat_route.any())
    #get_mat(input_cities,mat_route)
    
    # euclid_distances, source_closest = calc_euc_city(data, data_inb)
    # print(euclid_distances)
    # print(source_closest)

    #print(outbound_optimize_array(data,input_cities))
    #print(inbound_optimize_array(data, data_inb, input_cities))

    # Izbaciti minimum 
    # Izbaciti origin, 
    # euklidsko rastojanje delim sa ukupnum krugom,
    # komentar: Taj odnos se minimizuje, sto je postignuto uzimanjem najmnjeg ekulidskog rasrojanaj 
    pass








