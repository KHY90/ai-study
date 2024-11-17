from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai
from mangum import Mangum  # Lambda 서버
from prompt import get_system_prompt  # 분리된 프롬프트 불러오기

# .env 파일 로드
load_dotenv()

# 환경 변수 읽기
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI 앱 생성
app = FastAPI()

# 요청 형식을 정의
class ChatRequest(BaseModel):
    messages: list

@app.post("/chat/{role}")
async def chat(role: str, request: ChatRequest):
    try:
        # 역할에 따른 프롬프트 가져오기
        system_prompt = get_system_prompt(role)

        # 메시지 조합
        messages = [system_prompt] + request.messages

        # OpenAI API 호출
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = completion.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Lambda 핸들러
handler = Mangum(app)
