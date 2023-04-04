import pandas as pd
import numpy as np
from random import shuffle


def get_add_from_file(path,type):
    df = pd.read_excel(path)
    if type.lower() == 'muebles':
        addreses = list(df['Unnamed: 3'].dropna()[df['Unnamed: 3'] != 0].iloc[2:])
    else:
        addreses = list(df['Unnamed: 8'].dropna()[df['Unnamed: 8'] != 0].iloc[2:])
    
    shuffle(addreses)
    return addreses

def get_add_from_file_routes(path,type):
    df = pd.read_excel(path)
    if type.lower() == 'muebles':
        df = df.loc[df['Unnamed: 3']!=0, ['Unnamed: 3', 'Unnamed: 4']].iloc[3:]
        df.iloc[:,1] = np.where(df.index<df[df.iloc[:,1]=='Equipo 2'].index[0], 'Equipo 1', 'Equipo 2')
        return [df[df['Unnamed: 4']==eq].iloc[:,0].values.tolist() for eq in df.iloc[:,1].unique()]
    else:
        return [list(df['Unnamed: 8'].dropna()[df['Unnamed: 8'] != 0].iloc[2:])]

def test_report(route_num, type, report_t, report_km):    
    route_name = f'Ruta {type} {route_num}'    
    string = f'{route_name} porpuesta por Prezero: Duración estimada: {report_t} segundos ; Longitud: {report_km} metros.'    
    return string

