import cv2
import numpy as np

img = cv2.imread('../Resources/lambo.png')

# height, width, channel
# (462, 623, 3) -> 3 is for color images
print(img.shape)

# define width first here
imgResize = cv2.resize(img, (1000, 500))
print(imgResize.shape)

imgCropped = img[0:200, 200:500] # 200 height, 300 width
cv2.imshow("Image", img)

cv2.imshow("Image", img)
cv2.imshow("Image Resize",imgResize)
# remember in resize we define width first
cv2.imshow("Image Resize Same",cv2.resize(img, (300, 200)))

cv2.imshow("Image Cropped", imgCropped)

cv2.waitKey(0)