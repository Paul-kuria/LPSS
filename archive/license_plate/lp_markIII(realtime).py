import cv2
import imutils
import numpy as np
import pytesseract
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


#CREATE A VIDEO CAPTURING OBJECT
camera_port = 1
video = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)

#CAPTURE PHOTO FROM VIDEO
success,image = video.read()
count = 0
success = True

#
first_frame = None
#check if camera is opened correctly
if not video.isOpened():
    raise IOError("Cannot open webcam")
return_value, image = video.read()


while True:
    check, frame = video.read()

    #date and time
    today = datetime.today()
    now = datetime.now()
    dt = str(now)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 30, 30)
    edged = cv2.Canny(gray, 30, 200)
    greenpic = frame.copy()
    greenpic = cv2.putText(frame, dt, (10,450), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200,220,220), 1, cv2.LINE_8)


    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # loop over the contours
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        area = cv2.contourArea(c)
        print(area)
        if len(approx) == 4:
            screenCnt = approx
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(greenpic, (x, y), (x + w, y + h), (255, 0, 0), 3)
            break

    while success:
        success,frame = video.read()

        #mask the entire picture except for the place where the plate is
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255,-1)
        new_image = cv2.bitwise_and(frame, frame, mask=mask)

        #now crop
        (x,y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        #character recognition
        text = pytesseract.image_to_string(Cropped, config = '--psm 11')
        print("The Detected Number is: ", text)



        cv2.imshow('License', edged)
        cv2.imshow('Contour', greenpic)

        key = cv2.waitKey(1)#every 1 milisecond a new frame will appear
        if key == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
