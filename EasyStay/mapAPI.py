from django.http import HttpResponse, request
from django.shortcuts import render
import json
import requests




def get_key():
    key = 'ToCFmPC8oKry1IxVENwddP1yt2BKDBXl'  

    #reading file does not work in pythonAnywhere deployment  
    # try:
    #     with open('map.key', 'r') as file:
    #         key = file.readline().strip()
    # except:
    #     try:
    #         with open('../map.key') as file:
    #             key = file.readline().strip()
    #     except:
    #         raise IOError('map key not found')
    # if not key:
    #     raise KeyError('map key not found')
    #file.close()
    return key

def getLat_Long(city):
    qUrl = "https://api.tomtom.com/search/2/geocode/" + city +".json?storeResult=false&view=Unified&key=" + get_key()
    params = {
        'query' : city, 
        'ext' : 'json', 
        'key' : get_key()}

    response = requests.get(qUrl)
    response.raise_for_status()
    position = response.json()
    lat = position['results'][0]['position']['lat']
    lng = position['results'][0]['position']['lon']
    coords = {}
    coords['lat'] = lng
    coords['long'] = lat
    print(coords)
    return coords