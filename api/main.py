from fastapi import FastAPI
from pydantic import BaseModel
from imageProcessing import detect_face

app = FastAPI()

class Image(BaseModel):
    image64: str

@app.post("/detect_face")
async def Get_face(image: Image):
    return Image(image64=detect_face(image.image64))
