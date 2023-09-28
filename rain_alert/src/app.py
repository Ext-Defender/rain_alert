import requests
import json

from twilio.rest import Client

import os

owm_key = os.environ.get("OWM_API_KEY")
my_lat = os.environ.get
open_weather_map = "https://api.openweathermap.org/data/3.0/onecall"
weather_params = {
    "lat": os.environ.get("MY_LAT"),
    "lon": os.environ.get("MY_LON"),
    "exclude": "current,minutely,daily",
    "appid": owm_key,
    "units": "imperial",
}

twilio_key = os.environ.get("TWILIO_API_KEY")
twilio_sid = os.environ.get("TWILIO_SID")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")


def call_weather_api():
    weather_response = requests.get(open_weather_map, weather_params)
    return weather_response.json()


def load_test_data(path):
    file = open(path)
    data = json.load(file)
    file.close()
    return data


def check_for_rain_12hrs(data):
    for hour_data in data["hourly"][:12]:
        condition_code = hour_data["weather"][0]["id"]
        if condition_code < 700:
            return True


def send_sms(phone_number, msg="test"):
    client = Client(twilio_sid, twilio_key)
    if phone_number[:2] != "+1":
        phone_number = "+1" + phone_number
    client.messages.create(from_=twilio_phone_number, body=msg, to=phone_number)


def lambda_handler(event, context):
    phone_number = event["phone_number"]
    data = call_weather_api()
    if check_for_rain_12hrs(data):
        send_sms(phone_number, "It is going to rain today!")

    return {"statusCode": 200}
