# from fastapi import APIRouter, File, UploadFile
# from fastapi.responses import JSONResponse
# from transformers import pipeline
# from PIL import Image
# import io

# router = APIRouter()

# # 모델 로드
# emotion_recognition = pipeline("image-classification", model="ElenaRyumina/face_emotion_recognition")

# @router.post("/face")
# async def face(file: UploadFile = File(...)):

#     # 이미지 파일 읽기
#     image = Image.open(io.BytesIO(await file.read()))

#     # 감정 예측
#     results = emotion_recognition(image)

#     # 결과 반환
#     return JSONResponse(content={"results": results})

# from fastapi import APIRouter, File, UploadFile
# from fastapi.responses import JSONResponse
# from transformers import pipeline
# from PIL import Image
# import io

# router = APIRouter()

# # 대체 모델 로드
# emotion_recognition = pipeline("image-classification", model="microsoft/resnet-50")

# @router.post("/face")
# async def face(file: UploadFile = File(...)):
#     image = Image.open(io.BytesIO(await file.read()))
#     results = emotion_recognition(image)
#     return JSONResponse(content={"results": results})

from fastapi import APIRouter, File, UploadFile, WebSocket
from fastapi.responses import JSONResponse
from transformers import pipeline
from PIL import Image
import io
import cv2
import numpy as np

router = APIRouter()

# 대체 모델 로드
emotion_recognition = pipeline("image-classification", model="microsoft/resnet-50")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 이미지 분석
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            results = emotion_recognition(pil_image)

            # 결과 전송
            await websocket.send_json({"results": results})
        except Exception as e:
            print("Error:", e)
            break
    await websocket.close()
