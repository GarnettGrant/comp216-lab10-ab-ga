import random

import group_9_util as util
import json
from time import sleep
import paho.mqtt.client as mqtt


class publisher:
    def __init__(self, delay=0.05, topic='LAB9'):
        ## Create a client
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay
        self.x_min = 0.0
        self.x_max = 200.0
        self.samples = 200.0
        self.list_x = []
        self.list_y = []
        self.start_id = 0

    def publish(self):
        # x is used for counting the item's number
        x = 1
        #Continues looping forever
        while True:
            print(f'#{x}', end=' ')
            self.__publish()
            x += 1

    def __publish(self):
        # Get value from generator as dictionary
        dict_data, self.list_x, self.start_id = util.create_data(self.list_x, self.x_min, self.x_max, self.samples, self.start_id)
        # Convert the dictionary to a JSON string
        data = json.dumps(dict_data)
        # Sleep
        sleep(self.delay)
        print(f'Data: {data}')

        # miss transmissions 1 in every 100 times, non-deterministically
        # check if a random number between 0 and 1 is  than 0.99, which has a 1% chance of happening.
        # miss_transmission = (random.uniform(0, 1)) > 0.99
        # if not miss_transmission:
        # Connect to the server
        self.client.connect('localhost', 1883)
        # dict_data =  json.loads(dict_data)
        # If corrupt:
        # if corrupt_data:
        #     # Mutate (Fix) the data.
        #
        #
        #
        #     # Connect to the server, publish the message, print a message, and disconnect
        #     self.client.publish(self.topic, payload=data)
        #     print(f"Published to {self.topic}")
        #     sleep(self.delay)
        #     # Close the connection
        #     self.client.disconnect()
        #     return

        # Connect to the server, publish the message, print a message, and disconnect
        self.client.connect('localhost', 1883)
        self.client.publish(self.topic, payload=data)
        print(f"Published to {self.topic}")
        sleep(self.delay)
        # Close the connection
        self.client.disconnect()
        sleep(self.delay)


#    Extra:
#    • To simulate a real-world scenario, occasionally skip blocks of transmissions (or sets of transmission).
#    This condition must not throw the subscriber into confusion.
#    • Transmit “wild data” something that is completely off the chart.
#    Again your subscriber should be able to handle this.
#    • Anything that will add value to your project. You must make me aware of these.

import argparse
parser = argparse.ArgumentParser(description='Publisher Topic Selection')
parser.add_argument("-topic", required=True, help='Select the topic you would like to publish in.')
argslist = parser.parse_args()
print(argslist.topic)

pub = publisher(0.05, argslist.topic)
# Multiple messages are transmitted
pub.publish()
