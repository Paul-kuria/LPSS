import os 
from logic import VideoInfer
from api_request import get_one_record

def main():
    vehicles = "./datasets"
    ANPR = VideoInfer()

    for root, dirs, files in os.walk(vehicles):
        for file in sorted(files):
            path = os.path.join(root, file)
            print(file)
            ANPR.image_manipulate(path)
    # get_one_record(vehicle_plate)

if __name__ == "__main__":
    main()
