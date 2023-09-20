import os
import cv2 
import easyocr
import imutils
import numpy as np 
from datetime import datetime 



class VideoInfer:
    def __init__(self):
        self.source = 0 
        self.datenow = datetime.now().strftime("%Y-%m-%d")
        self.timenow = datetime.now().strftime("%H:%M:%S")
        self.img_dimensions = (640, 480)
        self.COLOR_RED = (0, 0, 255)
        self.COLOR_BLUE = (255,0,0)
        self.THICKNESS = 2

    def image_manipulate(self, vehicle: str):
        img = cv2.imread(vehicle)
        img = cv2.resize(img, self.img_dimensions)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert from BGR colorspace to grayscale, simplify the image to a single channel, makes it easier to perform image processing ops
        
        # Apply filter and find edges for localization
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection
        n = cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)

        # Find contours and apply mask
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        # Crop the image
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]

        # EASY OCR
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        # Render Result
        text = result[0][-2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        # Display
        print(text)
        # cv2.imshow("frame", res)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def main():
    data = "./datasets/round1"
    run = VideoInfer()
    
    for root, dirs, files in os.walk(data):
        for file in sorted(files):
            path = os.path.join(root, file)
            print(path)
            run.image_manipulate(path)

if __name__ == "__main__":
    main()