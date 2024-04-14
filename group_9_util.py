import random
import time
import json
import group_9_data_generator
from json import dumps



## Initially set to favourite number. Used to number the payload

## Function that will create and return a dictionary with the payload
def create_data(list_x:list=[], x_min=0.0, x_max=200.0, samples=200.0, id=0.0):
    start_id = id
    sensor = group_9_data_generator.DataGenerator(x_min, x_max, samples)
    next_x, next_y = sensor.get_next_pair(list_x)
    data = {
        "id": start_id,
        "sea_level_pressure": int(random.uniform(1000, 1030)),
        "temperature": int(random.uniform(20, 30)),
        "year": round(next_x,3),
        "global_mean_sea_level": round(next_y,3),
        "time_stamp": time.asctime(),
    }
    start_id += 1
    list_x.append(next_x)
    dict_data = dumps(data, indent=2)
    load = json.loads(dict_data)
    # print(f"data from util: {dict_data}")
    # print(f"loaded: {load}")
    return dict_data, list_x, start_id


## function that will take a dict and print the parts in a  human-readable format
def print_data(data):
    ocean_dict = json.loads(data)
    print('\n')
    for key in ocean_dict:
        print(f"{key}: {ocean_dict[key]}")

# graph:None
# def graph_data(x, y):
#     if graph:
#         graph.update_plot(x, y)
#     else:
#         graph = DynamicGraph()
# for i in range(200):
#     print(create_data()[1])