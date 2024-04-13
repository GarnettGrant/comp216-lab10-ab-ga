import paho.mqtt.client as mqtt
import json
from json import loads
import group_9_util as util


class subscriber:
    def __init__(self, topic='LAB9'):
        self.client = mqtt.Client()

        ## Assign the on_message delegate to the function message_handler
        self.client.on_message = subscriber.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        print(f'Subscriber listening to : {topic}\n...')

    ## 7. Create a function to decode the message, conert the decoded message to a dict using the json loads, call the function in utils to print the dictionary
    def message_handler(client, userdata, message):
        # print(f'Message received: {message.payload.decode("utf-8")}')
        ## Decode the Message
        decoded_message = message.payload.decode("utf-8")
        ## Convert the decoded message to a dictionary
        data = json.loads(decoded_message)
        ## Call the print_data function from the util module to print the dictionary
        util.print_data(data)

    def block(self):
        self.client.loop_forever()


sub = subscriber()
sub.block()
