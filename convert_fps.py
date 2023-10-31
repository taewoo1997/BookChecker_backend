import sys
import cv2
import os

videoFile1 = sys.argv[1]

if os.path.isfile(videoFile1):	# 해당 파일이 있는지 확인
    # 영상 객체(파일) 가져오기
    cap = cv2.VideoCapture(videoFile1)
else:
    print("파일이 존재하지 않습니다.")  


# 화면 크기 설정

# cap.set(3,320)
# cap.set(4,240)

videoFile1 = videoFile1.split("\\")[-1]

# 파일 쓰기

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('.\converted\\'+'convert_'+ videoFile1, fourcc, 30, (width,height)) # 비디오 재생 1초에 30 프레임의 속도로 set 

fps_skip_counter = 8 # 슬로우모션: 240fps
                      # 30fps로 낮추기 위해 1/8 해야함

print("...converting...")

while True:

    ret, frame = cap.read()
    fps_skip_counter -= 1

    if ret and fps_skip_counter == 0: # 8 프레임마다 1 프레임 추출

        fps_skip_counter = 8

        out.write(frame)
        print(".")
        # cv2.imshow('video', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
    elif ret:
        continue
    else:
        break



print("converted!")
 

cap.release()
out.release()
cv2.destroyAllWindows()