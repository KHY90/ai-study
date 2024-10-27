# STEP 1
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 2
base_options = python.BaseOptions(model_asset_path='models\efficientdet_lite0.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

import cv2
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    
    contents = await file.read()
    
    # STEP 3
    # binary = np.fromstring(contents, dtype = np.uint8)
    # cv_mat = cv2.imdecode(binary, cv2.IMREAD_COLOR)
    # cv_mat = cv2.imdecode(np.fromstring(contents, dtype = np.uint8), cv2.IMREAD_COLOR)
    # rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_mat)
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.imdecode(np.fromstring(contents, dtype = np.uint8), cv2.IMREAD_COLOR))

    # STEP 4
    detection_result = detector.detect(rgb_frame)
   
    # STEP 5
    person_count = 0
    for detection in detection_result.detections:
        category = detection.categories[0]
        if category.category_name == 'person':
            person_count += 1
   
    return {"result" : person_count }
