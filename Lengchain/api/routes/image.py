from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_image():
    return {"message": "Image API"}