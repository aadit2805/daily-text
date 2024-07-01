import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import date
import geocoder

# load .env file
load_dotenv()

# assign keys to variables
api_key = os.getenv('api_key')
sid = os.getenv('sid')
token = os.getenv('token')
to_num = os.getenv('to_num')
from_num = os.getenv('from_num')
city = os.getenv('city')
today = date.today().isoformat()  # need for api call

# get latitude and longitude of the city
def get_coords(city):
    geo = geocoder.arcgis(city)
    if geo.ok:
        return (geo.latlng[0], geo.latlng[1])
    else:
        return None

coords = get_coords(city)
if coords:
    lat, lon = coords
else:
    lat, lon = None, None

# get weather data
def get_weather(api_key, lat, lon, date):
    try:
        url = f'https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&units=imperial&appid={api_key}'
        response = requests.get(url)
        data = response.json()  # grabs data

        # extract data
        weather = {
            'max_temp': data['temperature']['max'],
            'min_temp': data['temperature']['min'],
            'morning': data['temperature']['morning'],
            'afternoon': data['temperature']['afternoon'],
            'evening': data['temperature']['evening'],
            'night': data['temperature']['night'],
            'rain': round(data['precipitation']['total'] / 25.4, 2),
        }
        return weather
    except Exception as e:
        return None

# send the twilio sms
def send_sms(sid, auth_token, to_num, from_num, msg):
    try:
        client = Client(sid, auth_token)  # creates the client object
        message = client.messages.create(  # twilio function, takes in 3 parameters (text, from, to)
            body=msg,
            from_=from_num,
            to=to_num
        )
    except Exception as e:
        return None

# calls the sms function and inputs the data to send the message
def send_msg():
    if lat and lon:
        weather = get_weather(api_key, lat, lon, today)
        if weather:
            msg = f"Today's weather summary for {city}: \n\nMax Temperature: {weather['max_temp']}°F\nMin Temperature: {weather['min_temp']}°F\nMorning Temperature: {weather['morning']}°F\nAfternoon Temperature: {weather['afternoon']}°F\nEvening Temperature: {weather['evening']}°F\nNight Temperature: {weather['night']}°F\nRainfall: {weather['rain']} inches."
            send_sms(sid, token, to_num, from_num, msg)
    else:
        return None

send_msg()
