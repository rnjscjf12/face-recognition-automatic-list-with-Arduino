import cv2
import numpy as np
import os
from PIL import Image

labels = os.listdir("./face_list")
#labels = ["Cheol", "JiEun", "JunHyong"] #라벨 지정
 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("lbfmodel.yml") #저장된 값 가져오기
 
image_list = [] 

test_images = os.path.join(os.getcwd(), "test_list") #이미지를 가져올 폴더 지정

for root, dirs, files in os.walk(test_images) : #파일 목록 가져오기
    for file in files :
        if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png") or file.endswith("PNG") : #이미지 파일 필터링
            image_path = os.path.join(test_images, file)
            print(image_path)
            image_list.append(cv2.imread(image_path))
2
for img in image_list : #가져온 이미지들에 대해 진행
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #흑백으로 변환
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3) #얼굴 인식
   

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w] #얼굴 부분만 가져오기
 
        id_, conf = recognizer.predict(roi_gray) #얼마나 유사한지 확인
           
        print(labels[id_], (200 - conf ) / 2)
        if((200 - conf ) / 2 >= 50):
            font = cv2.FONT_HERSHEY_SIMPLEX #폰트 지정
            name = labels[id_] #ID를 이용하여 이름 가져오기
            cv2.putText(img, name, (x,y-5), font, 1, (0,0,255), 2)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('Preview',img) #이미지 보여주기
    if cv2.waitKey() >= 0:
        continue

cv2.destroyAllWindows()
