import pytesseract
import cv2

def Read_Img(img):
    img_readed = cv2.imread(img)
    rgb = cv2.cvtColor(img_readed, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang="vie")
    text = text.strip()
    text = text.lower()
    return text

def Find_Str(text):
    if "hải châu" in text:
        return 1
    elif "cẩm lệ" in text:
        return 1
    elif "thanh khê" in text:
        return 1
    elif "liên chiểu" in text:
        return 2
    elif "ngũ hành sơn" in text:
        return 2
    elif "sơn trà" in text:
        return 2
    return 0