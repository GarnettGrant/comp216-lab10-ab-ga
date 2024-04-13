import random
import time
import json
import group_9_data_generator
from json import dumps


## Initially set to favourite number. Used to number the payload

## Function that will create and return a dictionary with the payload
def create_data(list_x:list=[], x_min=0.0, x_max=200.0, samples=200.0):
    start_id = 777
    ocean_name = "Atlantic"
    sensor = group_9_data_generator.DataGenerator(x_min, x_max, samples)

    next_x, next_y = sensor.get_next_pair(list_x)
    data = {
        "id": start_id,
        "sea_level_pressure": int(random.uniform(1000, 1030)),
        "temperature": int(random.uniform(20, 30)),
        "sea_level": int(random.uniform(0, 10)),
        "year": next_x,
        "global_mean_sea_level": next_y,
        "ocean_name": ocean_name,
        "time_stamp": time.asctime(),
        "data": "Payload number " + str(start_id)
    }
    start_id += 1
    list_x.append(next_x)
    return dumps(data, indent=2), list_x


## function that will take a dict and print the parts in a  human-readable format
def print_data(data):
    ocean_dict = json.loads(data)
    print('\n')
    for key in ocean_dict:
        print(f"{key}: {ocean_dict[key]}")

# for i in range(samples):
#     next_x, next_y = sensor.get_next_pair(list_x)
#     print(str(next_x) + ", " + str(next_y))
#     list_x.append(next_x)
