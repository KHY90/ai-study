# from fastapi import FastAPI, File, UploadFile
# import easyocr
# import cv2
# import mediapipe as mp
# import numpy as np

# reader = easyocr.Reader(['en','ko'])

# app = FastAPI()

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):

#     contents = await file.read()

#     rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.imdecode(np.fromstring(contents, dtype = np.uint8), cv2.IMREAD_COLOR))

#     result = reader.readtext(rgb_frame)

#     print(result)

#     return {"filename": result}

from fastapi import FastAPI, File, UploadFile
import easyocr
import cv2
import numpy as np

reader = easyocr.Reader(['en', 'ko'])

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    # 이미지 디코딩
    nparr = np.frombuffer(contents, dtype=np.uint8)
    rgb_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if rgb_frame is None:
        return {"error": "Could not decode image."}

    # EasyOCR로 텍스트 추출
    results = reader.readtext(rgb_frame)

    # 결과를 JSON으로 변환 가능한 형식으로 가공
    extracted_texts = [{"text": result[1], "confidence": result[2]} for result in results]

    return {"filename": extracted_texts}
