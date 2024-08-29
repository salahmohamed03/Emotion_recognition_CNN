import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import imageProcessing as ip
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Image(BaseModel):
    image64: str

@app.post("/detectFace64")
async def Get_face_base64(image: Image):
    return Image(image64=ip.detect_face(image.image64))

@app.post("/detectFaceJpg")
async def Get_face_file(file: UploadFile = File(...)):
    contents = await file.read()
    image64 = base64.b64encode(contents).decode('utf-8')
    return Image(image64=ip.detect_face(image64))

