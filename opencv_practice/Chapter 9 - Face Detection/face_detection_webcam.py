import cv2

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier('../Resources/haarcascades/haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    print(faces)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, 'Face', (x + w, y + h), cv2.FONT_HERSHEY_COMPLEX,0.7, (0,0,0),2)

    eyesCascade = cv2.CascadeClassifier('../Resources/haarcascades/haarcascade_eye.xml')
    eyes = eyesCascade.detectMultiScale(imgGray, 1.1, 4)
    print(eyes)

    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, 'Eye', (x + w, y + h), cv2.FONT_HERSHEY_COMPLEX,0.7, (0,0,0),2)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) and 0xF == ord('q'):
        break

cap.release();
cv2.destroyAllWindows();



