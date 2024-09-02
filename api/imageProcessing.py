import cv2 as cv
import base64
from fastapi import HTTPException
import numpy as np

face_cascade = cv.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

def detect_face(image: str):
    try:
        #remove this part data:image/png;base64,
        image = image.replace('data:image/jpg;base64,', '')
        image = image.replace('data:image/png;base64,', '')
        image = image.replace('data:image/jpeg;base64,', '')

        print(image[:30])
        img = base64_to_image(image)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # cv.imshow('image', img)
        faces = face_cascade.detectMultiScale(gray_img,scaleFactor=1.1, minNeighbors=5)
        face_images = []
        for (x, y, w, h) in faces:
            face = gray_img[y:y+h, x:x+w]
            face_resized = cv.resize(face, (48, 48))
            face_base64 = encode_image_to_base64(face_resized)
            face_images.append(face_base64)
        if len(face_images) == 0:
            return "No face detected"
        print(len(face_images[0]))
        return face_images[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail= 'error  :'+str(e))


def encode_image_to_base64(image):
    _, buffer = cv.imencode('.jpg', image)
    image64 = base64.b64encode(buffer).decode('utf-8')
    return image64

def base64_to_image(base64_str):
    img_data = base64.b64decode(base64_str)
    np_img = np.frombuffer(img_data, np.uint8)
    img = cv.imdecode(np_img, cv.IMREAD_COLOR)
    return img