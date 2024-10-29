from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from transformers import pipeline
from PIL import Image
import io
import numpy as np

router = APIRouter()

# 이미지 분류 모델 로드
emotion_recognition = pipeline("image-classification", model="microsoft/resnet-50")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 클라이언트로부터 바이너리 데이터 수신
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            image = Image.open(io.BytesIO(nparr))

            # 감정 예측
            results = emotion_recognition(image)

            # 결과 반환
            await websocket.send_json({"results": results})
    except Exception as e:
        print("Error:", e)
    finally:
        await websocket.close()
