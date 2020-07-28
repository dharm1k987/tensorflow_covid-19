import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

# myColors = [
#     [113,136,64,255,70,255], # purple # orange
#     [128,179,99,255,131,255], # pink # purple
#     [94,107,136,255,43,255], # blue # green
#     [27,86,84,255,30,255] # green
# ]

myColors = [
    [115,84,118,145,255,255], # purple # orange
    [161,84,146,179,255,255], # pink # purple
    [91,100,93,102,255,255], # blue # green
    [70,100,93,88,255,255] # green
]

myColorValues = [
    [137,86,81], # BGR values
    [132,111,222],
    [150,113,29],
    [114,213,26]
]

myPoints = [] # [x,y,colorId]


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        # print(lower, upper)
        # the mask should find the color that we want highlighted
        mask = cv2.inRange(imgHSV, lower, upper)
        # cv2.imshow(str(lower[0]), mask)
        x,y = getContours(mask)
        cv2.circle(imgResult, (x,y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]), mask)
    return newPoints


def getContours(img):
    contours, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)

        # threshold
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, closed=True)
            # create bounding box around shape
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgResult, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return x+w//2, y

def drawOnCanvas(myPoints, myColorValues):
    # print("in here")
    for point in myPoints:
        cv2.circle(imgResult, (point[0],point[1]), 5, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgResult = img.copy()

    newPoints = findColor(img, myColors, myColorValues)
    # print(newPoints)
    if newPoints:
        for newP in newPoints:
            myPoints.append(newP)
    if myPoints:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow('Result', imgResult)

    wait = cv2.waitKey(1)
    if wait & 0xFF == ord('q'):
        break
    elif wait & 0xFF == ord('c'):
        print("in here")
        myPoints = []
        drawOnCanvas(myPoints, myColorValues)

cv2.destroyAllWindows()
cap.release()