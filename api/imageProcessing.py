import cv2 as cv
import base64
from fastapi import HTTPException
import numpy as np
from keras.models import load_model
from pydantic import BaseModel
face_cascade = cv.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
import sys
sys.stdout.reconfigure(encoding='utf-8')
model=load_model('assets/model_file_30epochs.h5')
labels_dict={0:'Angry',1:'Disgust', 2:'Fear', 3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}

class FaceImage(BaseModel):
    image64: str
    emotion: str
    position: str

def detect_face(image: str,emotion: str):
    try:
        #remove this part data:image/png;base64,
        image = image.replace('data:image/jpg;base64,', '')
        image = image.replace('data:image/png;base64,', '')
        image = image.replace('data:image/jpeg;base64,', '')
        img = base64_to_image(image)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_img,1.3,3)
        face_images = []
        for (x, y, w, h) in faces:
            face = draw_rect_with_text(img, x, y, w, h, emotion)
            face64 = encode_image_to_base64(face)
            res = FaceImage(image64=face64, emotion=emotion, position=f'{x},{y},{w},{h}')
            face_images.append(res)
            
        if len(face_images) == 0:
            return "No face detected"
        return face_images[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail= 'error  :'+str(e))

def detect_face_preprocess(image: str):
    try:
        #remove this part data:image/png;base64,
        image = image.replace('data:image/jpg;base64,', '')
        image = image.replace('data:image/png;base64,', '')
        image = image.replace('data:image/jpeg;base64,', '')

        img = base64_to_image(image)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # cv.imshow('image', img)
        # faces= faceDetect.detectMultiScale(gray, 1.3, 3)
        faces = face_cascade.detectMultiScale(gray_img,1.3,3)
        face_images = []
        for (x, y, w, h) in faces:
            face = gray_img[y:y+h, x:x+w]
            face_resized = cv.resize(face, (48, 48))
            normalize=face_resized/255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            face_images.append(reshaped)
        if len(face_images) == 0:
            return "No face detected"
       
        return face_images[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail= 'error  :'+str(e))

def draw_rect_with_text(image, x, y, w, h, text):
    cv.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 1)
    cv.rectangle(image,(x,y),(x+w,y+h),(50,50,255),2)
    cv.rectangle(image,(x,y-40),(x+w,y),(50,50,255),-1)
    cv.putText(image, text, (x, y-10),cv.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    # ##
    # cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # cv.putText(image, text, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    return image

def encode_image_to_base64(image):
    _, buffer = cv.imencode('.jpg', image)
    image64 = base64.b64encode(buffer).decode('utf-8')
    return image64

def base64_to_image(base64_str):
    img_data = base64.b64decode(base64_str)
    np_img = np.frombuffer(img_data, np.uint8)
    img = cv.imdecode(np_img, cv.IMREAD_COLOR)
    return img

def predict_image(image):
    result = model.predict(image)
    label = np.argmax(result, axis=1)[0]
    return labels_dict[label]
print(model.summary())