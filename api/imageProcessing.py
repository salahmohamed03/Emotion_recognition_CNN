import cv2 as cv
import base64
from fastapi import HTTPException
import numpy as np

face_cascade = cv.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

def detect_face(image: str):
    try:
        img_data = base64.b64decode(image.image)
        np_img = np.frombuffer(img_data, np.uint8)
        img = cv.imdecode(np_img, cv.IMREAD_COLOR)

        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        

        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        face_images = []
        for (x, y, w, h) in faces:
            face = img[y:y+h, x:x+w]
            face_base64 = encode_image_to_base64(face)
            face_images.append(face_base64)
        

        return face_images[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def encode_image_to_base64(image: np.ndarray) -> str:
    _, buffer = cv.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')
