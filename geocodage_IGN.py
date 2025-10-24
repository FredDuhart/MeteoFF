import requests

import json


def dec(response) :
    r = response.content
    r = r.decode('utf-8')
    r = json.loads(r)

    return r



def feature_extract(feature) : 

    coord = feature['geometry']['coordinates']
    coord.reverse()
    type_ = feature['properties']['type']
    name = feature['properties']['name']
    postcode = feature['properties']['postcode']


    return coord, name, postcode, type_


def getrequest_BAN_ville(city) :



    #test_url = 'https://data.geopf.fr/geocodage/search?q=Bordeaux&autocomplete=1&index=address&limit=50&returntruegeometry=false&type=municipality'

    test_url = 'https://data.geopf.fr/geocodage/search'

    params = { 'q' : city,
            'type' : 'municipality',
            'limit' : 50,
            'autocomplete' : 1,
            'index' : 'address',
            'returntruegeometry' : False,
            }
    
    

    x = requests.get(test_url, params=params)
    

    features = dec(x)['features']

    return features
    

def trait_request(ville) : 

    #{nom_de_la_ville(code_postal) : [Latitude, Longituide]}

    features = getrequest_BAN_ville(ville)


    #{nom_de_la_ville(code_postal) : [Latitude, Longituide]}
    dico = {}
    for feature in features :
        coord, name, postcode, type_ = feature_extract(feature)
        #print (f'{name} - {postcode} /// {coord} /// {type_}')
        k = f'{name} ({postcode})'
        v = coord
        dico.update({k : v})
    
    return dico






