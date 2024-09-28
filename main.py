import requests
from twilio.rest import Client
import os

# Your Twilio credentials
account_sid = "Your Twilio sid"
auth_token = "Yor twilio token"
twilio_number = "+"  # Replace with your Twilio phone number
to_phone_number = "+923456968822"  # Replace with your phone number

# Initialize Twilio client
client = Client(account_sid, auth_token)

# OpenWeather API key and coordinates
api_key = "Api key of Openweather"
latitude = 34.7758
longitude = 72.3625

try:
    # Make the API call to get the weather forecast
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}")
    response.raise_for_status()
    data = response.json()

    # Initialize a flag to check for rain
    will_rain = False

    # Iterate over the forecast data
    for forecast in data['list'][:4]:  # Get only the next 4 periods (12 hours)
        if 'weather' in forecast:  # Check if 'weather' key exists
            for weather in forecast['weather']:
                if 'id' in weather:  # Check if 'id' key exists
                    weather_id = weather['id']
                    if weather_id < 700:  # Weather ID less than 700 indicates rain
                        will_rain = True
                        break
            if will_rain:
                break

    if will_rain:
        print("It will rain in the next 12 hours.")
        # Send SMS
        message = client.messages.create(
            body="Alert: It will rain in the next 12 hours!",
            from_=twilio_number,
            to=to_phone_number
        )
        print(f"Message sent: {message.sid}")
    else:
        print("It will not rain in the next 12 hours.")

except requests.RequestException as e:
    print(f"Error fetching weather data: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
