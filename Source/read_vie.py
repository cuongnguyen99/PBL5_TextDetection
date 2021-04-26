#import packet
from PIL import Image
import pytesseract
import cv2
import re

def khuVucHang():
    #############################Version 2#########################
    img = cv2.imread("/home/pi/Desktop/PBL/PBL5_TextDetection/Image/viet8.png")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang="vie")

    ###########################################
    text = text.strip()

    print(text)
    #cv2.imshow("image",rgb)


    quan=['hải châu','cẩm lệ','thanh khê','liên chiểu', 'ngũ hành sơn', 'sơn trà', 'hòa vang', 'hoàng sa']

    
    text=text.lower()

    textSplit= text.split("người nhận")

    if len(textSplit) > 1 :
        for x in quan:
            if textSplit[1].find(x) != -1:
                if x=='hải châu' or  x=='ngũ hành sơn' or x=='sơn trà':
                    return 1
                elif x=='cẩm lệ' or x=='thanh khê' or x=='liên chiểu':
                    return 2
                elif x=='hòa vang' or x=='hoàng sa':
                    return 0
    
    else:
        for x in quan:
            if text.find(x) != -1:
                if x=='hải châu' or  x=='ngũ hành sơn' or x=='sơn trà':
                    return 1
                elif x=='cẩm lệ' or x=='thanh khê' or x=='liên chiểu':
                    return 2
                elif x=='hòa vang' or x=='hoàng sa':
                    return 0
        return -1
            
print(khuVucHang())



    
    