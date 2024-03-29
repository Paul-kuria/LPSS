import csv
import os
from datetime import date, datetime

import cv2
import imutils
import numpy as np
import pytesseract
from Timestamp import query_reg

today = date.today()


def plateText(string):
    asc_value = []
    for character in string:
        ff = ord(character)
        # if (ff > 47 and ff <58) and (ff >64 and ff < 90) and (ff > 96 and ff < 122):
        if ff > 64 and ff < 91:
            asc_value.append(ff)
        if ff > 47 and ff < 58:
            asc_value.append(ff)
    for i in range(len(asc_value)):
        one = "".join(chr(i) for i in asc_value)
        return one


# pytesseract.pytesseract.tesseract_cmd = '/usr/local/share/tessdata'
def camera():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # esc pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # space pressed
            img_name = "frame_{}.png".format(img_counter)
            frame = cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    cap.release()
    cv2.destroyAllWindows()
    return frame


def main():
    # path = '/home/pablo/Documents/license_plate/NP/working/img9.jpeg'
    img = camera()
    img = cv2.resize(img, (640, 480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 30, 30)

    edged = cv2.Canny(gray, 30, 200)
    greenpic = img.copy()

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

    # mask the entire picture except for the place where the plate is
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx : bottomx + 1, topy : bottomy + 1]

    # character recognition
    text = pytesseract.image_to_string(Cropped, config="--psm 11")
    plate = plateText(text)
    print("The Detected Number is: ", plate)

    #
    cv2.imshow("original", Cropped)
    cv2.imshow("blur", edged)
    cv2.imshow("plate", greenpic)
    cv2.imshow("mask", new_image)
    # cv2.waitKey(0)

    # QUERY REG_NO
    query_reg((plate,))

    now = datetime.today()
    d_time = today.strftime("%d/%m/%Y")
    c_time = now.strftime("%H:%M:%S")
    print(d_time, c_time)


cv2.waitKey(0)

while True:
    main()
