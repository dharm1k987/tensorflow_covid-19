import cv2
import numpy as np

# 700 row = height, 500 col = width, color
# np.zeros means the image will be black
img = np.zeros((700, 500, 3), dtype=np.uint8)
print(img.shape)

# we follow BLUE GREEN RED, NOT RGB
# img[:] = (255, 0, 0)

# notice pt2 is the bottom rightmost point, which is (500, 700)
cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
cv2.rectangle(img, (0,0), (250, 300), (0,0,255), 2)
cv2.circle(img, (250, 350), 30, (255, 255, 0), 5)
cv2.putText(img, "DS", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)

cv2.imshow("Image", img)

cv2.waitKey(0)