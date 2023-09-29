# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from io import BytesIO

import easyocr
import numpy as np
from fastapi import FastAPI, File, UploadFile
from loguru import logger
from PIL import Image

app = FastAPI()

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    reader = easyocr.Reader(
        ["vi", "en"],
        gpu=True,
        detect_network="craft",
        model_storage_directory="./model_storage/model",
        download_enabled=False,
    )

    # Read image from route
    request_object_content = await file.read()
    pil_image = Image.open(BytesIO(request_object_content))

    logger.info("Read image successfully!")

    # Get the detection from EasyOCR
    detection = reader.readtext(pil_image)
    logger.info("Make predictions successfully!")

    # Create the final result
    result = {"bboxes": [], "texts": [], "probs": []}
    for bbox, text, prob in detection:
        # Convert a list of NumPy int elements to premitive numbers
        bbox = np.array(bbox).tolist()
        result["bboxes"].append(bbox)
        result["texts"].append(text)
        result["probs"].append(prob)
    logger.info("Parse results from predictions successfully!")

    return result