import json
import base64
import requests
import pprint
from glob import glob
import os
import shutil
import cv2
import sys

def img_Contrast(img):
    # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(4, 4))
    cl = clahe.apply(l)
    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))
    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return final

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


# print(glob(r'./runs/track/exp/crops/bookNumber/*'))
recent_exp = sys.argv[1]
idx_list = glob('./runs/track/' + recent_exp +'/crops/bookNumber/*')

result_list = []
img_path_list = []

for path in idx_list:
    idx = path.split('\\')[1]
    # print(idx)
    base_path = './runs/track/'+ recent_exp + '/crops/bookNumber/'
    base_path_id = base_path + idx
    # print(base_path)
    target = glob(base_path_id+'/*.jpg')[0]
    # print(target)
    target_name = target.split('\\')[1]
    target = target.replace('\\','/') # 경로형식 변경을 위해

    createFolder(base_path + 'send_images')
    shutil.copy(target, base_path + 'send_images/' + idx + '_'+ target_name)

    # with open(target, "rb") as f:
    #     img = base64.b64encode(f.read())

    img = cv2.imread(target)
    h, w, _ = img.shape

    bottom = int(h*0.1)
    top = int(h*0.9)
    left = int(w*0.05)
    right = int(w*0.95)
    roi = img[bottom:top, left:right]
    roi = img_Contrast(roi)

    createFolder(base_path + 'sharpening_images')
    cv2.imwrite(base_path + 'sharpening_images' + f'/{idx}.jpg', roi)
    createFolder("./static" + base_path[1:] + 'sharpening_images')
    cv2.imwrite("./static" + base_path[1:] + 'sharpening_images' + f'/{idx}.jpg', roi)

    # jpg_img = cv2.imencode('.jpg', roi)
    with open(base_path + 'sharpening_images' + f'/{idx}.jpg', "rb") as f:
        jpg_img = base64.b64encode(f.read())
    
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
                "format": "jpg",
                "data": jpg_img.decode('utf-8')
            }
        ]
    }

    # 네이버 OCR API 호출
    # print("네이버 OCR API 호출")
    data = json.dumps(data)
    response = requests.post(URL, data=data, headers=headers)
    res = json.loads(response.text)

    # print(data)
    # print(response)
    # print(res)

    # pprint.pprint(res)

    # pprint.pprint(res['images'][0]['fields'])

    dic_list = res['images'][0]['fields']

    str = ""

    for dic in dic_list:
        # print(dic['inferText'])
        str += dic['inferText'] + " "

    # print(str)

    # 안드로이드에서 받았을 때 처리하게 용이하게 슬라이싱.
    result_list.append(str[:-1] + "&&" + "static" + base_path[1:] + 'sharpening_images' + f'/{idx}.jpg')


print(result_list)
