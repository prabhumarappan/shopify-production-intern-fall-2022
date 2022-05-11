import requests as r
import environ
env = environ.Env()

api_key = env('OPENWEATHER_API_KEY')

def get_weather_data(lat, long):
    url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (lat, long, api_key)
    response = r.get(url)
    data = response.json()
    temp = data['main']['temp'] - 273.15

    return temp
