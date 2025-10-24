
"""
IMPORTS
"""

import os
from io import BytesIO
import base64

import pandas as pd


from io import StringIO

import numpy as np
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.cm as cm


import openmeteo_requests

import locale




"""
PREVISIONS OPEN METEO
"""


def recup_openmeteo (modele, localisation):
    """
    Cette fonction utilise l'API de OPEN-METEO pour renvoyer les prévisions du modèle sélectionné
    en un point (localisation)
    Renvoie un DataFrame des prévisions au pas horaire
    Args
        modele : string => nom du modèle dans l'API OPEN METEO
        loclisaiton : liste de deux float => coordonnées WGS84 du point
    """

    # création de la session d'appel à l'API
    openmeteo = openmeteo_requests.Client()#(session = retry_session)

    # paramétre de la requête API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": localisation[0],
        "longitude": localisation[1],
        "hourly": ["temperature_2m", "rain", "weather_code"],
        "timezone": "auto",
        "forecast_days": 15, 
        "models": modele
    }

    # Requête API
    try : # utilise le certificat stocké dans le fichier 'open-meteo-com-chain.pem' (sinon bloquage par le firewall du département...)
        verify = './open-meteo-com-chain.pem'
        responses = openmeteo.weather_api(url, params=params, verify = verify)
    except :
        verify = True
        responses = openmeteo.weather_api(url, params=params, verify = verify)

    # Traitement de la réponse de la requête API
    response = responses[0]
    
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = datetime.fromtimestamp(hourly.Time()),
        end = datetime.fromtimestamp(hourly.TimeEnd()),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    

    dec = response.UtcOffsetSeconds() / 3600
 
    # Récupération des heures --- impotant de mettre utc = False car comparaison avec des heures locales plus loin dans le script...
    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s", utc = False),
	    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = False),
	    freq = pd.Timedelta(seconds = hourly.Interval()),
	    inclusive = "left"
    )}

    hourly_data['date'] = hourly_data['date'] + timedelta (hours = dec)


    # création du DataFrame
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["rain"] = hourly_rain
    hourly_data["weather_code"] = hourly_weather_code


    # Ajustement du tableau d'heure
    
    # if len(hourly_data['temperature_2m']) < len(hourly_data['date']) :     
    #     hourly_data['date'] = hourly_data['date'] [0:-1]

    #print (f'long hours = {len(hourly_data['date'])}')
    #print (f'long temp = {len(hourly_data['temperature_2m'])}')
    #print (f'long prec = {len(hourly_data['rain'])}')

    hourly_dataframe = pd.DataFrame(data = hourly_data)


    return hourly_dataframe

"""
TRAITEMENT GRAPHIQUE
"""
'''
OBJECTIFS
1 graphique regroupant 
- température (plot)
- pluviométrie (bars)
- wetaher_code => idéalement sous forme d'applat gradué du jaune (0) au noir (100)
'''



def graph_prev_d (df_MF, df_IFS, ville, delai):

    """
    Crée le graphique temporel comprenant :
    - les prévisions météo (df_MF) 
    - les prévisions IFS (df_IFS) 
    
    Args :
        df_MF : DataFrame => Prévisions MétéFranec comportant les champs 'date','temperature_2m', 'rain' et 'weather_code'
        df_IFS : DataFrame => Prévisions MétéFranec comportant les champs 'date','temperature_2m', 'rain' et 'weather_code'
        ville : nom du lieu
        delai : delai d'affichage en jour depuis 0h00 du jour en cours 
        
    """
    
    # calcul de la date de fin d'affichage
    d_fin = aujour = datetime.now() + timedelta (days = delai)


    # limitation de IFS après MF
    df_MF_fin = df_MF['date'].max()
    df_IFS = df_IFS[(df_IFS['date'] >= df_MF_fin)]
    #limitation des dates
    date_min = df_MF['date'].min()
    if delai !=0 :
        date_max = d_fin
    else : 
        date_max = df_IFS['date'].max()

    
    # détermination des températres min et max
    tmin = min([df_MF['temperature_2m'].min(), df_IFS['temperature_2m'].min()]) -2  
    tmax = max([df_MF['temperature_2m'].max(), df_IFS['temperature_2m'].max()]) +2 
    





    # création du plot

    #fig, (ax1,ax2) = plt.subplots(2, figsize=(10,12), gridspec_kw={'height_ratio': [3, 1]})
    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,12), gridspec_kw={'height_ratios': [6, 1]})
    plt.subplots_adjust(hspace = 0.45, bottom = 0.1, top = 0.95,) #left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4,hspace=0.4)
    
    # titre général
    aujour = datetime.now()
    ddate = f'{aujour.day}-{aujour.month}-{aujour.year}'
    hhour = f'{aujour.hour} h {aujour.minute}'

    fig.suptitle (f'Prévisions météo pour {ville}, le {ddate} à {hhour}' , color = 'grey')
    
    ###### graphique température
    
    color = 'green'
    
    ax1.plot(df_MF['date'], df_MF['temperature_2m'], linewidth=2.0, color=color, alpha = 1, label = 'Prév. MétéoFrance')
    ax1.plot(df_IFS['date'], df_IFS['temperature_2m'], linewidth=2.0, linestyle='--', color=color, alpha = 1, label = 'Prév. IFS')
    
    
    # axe x (temps)
    ax1.set_xlabel('Jours')
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    ax1.xaxis.set_minor_locator(mdates.HourLocator(byhour = [0,12]))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    ax1.tick_params(axis='x', labelrotation=90)
    ax1.set_xlim([date_min, date_max])
    
    # axe y 
    ax1.set_ylabel('°C')
    ax1.set_ylim([tmin, tmax])
    ax1.tick_params(axis='y', colors=color)
    ax1.yaxis.label.set_color(color)
    ax1.title.set_color(color)

    # grille
    ax1.grid(axis='x', color='black', linestyle='dashed', linewidth=0.2)
    ax1.grid(axis='y', color='black', linestyle='dotted', linewidth=0.4)
        
    # légende
    ax1.legend()

    ###### graphique précipitations


    ax3 = ax1.twinx()
    
    color = 'blue'
    width = 0.025
    alpha = 0.5

    ax3.bar(df_MF['date'], df_MF['rain'], color = color, width = width, alpha = alpha)
    ax3.bar(df_IFS['date'], df_IFS['rain'], color = color, width = width, alpha = alpha)
    
    ax3.set_ylabel('mm')
    ax3.tick_params(axis='y', colors=color)
    ax3.yaxis.label.set_color(color)
    ax3.title.set_color(color)


    # ------ graphique weather code

    # création de la cmap
    ytob_cmap = LinearSegmentedColormap.from_list(name="yellow_to_black", colors=["yellow", "brown", "black"])
    ytob_cmap = LinearSegmentedColormap.from_list(name="yellow_to_black", colors=["yellow", "blue", "grey", "dimgrey", "black"])

   
    # création des linecollections
    cmap = 'viridis'
    cmap = 'hot'
    cmap = ytob_cmap
    lw = 400
    lc_MF = data_LC (df_MF, cmap, lw)
    lc_IFS = data_LC (df_IFS, cmap, lw)

    # ajout des line collections    
    ax2.add_collection(lc_MF)
    ax2.add_collection(lc_IFS)

    
   
    # axe x (temps)
    #ax.set_xlabel('Jours')
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    # ax.xaxis.set_minor_locator(mdates.HourLocator(byhour = [0,12]))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    ax2.set_xlim(date_min, date_max)
    # ax.tick_params(axis='x', labelrotation=90)

    
    # axe y 
    # ax.set_ylabel('w_code')
    ax2.set_ylim([-0 , 2])
    
    # grille
    ax2.grid(axis='x', color='black', linestyle='dashed', linewidth=0.2)
    ax2.grid(axis='y', color='black', linestyle='dotted', linewidth=0.4) 
    
    ax2.axis('off')
    #ax.set_ylim(-9, 11)



    
    #plt.tight_layout()



    # ===== SHOW

    #plt.show()

    
    return fig


def graph_prev_court (df_MF, ville, delai):

    """
    Crée le graphique temporel comprenant :
    - les prévisions météo (df_MF) 
    
    
    Args :
        df_MF : DataFrame => Prévisions MétéFranec comportant les champs 'date','temperature_2m', 'rain' et 'weather_code'
        ville : 
        delai : delai de prévisions en heures à partir de maintenant
      
        
    """
    
    # limitation de MF à 36 h
    maintenant = datetime.now()

    limite_MF = maintenant + timedelta(hours = delai)
   
    
    df_MF = df_MF[(df_MF['date'] <= limite_MF)]
    #limitation des dates
    date_min = df_MF['date'].min()
    date_max = df_MF['date'].max()
    
    # détermination des températres min et max
    tmin = df_MF['temperature_2m'].min() -2  
    tmax = df_MF['temperature_2m'].max() +2 
    





    # création du plot

    #fig, (ax1,ax2) = plt.subplots(2, figsize=(10,12), gridspec_kw={'height_ratio': [3, 1]})
    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,12), gridspec_kw={'height_ratios': [6, 1]})
    plt.subplots_adjust(hspace = 0.45, bottom = 0.1, top = 0.95,) #left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4,hspace=0.4)
    
    # titre général
    aujour = datetime.now()
    ddate = f'{aujour.day}-{aujour.month}-{aujour.year}'
    hhour = f'{aujour.hour} h {aujour.minute}'

    fig.suptitle (f'Prévisions météo pour {ville}, le {ddate} à {hhour}' , color = 'grey')
    
    ###### graphique température
    
    color = 'green'
    
    ax1.plot(df_MF['date'], df_MF['temperature_2m'], linewidth=2.0, color=color, alpha = 1, label = 'Prév. MétéoFrance')
   
    
    # axe x (temps)
    ax1.set_xlabel('Jours')
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    ax1.xaxis.set_minor_locator(mdates.HourLocator(byhour = [0,12]))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    ax1.tick_params(axis='x', labelrotation=90)
    ax1.set_xlim([date_min, date_max])
    
    # axe y 
    ax1.set_ylabel('°C')
    ax1.set_ylim([tmin, tmax])
    ax1.tick_params(axis='y', colors=color)
    ax1.yaxis.label.set_color(color)
    ax1.title.set_color(color)






    # grille
    ax1.grid(axis='x', color='black', linestyle='dashed', linewidth=0.2)
    ax1.grid(axis='y', color='black', linestyle='dotted', linewidth=0.4)
        
    # légende
    ax1.legend()

    ###### graphique précipitations


    ax3 = ax1.twinx()
    
    color = 'blue'
    width = 0.025
    alpha = 0.5

    ax3.bar(df_MF['date'], df_MF['rain'], color = color, width = width, alpha = alpha)
    
    
    ax3.set_ylabel('mm')
    ax3.tick_params(axis='y', colors=color)
    ax3.yaxis.label.set_color(color)
    ax3.title.set_color(color)


    # ------ graphique weather code

    # création de la cmap
    ytob_cmap = LinearSegmentedColormap.from_list(name="yellow_to_black", colors=["yellow", "brown", "black"])
    ytob_cmap = LinearSegmentedColormap.from_list(name="yellow_to_black", colors=["yellow", "blue", "grey", "dimgrey", "black"])

   
    # création des linecollections
    cmap = 'viridis'
    cmap = 'hot'
    cmap = ytob_cmap
    lw = 400
    lc_MF = data_LC (df_MF, cmap, lw)
   

    # ajout des line collections    
    ax2.add_collection(lc_MF)
    

    
   
    # axe x (temps)
    #ax.set_xlabel('Jours')
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    # ax.xaxis.set_minor_locator(mdates.HourLocator(byhour = [0,12]))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    ax2.set_xlim(date_min, date_max)
    # ax.tick_params(axis='x', labelrotation=90)

    
    # axe y 
    # ax.set_ylabel('w_code')
    ax2.set_ylim([-0 , 2])
    
    # grille
    ax2.grid(axis='x', color='black', linestyle='dashed', linewidth=0.2)
    ax2.grid(axis='y', color='black', linestyle='dotted', linewidth=0.4) 
    
    ax2.axis('off')
    #ax.set_ylim(-9, 11)



    
    #plt.tight_layout()



    # ===== SHOW

    #plt.show()

    
    return fig

def data_LC (df, cmap, lw):

    """
    trannsforme une dataframe de données en line collection
    x = dates
    y = 1
    z(couleur) = waethercode
        
    Args :
        df : DataFrame => Prévisions comportant les champs 'date','temperature_2m', 'rain' et 'weather_code'
        cmap : cmap à utiliser
        lw : largeur de la ligne        
    """
    
    # ======== LineCollection sur df_MF
    x = mdates.date2num(df["date"])
    y = np.ones(len(x))
    z = df["weather_code"].values

    # Préparation des segments pour LineCollection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Création de la LineCollection
    
    lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0,100))
    lc.set_array(z)
    lc.set_linewidth(lw)

    return lc

def graph_wcode (df_MF, df_IFS):

    """
    Crée le graphique temporel comprenant :
    - les prévisions météo (df_MF) 
    - les prévisions IFS (df_IFS) 
    
    Args :
        df_MF : DataFrame => Prévisions MétéFranec comportant les champs 'date','temperature_2m', 'rain' et 'weather_code'
        df_IFS : DataFrame => Prévisions MétéFranec comportant les champs 'date','temperature_2m', 'rain' et 'weather_code'
        
    """
    
    # création de la cmap
    ytob_cmap = LinearSegmentedColormap.from_list(name="yellow_to_black", colors=["yellow", "brown", "black"])
    ytob_cmap = LinearSegmentedColormap.from_list(name="yellow_to_black", colors=["blue", "grey", "black"])

    #cm.register_cmap(name="ytob_fdt", cmap=ytob_cmap)
    # Enregistrer dans matplotlib
    #plt.register_cmap(name="ytob", cmap=ytob_cmap)

    # limitation de IFS après MF
    df_MF_fin = df_MF['date'].max()
    df_IFS = df_IFS[(df_IFS['date'] >= df_MF_fin)]

    date_min = df_MF['date'].min()
    date_max = df_IFS['date'].max()
   
    # création des linecollections
    cmap = 'viridis'
    cmap = 'hot'
    cmap = ytob_cmap
    lw = 400
    lc_MF = data_LC (df_MF, cmap, lw)
    lc_IFS = data_LC (df_IFS, cmap, lw)

    # création du plot
    fig, ax = plt.subplots(1, figsize=(12,4))
    plt.subplots_adjust(hspace = 0.45, bottom = 0.2, top = 0.95) #left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4,hspace=0.4)
    
    """ # titre général
    aujour = datetime.now()
    ddate = f'{aujour.day}-{aujour.month}-{aujour.year}'
    hhour = f'{aujour.hour} h {aujour.minute}' """

    #fig.suptitle (f'Prévisions météo le {ddate} à {hhour}' , color = 'grey')
    
    ax.add_collection(lc_MF)
    ax.add_collection(lc_IFS)

    
   
    # axe x (temps)
    ax.set_xlabel('Jours')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour = [0,12]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    ax.set_xlim(date_min, date_max)
    ax.tick_params(axis='x', labelrotation=90)

    
    # axe y 
    ax.set_ylabel('w_code')
    ax.set_ylim([-0 , 2])
    
    # grille
    ax.grid(axis='x', color='black', linestyle='dashed', linewidth=0.2)
    ax.grid(axis='y', color='black', linestyle='dotted', linewidth=0.4) 
    
    # # Formater l'axe des x pour afficher les dates proprement
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # fig.autofmt_xdate()

    ax.axis('off')
    #ax.set_ylim(-9, 11)

    cbar = plt.colorbar(lc_MF, ax=ax)
    cbar.set_label("Weather Code")

    
    #plt.tight_layout()

    #plt.show() # a geler
    
    return fig


def recup_localisation():
    df = pd.read_csv("localisation.txt", sep= ",", header = None)
    df.columns = ['VILLE', 'X', 'Y']
    df = df.set_index('VILLE')
    
    a={}
    for row in df.iterrows() :
        ville = row[0]
        x = row[1]['X']
        y = row[1]['Y']
        
        a.update({ville : [x,y]})

    

    return a




def meteo (localisation, duree):

    locale.setlocale(locale.LC_ALL, 'fr_FR')

    for ville, loc in localisation.items() :
            
        modele = "meteofrance_seamless"
        df_MF = recup_openmeteo (modele, loc)
        df_MF = df_MF.dropna()

        modele = "ecmwf_ifs"
        df_IFS = recup_openmeteo (modele, loc)
        df_IFS = df_IFS.dropna()

        fig = graph_prev_d (df_MF, df_IFS, ville, duree) 
        
        
        
    return fig


''' -------------------------------------------------------
/////////// MAIN       ////////////////////////////////////
--------------------------------------------------------'''

""" loc_1 = {'BORDEAUX' : [44.85333334858167, -0.5684633360000539],
                    'BAYONNE' : [43.493105559049745, -1.475418819223812],
                    'ALLANCHE' : [45.22890369761655, 2.9337424098169604]
    }

loc_2 = {'BORDEAUX' : [44.85333334858167, -0.5684633360000539],
                    'BELISAIRE' :[44.6565820731742, -1.2398078085305464],
                    'LACANAU OCEAN' : [45.00222764423105, -1.200269217500147],
                    'SOULAC' : [45.51420227514413, -1.125603303362456],
                    'ALLANCHE' : [45.22890369761655, 2.9337424098169604]
                }
"""  


#loc_bdx = {'BORDEAUX' : [44.85333334858167, -0.5684633360000539],} 

#delai = 10 # délai en jours


#meteo(loc_bdx, delai)