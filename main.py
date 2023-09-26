import os
from pprint import pprint

from anpr_predict import YoloModel
from api_request import get_one_record

load_weights = os.path.join("assets", "anpr_v2.pt")
load_images = os.path.join("datasets", "plates")


def main():
    count = 1
    anpr_plate_list = []
    for root, dirs, files in os.walk(load_images):
        for file in sorted(files):
            imgpath = os.path.join(root, file)
            run = YoloModel(img_source=imgpath, weights_path=load_weights)
            vehicle_plate = run.predict(count)
            result = get_one_record(vehicle_plate)
            print(result)
            # anpr_plate_list.append(dct)
            count += 1
    pprint(anpr_plate_list)


if __name__ == "__main__":
    main()
