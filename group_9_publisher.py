import random
import sys
import time
import tkinter
from tkinter import BOTH, W

import group_9_data_generator
import json
from time import sleep
import paho.mqtt.client as mqtt


class publisher:
    def __init__(self, interface, delay=0.05, topic='LAB9'):
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
        self.gui = interface
    def create_data(self, list_x: list = [], x_min=0.0, x_max=200.0, samples=200.0, id=0.0):
        start_id = id
        sensor = group_9_data_generator.DataGenerator(x_min, x_max, samples)
        next_x, next_y = sensor.get_next_pair(list_x)
        next_x = round(next_x,3)
        next_y = round(next_y,3)

        # Checks for corrupt data: (negative, in this case):
        # if next_y < 0:
        #     # Mutate (Fix) the data.
        #     height = abs(next_y)

        data = {
            "id": start_id,
            "sea_level_pressure": int(random.uniform(1000, 1030)),
            "temperature": int(random.uniform(20, 30)),
            "year": next_x,
            "global_mean_sea_level": next_y,
            "time_stamp": time.asctime(),
        }
        # Increments start id
        self.start_id += 1
        # Appends new x to the list to generate the next pair of values later
        list_x.append(next_x)
        # convert the data dictionary into json
        dict_data = json.dumps(data, indent=2)

        return dict_data, list_x, start_id

    def publish(self):
        # x is used for counting the item's number
        x = 1
        #Continues looping forever
        while True and self.gui.status:
            print(f'#{x}', end=' ')
            self.__publish()
            x += 1

    def __publish(self):
        # Get value from generator as dictionary
        dict_data, self.list_x, self.start_id = self.create_data(self.list_x, self.x_min, self.x_max, self.samples, self.start_id)
        # Convert the dictionary to a JSON string
        data = json.dumps(dict_data)
        # Sleep
        sleep(self.delay)
        print(f'Data: {data}')

        # miss transmissions 1 in every 100 times, non-deterministically (randomly)
        # check if a random number between 0 and 1 is  than 0.99, which has a 1% chance of happening.
        miss_transmission = (random.uniform(0, 1)) > 0.99
        if miss_transmission: # do not transmit any data
           return
            # height = json.loads(dict_data)["global_mean_sea_level"]

        # Connect to the server, publish the message, print a message, and disconnect
        self.client.connect('localhost', 1883)
        self.client.publish(self.topic, payload=data)
        # # Convert from json to string
        # unformatted_data = json.loads(data)
        # # Convert from string to dictionary
        # formatted_data = json.loads(unformatted_data)
        # print(formatted_data)
        # # Store the data in variables to update the tkinter.Text listing the latest published data.
        # id = str(formatted_data["id"])
        # sea_level_pressure = str(formatted_data["sea_level_pressure"])
        # temperature = str(formatted_data["temperature"])
        # year = str(formatted_data["year"])
        # global_mean_sea_level = str(formatted_data["global_mean_sea_level"])
        # time_stamp = str(formatted_data["time_stamp"])
        # # Use the above values to update the Textbox
        # self.gui.update_text(self.topic, id, sea_level_pressure, temperature, year, global_mean_sea_level, time_stamp)
        self.gui.update()
        self.gui.update_idletasks()

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

# import argparse
# parser = argparse.ArgumentParser(description='Publisher Topic Selection')
# parser.add_argument("-topic", required=True, help='Select the topic you would like to publish in.')
# argslist = parser.parse_args()
# print(argslist.topic)


class Gui(tkinter.Frame):
    def __init__(self):
        super().__init__()
        self.status = True
        self.topic = None
        self.master.title('Publisher Gui')
        self.pack(fill=BOTH, expand=1)

        canvas = tkinter.Canvas(self, background="#eda031", name="content_canvas")

        canvas.pack(fill=BOTH, expand=1)

        button = tkinter.Button(canvas, text="BEGIN", command=self.publish_data, anchor=W, background='#eda031',
                            foreground='#272946')
        quit = tkinter.Button(canvas, text="QUIT", command=self.close, anchor=W, background='#eda031',
                            foreground='#272946')
        label = tkinter.Label(canvas, text="Start Publishing:", background='#eda031', foreground='#272946',
                           font=('calibri', 12, 'bold'))
        label2 = tkinter.Label(canvas, text="Publish to which topic?:", background='#eda031', foreground='#272946',
                           font=('calibri', 12, 'bold'))
        quit.pack(side=tkinter.BOTTOM)
        entry = tkinter.Entry(canvas, foreground='#272946', name="topic", font=('calibri', 12, 'bold'))
        text = tkinter.Text(master=self, height=7,foreground='#272946')
        text.pack(side=tkinter.BOTTOM)
        button.pack(side=tkinter.BOTTOM)
        label.pack(side=tkinter.BOTTOM)
        entry.pack(side=tkinter.BOTTOM)
        label2.pack(side=tkinter.BOTTOM)

    def publish_data(self):
        self.topic = self.nametowidget("content_canvas.topic").get()
        pub = publisher(interface=self, delay=0.05, topic=self.topic)
        pub.publish()
    def close(self):
        self.status = False
        self.master.destroy()
        sys.exit()

    # def update_text(self, topic="null", id="null", sea_level_pressure="null", temperature="null", year="null", global_mean_sea_level="null", time_stamp="null"):
    #     # Clear textbox text
    #     self.text.delete('1.0', tkinter.END)
    #     # Insert all fields at once, separated by newlines "\n"
    #     self.text.insert(tkinter.INSERT, f"Publishing to topic: {topic}\n"
    #                                 f"id: {id}\n"
    #                                 f"sea_level_pressure: {sea_level_pressure}\n"
    #                                 f"temperature: {temperature}\n"
    #                                 f"year: {year}\n"
    #                                 f"global_mean_sea_level: {global_mean_sea_level}\n"
    #                                 f"time_stamp: {time_stamp}\n")



root = tkinter.Tk()
gui = Gui()
root.geometry('400x250+550+300')
gui.mainloop()

