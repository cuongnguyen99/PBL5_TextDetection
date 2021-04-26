import cv2
import threading
import Img_Handling as hd
import Read_Text

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        success, img = cam.read()
        imgThres = hd.camProcessing(img)
    else:
        success = False

    while success:
        cv2.imshow(previewName, imgThres)
        success, img = cam.read()
        imgContour = img.copy()
        imgThres = hd.camProcessing(imgContour)
        biggest = hd.getContours(imgThres, imgContour)

        cv2.imshow(previewName, imgContour)
        key = cv2.waitKey(20)
        if biggest.size != 0:
            imgWraped = hd.getWrap(img, biggest)
            cv2.imshow("Picture", imgWraped)
            cv2.imwrite("filename1.jpg", imgWraped)
        else: pass
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

############## RUN PROGRAM #####################
thread1 = camThread("Camera", 0)
thread1.start()
