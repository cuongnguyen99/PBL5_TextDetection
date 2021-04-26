import numpy as np
import math
import cv2

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
    for i in countours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (0, 255, 0), 15)
    if biggest.size != 0:
        drawRectangle(imgContour, biggest, 2)
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

    h1 = int(math.sqrt((biggest[0][0][0] - biggest[1][0][0]) ** 2 + (biggest[0][0][1] - biggest[1][0][1]) ** 2))
    h2 = int(math.sqrt((biggest[2][0][0] - biggest[3][0][0]) ** 2 + (biggest[2][0][1] - biggest[3][0][1]) ** 2))
    h = max([h1, h2])
    w1 = int(math.sqrt((biggest[0][0][0] - biggest[3][0][0]) ** 2 + (biggest[0][0][1] - biggest[3][0][1]) ** 2))
    w2 = int(math.sqrt((biggest[1][0][0] - biggest[2][0][0]) ** 2 + (biggest[1][0][1] - biggest[2][0][1]) ** 2))
    w = max([w1, w2])

    point1 = np.float32(biggest)
    point2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(point1, point2)
    imgOutput = cv2.warpPerspective(img, matrix, (w, h))
    imgCrop = cv2.resize(imgOutput, (h, w))
    return imgCrop


####################DrawReactangle############################

def drawRectangle(img, biggest, thickness):
    # [0][0][0], [0][0][1]  :A
    # [1][0][0], [1][0][1]  :D
    # [2][0][0], [2][0][1]  :C
    # [3][0][0], [3][0][1]  :B
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[1][0][0], biggest[1][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[2][0][0], biggest[2][0][1]), (biggest[3][0][0], biggest[3][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[0][0][0], biggest[0][0][1]), (0, 255, 0), thickness)