#import packet
from PIL import Image
import pytesseract
import cv2

#############################Version 2#########################
# img = cv2.imread("D:\\Save\\viet2.png")
img = cv2.imread("D:\\Save\\Project\\viet10.png")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
text = pytesseract.image_to_string(rgb, lang="vie")

###########################################
text = text.strip()
# text = text.split('\n\n')
# z = '\n'.join(map(str, text))
# pattern = re.compile('\n')
# text = text.strip()
# text = text.replace("  ", " ")
# text = re.sub(pattern, " ", text)
###########################################

print(text)

# cv2.imshow("image",rgb)
# cv2.waitKey(0)


