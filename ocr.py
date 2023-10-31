import json
import base64
import requests
import pprint

with open("./runs/track/exp3/crops/bookNumber/01/convert_20220927_172412.jpg", "rb") as f:
    img = base64.b64encode(f.read())

URL = "https://nepyh7zrhm.apigw.ntruss.com/custom/v1/14944/a9fe726d2a1700d6c39c1946044fd34665ef80b621aed0f15845e6de421e3158/general"

KEY = "Rk1tV3ZVVmhNeW9iVm1HZ1JwckxycXVuU2dOUUFmbEM="

headers = {
    "Content-Type": "application/json",
    "X-OCR-SECRET": KEY
}

data = {
    "version": "V1",
    "requestId": "sample_id", # 요청을 구분하기 위한 ID, 사용자가 정의
    "timestamp": 0, # 현재 시간값
    "images": [
        {
            "name": "sample_image",
            "format": "png",
            "data": img.decode('utf-8')
        }
    ]
}

data = json.dumps(data)
response = requests.post(URL, data=data, headers=headers)
res = json.loads(response.text)

pprint.pprint(res)

