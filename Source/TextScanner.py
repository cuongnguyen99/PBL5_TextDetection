import cv2
import threading
import numpy as np
import math
import read_vie

import RPi.GPIO as GPIO
import time
import board
import pwmio
from adafruit_motor import servo

from PIL import Image
import pytesseract
import re

#Global variable
vatcan = 0

# =================== Servo and Cam bien =========================

def VatCan():
    #   GPIO.setmode(GPIO.BCM)
    inp = GPIO.input(26)
    #    GPIO.cleanup()
    return inp


def Servo_1():
    my_servo = servo.Servo(pwm1)
    my_servo.angle = 70
    time.sleep(0.5)
    my_servo.angle = 0
    time.sleep(2)
    my_servo.angle = 70


def Servo_2():
    my_servo = servo.Servo(pwm2)
    my_servo.angle = 70
    time.sleep(0.5)
    my_servo.angle = 0
    time.sleep(4)
    my_servo.angle = 70


def Servo_3():
    my_servo = servo.Servo(pwm3)
    my_servo.angle = 70
    time.sleep(0.5)
    my_servo.angle = 0
    time.sleep(13)
    my_servo.angle = 70


GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)  # Read output from PIR motion sensor

# =================== Read text ==================================

data = {"khu vực": "", "người nhận": "", "số điện thoại": "", "tiền thu hộ": "", "địa chỉ": "", "nội dung": ""}


def khuVucHang():
    #############################Version 2#########################
    img = cv2.imread("")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang="vie")

    ###########################################
    text = text.strip()

    # cv2.imshow("image",rgb)

    quan = ['hải châu', 'cẩm lệ', 'thanh khê', 'liên chiểu', 'ngũ hành sơn', 'sơn trà', 'hòa vang', 'hoàng sa']

    text = text.lower()
    text = text.replace("\n", " ")
    print(text)

    textSplit = text.split("người nhận:")
    if len(textSplit) > 1:
        for x in quan:
            if textSplit[1].find(x) != -1:
                if x == 'hải châu' or x == 'ngũ hành sơn' or x == 'sơn trà':
                    data["khu vực"] = x
                    break
                elif x == 'cẩm lệ' or x == 'thanh khê' or x == 'liên chiểu':
                    data["khu vực"] = x
                    break
                elif x == 'hòa vang' or x == 'hoàng sa':
                    data["khu vực"] = x
                    break

        txt = textSplit[1]
        nguoiNhan = 1
        diaChi = txt.find("địa chỉ")
        dienThoai = txt.find("điện thoại")
        noiDung = txt.find("nội dung")
        tienThuHo = txt.find("tiền thu hộ")
        trongLuong = txt.find("trọng lượng")
        if diaChi != -1:
            data["người nhận"] = txt[nguoiNhan:diaChi]
        if dienThoai != -1 and diaChi != -1:
            diaChi = diaChi + 8
            data["địa chỉ"] = txt[diaChi:dienThoai]
        if dienThoai != -1 and noiDung != -1:
            dienThoai = dienThoai + 11
            data["số điện thoại"] = txt[dienThoai:noiDung]
        if noiDung != -1 and tienThuHo != -1:
            noiDung = noiDung + 9
            data["nội dung"] = txt[noiDung:tienThuHo]
        if tienThuHo != -1 and trongLuong != -1:
            tienThuHo = tienThuHo + 12
            data["tiền thu hộ"] = txt[tienThuHo:trongLuong]

    else:
        for x in quan:
            if text.find(x) != -1:
                if x == 'hải châu' or x == 'ngũ hành sơn' or x == 'sơn trà':
                    data["khu vực"] = x
                    break
                elif x == 'cẩm lệ' or x == 'thanh khê' or x == 'liên chiểu':
                    data["khu vực"] = x
                    break
                elif x == 'hòa vang' or x == 'hoàng sa':
                    data["khu vực"] = x
                    break

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
        imgContour = img.copy()
        imgThres = camProcessing(imgContour)
        biggest = getContours(imgThres, imgContour)

        cv2.imshow(previewName, imgContour)
        key = cv2.waitKey(20)
# <<<<<<< HEAD
        #if biggest.size != 0:
            #imgWraped = getWrap(img, biggest)
            #cv2.imshow("Picture", imgWraped)
            #cv2.imwrite("filename1.jpg",imgWraped) 
        #if key == ord("q"):
            #if biggest.size != 0:
                #imgWraped = getWrap(img, biggest)
                
                #cv2.imshow("Picture", imgThres)
                #cv2.imwrite("filename1.jpg", imgThres) 
            #else:
                #pass
        
        if biggest.size != 0:
            imgWraped = getWrap(img, biggest)
            
            cv2.imshow("Picture", imgWraped)
            cv2.imwrite("filename1.jpg", imgWraped)
        else : pass 
# =======
                
        #Nếu phát hiện có 4 điểm thì tiến hành cắt ảnh và lưu ảnh
        # if biggest.size != 0:
        #     cv2.imshow("Picture", imgContour)       #show ảnh chưa qua xử lý
        #
        #     imgWraped = getWrap(img, biggest)       #imgWraped -> ảnh sau khi cắt
        #
        #     cv2.imwrite("filename1.jpg", imgWraped) #lưu ảnh sau khi cắt
        # else : pass

        #Phát hiện vật cản
        if VatCan() == 0:
            # Tăng chỉ số khi phát hiện vật cản lên 1 đơn vị
            vatcan += 1

            # Lần đầu phát hiện vật cản thì tiến hành chụp ảnh
            if vatcan == 1:
                cv2.imshow("Picture", imgContour)       #show ảnh chưa qua xử lý
                # imgWraped = getWrap(img, biggest)       #imgWraped -> ảnh sau khi cắt
                cv2.imwrite("filename1.jpg", imgContour) #lưu ảnh sau khi cắt

                #Đọc chữ trên ảnh đã lưu

            # Nếu không thì pass
            else : pass
        #Khi không phát hiện vật cản, đặt lại giá trị vatcan thành 0
        else: vatcan = 0

# >>>>>>> 1bbca717ee69806ca4eed786e31ace9fbd5be1be
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


############## RUN PROGRAM #####################
thread1 = camThread("Camera", 0)
thread1.start()

