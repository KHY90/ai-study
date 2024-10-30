from fastapi import FastAPI, APIRouter
import uvicorn

# router 폴더 내 router 객체를 module1_router란 이름으로 alias하여 가져옴
from router.face2 import router as faceEmotion_route
from router.textseti import router as textEmotion_route

app = FastAPI()

# router를 app에 등록
app.include_router(faceEmotion_route)

@app.get("/")
def index():
    return {"message": "마음:봄"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)