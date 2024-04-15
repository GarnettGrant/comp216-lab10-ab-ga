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
        self.amount_to_miss = 0.0

    def create_data(self):
        sensor = group_9_data_generator.DataGenerator(self.x_min, self.x_max, self.samples)
        next_x, next_y = sensor.get_next_pair(self.list_x)
        next_x = round(next_x, 3)
        next_y = round(next_y, 3)
        self.list_x.append(next_x)

        # Checks for corrupt data: (negative, in this case):
        # if next_y < 0:
        #     # Mutate (Fix) the data.
        #     height = abs(next_y)
        corrupt_data = (random.uniform(0, 100)) >= 95 and len(self.list_x) > 5
        if corrupt_data:
            next_y *= -1
            print("corrupt")

        extraneous_data = (random.uniform(0, 100)) <= 5 and len(self.list_x) > 5
        if extraneous_data:
            next_x = self.list_x[-2]
            print("extraneous")

        data = {
            "id": self.start_id,
            "sea_level_pressure": int(random.uniform(1000, 1030)),
            "temperature": int(random.uniform(20, 30)),
            "year": next_x,
            "global_mean_sea_level": next_y,
            "time_stamp": time.asctime(),
        }
        # Increments start id
        self.start_id += 1
        # Appends new x to the list to generate the next pair of values later
        # convert the data dictionary into json
        dict_data = json.dumps(data, indent=2)
        return dict_data

    def publish(self):
        # x is used for counting the item's number
        x = 1
        # Continues looping forever
        while True and self.gui.status:
            print(f'#{x}', end=' ')
            self.__publish()
            x += 1

    def __publish(self):
        # Get value from generator as dictionary
        dict_data = self.create_data()
        # Convert the dictionary to a JSON string
        data = json.dumps(dict_data)
        # Sleep
        sleep(self.delay)

        # Miss transmissions 1 in every 100 times, non-deterministically (randomly) check if a random number between
        # 0 and 100 is less than or equal to 1, which has a 1% chance of happening (depending on whether the 100 is
        # inclusive or exclusive. The method is definition is unclear).
        miss_transmission = (random.uniform(0, 100)) <= 1
        if miss_transmission:  # do not transmit any data
            print(f'transmission missed')
            return
            # height = json.loads(dict_data)["global_mean_sea_level"]
        # This is the same as before, but this time a block of five transmissions is skipped.
        miss_transmission_block = (random.uniform(0, 100)) >= 90
        if miss_transmission_block:
            self.amount_to_miss = 5
            print(f'multiple transmissions are being missed')
            return
        if self.amount_to_miss > 0:
            self.amount_to_miss -= 1
            print(f'multiple transmissions are being missed')
            return
        print(f"Data: {data}")
        # Connect to the server, publish the message, print a message, and disconnect
        self.client.connect('localhost', 1883)
        self.client.publish(self.topic, payload=data)
        # Update the gui to prevent it from freezing after being blocked by the publisher
        self.gui.update()
        self.gui.update_idletasks()
        # Sleep, then disconnect
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
        # Set status to be used to close the gui in the __publish method
        self.status = True
        # Set topic to none temporarily, will be corrected when the user clicks a button on the gui
        self.topic = None
        # Set gui parameters
        self.master.title('Publisher Gui')
        self.pack(fill=BOTH, expand=1)
        # Create gui widgets
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
        entry = tkinter.Entry(canvas, foreground='#272946', name="topic", font=('calibri', 12, 'bold'))
        # Pack gui widgets
        quit.pack(side=tkinter.BOTTOM)
        button.pack(side=tkinter.BOTTOM)
        label.pack(side=tkinter.BOTTOM)
        entry.pack(side=tkinter.BOTTOM)
        label2.pack(side=tkinter.BOTTOM)

    def publish_data(self):
        # This method retrieves the selected topic from the gui's Entry widget, and creates a new instance of the
        # publisher which sends data to that topic
        self.topic = self.nametowidget("content_canvas.topic").get()
        pub = publisher(interface=self, delay=0.05, topic=self.topic)
        pub.publish()

    def close(self):
        # This method closes the publisher gui and halts the publisher from sending more data to the subscriber.
        #
        # Because self.master.destroy() and sys.exit() were separately unable to close the publisher,I added a check
        # for the status of the gui in the main __publisher() loop. Additionally, both sys.exit() and
        # self.master.destroy were called in order to ensure the app does not run after the publisher is closed
        self.status = False
        self.master.destroy()
        sys.exit()

# Create instance of gui
root = tkinter.Tk()
gui = Gui()
# Set gui dimensions and screen position
root.geometry('400x250+550+300')
gui.mainloop()
