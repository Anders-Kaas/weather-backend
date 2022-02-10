from fastapi import FastAPI, HTTPException
import requests
import json
import os

app = FastAPI()

open_weather_map_key = os.environ.get("OpenWeatherMapKey")


def get_city_information(city):
    """
    Returns list of dicts with 
    city name in every language
    latitude
    longitude
    country code
    region
    """

    open_weather_map_city_information = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&APPID={open_weather_map_key}").content
    return_list = json.loads(open_weather_map_city_information)
    return return_list

def get_city_coordinates(city):
    """
    Returns latitude and longitude of city
    """
    city_info = get_city_information(city)
    if len(city_info) > 0:
        city_info = city_info[0]
        lat, lon = city_info["lat"], city_info["lon"]
        return (lat, lon)
    return city_info


@app.get("/weather-info/")
async def current_weather(city: str = ""):

    if city == "":
        raise HTTPException(status_code=400, detail="city must be specified")
    
    coordinates = get_city_coordinates(city)
    if not coordinates:
        raise HTTPException(status_code=400, detail="city not found")
    lat, lon = coordinates

    open_weather_map_response = requests.get(f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&APPID={open_weather_map_key}")
    response = json.loads(open_weather_map_response.content)
    return response