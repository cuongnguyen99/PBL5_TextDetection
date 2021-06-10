import cv2
import threading
import numpy as np
import math
import read_vie

# ===========================================
# widthImg  = 960
# heightImg = 540

# ===========================================
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)


#Đưa ảnh về màu xám để xử lý
def camProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5, 5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=2)
    imgErode = cv2.erode(imgDialation, kernel, iterations=1)
    return imgErode

#Tìm tọa độ 4 điểm
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
    cv2.drawContours(imgContour, biggest, -1, (0, 255, 0), 15)
    if biggest.size != 0:
        drawRectangle(imgContour, biggest, 2)
    return biggest

#Tìm 4 điểm trên ảnh
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

#Cắt ảnh 
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
#Nối 4 điểm lại với nhau
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
        success, img = cam.read()                   #img -> ảnh lúc chưa qua xử lý
        imgThres = camProcessing(img)               #imgThres -> ảnh sau khi đã được đưa về màu xám
        # biggest = getContours(imgThres, img)
    else:
        success = False

    while success:
        cv2.imshow(previewName, imgThres)           
        success, img = cam.read()                   #img -> ảnh lúc chưa qua xử lý
        # img = cv2.resize(img, (widthImg, heightImg))
        imgContour = img.copy()
        imgThres = camProcessing(imgContour)        #imgThres -> ảnh sau khi đã được đưa về màu xám
        biggest = getContours(imgThres, imgContour) #Lấy 4 điểm từ imgThes, vẽ 4 điểm (nếu có)

        cv2.imshow(previewName, imgContour)
        key = cv2.waitKey(20)
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
                
        #Nếu phát hiện có 4 điểm thì tiến hành cắt ảnh và lưu ảnh
        if biggest.size != 0:
            cv2.imshow("Picture", imgContour)       #show ảnh chưa qua xử lý
            
            imgWraped = getWrap(img, biggest)       #imgWraped -> ảnh sau khi cắt
            
            cv2.imwrite("filename1.jpg", imgWraped) #lưu ảnh sau khi cắt
        else : pass 
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


############## RUN PROGRAM #####################
thread1 = camThread("Camera", 0)
thread1.start()

