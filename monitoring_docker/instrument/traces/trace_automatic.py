# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from io import BytesIO

import joblib
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from loguru import logger
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from pydantic import BaseModel

set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "diabetes-prediction-service"})
    )
)
tracer = get_tracer_provider().get_tracer("diabetes-prediction", "1.0.0")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)


# Class to define the request body
class Diabetes_measures(BaseModel):
    Pregnancies: int = 6  # Number of times pregnant
    Glucose: int = (
        148  # Plasma glucose concentration a 2 hours in an oral glucose tolerance test
    )
    BloodPressure: int = 72  # Diastolic blood pressure (mm Hg)
    SkinThickness: int = 35  # Triceps skin fold thickness (mm)
    Insulin: int = 0  # 2-Hour serum insulin
    BMI: float = 33.6  # Body mass index
    DiabetesPedigreeFunction: float = 0.627  # Diabetes pedigree function
    Age: int = 50  # Age (years)


# Load model
model = joblib.load("./models/model.pkl")

# Initialize instance
app = FastAPI()


# Create an endpoint to check api work or not
@app.get("/")
def check_health():
    return {"status": "Oke"}


# Create an endpoint to make prediction
@app.post("/predict")
def predict(data: Diabetes_measures):
    logger.info("Making predictions...")
    logger.info(data)
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
    result = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]

    return {"result": ["Normal", "Diabetes"][result]}


if __name__ == "__main__":
    FastAPIInstrumentor.instrument_app(app)
    uvicorn.run(app, host="0.0.0.0", port=8089)
