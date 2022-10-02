import cv2
import numpy as np
import time
import serial
import os
from PIL import Image


timeStamp = time.time()
tm = time.localtime(timeStamp)
timeString = time.strftime('%Y-%m-%d-%H%M%S')
#arduino = serial.Serial(port = "COM3", baudrate = 9600)
#time.sleep(3)

test_camera01 = cv2.VideoCapture(0)
test_camera01.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
test_camera01.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
data = 1 #data값이 1이면 3초뒤 캡처되고 얼굴비교 실행

while cv2.waitKey(0) < 0:

    while data != 1:
        #data = arduino.read_all()
        camStat, camImg = test_camera01.read()
        cv2.imshow("TEST_Camera Out", camImg)
        cv2.waitKey(200)
        print(data)


    #data -= 1
   

    c = 0

    while c < 15:
        camStat, camImg = test_camera01.read()
        cv2.imshow("TEST_Camera Out", camImg)
        cv2.waitKey(200)
        c += 1
    #camStat, camImg = test_camera01.read()
    #cv2.imwrite(f"./test_list/cap{timeString}.png",camImg)
    # 보안상 이슈로 카메라에 다가온 방문자의 얼굴을 저장하는 기능은 주석처리함
    c = 0


    labels = os.listdir("./face_list") #라벨 지정
 
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("lbfmodel.yml") #저장된 값 가져오기
    
    camStat, camImg = test_camera01.read()
    gray  = cv2.cvtColor(camImg, cv2.COLOR_BGR2GRAY) #흑백으로 변환
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3) #얼굴 인식
   

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w] #얼굴 부분만 가져오기
 
        id_, conf = recognizer.predict(roi_gray) #얼마나 유사한지 확인
           
        print(labels[id_], (200 - conf ) / 2)
        confPer = int((200 - conf ) / 2)
        if(confPer > 70):
            font = cv2.FONT_HERSHEY_SIMPLEX #폰트 지정
            name = labels[id_] #ID를 이용하여 이름 가져오기
            cv2.putText(camImg, name + " " + str(confPer) + "%", (x,y-5), font, 1, (255,255,0), 2)
            cv2.rectangle(camImg,(x,y),(x+w,y+h),(0,255,0),2)
        if (confPer <= 70):
            font = cv2.FONT_HERSHEY_SIMPLEX #폰트 지정
            name = labels[id_] #ID를 이용하여 이름 가져오기
            cv2.putText(camImg, "Unknown", (x,y-5), font, 1, (0,0,255), 2)
            cv2.rectangle(camImg,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imshow('Preview',camImg) #이미지 보여주기
    cv2.waitKey(5000)
         

    cv2.destroyAllWindows()

    #break
    
test_camera01.release()
cv2.destroyAllWindows()

