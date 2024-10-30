from fastapi import APIRouter, UploadFile, File, HTTPException
import torch
import numpy as np
import io
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pydub import AudioSegment

router = APIRouter()

AudioSegment.converter = "C:\새 폴더\\ffmpeg-master-latest-win64-gpl-shared\\bin"  # FFmpeg 경로 설정

# 모델과 프로세서 로드
model_name = "Talha/urdu-audio-emotions"
try:
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
except Exception as e:
    print(f"Error loading model: {e}")


@router.post("/speech-emotion/")
async def analyze_emotion(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Pydub로 파일 읽기 (MP4, Opus 포함 가능)
        audio_segment = AudioSegment.from_file(io.BytesIO(contents))

        # WAV 형식으로 변환하고 numpy 배열로 변환
        audio_input = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
        audio_input = audio_input / np.max(np.abs(audio_input))  # 정규화
        audio_input = audio_input.reshape(-1, 1)  # (N, 1) 형식으로 변경

        input_values = processor(audio_input, sampling_rate=16000, return_tensors="pt").input_values
        
        with torch.no_grad():
            logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_emotion = processor.batch_decode(predicted_ids)

        return {"emotion": predicted_emotion}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
