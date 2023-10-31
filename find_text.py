import cv2
import matplotlib.pyplot as plt
import numpy as np

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


image = cv2.imread('./runs/track/exp3/crops/bookNumber/09/convert_20220927_172412.jpg')
print("[ 원본이미지 ]")
plt.imshow(image)
plt.show()

h, w, _ = image.shape

bottom = int(h*0.1)
top = int(h*0.9)
left = int(w*0.05)
right = int(w*0.95)
roi = image[bottom:top, left:right]
plt.imshow(roi)
plt.show()
roi = img_Contrast(roi)


# cv2.drawContours(image, contours, whitebox_idx, (0, 255, 0), 1, 8)


print("[ contour 추출 ]")
plt.imshow(roi)
plt.show()

cv2.imwrite('./test.jpg', roi)