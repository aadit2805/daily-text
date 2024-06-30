import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import date
import geocoder

# load .env file
load_dotenv()

# assign keys to variables
api_key = os.getenv('API_KEY')
sid = os.getenv('SID')
token = os.getenv('TOKEN')
to_num = os.getenv('TO_NUM')
from_num = os.getenv('FROM_NUM')

#need for api call
geo = geocoder.ip('me') 
lat = geo.latlng[0]
lon = geo.latlng[1]
city = geo.city

today = date.today().isoformat() #need for api call

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
        print(f"failed to retrieve weather data: {e}")
        return None

# send the twilio sms
def send_sms(sid, auth_token, to_num, from_num, msg):
    try:
        client = Client(sid, auth_token)  # creates the client object
        message = client.messages.create(  # Twilio function, takes in 3 parameters (text, from, to)
            body=msg,
            from_=from_num,
            to=to_num
        )
    except Exception as e:
        print(f"failed to send SMS: {e}")
        return None

# calls the sms function and inputs the data to send the message
def send_msg():
    weather = get_weather(api_key, lat, lon, today)
    if weather:
        msg = f"Today's weather summary: Max Temperature: {weather['max_temp']}°F, Min Temperature: {weather['min_temp']}°F, Morning Temperature: {weather['morning']}°F, Afternoon Temperature: {weather['afternoon']}°F, Evening Temperature: {weather['evening']}°F, Night Temperature: {weather['night']}°F, Rainfall: {weather['rain']} inches."
        send_sms(sid, token, to_num, from_num, msg)

send_msg()
