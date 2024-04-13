import group_9_util as util
import json
from time import sleep
import paho.mqtt.client as mqtt

class publisher:
    def __init__(self, delay =0.75, topic='LAB9'):
        ## Create a client
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay

    def publish(self, times=1):
        for x in range(times):
            print(f'#{x}', end=' ' )
            self.__publish()

    def __publish(self):
        ## Call the create_data method from the util module to obtain a dictionary
        dict_data = util.create_data()
        ## Convert the dictionary to a JSON string
        data = json.dumps(dict_data)
        print(f'{data} to broker')
        ## Connect to the server, publish the message, print a message, and disconnect
        self.client.connect('localhost', 1883)
        self.client.publish(self.topic, payload=data)
        print(f"Published to {self.topic}")
        sleep(self.delay)                           #necessary
        ## Close the connection
        self.client.disconnect()

pub = publisher()
## Multiple messages are transmitted
pub.publish(10)