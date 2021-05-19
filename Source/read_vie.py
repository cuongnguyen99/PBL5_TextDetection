#import packet
from PIL import Image
import pytesseract
import cv2
import re


data={"khu vực": "", "người nhận": "", "số điện thoại": "", "tiền thu hộ": "", "địa chỉ": "", "nội dung": ""}
def khuVucHang():
    #############################Version 2#########################
    img = cv2.imread("/home/pi/Desktop/PBL/PBL5_TextDetection/Image/don2.png")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang="vie")

    ###########################################
    text = text.strip()

    #cv2.imshow("image",rgb)


    quan=['hải châu','cẩm lệ','thanh khê','liên chiểu', 'ngũ hành sơn', 'sơn trà', 'hòa vang', 'hoàng sa']

    
    text=text.lower()
    text= text.replace("\n", " ")
    print(text)

    textSplit= text.split("người nhận:")
    if len(textSplit) > 1 :
        for x in quan:
            if textSplit[1].find(x) != -1:
                if x=='hải châu' or  x=='ngũ hành sơn' or x=='sơn trà':
                    data["khu vực"]= x
                    break 
                elif x=='cẩm lệ' or x=='thanh khê' or x=='liên chiểu':
                    data["khu vực"]= x
                    break
                elif x=='hòa vang' or x=='hoàng sa':
                    data["khu vực"]= x
                    break
          
        txt=textSplit[1]
        nguoiNhan=1
        diaChi=txt.find("địa chỉ")
        dienThoai=txt.find("điện thoại")
        noiDung=txt.find("nội dung")
        tienThuHo=txt.find("tiền thu hộ")
        trongLuong=txt.find("trọng lượng")
        if diaChi != -1:
            data["người nhận"]=txt[nguoiNhan:diaChi]
        if dienThoai!=-1 and diaChi != -1:
            diaChi=diaChi+8
            data["địa chỉ"]=txt[diaChi:dienThoai]
        if dienThoai!=-1 and noiDung != -1:
            dienThoai=dienThoai+11
            data["số điện thoại"]=txt[dienThoai:noiDung]
        if noiDung!=-1 and tienThuHo != -1:
            noiDung=noiDung+9
            data["nội dung"]=txt[noiDung:tienThuHo]
        if tienThuHo!=-1 and trongLuong != -1:
            tienThuHo=tienThuHo+12
            data["tiền thu hộ"]=txt[tienThuHo:trongLuong]
            
    else:
        for x in quan:
            if text.find(x) != -1:
                if x=='hải châu' or  x=='ngũ hành sơn' or x=='sơn trà':
                    data["khu vực"]= x
                    break
                elif x=='cẩm lệ' or x=='thanh khê' or x=='liên chiểu':
                    data["khu vực"]= x
                    break
                elif x=='hòa vang' or x=='hoàng sa':
                    data["khu vực"]= x
                    break
    
    
            
khuVucHang()
for i in data.values() :
    i.strip()
print(data)


    
    