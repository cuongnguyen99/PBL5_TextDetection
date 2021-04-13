import cv2
import threading
import numpy as np
#===========================================
widthImg=640
heightImg=480

#===========================================
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

#Xử lý ảnh
def camProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5,5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
    imgErode = cv2.erode(imgDialation, kernel, iterations=2)
    return imgDialation

def getContours(imgThres, imgContour):
    biggest = np.array([])
    maxArea = 0
    # countours, rank = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    countours, rank = cv2.findContours(imgThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in countours:
        area = cv2.contourArea(i)
        if area> 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    # cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 10)
    cv2.drawContours(imgContour, biggest, -1, (0, 255, 0), 15)
    if biggest.size !=0:
        drawRectangle(imgContour, biggest, 2)
    # drawRectangle(imgContour, biggest, 2)
    return biggest

def reorderToDrawRectangle(myPoints):
    myPoints = myPoints.reshape((3,2))
    myPointsNew = np.zeros((3,1,2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmin(diff)]
    return myPointsNew
def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2), np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmin(diff)]
    return myPointsNew

def getWrap(img, biggest):
    biggest = reorder(biggest)
    point1 = np.float32(biggest)
    point2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(point1, point2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    # imgCrop = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1]-20]
    # imgCrop = cv2.resize(imgCrop, (widthImg, heightImg))
    return imgOutput
####################DrawReactangle############################

def drawRectangle(img,biggest,thickness):
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[1][0][0], biggest[1][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[2][0][0], biggest[2][0][1]), (biggest[3][0][0], biggest[3][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[0][0][0], biggest[0][0][1]), (0, 255, 0), thickness)
    # return img

################################################
def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, widthImg)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, heightImg)
    if cam.isOpened():  # try to get the first frame
        success, img = cam.read()
        # imgContour = img.copy()
        imgThres = camProcessing(img)
        biggest = getContours(imgThres, img)
    else:
        success = False

    while success:
        cv2.imshow(previewName, imgThres)
        success, img = cam.read()
        img = cv2.resize(img, (widthImg, heightImg))
        # imgContour = img.copy()
        imgThres = camProcessing(img)
        biggest = getContours(imgThres, img)

        print("================")
        print(biggest)
        if biggest.size != 0:
            print(biggest[0][0][0])
        print("================")

        cv2.imshow(previewName, img)
        key = cv2.waitKey(20)
        if key == ord("q"):
            if biggest.size != 0:
                # imgWraped = getWrap(frame, biggest)
                cv2.imshow("Picture", img)
            else:
                cv2.imshow("Picture", img)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)
############## RUN PROGRAM #####################
thread1 = camThread("Camera 1", 0)
thread1.start()

