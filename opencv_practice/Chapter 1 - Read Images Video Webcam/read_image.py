import cv2

img = cv2.imread("../Resources/lena.png")

cv2.imshow("Lena", img)

# infinite delay
# if we add 1, then it will show after 1s
cv2.waitKey(0)