from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.face import router as module1_router

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(module1_router)

@app.get("/")
def index():
    return {"message": "Hello World"}
