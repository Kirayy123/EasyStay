import requests
from EasyStay import mapAPI

def get_weather(city):
    api_key = "3cfb43edb35caaca2d0bba48e86cf621"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    #first gets the coords from the geocoding api
    coords = get_coords(city)
    lat = coords['lat']
    long = coords['lng']

    #passes coords to url query
    complete_url = f"{base_url}?lat={lat}&lon={long}&units=metric&appid={api_key}"
    response = requests.get(complete_url)
    weather_data = response.json()

    description = {}
    description['description'] = weather_data['weather'][0]['description']    
    icon = weather_data['weather'][0]['icon']
    temp = weather_data['main']['temp']

    iconUrl = f'https://openweathermap.org/img/wn/{icon}@2x.png'
    description['icon'] = iconUrl
    description['temp'] = temp
    return description


def get_coords(city):
    api_key = "3cfb43edb35caaca2d0bba48e86cf621"
    qUrl = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={1}&appid={api_key}"
    response = requests.get(qUrl)
    coords = response.json()

    coordsDict = {}
    coordsDict['lat'] = coords[0]['lat']
    coordsDict['lng'] = coords[0]['lon']
    return coordsDict

