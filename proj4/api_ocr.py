import easyocr
from fastapi import FastAPI, File, UploadFile
import mediapipe as mp
import cv2
import numpy as np

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    contents = await file.read()

    binary = np.fromstring(contents, dtype=np.uint8)
    
    img = cv2.imdecode(binary, cv2.IMREAD_COLOR)

    reader = easyocr.Reader(['ch_sim','en'])
    result = reader.readtext()
    
    cv_mat = cv2.imdecode(binary, cv2.IMREAD_COLOR)
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_mat)
    


    return {"result" : ocr_result }
