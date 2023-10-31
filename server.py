from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import os
from glob import glob
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 다른 폴더에 있는 파일 import 하기 위해서

import subprocess

app = Flask(__name__)

@app.route('/postVideo', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['video']
        f.save(f'uploads/{secure_filename(f.filename)}')
        print('동영상이 저장되었습니다')

        uploaded_video = r".\uploads\\" + f.filename
        cmd = f"python convert_fps.py {uploaded_video}"
        subprocess.run(cmd, shell=True) 
        print("동영상이 변환되었습니다")

        print("객체 추출작업을 진행하겠습니다")
        uploaded_video = "./converted/" + "convert_" + f.filename
        cmd = f"python track.py --source {uploaded_video} --yolo-weights best2.pt --img 416 --save-txt --save-conf --save-crop --save-vid"
        subprocess.run(cmd, shell=True) 
        print('객체를 추출을 완료하였습니다')         

        print("청구기호 추출작업을 진행하겠습니다")
        # exp_list = list(filter(os.path.isdir, glob(r'./runs/track/*')))
        exp_list = sorted(glob(r'./runs/track/*'), key=os.path.getctime) # 파일 생성일
        for fname in exp_list:
            pass
        recent_exp = exp_list[-1].split("\\")[-1]
        cmd = f"python clova_ocr.py {recent_exp}"
        result = subprocess.run(cmd, capture_output=True, shell=True, encoding='cp949') 
        print(result.stdout)
        print('청구기호 추출을 완료하였습니다')

        return result.stdout
    else: 
        return render_template('file_upload.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)