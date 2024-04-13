import random

import group_9_util as util
import json
from time import sleep
import paho.mqtt.client as mqtt


class publisher:
    def __init__(self, delay=0.01, topic='LAB9'):
        ## Create a client
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay
        self.x_min = 0.0
        self.x_max = 200.0
        self.samples = 200.0
        self.list_x = []

    def publish(self, times=1):
        x = 1
        while True:
            print(f'#{x}', end=' ')
            self.__publish()
            x += 1

    def __publish(self):
        # Get value from generator as dictionary
        dict_data, self.list_x = util.create_data(self.list_x, self.x_min, self.x_max, self.samples)
        # Convert the dictionary to a JSON string
        data = json.dumps(dict_data)
        # Sleep
        sleep(self.delay)
        print(f'Data: {data}')

        # miss transmissions 1 in every 100 times, non-deterministically
        # check if a random number between 0 and 1 is  than 0.99, which has a 1% chance of happening.
        miss_transmission = (random.uniform(0, 1)) > 0.99
        if not miss_transmission:
            corrupt_data: bool = (random.uniform(0, 1)) > 0.95
            if corrupt_data:
                # Connect to the server, publish the message, print a message, and disconnect
                self.client.connect('localhost', 1883)
                self.client.publish(self.topic, payload=data)
                print(f"Published to {self.topic}")
                sleep(self.delay)
                # Close the connection
                self.client.disconnect()
                return

            # Connect to the server, publish the message, print a message, and disconnect
            self.client.connect('localhost', 1883)
            self.client.publish(self.topic, payload=data)
            print(f"Published to {self.topic}")
            sleep(self.delay)
            # Close the connection
            self.client.disconnect()
        sleep(self.delay)


pub = publisher()
# Multiple messages are transmitted
pub.publish()
