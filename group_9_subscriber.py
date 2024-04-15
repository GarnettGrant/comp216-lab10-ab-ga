from time import sleep
from tkinter import BOTH, W

import paho.mqtt.client as mqtt
import json
import tkinter
from json import loads

from group_9_graph import DynamicGraph


class subscriber:
    def __init__(self, topic='LAB9'):
        self.client = mqtt.Client()

        ## Assign the on_message delegate to the function message_handler
        self.client.on_message = subscriber.message_handler
        # Connect to port 1883
        self.client.connect('localhost', 1883)
        # Subscribe to the selected topic
        self.client.subscribe(topic)
        # Create an instance of our DynamicGraph class to plot the values from the publisher
        self.graph = DynamicGraph()
        # Reference self.graph inside self.client.graph so we can access it inside our message handler
        self.client.graph = self.graph
        # allow self.client to access the topic information within the message handler
        self.client.topic = topic

        # print(f'Subscriber listening to : {topic}\n...') # for debugging

    def message_handler(client, userdata, message):
        # Decodes the message retrieved from the publisher
        decoded_message = message.payload.decode("utf-8")
        # Convert the decoded message to json string
        unformatted_data = json.loads(decoded_message)
        # Format the data as a proper dict which we can retrieve items from
        data = json.loads(unformatted_data)

        # Store the data in variables to later update the tkinter.Text under the graph.
        id = str(data["id"])
        sea_level_pressure = str(data["sea_level_pressure"])
        temperature = str(data["temperature"])
        year = float(data["year"])
        global_mean_sea_level = float(data["global_mean_sea_level"])
        time_stamp = str(data["time_stamp"])

        # Check for corrupt data (negative Y values):
        if global_mean_sea_level < 0:
            global_mean_sea_level *= -1 # Multiply by -1 to become positive

        # Check for extraneous data (x values which already exist):
        if year in client.graph.x:
            return  # Do not plot this data. Ignore.

        # Update the graph
        client.graph.update_plot(year, global_mean_sea_level)
        print(year, global_mean_sea_level)
        client.graph.update_text(client.topic, id, sea_level_pressure, temperature, year, global_mean_sea_level, time_stamp)

        # Because the subscriber is blocking (looping forever and preventing code after it from running), we have to
        # use "update()" and "update_idletasks()". "mainloop()" is not appropriate here because it would also block
        # if called.
        client.graph.update()
        client.graph.update_idletasks()

    def block(self):
        # This method tells the subscriber to loop forever
        self.client.loop_forever()

class Gui(tkinter.Frame):
    def __init__(self):
        super().__init__()
        # Set gui parameters
        self.master.title('Subscriber Topic Selector')
        self.pack(fill=BOTH, expand=1)

        #Create gui widgets
        canvas = tkinter.Canvas(self, background="#eda031", name="content_canvas")

        canvas.pack(fill=BOTH, expand=1)

        button = tkinter.Button(canvas, text="BEGIN", command=self.listen, anchor=W, background='#eda031',
                            foreground='#272946')
        quit = tkinter.Button(canvas, text="QUIT", command=self.master.destroy, anchor=W, background='#eda031',
                              foreground='#272946')
        label = tkinter.Label(canvas, text="Start Listening:", background='#eda031', foreground='#272946',
                           font=('calibri', 12, 'bold'))
        label2 = tkinter.Label(canvas, text="Listen to which topic?:", background='#eda031', foreground='#272946',
                           font=('calibri', 12, 'bold'))
        entry = tkinter.Entry(canvas, foreground='#272946', name="topic", font=('calibri', 12, 'bold'))

        # Pack gui widgets

        quit.pack(side=tkinter.BOTTOM)
        button.pack(side=tkinter.BOTTOM)
        label.pack(side=tkinter.BOTTOM)
        entry.pack(side=tkinter.BOTTOM)
        label2.pack(side=tkinter.BOTTOM)

    def listen(self):
        # This method obtains the topic to listen to and then creates an instance of the subscriber, then sets
        # blocking to true (subscriber will loop forever)
        topic = self.nametowidget("content_canvas.topic").get()
        sub = subscriber(topic)
        sub.graph.after(0, sub.block) # same as sub.block(), no difference in execution
        # start graph and loop
        sub.graph.mainloop()

# Create instance of gui
root = tkinter.Tk()
gui = Gui()
# Set gui dimensions and screen position
root.geometry('400x250+550+300')
gui.mainloop()

# import argparse
# parser = argparse.ArgumentParser(description='Subscriber Topic Selection')
# parser.add_argument("-topic", required=True, help='Select the topic you would like to listen to.')
# argslist = parser.parse_args()
# print(argslist.topic)

# sub = subscriber("first")
# sub.graph.after(0, sub.block) #no different from just sub.block()
# sub.graph.mainloop()

