from time import sleep

import requests
from loguru import logger

json_data = {
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50,
}


def predict():
    logger.info("Sending POST requests!")
    response = requests.post(
        "http://localhost:8098/predict",
        headers={
            "accept": "application/json",
        },
        json=json_data,
    )


if __name__ == "__main__":
    while True:
        predict()
        sleep(1)
