import cv2

# COLORMAP_AUTUMN = 0,
# COLORMAP_BONE = 1,
# COLORMAP_JET = 2,
# COLORMAP_WINTER = 3,
# COLORMAP_RAINBOW = 4,
# COLORMAP_OCEAN = 5,
# COLORMAP_SUMMER = 6,
# COLORMAP_SPRING = 7,
# COLORMAP_COOL = 8,
# COLORMAP_HSV = 9,
# COLORMAP_PINK = 10,
# COLORMAP_HOT = 11

# img = cv2.imread("resource/girl.jpeg")
img = cv2.imread("resource/black.png")
for i in range(0, 13):
    im_color = cv2.applyColorMap(img, i)
    cv2.imwrite("resource/{}.jpg".format(i), im_color)
