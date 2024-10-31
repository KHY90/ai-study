# 설치 라이브러리
# pip install fastapi uvicorn torch transformers Pillow

from fastapi import APIRouter, File, UploadFile, HTTPException
import torch
from transformers import ViTForImageClassification, ViTFeatureExtractor
from PIL import Image
import io

router = APIRouter()

# 모델과 피처 추출기 로드
try:
    model = ViTForImageClassification.from_pretrained("motheecreator/vit-Facial-Expression-Recognition")
    feature_extractor = ViTFeatureExtractor.from_pretrained("motheecreator/vit-Facial-Expression-Recognition")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"모델 로드 실패: {str(e)}")


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # 이미지 파일 읽기
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
        
        # 이미지 전처리
        inputs = feature_extractor(images=image, return_tensors="pt")
        
        # 모델 예측
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = outputs.logits.argmax(-1).item()  # 최상위 클래스 인덱스
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy().flatten()  # 확률 계산

        # 감정 클래스 매핑
        emotions = [
            "화남",
            "역겨움",
            "두려움",
            "기쁨",
            "슬픔",
            "놀람",
            "아무생각없음"
        ]

        return {
            "predicted_class": predictions,
            "emotion": emotions[predictions],
            "probabilities": probabilities.tolist()  # 확률 반환
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
