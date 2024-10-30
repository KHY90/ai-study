# router/textseti.py
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

router = APIRouter()

# 모델과 토크나이저 초기화
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 입력 데이터 모델 정의
class TextInput(BaseModel):
    text: str

# 감정 분석 API 엔드포인트
@router.post("/analyze-sentiment/")
async def analyze_sentiment(input: TextInput):
    inputs = tokenizer(input.text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    sentiment = probabilities.argmax().item()

    # 감정 레이블 (0: 부정, 1: 중립, 2: 긍정)
    sentiment_labels = {0: "negative", 1: "neutral", 2: "positive"}
    return {"sentiment": sentiment_labels[sentiment], "probabilities": probabilities.numpy().tolist()}
