from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import logging
import os
import pickle
import pandas as pd
import json
import sys

# Define load_model function to load the trained machine learning model
def load_model(model_path):
    """
    Function to load the trained machine learning model.
    
    Args:
    model_path (str): Path to the saved model file.
    
    Returns:
    model: Loaded machine learning model.
    """
    with open(model_path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    return loaded_model

# Create FastAPI app
app = FastAPI(debug=True)

@app.get("/")
def root():
    return {"message": "Welcome to the House Price Prediction API!"}

# Define Pydantic model for input data
class HouseFeatures(BaseModel):
    total_area_sqm: float
    surface_land_sqm: float
    nbr_frontages: int
    nbr_bedrooms: int
    terrace_sqm: float
    garden_sqm: float
    primary_energy_consumption_sqm: float
    fl_furnished: bool
    fl_open_fire: bool
    fl_terrace: bool
    fl_garden: bool
    fl_swimming_pool: bool
    fl_floodzone: bool
    fl_double_glazing: bool
    subproperty_type: str
    region: str
    province: str
    locality: str
    equipped_kitchen: str
    state_building: str
    epc: str
    heating_type: str
    zip_code: str  # Add zip_code attribute
    latitude: float  # Add latitude attribute
    longitude: float  # Add longitude attribute

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Define the relative path to the saved model
model_path = os.path.join(current_dir, "api/model.pkl")
print("Model path:", model_path)  # Print the model path for verification

# Load the trained model
model = load_model(model_path)

# Define function to make predictions
def make_prediction(input_data, model):
    """
    Function to make predictions using a trained machine learning model.
    
    Args:
    input_data (pd.DataFrame): Input data for making predictions.
    model: Trained machine learning model.
    
    Returns:
    prediction (list): List of predictions.
    """
    try:    
        # Make predictions using the loaded model
        prediction = model.predict(input_data)
        
        return prediction.tolist()  # Convert predictions to a list
    except Exception as e:
        # Handle exceptions during prediction
        # You can log the error or raise it depending on your requirements
        raise RuntimeError(f"An error occurred during prediction: {str(e)}")

# Define API endpoint for making predictions
@app.post("/predict/")  # Define the /predict/ endpoint for POST requests
def predict_house_price(features: HouseFeatures):
    try:
        # Load the input data from inputdata.json
        input_data_path = os.path.join(current_dir, "input.json")
        with open(input_data_path, 'r') as json_file:
            input_data = json.load(json_file)

        # Prepare the input data for prediction
        input_data_df = pd.DataFrame([input_data])

        # Logging before prediction
        logging.info("Predicting house price...")

        # Make predictions using the loaded model
        prediction = make_prediction(input_data_df, model)

        # Logging after prediction
        logging.info("Prediction successful.")

        # Return the prediction
        return {"predicted_price": prediction[0]}
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred during prediction: {e}")

        # If an error occurs, return an HTTP 500 error
        raise HTTPException(status_code=500, detail=str(e))

# Define API endpoint for retrieving model path
@app.get("/model-path/")
def get_model_path():
    return {"model_path": model_path}

# Define endpoint for serving Swagger UI documentation page
@app.get("/docs", response_class=HTMLResponse)
async def get_documentation():
    with open("path/to/swagger.html", "r") as file:
        return file.read()

# Pydantic model for location data
class Location(BaseModel):
    latitude: float
    longitude: float

# Function to construct OpenMap URL
def construct_openmap_url(latitude: float, longitude: float) -> str:
    return f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"

# API endpoint to get OpenMap link
@app.post("/get-openmap-link/")
async def get_openmap_link(location: Location):
    if not (-90 <= location.latitude <= 90) or not (-180 <= location.longitude <= 180):
        raise HTTPException(status_code=400, detail="Invalid latitude or longitude values.")
    
    openmap_url = construct_openmap_url(location.latitude, location.longitude)
    return {"openmap_url": openmap_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
