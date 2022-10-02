import cv2
import numpy as np
import time
import serial
import os
from PIL import Image
# 콘솔창에 Enter Username 이라는 문구가 뜰때까지 로딩중임 (1분소요)
# 이름을 입력하면 3초뒤 촬영이 시작되고 사진이 로컬 폴더 face_list에 저장된다.
timeStamp = time.time()
tm = time.localtime(timeStamp)
timeString = time.strftime('%Y-%m-%d-%H%M%S') #현재 시각을 저장한 스트링 변수
#arduino = serial.Serial(port = "COM3", baudrate = 9600)
#time.sleep(3)

test_camera01 = cv2.VideoCapture(0)
test_camera01.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
test_camera01.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
data = 1 #data값이 1이면 3초뒤 5장 캡처

while cv2.waitKey(0) < 0:

    while data != 1:
        #data = arduino.read_all()
        camStat, camImg = test_camera01.read()
        cv2.imshow("TEST_Camera Out", camImg)
        cv2.waitKey(200)
        print(data)


    #data -= 1
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
    cv2.waitKey(2000)
    #break
    
test_camera01.release()
cv2.destroyAllWindows()

