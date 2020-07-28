import cv2
import numpy as np

img = cv2.imread('../Resources/cards.jpg')

cv2.imshow('Original Image', img)

# we want to select the King of Spades
# a normal card has dimensions 250x350
width, height= 250, 350

# define 4 corners of the King of Spades card
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
# now define which corner we are referring to
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])

# transformation matrix
matrix = cv2.getPerspectiveTransform(pts1, pts2)

imgOutput = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow('Warped Image', imgOutput)



cv2.waitKey(0)