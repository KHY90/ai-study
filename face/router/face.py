from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import torch
from transformers import AutoModelForImageClassification, AutoTokenizer
from PIL import Image
import io

router = APIRouter()

# 모델과 토크나이저 로드
model_name = "emotion_recognition_model"
try:
    model = AutoModelForImageClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
except Exception as e:
    print(f"Model loading failed: {e}")

@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # 이미지를 PIL 형식으로 변환
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # 이미지 전처리 및 모델 예측
    inputs = tokenizer(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1).detach().numpy()
    
    # 예측 결과를 JSON 형태로 반환
    return JSONResponse(content={"probabilities": probabilities.tolist()})
