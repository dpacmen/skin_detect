import cv2
import numpy as np
def nothing(x):
	pass

img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H', 'image', 0, 179, nothing)
cv2.createTrackbar('S', 'image', 0, 255, nothing)
cv2.createTrackbar('V', 'image', 0, 255, nothing)

while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    h = cv2.getTrackbarPos('H', 'image')
    s = cv2.getTrackbarPos('S', 'image')
    v = cv2.getTrackbarPos('V', 'image')

    img[:] = [h,s,v]
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR )

cv2.destroyAllWindows()
