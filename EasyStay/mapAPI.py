# from django.http import HttpResponse
# from django.shortcuts import render
# import json
# import requests


def get_key():
    key = None    
    try:
        with open('map.key', 'r') as file:
            key = file.readline().strip()
    except:
        try:
            with open('../map.key') as file:
                key = file.readline().strip()
        except:
            raise IOError('map key not found')
    if not key:
        raise KeyError('map key not found')
    
    return key

def display_Map(request):
    sdkURl = "https://api.tomtom.com/maps-sdk-for-web/cdn/6.x/6.25.0/maps/maps-web.min.js"

    getParams =  {"key": get_key() , "container" : "map"}
    response = requests.get(sdkURl,params=getParams)
    response.raise_for_status()





# def get_Lat_Long(request):
#     requests.get()