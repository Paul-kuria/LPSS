import cv2
import imutils
import numpy as np
import pytesseract
import csv
import RPi.GPIO as GPIO
import time
from time import sleep
from datetime import datetime
from datetime import date
from Timestamp import query_reg

today = date.today()

#BUILD GATEOPEN
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(12, GPIO.OUT)
servo1 = GPIO.PWM(12, 50)
servo1.start(0)
time.sleep(2)



def setAngle(angle):
    duty = angle/18 + 2
    GPIO.output(12,True)
    servo1.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(12,False)
    servo1.ChangeDutyCycle(0)

setAngle(100)

def plateText(string):
    asc_value = []
    for character in string:
        ff = (ord(character))
        if ff > 47 and ff<90:
            asc_value.append(ff)
    for i in range(len(asc_value)):
        one = ''.join(chr(i) for i in asc_value)
    return one

def openGate():
    setAngle(20)
    sleep(4)
    setAngle(100)
    sleep(2)
    servo1.stop()
#pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'
def mainProgram():
    path = 'frame_2.png'
    img = cv2.imread(path)

    img = cv2.resize(img, (640,480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 30, 30)

    edged = cv2.Canny(gray, 30, 200)
    greenpic = img.copy()

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    #loop over the contours
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018*peri, True)
        area = cv2.contourArea(c)
        print(area)
        if len(approx) ==4:
            screenCnt = approx
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(greenpic, (x,y), (x+w,y+h), (255,0,0), 3)
            break

    #mask the entire picture except for the place where the plate is
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255,-1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    #now crop
    (x,y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    #character recognition
    text = pytesseract.image_to_string(Cropped, config = '--psm 11')
    plate = plateText(text)
    print("The Detected Number is: ", plate)



    #QUERY REG_NO

    #query_reg((plate,))
    while query_reg((plate,)) == True:
        openGate()
    else:
        sleep(2)
        setAngle(20)
    
    cv2.imshow("original", Cropped)
    cv2.imshow("blur", edged)
    cv2.imshow("plate", greenpic)
    k = cv2.waitKey(0)
    
        
    setAngle(100)

    now = datetime.today()
    d_time = today.strftime("%d/%m/%Y")
    c_time = now.strftime("%H:%M:%S")
    print(d_time,c_time)
    
    if k%256 == 27:
        cv2.destroyAllWindows()
        
    
    GPIO.cleanup()
    
mainProgram()




