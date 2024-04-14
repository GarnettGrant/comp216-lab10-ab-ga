from time import sleep

import paho.mqtt.client as mqtt
import json
import tkinter
from json import loads

from group_9_graph import DynamicGraph
import group_9_util as util


class subscriber:
    def __init__(self, topic='LAB9'):
        self.client = mqtt.Client()

        ## Assign the on_message delegate to the function message_handler
        self.client.on_message = subscriber.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        self.graph = DynamicGraph()
        self.client.graph = self.graph
        print("created")
        # self.client.graph.display_textbox.insert(f"sea_level_pressure: \n")
        # self.client.graph.display_textbox.insert(f"temperature: \n")
        # self.client.graph.display_textbox.insert(f"year: \n")
        # self.client.graph.display_textbox.insert(f"global_mean_sea_level: \n")
        # self.client.graph.display_textbox.insert(f"time_stamp: \n")

        # create graph
        # self.graph = DynamicGraph()
        print(f'Subscriber listening to : {topic}\n...')

    ## 7. Create a function to decode the message, conert the decoded message to a dict using the json loads, call the function in utils to print the dictionary
    def message_handler(client, userdata, message):
        # Decode the Message
        decoded_message = message.payload.decode("utf-8")
        # Convert the decoded message to json string
        unformatted_data = json.loads(decoded_message)
        # Format the data as a proper dict which we can retrieve items from
        data = json.loads(unformatted_data)

        id = str(data["id"])
        sea_level_pressure = str(data["sea_level_pressure"])
        temperature = str(data["temperature"])
        year = str(data["year"])
        global_mean_sea_level = str(data["global_mean_sea_level"])
        time_stamp = str(data["time_stamp"])

        # update the graph
        client.graph.update_plot(year, global_mean_sea_level)
        client.graph.update_text(id, sea_level_pressure, temperature, year, global_mean_sea_level, time_stamp)
        client.graph.update()
        client.graph.update_idletasks()
        # sleep(2)

    def block(self):
        self.client.loop_forever()


import argparse
parser = argparse.ArgumentParser(description='Subscriber Topic Selection')
parser.add_argument("-topic", required=True, help='Select the topic you would like to listen to.')
argslist = parser.parse_args()
print(argslist.topic)

sub = subscriber(argslist.topic)

sub.graph.after(0, sub.block) #no different from just sub.block()

sub.graph.mainloop()

