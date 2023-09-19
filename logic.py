import cv2 
import pytesseract
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

    def licence_plate_to_text(self, object_string):
        asc_value = []
        for char in object_string:
            val = (ord(char))
            if (val > 64 and val < 91):
                asc_value.append(val)
            elif (val > 47 and val < 58):
                asc_value.append(val)
        
        for i in range(len(asc_value)):
            obj = ''.join(chr(i) for i in asc_value)
        
        return obj   
    
    def camera(self):
        img_counter = 0
        cap = cv2.VideoCapture(self.source)

        while True:
            retr, frame = cap.read()
            if not retr:
                print("Camera capture failed, restart program")
                break 
            cv2.imshow("camera", frame)

            if (cv2.waitKey(30) == 27):
                break
            elif (cv2.waitKey(30) == 32):
                img_name = f"frame_{img_counter}.jpg"
                frame_new = cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1 
        
        cap.release()
        cv2.destroyAllWindows() 
        return frame_new 

    def run_inference(self):
        dataset = "./datasets/im1.jpg"
        # im = self.camera() 
        im = cv2.imread(dataset)
        img = cv2.resize(im, self.img_dimensions)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayf = cv2.bilateralFilter(gray, 11, 30, 30)

        # Detect the edges using canny
        edged = cv2.Canny(gray, 30, 200)
        greenpic = img.copy()

        # Find contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse=True)[:10]
        
        screenCnt = None
    
    def image_manipulate(self):
        dataset = "./datasets/im1.jpg"
        im = cv2.imread(dataset)
        img = cv2.resize(im, self.img_dimensions)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert from BGR colorspace to grayscale, simplify the image to a single channel, makes it easier to perform image processing ops
        grayf = cv2.bilateralFilter(gray, 11, 30, 30) # noise reducing technique that preserves edges while smoothing other areas of the image

        # Detect the edges using canny
        edged = cv2.Canny(gray, 30, 200) # uses canny edge detection algorith, finds areas with significant changes in density, corresponding to the object edges
        greenpic = img.copy()

        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # RETR_TREE, retrieval mode, gets all the contours and reconstructs a full hierarchy of nested contours. CHAIN, compresses H,V and diagonal segments, leaving only endpoints
        
        cnts = imutils.grab_contours(cnts) # Grabs actual contours returned by findContours. Helper Function
        cnts = sorted(cnts, key = cv2.contourArea) # sorts contours by their area in desc order and keeps the largest 10 contours
        screenContour = None # Initialize a variable, used to store the required rectangular shape.

        # Loop over contours:
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018*perimeter, True) # Approximates the contour by reducing the number of vertices using the Douglas-Peucker algorithm. The 0.018 * peri parameter controls the approximation accuracy.
            area = cv2.contourArea(c)
            if len(approx) == 4:
                screenContour = approx 
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(greenpic, (x,y), (x+w,y+h), self.COLOR_BLUE, self.THICKNESS)

        
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenContour], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask) # btwise and btwn original and mask, resulting in the ROI reamaining visible and the rest is blacked out.

        #now crop
        (x,y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        
        #character recognition
        text = pytesseract.image_to_string(Cropped, config = '--psm 11')
        try:
            plate = self.licence_plate_to_text(text)
            print("The Detected Number is: ", plate)
            return plate
        except Exception as e:
            print(e)
            pass

        '''Display'''
        # cv2.imwrite("try.jpg", new_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    