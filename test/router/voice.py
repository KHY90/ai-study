from fastapi import APIRouter, UploadFile, File, HTTPException
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import moviepy.editor as mp
import io

# 라우터 객체 생성
router = APIRouter()

# Whisper 모델 및 프로세서 로드
model_name = "openai/whisper-large-v3-turbo"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # 업로드된 파일을 읽음
    audio_input = await file.read()
    
    try:
        # 파일의 확장자를 확인
        if file.filename.endswith('.mp4'):
            # 비디오 파일을 직접 처리
            video_bytes = io.BytesIO(audio_input)
            with mp.VideoFileClip(video_bytes) as audio_clip:
                # 오디오를 WAV 형식으로 메모리에 저장
                audio_buffer = io.BytesIO()
                audio_clip.audio.write_audiofile(audio_buffer, codec='pcm_s16le')
                audio_buffer.seek(0)  # 버퍼의 시작으로 이동

            # WAV 오디오 파일을 읽기
            audio_input = audio_buffer.read()

        # Whisper 모델을 사용하여 텍스트로 변환
        inputs = processor(audio_input, return_tensors="pt", sampling_rate=16000)
        with torch.no_grad():
            logits = model.generate(**inputs)

        # 생성된 텍스트를 디코드
        transcription = processor.batch_decode(logits, skip_special_tokens=True)[0]

        return {"transcription": transcription}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
