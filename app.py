import streamlit as st
import requests
from datetime import datetime
import pandas as pd

'''
# TaxiFareModel front
'''

# Input fields for user to provide ride parameters
date = st.date_input("Date", datetime.now())
time = st.time_input("Time", datetime.now().time())
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=10, value=1)

# Combine date and time into a single datetime object
pickup_datetime = datetime.combine(date, time)

# Define the URL for the API
url = 'https://taxifare.lewagon.ai/predict'

if st.button('Get Fare Prediction'):
    # Create a dictionary containing the parameters for the API
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    # Make the API request
    response = requests.get(url, params=params)
    prediction = response.json()

    # Display the prediction to the user
    st.write(f"Predicted Fare: ${prediction['fare']}")

    # Create a DataFrame for the map
    map_data = pd.DataFrame({
        'lat': [pickup_latitude, dropoff_latitude],
        'lon': [pickup_longitude, dropoff_longitude]
    })

    # Display the map
    st.map(map_data)

