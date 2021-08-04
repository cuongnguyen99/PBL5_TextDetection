#import packet
from PIL import Image
import pytesseract
import cv2
import re
from unidecode import unidecode


# data={"khu vuc": "", "nguoi nhan": "", "so dien thoai": "", "tien thu ho": "", "dia chi": "", "noi dung": ""}
def khuVucHang():
    data={"area": "", "receiver": "", "phone": "", "price": "", "address": "", "content": ""}
    #############################Version 2#########################
    img = cv2.imread("/home/pi/Desktop/PBL/PBL5_TextDetection/Demo 12-6-2021/filename1.jpg")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang="vie")

    ###########################################
    text = text.strip()

    #cv2.imshow("image",rgb)


    quan=['hai chau','cam le','thanh khe','lien chieu', 'ngu hanh son', 'son tra', 'hoa vang', 'hoang sa']

    
    text=text.lower()
    text= text.replace("\n", " ")
    text= unidecode(text)
#     print(text)

    textSplit= text.split("nguoi nhan:")
    if len(textSplit) > 1 :
        for x in quan:
            if textSplit[1].find(x) != -1:
                data["area"]= x
                break
            
        txt=textSplit[1]
        nguoiNhan=1
        diaChi=txt.find("dia chi")
        dienThoai=txt.find("dien thoai")
        noiDung=txt.find("noi dung")
        tienThuHo=txt.find("tien thu ho")
        trongLuong=txt.find("trong luong")
        if diaChi != -1:
            data["receiver"]=txt[nguoiNhan:diaChi].strip()
        if dienThoai!=-1 and diaChi != -1:
            diaChi=diaChi+8
            data["address"]=txt[diaChi:dienThoai].strip()
        if dienThoai!=-1 and noiDung != -1:
            dienThoai=dienThoai+11
            data["phone"]=txt[dienThoai:noiDung].strip()
        if noiDung!=-1 and tienThuHo != -1:
            noiDung=noiDung+9
            data["content"]=txt[noiDung:tienThuHo].strip()
        if tienThuHo!=-1 and trongLuong != -1:
            tienThuHo=tienThuHo+12
            data["price"]=txt[tienThuHo:trongLuong].strip()
            
    else:
        for x in quan:
            if text.find(x) != -1:
                data["area"]= x
                break
        textSplit2= text.split("dia chi")
        if len(textSplit2) > 2 :
            txt= textSplit2[2]
            diaChi=1
            dienThoai=txt.find("dien thoai")
            noiDung=txt.find("noi dung")
            tienThuHo=txt.find("tien thu ho")
            trongLuong=txt.find("trong luong")
            if dienThoai!=-1:
                data["address"]=txt[diaChi:dienThoai].strip()
            if dienThoai!=-1 and noiDung != -1:
                dienThoai=dienThoai+11
                data["phone"]=txt[dienThoai:noiDung].strip()
            if noiDung!=-1 and tienThuHo != -1:
                noiDung=noiDung+9
                data["content"]=txt[noiDung:tienThuHo].strip()
            if tienThuHo!=-1 and trongLuong != -1:
                tienThuHo=tienThuHo+12
                data["price"]=txt[tienThuHo:trongLuong].strip()
        else:
            textSplit3= text.split("dien thoai")
            if len(textSplit3) > 2 :
                txt= textSplit3[2]
                dienThoai=1
                noiDung=txt.find("noi dung")
                tienThuHo=txt.find("tien thu ho")
                trongLuong=txt.find("trong luong")
                if noiDung != -1:
                    data["phone"]=txt[dienThoai:noiDung].strip()
                if noiDung!=-1 and tienThuHo != -1:
                    noiDung=noiDung+9
                    data["content"]=txt[noiDung:tienThuHo].strip()
                if tienThuHo!=-1 and trongLuong != -1:
                    tienThuHo=tienThuHo+12
                    data["price"]=txt[tienThuHo:trongLuong].strip()
#                 
    print(data)
    return data
    
            



    
    