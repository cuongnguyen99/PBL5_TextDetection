import requests

# defining the api-endpoint
API_ENDPOINT = "http://localhost:8080/apis/orders"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"

# data to be sent to api
# data={"khu vực": "", "người nhận": "", "số điện thoại": "", "tiền thu hộ": "", "địa chỉ": "", "nội dung": ""}
data={"area": "Đại Lộc", "receiver": "Tăng Phuc", "phone": "0366061247 ", "price": "4500000", "address": "266/11 Truong Chinh", "content": "het no"}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, headers={'token': 'abcxyz'}, data=data)

# extracting response text
pastebin_url = r.text
print("The pastebin URL is:%s" % pastebin_url)