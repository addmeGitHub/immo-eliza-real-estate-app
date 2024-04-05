# Use Linux as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the background.gif file into the Docker image
COPY api/background.gif /app/api/background.gif

# copy model to the container
COPY api/model.pkl /app/api/model.pkl

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose ports for FastAPI and Streamlit
EXPOSE 8002 8501

# Command to run the FastAPI server and Streamlit app when the container starts
CMD uvicorn main:app --host 0.0.0.0 --port 8002 & streamlit run app.py
