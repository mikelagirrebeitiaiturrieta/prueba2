import pandas as pd
# import functions as ft
import os
from bounding_boxes import *
from test import *

# lista1_1_1 = ft.geocode_to_polygon(lista1_1)
# lista1_2_1 = ft.geocode_to_polygon(lista1_2)
# lista2_1_1 = ft.geocode_to_polygon(lista2_1)
# lista2_2_1 = ft.geocode_to_polygon(lista2_2)
# elec_1_1 = ft.geocode_to_polygon(elec_1)
# elec_2_1 = ft.geocode_to_polygon(elec_2)

# def main(config, file, tipo):
#     upload_folder = config['upload_folder']
#     # datadir = config['datadir']
#     templatesdir = config['templatesdir']
#     filepath = os.path.join(upload_folder,file)

#     base = {"lat":43.35091, "lng": -8.43284}
#     unload = {"lat":43.35622, "lng": -8.45764}
#     endings = {'muebles':[{'lat':43.36722825763309, 'lng':-8.407918317317424},{'lat':43.35507941519058, 'lng':-8.40410800474373}], 'electrodomesticos':[{'lat':43.37411501888933, 'lng':-8.437384493837364}]}

#     # print(filepath)
#     data = ft.get_geocode(file_dir_name=filepath, tipo = tipo,directory=upload_folder, test=True)
#     if tipo=='muebles':
#         clusters = ft.clusterize_prezero(data, [[lista1_1_1, lista1_2_1], [lista2_1_1, lista2_2_1]])
#     else:
#         # print('here')
#         clusters = ft.clusterize_prezero(data, [[elec_1_1, elec_2_1]])
#         clusters=clusters[:-1]
#     all_routes, address_descriptions, lat_longs, report_t, report_km = [], [], [], [], []
#     # print('starting')
#     for cluster in range(len(clusters)):
#         starting_point = base
#         ending_point = endings[tipo][cluster]
#         # print(ending_point)
#         n = 0
#         all_routes_, address_descriptions_, lat_longs_ , report_t_, report_km_= [], [], [], [],[]
#         for zone in range(len(clusters[cluster])):
#             # if type=='muebles':
#             route_, address_description_, lat_long_, report_ = ft.creating_route(clusters[cluster], zone, starting_point, ending_point)
#             route_ = [rt+n for rt in route_]
#             all_routes_+=route_[1:-1]
#             report_t_.append(report_[0])
#             report_km_.append(report_[1])
#             address_descriptions_+=address_description_
#             lat_longs_+=lat_long_[2:]
#             if zone != (len(clusters[cluster])-1):
#                 starting_point = lat_long_[route_[-2]]
#                 ending_point = unload

#             n = len(lat_longs_)
#             # else:
#             #     all_routes_, address_descriptions_, lat_longs_ = ft.creating_route(clusters[cluster], zone, base, ending_point)
#             #     all_routes_ = all_routes_[1:-1]
#         report_t.append(sum(report_t_))
#         report_km.append(sum(report_km_))
#         all_routes_ = [0]+all_routes_+[1]
#         lat_longs_ = [base, unload]+lat_longs_
#         all_routes.append(all_routes_)
#         address_descriptions.append(address_descriptions_)
#         lat_longs.append(lat_longs_)


#     # sort coordinates for maps visualization
#     coordinates_routes = [[lat_longs[j][i] for i in all_routes[j]] for j in range(len(all_routes))]


#     # delete the starting and ending point from the routes and drop the indexes to sort the addresses list
#     all_routes = [x[1:-1] for x in all_routes]
#     all_routes = [[y-2 for y in x] for x in all_routes]

#     # reorder address descriptions to route orders
#     address_routes = [[address_descriptions[j][i] for i in all_routes[j]] for j in range(len(all_routes))]


#     # map_save_path = tipo + '_map_base.html'
#     map_save_path = tipo + '_map_base.html'
#     map_save_path = os.path.join(templatesdir, map_save_path)
#     ft.create_map(coordinates_list=coordinates_routes,
#                 address_list=[['start']+x+['end'] for x in address_routes],
#                 type = tipo,
#                 save_path=map_save_path)

#     # prezero_routes = get_add_from_file_routes(filepath, tipo)
#     # prezero_routes = [ft.get_route_distance([base]+[data[k] for k in r]+[unload], use_google=True) for r in prezero_routes]
#     #save the routes to excel files
#     for i in range(len(address_routes)):
#         save_path = os.path.join(config['upload_folder'], file[:-5]+'_'+tipo+'_%s_ordenado.xlsx'%str(i))
#         df_new = pd.DataFrame(address_routes[i])
#         report_text = ft.create_report(i,tipo,report_t[i],report_km[i])
#         # report_text_2 = test_report(i, tipo, prezero_routes[i][1], prezero_routes[i][0])
#         df_new.loc[len(df_new)]=report_text
#         # df_new.loc[len(df_new)]=report_text_2
#         df_new.to_excel(save_path, index=None)
    
#     print('Ruta %s archivo %s' %(tipo,file))
#     print('Global Data Quantum: tiempo total %f segundos y distancia total %f'%(sum(report_t), sum(report_km)))
    # print('Prezero: tiempo total %f segundos y distancia total %f' %(sum([x[1] for x in prezero_routes]), sum([x[0] for x in prezero_routes])))

    # return sum(report_t), sum(report_km),sum([x[1] for x in prezero_routes]), sum([x[0] for x in prezero_routes])



# config = json.load(open('config.json','rb'))

# main(config=config, file=config['filename'], tipo='electrodomesticos')



