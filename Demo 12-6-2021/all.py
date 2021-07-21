import cv2
import threading
import numpy as np
import math
from datetime import datetime
import read_vie

import RPi.GPIO as GPIO
import time
#import board
#import pwmio
#from adafruit_motor import servo

from PIL import Image
import pytesseract
import re
import os
import apiServer

#Global variable

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.OUT) #GPIO23
GPIO.setup(24, GPIO.OUT) #GPIO24
GPIO.setup(25, GPIO.OUT) #GPIO25
GPIO.setup(16, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(6, GPIO.IN)

datas=[]


def onServo_1(state):
    if state == 1:
        GPIO.output(23, GPIO.HIGH)
    else:        
        GPIO.output(23, GPIO.LOW)
        
def onServo_2(state):
    if state == 1:
        GPIO.output(24, GPIO.HIGH)
    else:        
        GPIO.output(24, GPIO.LOW)
        
def onServo_Stop(state):    
    if state == 1:
        GPIO.output(25, GPIO.HIGH)
    else:        
        GPIO.output(25, GPIO.LOW)

def VatCan():    
    GPIO.setmode(GPIO.BCM)
    inp = GPIO.input(16)
    return inp

def Finished1():    
    GPIO.setmode(GPIO.BCM)
    inp = GPIO.input(26)
    return inp

def Finished2():    
    GPIO.setmode(GPIO.BCM)
    inp = GPIO.input(6)
    return inp



class api(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            if len(datas)>0:
                messenger=apiServer.send(datas[0])
                if messenger == "Insert data is success" or messenger == "something are invalid":
                    datas.pop(0)
                    
                
            

# =================== Camera =====================================
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)


# Xử lý ảnh
def camProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5, 5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=2)
    imgErode = cv2.erode(imgDialation, kernel, iterations=1)
    return imgErode


def getContours(imgThres, imgContour):
    biggest = np.array([])
    maxArea = 0
    countours, rank = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # countours, rank = cv2.findContours(imgThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in countours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    # cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 10)
    # cv2.drawContours(imgContour, biggest, -1, (0, 255, 0), 15)
    # if biggest.size != 0:
    #     drawRectangle(imgContour, biggest, 2)
    return biggest


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


def getWrap(img, biggest):
    biggest = reorder(biggest)
    #h, w, c = img.shape

    h1=int(math.sqrt((biggest[0][0][0]-biggest[1][0][0])**2 + (biggest[0][0][1]-biggest[1][0][1])**2))
    h2=int(math.sqrt((biggest[2][0][0]-biggest[3][0][0])**2 + (biggest[2][0][1]-biggest[3][0][1])**2))
    h=max([h1,h2])
    print("h")
    print(h)
    print("h1")
    print(h1)
    print("h2")
    print(h2)
    
    w1=int(math.sqrt((biggest[0][0][0]-biggest[3][0][0])**2 + (biggest[0][0][1]-biggest[3][0][1])**2))
    w2=int(math.sqrt((biggest[1][0][0]-biggest[2][0][0])**2 + (biggest[1][0][1]-biggest[2][0][1])**2))
    w=max([w1,w2])
    print("w")
    print(w)
    

    point1 = np.float32(biggest)
    point2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(point1, point2)
    imgOutput = cv2.warpPerspective(img, matrix, (w, h))
    # imgCrop = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCrop = cv2.resize(imgOutput, (w, h))
    return imgCrop

####################DrawReactangle############################

def drawRectangle(img, biggest, thickness):
    #[0][0][0], [0][0][1]  :A
    #[1][0][0], [1][0][1]  :D
    #[2][0][0], [2][0][1]  :C
    #[3][0][0], [3][0][1]  :B
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness) 
    cv2.line(img, (biggest[1][0][0], biggest[1][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness) 
    cv2.line(img, (biggest[2][0][0], biggest[2][0][1]), (biggest[3][0][0], biggest[3][0][1]), (0, 255, 0), thickness) 
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[0][0][0], biggest[0][0][1]), (0, 255, 0), thickness)
    # return img

################################################
def camPreview(previewName, camID):
    vatcan = 0
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        success, img = cam.read()
        imgThres = camProcessing(img)
        # biggest = getContours(imgThres, img)
    else:
        success = False

    while success:
        cv2.imshow(previewName, imgThres)
        success, img = cam.read() 
        # img = cv2.resize(img, (widthImg, heightImg))
#         imgContour = img.copy()
#         imgThres = camProcessing(imgContour)
#         biggest = getContours(imgThres, imgContour)

        cv2.imshow(previewName, img)
        key = cv2.waitKey(20)
#         print(1)
        #Phát hiện vật cản
   
        if VatCan() == 0:
            # Tăng chỉ số khi phát hiện vật cản lên 1 đơn vị
            vatcan += 1
#             print(2)

            # Lần đầu phát hiện vật cản thì tiến hành chụp ảnh
            if vatcan == 1:
#                 print(3)
                continue
            elif vatcan == 2:
#                 print(4)                
                timeRead = datetime.timestamp(datetime.now())
                while (timeRead > datetime.timestamp(datetime.now()) - 2):
                    success, img = cam.read()                    
                    cv2.imshow(previewName, img)
                    key = cv2.waitKey(20)
                cv2.imshow("Picture", img)       #show ảnh chưa qua xử lý
                # imgWraped = getWrap(img, biggest)       #imgWraped -> ảnh sau khi cắt
                cv2.imwrite("filename1.jpg", img) #lưu ảnh sau khi cắt
                
                #Đọc chữ trên ảnh đã lưu
                data=read_vie.khuVucHang()
                print(data)
                print(data["area"])
                if data["area"]=='hai chau' or data["area"]=='cam le' or data["area"]=='thanh khe' or data["area"]=='lien chieu':
                    datas.append(data)
                    print("if 1")
                    onServo_1(1)
                    onServo_Stop(0)
                    while True:
                        success, img = cam.read()                    
                        cv2.imshow(previewName, img)
                        key = cv2.waitKey(20)
                        if(Finished1()==0):
                            print("break")
                            onServo_1(0)
                            onServo_Stop(1)
                            break
                elif data["area"]=='ngu hanh son' or data["area"]=='son tra' or data["area"]=='hoa vang' or data["area"]=='hoang sa':
                    print("if 2")
                    datas.append(data)
                    onServo_2(1)
                    onServo_Stop(0)
                    while True:
                        success, img = cam.read()                    
                        cv2.imshow(previewName, img)
                        key = cv2.waitKey(20)
                        if(Finished1()==0):
                            print("break")
                            onServo_2(0)
                            onServo_Stop(1)
                            break
                else:
                    onServo_Stop(0)
                    while True:
                        success, img = cam.read()                    
                        cv2.imshow(previewName, img)
                        key = cv2.waitKey(20)
                        if (Finished2()==0):
                            onServo_Stop(1)
                    
                os.system('rm \'/home/pi/Desktop/PBL/Demo 12-6-2021/filename1.jpg\'')
                
                
#                 if Finished()==0:
#                     if data["area"]=='hai chau' or data["area"]=='cam le' or data["area"]=='thanh khe' or data["area"]=='lien chieu':
#                         onServo_1(0)
#                     elif data["area"]=='ngu hanh son' or data["area"]=='son tra' or data["area"]=='hoa vang' or data["area"]=='hoang sa':
#                         onServo_2(0)
#                     onServo_Stop(1)
                
            # Nếu không thì pass
            else : pass
        #Khi không phát hiện vật cản, đặt lại giá trị vatcan thành 0
        else: vatcan = 0

    cv2.destroyWindow(previewName)


############## RUN PROGRAM #####################
onServo_Stop(1)
onServo_1(0)
onServo_2(0)
thread1 = camThread("Camera", 0)
thread1.start()
thread2 = api()
thread2.start()



