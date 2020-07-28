import cv2
import numpy as np

def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


cv2.namedWindow('TrackBars')
# name should be the same
cv2.resizeWindow('TrackBars', 640, 240)
# name of trackbar, window it belongs to, intial starting value, max value, onChange method
# these initial starting points match the color orange
cv2.createTrackbar('Hue Min', 'TrackBars', 0, 179, empty)
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
cv2.createTrackbar("Val Min","TrackBars",153,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

while True:
    img = cv2.imread('../Resources/lambo.png')

    # convert img to HSV (hue sat variance)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # get the value in hue min and the rest of them
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBars')
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    # create a mask that is in the range of these colors
    # min and max range
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    # the mask should find the color that we want highlighted
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    '''
    cv2.imshow("Original", img)
    cv2.imshow("HSV", imgHSV)
    # slide the taskbar until the mask shows only the color that we want
    # in our case it is orange
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", imgResult)
    '''
    # cv2.putText(img, "DS", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)

    cv2.putText(img, 'Original', (0,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)
    cv2.putText(imgHSV, 'HSV', (0,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)
    cv2.putText(mask, 'Mask', (0,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)
    cv2.putText(imgResult, 'Result', (0,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)

    imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Stacked Images", imgStack)

    cv2.waitKey(1)