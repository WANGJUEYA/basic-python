import cv2
import numpy as np

from pyqt5 import function


def nothing(x):
    pass


img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)
cv2.createTrackbar('HSV', 'image', 0, 35999, nothing)
switch = '0:OFF\n1:ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)
while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    s = cv2.getTrackbarPos(switch, 'image')

    # 通过HSV计算RGB
    HSV = cv2.getTrackbarPos('HSV', 'image')
    h = HSV // 100
    s = (HSV % 100) // 10
    v = HSV % 10
    s = s == 0 and 1 or s / 10
    v = v == 0 and 1 or v / 10
    print(HSV)
    print(h)
    print(s)
    print(v)
    r, g, b = function.hsv2rgb(h, s, v)

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b, g, r]
cv2.imwrite('/home/wl/1.jpg', img)
cv2.destroyAllWindows()
