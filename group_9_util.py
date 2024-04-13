import random
import time
import json
from json import dumps
## Initially set to favourite number. Used to number the payload
start_id = 777
ocean_name = "Atlantic"

## Function that will create and return a dictionary with the payload
def create_data():
    global start_id
    global ocean_name
    start_id += 1
    data = {
        "id": start_id,
        "sea_level_pressure":int(random.uniform(1000, 1030)),
        "temperature":int(random.uniform(20, 30)),
        "sea_level":int(random.uniform(0, 10)),
        "ocean_name": ocean_name,
        "time": time.asctime(),
        "data": "Payload number " + str(start_id)
    }
    return dumps(data, indent=2)

## function that will take a dict and print the parts in a  human-readable format
def print_data(data):
    ocean_dict = json.loads(data)
    print('\n')
    for key in ocean_dict:
        print(f"{key}: {ocean_dict[key]}")