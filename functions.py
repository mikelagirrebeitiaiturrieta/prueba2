from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests
import re
import os
import numpy as np
import folium
from folium import plugins
import webbrowser
import openrouteservice as ors
import pickle
import time
from geopy.geocoders import Nominatim 
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from shapely.geometry.polygon import Polygon
from bounding_boxes import *
import json
from test import get_add_from_file
# sp = stopwords.words
# ors_key = "5b3ce3597851110001cf624847c29f8864ce433699208e1c6c1cb793"
# client = ors.Client(key=ors_key)
# # API_key = 'AIzaSyCcb-HIYqA-N4JhPP-zlIe_onpgxgFn9rI'
# API_key = 'AIzaSyACG6EutbA0rKDpZA_Ny5vquytD2THwUks'
# api_distance_matrix =  'Au4AJmZEHNaKt5qU6qpxp5DazATW6' #'o0m7tdE0dwHQE14hsacTnDjzYFOFC'

# config = json.load(open('config.json','rb'))
# sp = stopwords.words('spanish')
# spanish = SpellChecker(language='es')
# locator = Nominatim(user_agent='myGeocoder')

# centro_coruña = [43.3713500, -8.3960000]
# coruña_limits = locator.geocode('A Coruña, Galicia, España',timeout = 100, language='es').raw['boundingbox']
# box = [[float(coruña_limits[0]), float(coruña_limits[2])], [float(coruña_limits[1]), float(coruña_limits[3])]]
# coruña_limits = locator.geocode('A Coruña, Galicia, España',timeout = 100, language='es').raw['boundingbox']
# bounds = f'{coruña_limits[0]},{coruña_limits[1]}%7C{coruña_limits[2]},{coruña_limits[3]}' 
# coruña_postcodes = [str(v) for v in list(range(15000,15012))+[15170,15190,15191,15192]]

# def get_lat_long_google(address): 
#     url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&bounds={bounds}&key={API_key}' 
#     response = requests.get(url) 
#     resp_json_payload = response.json() 
#     return(resp_json_payload['results'][0]['geometry']['location']), resp_json_payload['results'][0]['address_components'][-1]['long_name']

# def get_lat_long_osm(address):
#     x = address
#     addresses_mod_dict = {x:(re.split(r'\d+',x)[0], '' if re.findall(r'\d+',x)==[] else re.findall(r'\d+',x)[0])}
#     addresses_mod = list(addresses_mod_dict.values())
#     new_adresses_dict = {addresses_mod[i]:re.sub(r"\bTrav\b", "Travesia",re.sub(r"\bA Milton\b", "Archer Milton",re.sub(r"\bFraga do Eume\b","Fraga", \
#         re.sub(r"\bCrta. \b","Carretera ",re.sub(r"\bVales Villamartín\b","Vales Villamarín",re.sub(r"\bOzán\b","Orzán",re.sub(r"\bJ Sebastián\b","Juan Sebastián", \
#         re.sub(r"\bJosé L\b","Jose Luis",re.sub(r"\bLuciano Y\b","Luciano Yordi",re.sub(r"\bFdez\b","Fernandez", \
#         re.sub(r"\bRua A. \b","",re.sub(r"\bRua A. Sanjurjo de Carricarte\b","Sanjurjo Carricarte",re.sub(r"\bPlg.\b","Poligono ", \
#         re.sub(r"\bFco\b","Francisco",re.sub(r"\bP. Barrié la Maza\b","Pedro Barrié la Maza",re.sub(r"\bJosé Mara Hernansáez\b","José Maria Hernansáez", \
#         re.sub(r"\bGrupo de Viviendas Nuestra Señora del Carmen\b","Grupo de Vivendas Nosa Señora do Carme",re.sub(r"\bOza\b","de Oza", re.sub(r"\bel Cano\b","Elcano", \
#         re.sub(r"\bBoquete\b","Boquete de",re.sub(r"\bPintor Vilar\b","Pintor Villar",re.sub(r"\bLuis Peña Nova\b","Luis Peña Novo",re.sub(r"\bEnrique Mariño\b","Enrique Mariñas", \
#         re.sub(r"\bAvenida Concordia\b","Concordia", re.sub(r"\bJoaquín Cotarelo Martínez\b","Doctor Joaquín Cotarelo",re.sub(r"\bJubias\b","Xubias",re.sub(r"\bSanmartín\b","San Martín", \
#         re.sub(r"\bherrería\b","herrerías",re.sub(r"\bSegunda\b","",re.sub(r"\bAboage\b","Amboage",re.sub(r"\bIlla\b","Illas",re.sub(r"\bPascoas\b","Pascoaes",re.sub(r"\bpascuas\b","Pascoaes", \
#         re.sub(r"\bCalla\b","Rua",re.sub(r"\barresto\b","Armesto",re.sub(r"\bRonde\b","Ronda",re.sub(r"\bRúa\b",'Rua',re.sub(r"\bCale\b",'Rua',re.sub(r"\bCalle\b",'Rua', \
#         (' '.join([addresses_mod[i][0].split()[j] for j in range(0,len(addresses_mod[i][0].split())-1) if (addresses_mod[i][0].split()[j]==addresses_mod[i][0].split()[j].title()) | (addresses_mod[i][0].split()[j] not in sp) | (addresses_mod[i][0].split()[j+1] not in sp)] \
#         + [addresses_mod[i][0].split()[-1] if addresses_mod[i][0].split()[-1] not in sp else '']) +' '+addresses_mod[i][-1]+', A Coruña, Galicia, España')))))))))))))))))))))))))))))))))))))))) \
#         for i in range(len(addresses_mod))}
#     new_adresses = list(set(new_adresses_dict.values()))

#     addr_geocoded = {}
#     addr = new_adresses[0]
#     loc = locator.geocode(addr,timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#     pc, city = check_pc(loc), check_city(loc)
#     try:
#         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#             loc = locator.geocode(re.sub(r"\bRua\b","Calle", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#             pc, city = check_pc(loc), check_city(loc)
#             if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                 loc = locator.geocode(re.sub(r"\bel\b","de", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                 pc, city = check_pc(loc), check_city(loc)
#                 if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                     loc = locator.geocode(re.sub(r"\bRua\b","", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                     pc, city = check_pc(loc), check_city(loc)
#                     if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                         loc = locator.geocode(re.sub(r"\bde\b", "", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                         pc, city = check_pc(loc), check_city(loc)
#                         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                             if 'de' in addr.lower():
#                                 loc = locator.geocode(re.sub(r"\bde\b", "da", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                 pc, city = check_pc(loc), check_city(loc)
#                             elif 'do' in addr.lower():
#                                 loc = locator.geocode(re.sub(r"\bdo\b", "de", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                 pc, city = check_pc(loc), check_city(loc)
                                
#                             if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                 loc = locator.geocode(re.sub(r",","", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                 pc, city = check_pc(loc), check_city(loc)

#                                 if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                     if ('travesía' in addr.lower()) and ('buenavista' in addr.lower()):
#                                         loc = locator.geocode(re.sub(r"\bde\b", "", re.sub(r"\brua\b", "", addr.lower())),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'Plaza' in addr:
#                                         loc = locator.geocode(re.sub(r"\bPlaza\b","Plaza de", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                             loc = locator.geocode(re.sub(r"\bPlaza\b","Praza", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                             pc, city = check_pc(loc), check_city(loc)
#                                             if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                                 loc = locator.geocode(re.sub(re.findall(r'\d+',addr)[0],"", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                                 pc, city = check_pc(loc), check_city(loc)
#                                     elif ('lugar' in addr.lower()) and ('birloque' in addr.lower()):
#                                         loc = locator.geocode(re.sub(r"\bel\b", "", re.sub(r"\blugar\b", "", addr.lower())),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                             loc = locator.geocode(re.sub(r"\bdel\b", "", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                             pc, city = check_pc(loc), check_city(loc)
#                                     elif 'Lugar' in addr:
#                                         loc = locator.geocode(re.sub(r"\bLugar\b","", addr),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                             loc = locator.geocode(re.sub(r"\bdel\b", "", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                             pc, city = check_pc(loc), check_city(loc)
#                                     elif 'cantera' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bcantera\b","carretera",re.sub(r"\brua\b","", addr.lower())),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'rrr' in addr.lower():
#                                         loc = locator.geocode(addr.replace('rrr','rr'),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'ss' in addr.lower():
#                                         loc = locator.geocode(addr.replace('ss','s'),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'manuela' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bmanuela\b","manuel", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'novoa' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bnovoa\b","novo", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'avenida' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bavenida\b","", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                             loc = locator.geocode(re.sub(r"\bla\b","",re.sub(r"\btorre\b","", addr.lower())),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                             pc, city = check_pc(loc), check_city(loc)
#                                     elif 'travesía' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\btravesía\b","calle", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                         if (loc == None) | (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])==0):
#                                             loc = locator.geocode('travesía '+ addr.lower().split('travesía')[-1],timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                             pc, city = check_pc(loc), check_city(loc)
#                                     elif 'neira' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bneira\b","neyra", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'juan' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bjuan\b","juana", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'ramón' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bramón\b","román", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'naturalista' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bnaturalista\b","", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'nuestra señora' in addr.lower():
#                                         loc = locator.geocode(addr.lower().split('nuestra')[-1],timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'pereira' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bpereira\b","pedreira", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'villa' in addr.lower():
#                                         loc = locator.geocode(re.sub(r"\bvilla\b","vila", addr.lower()),timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)
#                                     elif 'Igualdad'.lower() in addr.lower():
#                                         loc = {'latitude':43.3570754, 'longitude':-8.4119984}
#                                         pc = '15008'
#                                         city = 'A Coruña'

                                        

#                                     else:
#                                         pre_num = re.split(r'\d+',addr)[0]
#                                         num = re.findall(r'\d+',addr)[0]
#                                         post_num = re.split('\d+',addr)[-1]
#                                         new_addr = ' '.join([word if (spanish.candidates(word)==None) else(spanish.correction(word) if len(spanish.candidates(word))==1 else word) for word in pre_num.split()]+[num,post_num])
#                                         loc = locator.geocode(new_addr,timeout = 100, language='es', addressdetails=True, viewbox=box, bounded=True)
#                                         pc, city = check_pc(loc), check_city(loc)

#         if loc != None:
#             if (sum([pc in coruña_postcodes, 'a coruña' in city.lower()])!=0):
#                 if type(loc) == dict:
#                     addr_geocoded[addr] = [loc['latitude'],loc['longitude']]
#                 else:
#                     addr_geocoded[addr] = [loc.latitude,loc.longitude]
#             else:
#                 addr_geocoded[addr] = None
#         else:
#             addr_geocoded[addr] = None

#     except:
#         addr_geocoded[addr] = None

#     return {'lat':addr_geocoded[new_adresses_dict[addresses_mod_dict[x]]][0],'lng':addr_geocoded[new_adresses_dict[addresses_mod_dict[x]]][1]}


# def get_geocode(file_dir_name, tipo, directory='datos/', test = False):

#     if 'sp.pkl' in os.listdir('SavedData/'):
#         sp = pickle.load(open('SavedData/sp.pkl','rb'))
#     else:
#         all_files = [directory+x for x in os.listdir(directory) if x.endswith('.xls')]
#         all_addresses = []
#         for file in all_files:
#             df = pd.read_excel(file)
#             all_addresses = all_addresses+list(df.iloc[1:]['Localización'].values)

#         all_addresses_mod = [re.split(r'\d+',x)[0] for x in all_addresses]
#         sp = sp + [v[0] for v in Counter([word for addr in all_addresses_mod for word in addr.split(' ')]).most_common(10) if v[-1]>3000]+['al','número','números','frente','atura','ala','latura','lauta','n','º','alturta','bloque','de.']
#         pickle.dump(sp,open('SavedData/sp.pkl','wb'))

#     if not test:
#         addresses = list(pd.read_excel(file_dir_name).iloc[1:]['Localización'].drop_duplicates().values)
#     else:
#         addresses = get_add_from_file(file_dir_name,tipo)

#     addresses_mod_dict = {(re.split(r'\d+',x)[0], '' if re.findall(r'\d+',x)==[] else re.findall(r'\d+',x)[0]):x for x in addresses}
#     addresses_mod = list(addresses_mod_dict.keys())
#     new_adresses_dict = {(' '.join([addresses_mod[i][0].split()[j] for j in range(0,len(addresses_mod[i][0].split())-1) \
#         if (addresses_mod[i][0].split()[j]==addresses_mod[i][0].split()[j].title()) | (addresses_mod[i][0].split()[j] not in sp) | (addresses_mod[i][0].split()[j+1] not in sp)] \
#         + [addresses_mod[i][0].split()[-1] if addresses_mod[i][0].split()[-1] not in sp else '']) +' '+addresses_mod[i][-1]+', A Coruña, Galicia, España'):addresses_mod[i] \
#         for i in range(len(addresses_mod))}
#     new_adresses = list(set(new_adresses_dict.keys()))

#     addr_geocoded = {}
#     for addr in new_adresses:
#         lat_lng, pc = get_lat_long_google(addr)
#         if pc in coruña_postcodes:
#             addr_geocoded[addresses_mod_dict[new_adresses_dict[addr]]] = lat_lng
#         else:
#             addr_geocoded[addresses_mod_dict[new_adresses_dict[addr]]] = get_lat_long_osm(addr)


#     return addr_geocoded



# def create_data_model(distance_matrix, num_vehicles, initial_routes):
#     """Stores the data for the problem."""
#     data = {}
#     data['distance_matrix'] = distance_matrix
#     data['num_vehicles'] = num_vehicles
#     data['starts'] = [0]*num_vehicles
#     data['ends'] = [1]*num_vehicles

#     if initial_routes:
#         data['initial_routes'] = initial_routes
#     return data

# def print_solution(data, manager, routing, solution):
#     """Prints solution on console."""
#     print(f'Objective: {solution.ObjectiveValue()}')
#     max_route_distance = 0
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
#         route_distance = 0
#         while not routing.IsEnd(index):
#             plan_output += ' {} -> '.format(manager.IndexToNode(index))
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             route_distance += routing.GetArcCostForVehicle(
#                 previous_index, index, vehicle_id)
#         plan_output += '{}\n'.format(manager.IndexToNode(index))
#         plan_output += 'Distance of the route: {}m\n'.format(route_distance)
#         print(plan_output)
#         max_route_distance = max(route_distance, max_route_distance)
#     print('Maximum of the route distances: {}m'.format(max_route_distance))

# def get_routes(solution, routing, manager):
#     """Get vehicle routes from a solution and store them in an array."""
#   # Get vehicle routes and store them in a two dimensional array whose
#   # i,j entry is the jth location visited by vehicle i along its route.
#     routes = []
#     for route_nbr in range(routing.vehicles()):
#         index = routing.Start(route_nbr)
#         route = [manager.IndexToNode(index)]
#         while not routing.IsEnd(index):
#             index = solution.Value(routing.NextVar(index))
#             route.append(manager.IndexToNode(index))
#         routes.append(route)
#     return routes
# def solve_vrp(distance_matrix,num_vehicles, initial_routes):

#     """Entry point of the program."""
#     # Instantiate the data problem.
#     data = create_data_model(distance_matrix,num_vehicles, initial_routes)

#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                            data['num_vehicles'], data['starts'],
#                                            data['ends'])

#     # Create Routing Model.
#     routing = pywrapcp.RoutingModel(manager)

#     # Create and register a transit callback.
#     def distance_callback(from_index, to_index):
#         """Returns the distance between the two nodes."""
#         # Convert from routing variable Index to distance matrix NodeIndex.
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return data['distance_matrix'][from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Add Distance constraint.
#     dimension_name = 'Distance'
#     routing.AddDimension(
#         transit_callback_index,
#         0,  # no slack
#         200000000,  # vehicle maximum travel distance
#         True,  # start cumul to zero
#         dimension_name)
#     distance_dimension = routing.GetDimensionOrDie(dimension_name)
#     distance_dimension.SetGlobalSpanCostCoefficient(100)

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.local_search_metaheuristic = (
#         routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
#     search_parameters.time_limit.seconds = 50
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

#     # Solve the problem.
#     if initial_routes:
#         initial_solution = routing.ReadAssignmentFromRoutes(data['initial_routes'], True)
#         solution = routing.SolveFromAssignmentWithParameters(initial_solution,search_parameters)
#     else:
#         solution = routing.SolveWithParameters(search_parameters)

#     # Print solution on console.
#     if solution:
#         routes = get_routes(solution, routing, manager)
#         # print_solution(data, manager, routing, solution)
#         return routes

# def get_matrix_from_record(addresses,filename):
#     #check if file exists

#     if not os.path.isfile(filename):
#         #if it doesn't create the file and add an empty dictionary to append the downloaded matrix
#         d = {}
#         pickle.dump(d,open(filename,'wb'))
#         return False
#     d = pickle.load(open(filename,'rb'))
#     if d.get(tuple(addresses)) is None:
#         return False
#     return d[tuple(addresses)]

# def get_matrix_from_coordinates(coordinates, addresses, recalculate = False, use_google = False):
#     data_folder = config['distance_matrix_folder']
#     filename = os.path.join(data_folder, 'saved_matrixes.pickle')
#     m = get_matrix_from_record(addresses, filename)
#     if not recalculate:
#         if m:
#             return m
#     distance_matrix = np.zeros((len(coordinates),len(coordinates)))
#     km_matrix = np.zeros((len(coordinates),len(coordinates)))
#     for k in range(10, len(coordinates)+10, 10):
#         for j in range(10, len(coordinates)+10, 10):

#             # origins_destinations_x = '|'.join(addresses[k-10:k])
#             # origins_destinations_y = '|'.join(addresses[j-10:j])

#             origins_destinations_x = dest_creator(coordinates[k-10:k])
#             origins_destinations_y = dest_creator(coordinates[j-10:j])
#             if use_google:
#                 url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s"%(origins_destinations_x,origins_destinations_y,API_key)
#             else:
#                 url = f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins={origins_destinations_x}&destinations={origins_destinations_y}&key={api_distance_matrix}'
#             payload={}
#             headers = {}

#             response = requests.request("GET", url, headers=headers, data=payload)
#             try:
#                 distance_matrix_1 = [[response.json()['rows'][i]['elements'][j]['duration']['value'] for j in range(len(response.json()['rows'][i]['elements']))] for i in range(len(response.json()['rows']))]
#                 km_matrix_1 =  [[response.json()['rows'][i]['elements'][j]['distance']['value'] for j in range(len(response.json()['rows'][i]['elements']))] for i in range(len(response.json()['rows']))]
#             except:
#                 print('ERROR IN DISTANCE MATRIX RESPONSE')
#                 break
#             distance_matrix[k-10:k,j-10:j] = distance_matrix_1
#             km_matrix[k - 10:k, j - 10:j] = km_matrix_1
#             if not use_google:
#                 time.sleep(5)
#     distance_matrix = distance_matrix.tolist()
#     distance_matrix = [[np.round(y).astype(int) for y in x] for x in distance_matrix]
#     if not os.path.isfile('SavedData/saved_matrixes.pickle'):
#         d = {}
#         pickle.dump(d,open(filename,'wb'))
#     d = pickle.load(open(filename,'rb'))
#     d[tuple(addresses)]=distance_matrix,km_matrix
#     pickle.dump(d,open(filename,'wb'))
#     return distance_matrix,km_matrix

# def dest_creator(values):
#     dest = ''
#     for c in values:
#         dest += f"{c['lat']},{c['lng']}|"
#     dest=dest[:-1]
#     return dest
# def get_waypoints(coordinates_list):
#     coordinates = []
#     for coordinate in coordinates_list:
#         pair = [coordinate['lng'],coordinate['lat']]
#         coordinates.append(pair)
#     route = client.directions(coordinates=coordinates,
#                           profile='driving-car',
#                           format='geojson')
#     return route["features"][0]["geometry"]
# def auto_open(path):
#     html_page = f'{path}'
#     # open in browser.
#     new = 2
#     webbrowser.open(html_page, new=new)

# def create_map(coordinates_list, address_list, type, save_path):
#     start = [coordinates_list[0][0]['lat'], coordinates_list[0][0]['lng']]
#     styles = [lambda x: {'color': '#00b0ffff', 'opacity': 0.8, 'weight': 4},
#               lambda x: {'color': '#FF2F2F', 'opacity': 0.8, 'weight': 4}]
#     colors = ['#1d6ad2ff', '#FF2F2F']
#     bcolors = ['#00b0ffff', '#ff5959ff']
#     m = folium.Map(location=start, tiles="cartodbpositron", zoom_start=12)
#     for k, coordinates in enumerate(coordinates_list):
#         style = styles[k]
#         color = colors[k]
#         bcolor = bcolors[k]
#         route = get_waypoints(coordinates)
#         waypoints = folium.GeoJson(route, style_function=style)
#         waypoints.layer_name = f'{type} {k + 1}'
#         waypoints.add_to(m)
#         addresses = address_list[k]

#         for i in range(0, len(coordinates)):
#             folium.Marker(
#                 location=[coordinates[i]['lat'], coordinates[i]['lng']], popup=addresses[i],
#                 icon=plugins.BeautifyIcon(
#                     icon="arrow-down", icon_shape="marker",
#                     number=i,
#                     border_color=color,
#                     background_color=bcolor,
#                     border_width=2.5,
#                     text_color='white'

#                 )
#             ).add_to(waypoints)

#     folium.LayerControl().add_to(m)
#     m.save(save_path)
#     auto_open(save_path)

# def check_pc(loc):
#     if loc is None: 
#         return None
#     else: 
#         try:
#             if loc.raw['address']['postcode'] != None:
#                 return int(loc.raw['address']['postcode'])
#         except:
#             return 0

# def check_city(loc):
#     if loc is None: 
#         return 'None'
#     else: 
#         try:
#             if loc.raw['address']['city'] != None:
#                 return loc.raw['address']['city']
#         except:
#             return 'None'

    
# def clusterize_routes(a, file='map'):
#     b = pd.DataFrame([[k,v['lat'],v['lng']] for k,v in a.items()], columns=['address','lat','lng'])
#     kmeans = KMeans(n_clusters=2, random_state=0, n_init=20).fit(b[['lat','lng']]).fit(b[['lat','lng']])
#     b['cluster'] = kmeans.labels_

#     b_modified = b.copy()

#     len_a = b.cluster.value_counts()[0]
#     len_b = b.cluster.value_counts()[1]
#     c = b.cluster.value_counts().reset_index()
#     c = c[c.cluster==c.cluster.min()]['index'].values[0]
#     min_group = b[b.cluster==c]
#     neigh = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', metric='euclidean')
#     neigh.fit(min_group[['lat','lng']])
#     res = neigh.kneighbors(b[b.cluster!=c][['lat','lng']])
#     res = sorted([(res[0][i][0],i) for i in range(len(res[0]))], key=lambda x: x[0])
#     while (abs(len_a-len_b)/len(b))>.1:
#         ind = b.loc[b.cluster!=c].index[res[0][-1]]
#         b_modified.loc[b_modified.index==ind,'cluster'] = c
#         res.pop(0)
#         len_a = b_modified.cluster.value_counts()[0]
#         len_b = b_modified.cluster.value_counts()[1]

#     max_cluster_zone = Counter([b_modified.loc[i,'cluster'] for i in range(len(b_modified)) if ((b_modified.loc[i,'lat']>=43.36517557656243) & (b_modified.loc[i,'lat']<=43.415175576562436)) & ((b_modified.loc[i,'lng']>=-8.405116816178221) & (b_modified.loc[i,'lng']<=-8.365116816178221)) | ((b_modified.loc[i,'lat']>=43.36517557656243)&((b_modified.loc[i,'lng']<=-8.405116816178221)&(b.loc[i,'lng']>=-8.455116816178221)))]).most_common(1)[0][0]
#     for i in range(len(b_modified)): 
#         if ((b_modified.loc[i,'lat']>=43.36517557656243) & (b_modified.loc[i,'lat']<=43.415175576562436)) & ((b_modified.loc[i,'lng']>=-8.405116816178221) & (b_modified.loc[i,'lng']<=-8.365116816178221)) | ((b_modified.loc[i,'lat']>=43.36517557656243)&((b_modified.loc[i,'lng']<=-8.405116816178221)&(b.loc[i,'lng']>=-8.455116816178221))):
#             b_modified.loc[i,'cluster'] = max_cluster_zone   

#     # plot_map(b_modified, name=file+'_post')

#     route_0 = b_modified[b_modified.cluster==0]
#     route_0 = {route_0.iloc[i,0]:{'lat':route_0.iloc[i,1],'lng':route_0.iloc[i,2]} for i in range(len(route_0))}
#     route_1 = b_modified[b_modified.cluster==1]
#     route_1 = {route_1.iloc[i,0]:{'lat':route_1.iloc[i,1],'lng':route_1.iloc[i,2]} for i in range(len(route_1))}
#     return [route_0, route_1]


# def router(container_list):
#     route = client.directions(coordinates=container_list,
#                           profile='driving-car',
#                           format='geojson')
#     return route["features"][0]["geometry"]

# def plot_map(b, name='map'):
#     coordinates_list = [[[b.loc[i,'lng'],b.loc[i,'lat']] for i in range(len(b)) if b.loc[i,'cluster']==j] for j in range(2)]
#     addresses = [[b.loc[i,'address'] for i in range(len(b)) if b.loc[i,'cluster']==j] for j in range(2)]
#     m = folium.Map(location=[b.loc[0,'lat'],b.loc[0,'lng']], tiles="OpenStreetMap", zoom_start=12)
#     styles = [lambda x: {'color': '#00b0ffff', 'opacity': 0.8, 'weight': 4},
#                 lambda x: {'color': '#FF2F2F', 'opacity': 0.8, 'weight': 4}]
#     colors = ['#1d6ad2ff', '#FF2F2F']
#     for k, coordinates in enumerate(coordinates_list):
#         style = styles[k]
#         color = colors[k]
#         route = router(coordinates)
#         waypoints = folium.GeoJson(route,style_function=style)
#         waypoints.layer_name = f'route {k + 1}'
#         waypoints.add_to(m)
#         addresses_ = addresses[k]
#         i=0
#         for add in addresses_:
#             folium.Marker(
#                 location=[b.loc[b['address']==add,'lat'], b.loc[b['address']==add,'lng']],
#                 popup=add,
#                 icon=folium.DivIcon(
#                     html=f"""<div style="font-family: courier new; font-size: 15pt; color: {color}">{i}</div>""")
            
#             ).add_to(waypoints)
        
#             i+=1
#         # Show the map
#     folium.LayerControl().add_to(m)
#     m.save(name+'.html')

# def geocode_to_polygon(geocodes):
#     lons_vect = np.array([i[0] for i in geocodes])
#     lats_vect = np.array([i[1] for i in geocodes])

#     # Point of interest P
#     lats_vect = np.append(lats_vect, lats_vect[0])
#     lons_vect = np.append(lons_vect, lons_vect[0])
#     lons_lats_vect = np.column_stack((lons_vect, lats_vect)) # Reshape coordinates
#     polygon = Polygon(lons_lats_vect) # create polygon

#     return polygon

# def clusterize_prezero(data, zone):
#     global zones, a
#     zones = zone
#     a = data
#     def sub():
#         c="{k:"
#         for z in range(len(zones)):
#             for i in range(len(zones[z])):
#                 c += "{'lat':v['lat'], 'lng':v['lng'], 'cluster':'zona_%i_%i'} if Point(v['lng'], v['lat']).within(zones[%i][%i]) == True else("%(z+1,i+1,z,i)

#         b = eval("}".join([c.split("}")[:-1][v] if v!=(len(c.split("}")[:-1])-1) else c.split("}")[:-1][v].replace("else(", "else ") for v in range(len(c.split("}")[:-1]))])+"}"+")"*(sum([len(i) for i in zones])-2) + "for k,v in a.items()}")
#         b_modified = pd.DataFrame(b).T.reset_index().rename(columns={'index':'address'})
#         routes = []
#         for zone in sorted(b_modified.cluster.unique()): 
#             route = b_modified[b_modified.cluster==zone]
#             route = {route.iloc[i,0]:{'lat':route.iloc[i,1],'lng':route.iloc[i,2]} for i in range(len(route))}
#             routes.append(route)
#         route_0, route_1 = routes[:2], routes[2:]
#         return [route_0, route_1]
#     return sub()


# def creating_route(clusters, cluster, starting_point, ending_point):
#     address_description=list(clusters[cluster].keys())
#     lat_long = list(clusters[cluster].values())

#     # add start and end points to the adresses list
#     #addresses = [','.join([str(v['lat']), str(v['lng'])]) for v in [starting_point, ending_point]] + addresses

#     # add start and end points to the lat-long list
#     lat_long = [starting_point,ending_point]+lat_long


#     # compute the distance matrix for every location
#     distance_matrix, km_matrix = get_matrix_from_coordinates(coordinates=lat_long,
#                                                     addresses=address_description,
#                                                     recalculate=False,
#                                                     use_google=True)

#     # solve the TSP and save the routes
#     routes = solve_vrp(distance_matrix=distance_matrix,
#                         num_vehicles=1,
#                         initial_routes=None)

#     report = [calculate_distance(routes[0],distance_matrix, cluster), calculate_distance(routes[0],km_matrix, cluster)]



#     return routes[0], address_description, lat_long, report


# def calculate_distance(route, distance_matrix, zone):
#     total_distance = 0
#     for i in range(len(route)-1):
#         if ((zone==0)&(i==(len(route)-2))):
#             pass
#         else:
#             idx1 = route[i]
#             idx2 = route[i+1]
#             total_distance+= distance_matrix[idx1][idx2]

#     return total_distance

# def create_report(route_num, type, report_t, report_km):    
#     route_name = f'Ruta {type} {route_num}'    
#     string = f'{route_name} porpuesta por GlobalDataQuantum: Duración estimada: {report_t} segundos ; Longitud: {report_km} metros.'    
#     return string
#     # with open(save_path,'w') as file:
#     #     file.write(string)


# def get_route_distance(coordinates, use_google = False):
#     distance_matrix = []
#     km_matrix = []
#     for k in range(len(coordinates)-1):
#             if use_google:
#                 url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s"%(str(str(coordinates[k]['lat'])+','+str(coordinates[k]['lng'])),str(str(coordinates[k+1]['lat'])+','+str(coordinates[k+1]['lng'])),API_key)
#             else:
#                 url = f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins={coordinates[k]}&destinations={coordinates[k+1]}&key={api_distance_matrix}'
#             payload={}
#             headers = {}

#             response = requests.request("GET", url, headers=headers, data=payload)
#             try:
#                 distance_matrix_1 = [[response.json()['rows'][i]['elements'][j]['duration']['value'] for j in range(len(response.json()['rows'][i]['elements']))] for i in range(len(response.json()['rows']))]
#                 km_matrix_1 =  [[response.json()['rows'][i]['elements'][j]['distance']['value'] for j in range(len(response.json()['rows'][i]['elements']))] for i in range(len(response.json()['rows']))]
#             except:
#                 print('ERROR IN DISTANCE MATRIX RESPONSE')
#                 break
#             distance_matrix.append(distance_matrix_1[0][0])
#             km_matrix.append(km_matrix_1[0][0])
#             if not use_google:
#                 time.sleep(5)
#     # distance_matrix = distance_matrix.tolist()
#     distance_matrix = [np.round(x).astype(int) for x in distance_matrix]
    
#     return sum(km_matrix),sum(distance_matrix)

