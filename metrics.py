# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from io import BytesIO
from time import time
from pydantic import BaseModel

import joblib
import uvicorn
import pandas as pd
import numpy as np
from loguru import logger
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server

# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")

# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "diabetes-prediction-service"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("diabetes-prediction", "1.0.0")

# Create your first counter
counter = meter.create_counter(
    name="Service_request_counter",
    description="Number of service requests"
)

histogram = meter.create_histogram(
    name="Service_response_histogram",
    description="Service response histogram",
    unit="seconds",
)

# Class to define the request body
class Diabetes_measures(BaseModel):
    Pregnancies: int = 6 # Number of times pregnant
    Glucose: int = 148 # Plasma glucose concentration a 2 hours in an oral glucose tolerance test
    BloodPressure: int = 72 # Diastolic blood pressure (mm Hg)
    SkinThickness: int = 35 # Triceps skin fold thickness (mm)
    Insulin: int = 0 # 2-Hour serum insulin
    BMI: float = 33.6 # Body mass index 
    DiabetesPedigreeFunction: float = 0.627 # Diabetes pedigree function
    Age: int = 50 # Age (years)

# Load model
model = joblib.load("./models/model.pkl")

app = FastAPI()

# Create an endpoint to check api work or not
@app.get("/")
def check_health():
    return {"status": "Oke"}

# Create an endpoint to make prediction
@app.post("/predict_cache")
def predict(data: Diabetes_measures):
    # starting time
    starting_time = time()

    logger.info("Making predictions...")
    logger.info(data)
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
    result = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]

    # Labels for all metrics
    label = {"api": "/predict"}

    # Increase the counter
    counter.add(1, label)

    # Mark the end of the response
    ending_time = time()
    elapsed_time = ending_time - starting_time

    # Add histogram
    logger.info("elapsed time: ", elapsed_time)
    logger.info(elapsed_time)
    histogram.record(elapsed_time, label)

    return {"result": ["Normal", "Diabetes"][result]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4001)
