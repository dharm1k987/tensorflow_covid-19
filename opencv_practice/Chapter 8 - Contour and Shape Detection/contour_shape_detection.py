import cv2
import numpy as np

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

def getContours(img):
    # cv2.RETR_EXTERNAL is good for retrieving outer edges
    # cv2.CHAIN_APPROX_NONE is good if you want more detail
    contours, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)
        print(cnt.shape)
        print(area)
        print(perimeter)
        print("-------")

        # threshold
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            # approximate number of corner points
            # approx contains the corner point locations
            # if it is a triangle, there are 3 sets of 2 items each
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, closed=True)

            numCorners = len(approx)

            # create bounding box around shape
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # highlight the corners
            for a in approx:
                print((a[0][0], a[0][1]))
                cv2.circle(imgContour, (a[0][0], a[0][1]), 3, (0, 0, 0), 3)

            if numCorners == 3:
                objectType = "Tri"
            elif numCorners == 4:
                objectType = "Rec"
                aspRatio = w/float(h)
                if aspRatio > 0.98 and aspRatio < 1.03:
                    objectType = "Squ"
            elif numCorners > 4:
                objectType = "Circ"
            else:
                objectType = "None"

            # write the shape name
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-5,y+(h//2)-5),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)



img = cv2.imread('../Resources/shapes.png')
imgContour = img.copy()

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
# find edges
imgCanny = cv2.Canny(imgBlur,50,50)
# find contours
getContours(imgCanny)

imgStack = stackImages(0.6, (
    [img, imgGray, imgBlur],
    [imgCanny, imgContour, np.zeros_like(img)]
))

cv2.imshow('Stack', imgStack)

cv2.waitKey(0)