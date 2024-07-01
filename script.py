import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import date
import geocoder
from openai import OpenAI

# load .env file
load_dotenv()

# assign keys to variables
api_key = os.getenv('api_key')
sid = os.getenv('sid')
token = os.getenv('token')
to_num = os.getenv('to_num')
from_num = os.getenv('from_num')
city = os.getenv('city')
gpt_key = os.getenv('gpt_key')

today = date.today().isoformat()

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
        'humidity': data['humidity']['afternoon'],
            
    }
    return weather

# send the twilio sms
def send_sms(sid, auth_token, to_num, from_num, msg):
    client = Client(sid, auth_token)  # creates the client object
    message = client.messages.create(  # twilio function, takes in 3 parameters (text, from, to)
        body=msg,
        from_=from_num,
        to=to_num
    )

# function to call GPT API
def get_gpt(model_name, system_msg, user_msg):
    client = OpenAI(api_key=gpt_key)
    response = client.completions.create(
        model=model_name,
        prompt=f"{system_msg} {user_msg}",
        max_tokens=3990
    )
    return response.choices[0].text.strip()

# calls the sms function and inputs the data to send the message
def send_msg():
    if lat and lon:
        weather = get_weather(api_key, lat, lon, today)
        if weather:
            model = "gpt-3.5-turbo-instruct"
            system_msg = "You are a helpful assistant who is being given information about the weather, and will help with picking out someone's outfit based on the weather."
            user_msg = f"What should I wear given this weather data: {weather}"
            gpt_msg = get_gpt(model, system_msg, user_msg)
            msg = (f"Today's weather summary for {city}:\n\n"
                   f"High: {weather['max_temp']}°F\n"
                   f"Low: {weather['min_temp']}°F\n"
                   f"Morning: {weather['morning']}°F\n"
                   f"Afternoon: {weather['afternoon']}°F\n"
                   f"Evening: {weather['evening']}°F\n"
                   f"Night: {weather['night']}°F\n"
                   f"Rainfall: {weather['rain']} inches\n"
                   f"Humidity: {weather['humidity']}%\n\n"
                   f"What you should wear: {gpt_msg}")
            send_sms(sid, token, to_num, from_num, msg)

send_msg()
