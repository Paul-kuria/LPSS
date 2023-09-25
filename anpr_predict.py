from ultralytics import YOLO
import supervision as sv
import os 
import cv2 
import numpy as np 
import pytesseract
import easyocr
from pprint import pprint




class YoloModel:
    def __init__(self, img_source, weights_path) -> None:
        self.img_source = img_source 
        self.weights = weights_path

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
    
    def predict(self, counts):
        plate_dict = {}
        img_names = self.img_source.split('/')[-1]

        image = cv2.imread(self.img_source)
        model = YOLO(self.weights)
        results = model(image)[0]
        detections = sv.Detections.from_yolov8(results)

        # Draw bboxes annotations:
        box_annotator = sv.BoxAnnotator(
            thickness=1, text_thickness=1, text_scale=1
        )
        labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for xyxy, confidence, class_id, tracker_id
                in detections
                ]
        conf = [
                confidence
                for _, confidence, class_id, _
                in detections
                ][0]  
        # print(conf)

        # Extract only plate bbox with high confidence thresholds
        if conf > 0.6:
            frame = box_annotator.annotate(
                    scene=image,
                    detections=detections,
                    labels=labels
                )
            bbox = detections.xyxy[0]
            x1, y1, x2, y2 = bbox.astype(int)

            # Create a mask the same size as the image
            mask = np.zeros_like(image)
            
            cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), thickness=cv2.FILLED)
            extracted_region = cv2.bitwise_and(image, mask)

            plate_roi = image[y1: y2, x1: x2]
            
            text = pytesseract.image_to_string(plate_roi, config = '--psm 11')
            reader = easyocr.Reader(['en'], gpu=False)
            ocr_result = reader.readtext(plate_roi)
            ocr_text = ''
            for result in ocr_result:
                ocr_text += result[1] + ' '
            try:
                # plate = self.licence_plate_to_text(text)
                plate = self.licence_plate_to_text(ocr_text)
                print("The Detected Number is: ", plate)
                plate_dict[img_names] = plate
                # return plate_dict
                return plate
            except Exception as e:
                print(f"Error: {e}. Image prediction failed.")
                pass
            # '''Display'''
            # cv2.imwrite(f"datasets/output/img_{counts}.jpg", new_img)


    


def main():
    
    count = 1
    anpr_plate_list = []
    for root, dirs, files in os.walk(load_images):
        for file in sorted(files):
            imgpath = os.path.join(root, file)
            # print(imgpath)
            run = YoloModel(
                img_source=imgpath,
                weights_path=load_weights
            )
            dct = run.predict(count)
            anpr_plate_list.append(dct)
            count += 1
    pprint(anpr_plate_list)

if __name__ == "__main__":
    main()
