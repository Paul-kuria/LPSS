from typing import List 
import requests
import json 
import csv 

example_licence = "KCX623S"
new_member: dict = {
    "name": "Mike Mann",
    "vehicle_type" : "Mazda Demio",
    "vehicle_color" : "Silver",
    "vehicle_plate" : "KBH143Y"
}

'''Fetch One Record'''
def get_one_record(vehicle_id):
    url = f"http://127.0.0.1:8000/members/{vehicle_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            member = response.json()
            print(member) 
    except Exception as e:
        print(e)

'''Update One Record'''
def update_one_record(vehicle_id: str, updated_data: dict):
    url = f"http://127.0.0.1:8000/members/{vehicle_id}"
    try:
        # Send a PUT  request with the updated data as JSON in the request body
        response = requests.put(url, json=updated_data)

        if response.status_code == 200:
            member = response.json()
            print(f"Updated member: {member}")
        
        elif response.status_code == 404:
            print("Member not found.")

    except Exception as e:
        print(f"{e}: HTTP request failed with status code: {response.status_code}")

'''Delete One Record'''
def delete_one_record(vehicle_id):
    url = f"http://127.0.0.1:8000/members/{vehicle_id}"
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            print(f"Successfully deleted member with vehicle {vehicle_id}")
    except Exception as e:
        print(e)


'''Fetch All Records'''
def fetch_records():
    url = "http://127.0.0.1:8000/members/all/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() 
            for i in data:
                print(i)
    except Exception as e:
        print(e)


'''Upload Many Records'''
def upload_records():
    url = "http://127.0.0.1:8000/members/upload/"

    count = 0
    with open("./update.csv", 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        rows = list(reader) # Convert to a list of dictionaries
    try:
        response = requests.post(url, json=rows)
        print(response.text)
        if response.status_code == 200:
            print("Successfully uploaded data")
        else:
            print(f"HTTP request failed with status code: {response.status_code}")
    except Exception as e:
        print(e)



if __name__ == "__main__":
    # update_one_record(
    #     vehicle_id="b", 
    #     updated_data=new_member)
    upload_records()
