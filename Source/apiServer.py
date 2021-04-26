import requests
import re

# address
API_ENDPOINT = "http://localhost:8080/apis/orders/send-data"
# your API key here
API_KEY = "apiabcdefghjklmnpqaaaa1111222"


# data to be sent to api
data = {'orderCode': "abc1222",
        'name': 'paste',
        'subPrice': '15000',
        'shipPrice': '5000',
        'totalPrice': '30000'}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, headers={'token': 'abcxyz'}, data=data)
# extracting response text
pastebin_url = r.text
print("The pastebin URL is:%s" % pastebin_url)