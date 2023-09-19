from logic import VideoInfer
from api_request import get_one_record

if __name__ == "__main__":
    vehicle_plate = VideoInfer().image_manipulate()
    get_one_record(vehicle_plate)