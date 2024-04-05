import streamlit as st
import os
import pandas as pd
import json
import requests

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the input JSON data
input_data = {
    "total_area_sqm": 100,
    "surface_land_sqm": 120,
    "nbr_frontages": 2,
    "nbr_bedrooms": 3,
    "terrace_sqm": 20,
    "garden_sqm": 50,
    "primary_energy_consumption_sqm": 200,
    "fl_furnished": True,
    "fl_open_fire": False,
    "fl_terrace": True,
    "fl_garden": True,
    "fl_swimming_pool": False,
    "fl_floodzone": False,
    "fl_double_glazing": True,
    "subproperty_type": "apartment",
    "region": "Brussels",
    "province": "Brussels",
    "locality": "Ixelles",
    "equipped_kitchen": "standard",
    "state_building": "good",
    "epc": "D",
    "heating_type": "gas",
    "zip_code": "1000",
    "latitude": 50.8503,
    "longitude": 4.3517
}

# Streamlit app title
st.title("House Price Prediction")

# Display input fields for user input
total_area_sqm = st.number_input("Total Area (sqm)", value=input_data["total_area_sqm"])
surface_land_sqm = st.number_input("Surface Land (sqm)", value=input_data["surface_land_sqm"])
nbr_frontages = st.number_input("Number of Frontages", value=input_data["nbr_frontages"])
nbr_bedrooms = st.number_input("Number of Bedrooms", value=input_data["nbr_bedrooms"])
terrace_sqm = st.number_input("Terrace Area (sqm)", value=input_data["terrace_sqm"])
garden_sqm = st.number_input("Garden Area (sqm)", value=input_data["garden_sqm"])
primary_energy_consumption_sqm = st.number_input("Primary Energy Consumption (sqm)", value=input_data["primary_energy_consumption_sqm"])
fl_furnished = st.checkbox("Furnished", value=input_data["fl_furnished"])
fl_open_fire = st.checkbox("Open Fire", value=input_data["fl_open_fire"])
fl_terrace = st.checkbox("Terrace", value=input_data["fl_terrace"])
fl_garden = st.checkbox("Garden", value=input_data["fl_garden"])
fl_swimming_pool = st.checkbox("Swimming Pool", value=input_data["fl_swimming_pool"])
fl_floodzone = st.checkbox("Flood Zone", value=input_data["fl_floodzone"])
fl_double_glazing = st.checkbox("Double Glazing", value=input_data["fl_double_glazing"])
subproperty_type = st.selectbox("Subproperty Type", ["apartment", "house"])
region = st.text_input("Region", value=input_data["region"])
province = st.text_input("Province", value=input_data["province"])
locality = st.text_input("Locality", value=input_data["locality"])
equipped_kitchen = st.selectbox("Equipped Kitchen", ["standard", "luxury"])
state_building = st.selectbox("Building State", ["good", "average", "bad"])
epc = st.text_input("EPC", value=input_data["epc"])
heating_type = st.text_input("Heating Type", value=input_data["heating_type"])
zip_code = st.text_input("Zip Code", value=input_data["zip_code"])
latitude = st.number_input("Latitude", value=input_data["latitude"])
longitude = st.number_input("Longitude", value=input_data["longitude"])

# Define a function to make a request to the FastAPI endpoint for prediction
def make_prediction():
    # Define the URL of the FastAPI endpoint
    url = "http://localhost:8002/predict/"
    
    # Prepare the input data as a dictionary
    input_data = {
        "total_area_sqm": total_area_sqm,
        "surface_land_sqm": surface_land_sqm,
        "nbr_frontages": nbr_frontages,
        "nbr_bedrooms": nbr_bedrooms,
        "terrace_sqm": terrace_sqm,
        "garden_sqm": garden_sqm,
        "primary_energy_consumption_sqm": primary_energy_consumption_sqm,
        "fl_furnished": fl_furnished,
        "fl_open_fire": fl_open_fire,
        "fl_terrace": fl_terrace,
        "fl_garden": fl_garden,
        "fl_swimming_pool": fl_swimming_pool,
        "fl_floodzone": fl_floodzone,
        "fl_double_glazing": fl_double_glazing,
        "subproperty_type": subproperty_type,
        "region": region,
        "province": province,
        "locality": locality,
        "equipped_kitchen": equipped_kitchen,
        "state_building": state_building,
        "epc": epc,
        "heating_type": heating_type,
        "zip_code": zip_code,
        "latitude": latitude,
        "longitude": longitude
    }
    
    # Send a POST request to the FastAPI endpoint with the input data
    response = requests.post(url, json=input_data)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        prediction = response.json()["predicted_price"]
        
        # Display the prediction
        st.success(f"Predicted Price: {prediction}")
    else:
        # Display an error message if the request failed
        st.error("Failed to make prediction. Please try again later.")

# Add a button to trigger the prediction
if st.button("Predict"):
    make_prediction()
