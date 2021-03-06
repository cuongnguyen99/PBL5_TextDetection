#import packet
from PIL import Image
import pytesseract
import cv2
import re
from unidecode import unidecode


data={"khu vuc": "", "nguoi nhan": "", "so dien thoai": "", "tien thu ho": "", "dia chi": "", "noi dung": ""}
def khuVucHang():
    #############################Version 2#########################
    img = cv2.imread("/home/pi/Desktop/PBL/Demo 12-6-2021/filename1.jpg")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang="vie")

    ###########################################
    text = text.strip()

    #cv2.imshow("image",rgb)


    quan=['hai chau','cam le','thanh khe','lien chieu', 'ngu hanh son', 'son tra', 'hoa vang', 'hoang sa']

    
    text=text.lower()
    text= text.replace("\n", " ")
    text= unidecode(text)
    print(text)

    textSplit= text.split("nguoi nhan:")
    if len(textSplit) > 1 :
        for x in quan:
            if textSplit[1].find(x) != -1:
                data["khu vuc"]= x
                break
            
        txt=textSplit[1]
        nguoiNhan=1
        diaChi=txt.find("dia chi")
        dienThoai=txt.find("dien thoai")
        noiDung=txt.find("noi dung")
        tienThuHo=txt.find("tien thu ho")
        trongLuong=txt.find("trong luong")
        if diaChi != -1:
            data["nguoi nhan"]=txt[nguoiNhan:diaChi].strip()
        if dienThoai!=-1 and diaChi != -1:
            diaChi=diaChi+8
            data["dia chi"]=txt[diaChi:dienThoai].strip()
        if dienThoai!=-1 and noiDung != -1:
            dienThoai=dienThoai+11
            data["so dien thoai"]=txt[dienThoai:noiDung].strip()
        if noiDung!=-1 and tienThuHo != -1:
            noiDung=noiDung+9
            data["noi dung"]=txt[noiDung:tienThuHo].strip()
        if tienThuHo!=-1 and trongLuong != -1:
            tienThuHo=tienThuHo+12
            data["tien thu ho"]=txt[tienThuHo:trongLuong].strip()
            
    else:
        for x in quan:
            if text.find(x) != -1:
                data["khu vuc"]= x
                break
    
            
khuVucHang()
print(data)


    
    