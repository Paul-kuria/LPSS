import csv
import os
from datetime import datetime

import cv2
import numpy as np
from detection.detector import Detector
from detectron2 import model_zoo
from argparse import ArgumentParser

class Predict:
    # Some predefines
    COLOR = (255, 255, 255)
    COLOR_BLUE = (255, 0, 0)
    COLOR_RED = (0, 0, 255)
    THICKNESS = 2
    manifest_list = ["BED"]

    def __init__(self, dest_folder, model_path):
        self.naming = datetime.now().strftime("%y_%m_%d_%H:%M:%S")
        self.source_folder = self.enter_location()
        self.destination = os.path.join(dest_folder, self.naming)
        self.csvpath = f"{self.destination}/{self.naming}.csv"
        self.model_path = model_path
        self.variety_name = "001-HTF"

        if not os.path.exists(self.source_folder):
            print(f"WARNING: File '{self.source_folder}' does not exist!")
            exit(0)

        if not os.path.exists(self.destination):
            os.makedirs(self.destination, exist_ok=True)
    
    def enter_location(self):
        parser = ArgumentParser(description="Inputs folder to be created")
        parser.add_argument("file", metavar="file", type=str, help="Alchemy_A: 5, Alchemy_B: 6, Alchemy_C: 7")
        args = parser.parse_args()
        return args.file 
    
    def bed_detection(self, img_file: str):
        # Input image read with cv2
        image_input = cv2.imread(img_file)

        # Input video properties
        scale = 20
        width = int(image_input.shape[1] * scale / 100)
        height = int(image_input.shape[0] * scale / 100)
        print(f"{img_file} frame size is {width}x{height}.")
        resize_img = cv2.resize(src=image_input, dsize=(width, height))
        new_img = cv2.resize(src=image_input, dsize=(width, height))

        # Get detected points
        inferrer = Detector(
            variety_name=self.variety_name,
            weights_path=self.model_path,
            class_names=self.manifest_list,
        )
        iname = img_file.split("/")[-1].split(".")[0]
        block = img_file.split("/")[-2]

        detected_box = inferrer.box_coordinates(image=new_img)
        draw_boxes = inferrer.bbox(detected_box)[0]
        draw_lines = inferrer.bbox(detected_box)[1]

        x_min, y_min, x_max, y_max = draw_boxes[:]  # Needed y_min and y_max
        top, bottom, length = draw_lines[:]

        """IS_mask_list
        _inputs: save_points, center, top_center, bottom_center
        _outputs: image
        """
        detected_masks = inferrer.test_area(image=new_img)
        # print(detected_masks)
        # exit()

        points_array = np.array(detected_masks[0], dtype=np.int32)
        center, topcenter, bottomcenter, bedlength = (
            detected_masks[1],
            detected_masks[2],
            detected_masks[3],
            detected_masks[4]
        )
        # top_y = detected_masks[4]
        # top = (center[0], top_y)
        top = (center[0], topcenter[1])
        bottom = (center[0], bottomcenter[1])

        """Masking"""
        background = np.zeros_like(
            resize_img
        )  # np.zeros(image_input.shape[:2], dtype='uint8')
        cv2.fillPoly(background, [points_array], color=self.COLOR)
        masked = cv2.bitwise_and(resize_img, background)

        """Polyline & Centerline"""
        cv2.polylines(
            masked,
            [points_array],
            isClosed=False,
            color=self.COLOR_RED,
            thickness=self.THICKNESS,
        )
        cv2.circle(masked, center, 8, self.COLOR_RED, -1)
        cv2.line(masked, (top), (bottom), self.COLOR_RED, self.THICKNESS)

        """Save Bed Image"""
        self.naming = datetime.now().strftime("%H:%M:%S")
        # cv2.imwrite(f"{self.destination}/out_{self.naming}.JPG", new_img)
        cv2.imwrite(f"{self.destination}/masks_{iname}.JPG", masked)
        lists = [iname, width, bedlength, block]
        print(lists)
        # return lists
        with open(self.csvpath, "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(lists)

def main():
    detection = Predict(
        # source_folder="dataset/images/wild_28th",
        dest_folder="dataset/results",
        model_path="./assets/model_final_v2.pth",
    )
    for root, subdirs, files in os.walk(detection.source_folder):
        for file in files:
            img = os.path.join(root, file)
            try:
                detection.bed_detection(img)

                
            except Exception as e:
                print(e)
                pass


if __name__ == "__main__":
    main()