import cv2
import numpy as np


# function that helps stack images so it stays in one window
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


# function to convert a HSV color to rgb, hsvColor is given as [hue,sat,value]
def hsvToBGR(hsvColor):
    return cv2.cvtColor(np.uint8([[hsvColor]]), cv2.COLOR_HSV2BGR)[0][0]


# function to find the color of the marker given the image and return the set of points to add
def findColor(img, markerColors, colorToShow, imgResult):
    # convert image to HSV format
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    # go through each marker color
    for i in range(0, len(markerColors)):
        # find the upper and lower bounds which are stored in the array
        color = markerColors[i]
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        # create a mask which only shows this color
        mask = cv2.inRange(imgHSV, lower, upper)
        # get the contours for this mask, which represent the marker lid
        x, y, w, h = getContours(mask, imgResult)
        # create a circle around the top center point
        cv2.circle(imgResult, (x + w // 2, y), 15, colorToShow[i], cv2.FILLED)
        # if it was a valid contour, then add the points
        if x != 0 and y != 0:
            # add the x and y position along with the color id
            # with multiple markers on screen at once, this will have more than one item
            newPoints.append([x + w // 2, y, i])
    return newPoints


# function to return the contours of the marker lid given an image
def getContours(img, imgResult):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    # there is only one contour we are after, the marker lid
    for cnt in contours:
        # for each contour, store the area and perimeter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)

        # this should match the marker lid
        if area > 500:
            # approximate the location of the corner points and create a bounding box around it
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, closed=True)
            x, y, w, h = cv2.boundingRect(approx)
            # show the box
            cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # we found our main contour so we can return
            return x, y, w, h
    return x, y, w, h


# given a set of points [[x,y,colorId], [..], ...], draw circles on screen with the x,y and the color
def drawOnCanvas(points, myColorValues, imgResult):
    for point in points:
        if point[0] != 0 and point[1] != 0:
            cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


# webcam setup
frameWidth = 1024
frameHeight = 768
brightness = 150
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)

# HSV low to high of the marker colors
markerColors = [
    [115, 84, 118, 145, 255, 255],  # purple
    [161, 84, 146, 179, 255, 255],  # pink
    [91, 100, 93, 102, 255, 255],  # blue
    [70, 100, 93, 88, 255, 255]  # green
]

# show a brighter version of the HSV color when actually painting with that marker
bgrShift = 70
colorToShow = [np.array(hsvToBGR([a, b + bgrShift, c + bgrShift])).tolist() for a, b, c, _, _, _ in markerColors]

# will store the points that the marker takes on screen
points = []  # [[x,y,colorId], [..], ...]

while True:
    # read the current image, and flip it so its easy to paint
    # create a copy which we will modify
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgResult = img.copy()

    # get the set of new points to add
    newPoints = findColor(img, markerColors, colorToShow, imgResult)

    # we have to extend the original points (not append), since newPoints is a list itself
    points.extend(newPoints)

    drawOnCanvas(points, colorToShow, imgResult)

    cv2.imshow('Original and New', stackImages(0.8, [img, imgResult]))

    # cv2.imshow('Result', imgResult)

    wait = cv2.waitKey(1)
    if wait & 0xFF == ord('q'):
        break
    elif wait & 0xFF == ord('c'):
        # clear the screen
        points = []
        drawOnCanvas(points, colorToShow, imgResult)

cv2.destroyAllWindows()
cap.release()
