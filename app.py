
# Define the URL for the API
url = 'https://taxifare.lewagon.ai/predict'


import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from geopy.geocoders import Nominatim
import random
import math


# Title of the app
st.title("🚖 Taxi Fare Prediction 🎉")

# Input fields for user to provide ride parameters
date = st.date_input("📅 Date", datetime.now())
time = st.time_input("⏰ Time", datetime.now().time())
pickup_address = st.text_input("📍 Pickup Address", "Empire State Building, New York, NY")
dropoff_address = st.text_input("📍 Dropoff Address", "Central Park, New York, NY")
passenger_count = st.number_input("👥 Passenger Count", min_value=1, max_value=10, value=1)

# Combine date and time into a single datetime object
pickup_datetime = datetime.combine(date, time)

# Initialize the geocoder
geolocator = Nominatim(user_agent="taxi_fare_app")

def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        st.error(f"Could not geocode address: {address}")
        return None, None

fun_messages = [
    "Safe travels! 🚕💨",
    "Hope you enjoy your ride! 🌟",
    "Bon voyage! 🌍✈️",
    "You're all set! 🚖😊"
]

if st.button('🎯 Get Fare Prediction'):
    with st.spinner('Fetching your fare prediction...'):
        # Geocode the pickup and dropoff addresses
        pickup_latitude, pickup_longitude = geocode_address(pickup_address)
        dropoff_latitude, dropoff_longitude = geocode_address(dropoff_address)

        if pickup_latitude is not None and dropoff_latitude is not None:
            # Create a dictionary containing the parameters for the API
            params = {
                "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "pickup_longitude": pickup_longitude,
                "pickup_latitude": pickup_latitude,
                "dropoff_longitude": dropoff_longitude,
                "dropoff_latitude": dropoff_latitude,
                "passenger_count": passenger_count
            }

            try:
                # Make the API request
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an exception for HTTP errors
                prediction = response.json()

                # Round up the fare price
                fare = prediction['fare']
                rounded_fare = math.ceil(fare)

                # Display the rounded fare to the user
                st.success(f"Predicted Fare: ${rounded_fare}")
                st.write(random.choice(fun_messages))

                # Create a DataFrame for the map
                map_data = pd.DataFrame({
                    'lat': [pickup_latitude, dropoff_latitude],
                    'lon': [pickup_longitude, dropoff_longitude]
                })

                # Display the map
                st.map(map_data)
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
            except ValueError:
                st.error("Unexpected response format")
