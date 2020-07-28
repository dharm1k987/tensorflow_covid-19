import cv2
import numpy as np


# function to convert a hsv color to rgb
def hsvToBGR(hsvColor):
    return cv2.cvtColor(np.uint8([[hsvColor]]), cv2.COLOR_HSV2BGR)[0][0]


# function to find the color of the marker given the image and return the set of points to add
def findColor(img, markerColors, colorToShow):
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
        x, y, w, h = getContours(mask)
        # create a circle around the top center point
        cv2.circle(imgResult, (x + w // 2, y), 15, colorToShow[i], cv2.FILLED)
        # if it was a valid contour, then add the points
        if x != 0 and y != 0:
            # add the x and y position along with the color id
            # with multiple markers on screen at once, this will have more than one item
            newPoints.append([x + w // 2, y, i])
    return newPoints


# function to return the contours of the marker lid given an image
def getContours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    # there is only one contour we are after, the marker lid
    for cnt in contours:
        # for each contour, store the area and perimeter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)

        if area > 500:
            # approximate the location of the corner points and create a bounding box around it
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, closed=True)
            x, y, w, h = cv2.boundingRect(approx)
            # show the box
            cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # we found our main contour so we can return
            return x, y, w, h
    return x, y, w, h


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
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
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgResult = img.copy()

    # get the set of new points to add
    newPoints = findColor(img, markerColors, colorToShow)

    # we have to extend the original points (not append), since newPoints is a list itself
    points.extend(newPoints)

    drawOnCanvas(points, colorToShow)

    cv2.imshow('Result', imgResult)

    wait = cv2.waitKey(1)
    if wait & 0xFF == ord('q'):
        break
    elif wait & 0xFF == ord('c'):
        # clear the screen
        points = []
        drawOnCanvas(points, colorToShow)

cv2.destroyAllWindows()
cap.release()
