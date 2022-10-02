import cv2
import numpy as np
import time
import serial
import os
import pymysql
from PIL import Image

#space : retry
#m : match mode
#ESC : quit

conn = None
cur = None

dateDB = ""
nameDB = ""
temperateDB = ""

sql = ""

conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="capstonedesign", charset="utf8")  # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

Face_ID = -1 
pev_person_name = ""
y_ID = []
x_train = []

Face_Images = os.path.join(os.getcwd(), "face_list") #이미지 폴더 지정
print (Face_Images)

for root, dirs, files in os.walk(Face_Images) : #파일 목록 가져오기
    for file in files :
        if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png") or file.endswith("PNG") : #이미지 파일 필터링
            path = os.path.join(root, file)
            person_name = os.path.basename(root)
            print(path, person_name)
            if pev_person_name != person_name : #이름이 바뀌었는지 확인
                Face_ID=Face_ID+1
                pev_person_name = person_name
            
            img = cv2.imread(path) #이미지 파일 가져오기
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_image, 1.3, 3) #얼굴 찾기
            print (Face_ID, faces)
            
            for (x,y,w,h) in faces:
                roi = gray_image[y:y+h, x:x+w] #얼굴부분만 가져오기
                x_train.append(roi)
                y_ID.append(Face_ID)

                recognizer.train(x_train, np.array(y_ID)) #matrix 만들기
                recognizer.save("lbfmodel.yml") #저장하기




arduino = serial.Serial(port = "COM5", baudrate = 9600)
time.sleep(3)

test_camera01 = cv2.VideoCapture(0)
test_camera01.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
test_camera01.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
data = 0 #data값이 1이면 3초뒤 캡처되고 얼굴비교 실행
temper = 0
while True :
    while True: #매치 모드

        while temper == 0:
            camStat, camImg = test_camera01.read()
            cv2.imshow("Match", camImg)
            print(data, temper)
            data = int(arduino.readline())
            if(data > 29):
                temper = float(data) / 100
                print(data, temper)
            #camStat, camImg = test_camera01.read()
            #cv2.imshow("Camera Out", camImg)
            cv2.waitKey(200)
            


        data = 0
        

        c = 0

        while c < 15:
            camStat, camImg = test_camera01.read()
            cv2.imshow("Match", camImg)
            cv2.waitKey(200)
            c += 1
           
        #camStat, camImg = test_camera01.read()
        #cv2.imwrite(f"./test_list/cap{timeString}.png",camImg)
        # 보안상 이슈로 방문자의 얼굴 저장 기능은 주석처리
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

                timeStamp = time.time()
                tm = time.localtime(timeStamp)
                timeString = time.strftime('%Y-%m-%d %H:%M:%S')

                dateDB = timeString
                nameDB = name
                temperateDB = str(temper)
                

                sql = "INSERT INTO 명부 VALUES('"+dateDB+"','"+nameDB+"', '"+temperateDB+"' )"
                cur.execute(sql)
                conn.commit()
                
                cv2.putText(camImg, name + " " + str(confPer) + "%", (x,y-5), font, 1, (255,255,0), 2)
                cv2.rectangle(camImg,(x,y),(x+w,y+h),(0,255,0),2)
            if (confPer <= 70):
                font = cv2.FONT_HERSHEY_SIMPLEX #폰트 지정
                name = labels[id_] #ID를 이용하여 이름 가져오기
                cv2.putText(camImg, "Unknown", (x,y-5), font, 1, (0,0,255), 2)
                cv2.rectangle(camImg,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow('Match Result',camImg) #이미지 보여주기
         
             

        keyInput = -1
        keyInput = cv2.waitKey(5000)
        cv2.destroyWindow("Match Result")
        temper = 0
        data = 0
        cv2.destroyAllWindows()
        
        if keyInput == 32:
            keyInput = -1
            cv2.destroyAllWindows()

        if keyInput == 109 or keyInput == 27:
            cv2.destroyAllWindows()
            break
        
    
    

    while keyInput != 27: #등록 모드
        
        #while True:
            

            #data = arduino.read_all()
            #camStat, camImg = test_camera01.read()
            #cv2.imshow("TEST_Camera Out", camImg)
            #cv2.waitKey(200)
            #print(data)


        #data == 1
        print("Enter Username" )
        username = input()
        while os.path.exists(f"./face_list/{username}"):
            print("Already Exists, Try Another. " )
            username = input()
        
        os.makedirs(f"./face_list/{username}")
        c = 0

        while c < 15:
            camStat, camImg = test_camera01.read()
            cv2.imshow("TEST_Camera Out", camImg)
            cv2.waitKey(200)
            c += 1
        c = 0
       
        while c < 5:
            camStat, camImg = test_camera01.read()
            cv2.imwrite(f"./face_list/{username}/{c+1}.png",camImg)
            cv2.waitKey(300)
            c += 1
        username = ''
        cv2.destroyAllWindows()
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create() #LBPH를 사용할 새 변수 생성

        Face_ID = -1 
        pev_person_name = ""
        y_ID = []
        x_train = []

        Face_Images = os.path.join(os.getcwd(), "face_list") #이미지 폴더 지정
        print (Face_Images)

        for root, dirs, files in os.walk(Face_Images) : #파일 목록 가져오기
            for file in files :
                if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png") or file.endswith("PNG") : #이미지 파일 필터링
                    path = os.path.join(root, file)
                    person_name = os.path.basename(root)
                    print(path, person_name)
                    if pev_person_name != person_name : #이름이 바뀌었는지 확인
                        Face_ID=Face_ID+1
                        pev_person_name = person_name
                
                    img = cv2.imread(path) #이미지 파일 가져오기
                    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray_image, 1.3, 3) #얼굴 찾기
                    print (Face_ID, faces)
                
                    for (x,y,w,h) in faces:
                        roi = gray_image[y:y+h, x:x+w] #얼굴부분만 가져오기
                        x_train.append(roi)
                        y_ID.append(Face_ID)

                        recognizer.train(x_train, np.array(y_ID)) #matrix 만들기
                        recognizer.save("lbfmodel.yml") #저장하기

                        

        labels = os.listdir("./face_list") #라벨 지정
     
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("lbfmodel.yml") #저장된 값 가져오기
        
        
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
        cv2.imshow('Match Result',camImg) #이미지 보여주기

        print("space : retry\nm : match mode\nESC : quit\n")
        keyInput = -1
        keyInput = cv2.waitKey(10000)
        
        if keyInput == 109:
            keyInput = -1
            cv2.destroyAllWindows()
            break

        cv2.destroyAllWindows()

        
    if keyInput == 27:
        break
test_camera01.release()
cv2.destroyAllWindows()
conn.close()
