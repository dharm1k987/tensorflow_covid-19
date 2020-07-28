import cv2

img = cv2.imread('../Resources/lena.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier('../Resources/haarcascades/haarcascade_frontalface_default.xml')
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
print(faces)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

eyesCascade = cv2.CascadeClassifier('../Resources/haarcascades/haarcascade_eye.xml')
eyes = eyesCascade.detectMultiScale(imgGray, 1.1, 4)
print(eyes)

for (x, y, w, h) in eyes:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)



cv2.imshow("Result", img)
cv2.waitKey(0)
