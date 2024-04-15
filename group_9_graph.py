import random
import sys
import tkinter
import group_9_data_generator
import threading
import time
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


class DynamicGraph(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        # Set graph and tkinter attributes
        self.wm_title("Subscriber's Dynamic Water Levels Graph")
        self.fig = Figure(figsize=(6, 5))
        self.plot = self.fig.add_subplot()
        # Create placeholder variables for the x-axis list and y-axis list of positions
        self.x = []
        self.y = []
        # Set up graph
        self.plot_graph()
        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        # Add tkinter.Text widget for outputting recieved data.
        self.display_textbox = tkinter.Text(master=self, height=7, width=20)
        # Add quit button
        self.button_quit = tkinter.Button(master=self, text="Quit", command=self.destroy)
        self.done = False
        self.pack_all()
        self.thread = None

    def plot_graph(self):
        # This method contains the code required to set up, redraw, or update the graph

        # Set plot attributes and style
        self.plot.plot(self.x, self.y, "b")
        self.plot.fill_between(self.x, self.y)
        self.plot.set_xlabel('Time, in years')
        self.plot.set_ylabel('Rise in global sea levels, in millimeters')
        self.plot.set_title('Global rise in sea levels since 1880')
        # If the canvas does not exist, create it before moving forward
        if not hasattr(self, "canvas"):
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        # Redraw canvas
        self.canvas.draw()
        # Update tkinter gui
        self.update()
        self.update_idletasks()

    def update_plot(self, new_x, new_y):
        # This method takes in the data retrieved and parsed from the json payload sent from the publisher class,
        # and adds it to the currently held list of x and y positions, and then the graph is updated and redrawn to
        # include these positions

        print(f"new_x: {new_x}, new_y: {new_y}")
        self.y.append(float(new_y))
        self.x.append(float(new_x))
        self.plot.clear()
        self.plot_graph()
        # redraw graph
        self.canvas.draw()


    def update_text(self, topic="null", id="null", sea_level_pressure="null", temperature="null", year="null", global_mean_sea_level="null", time_stamp="null"):
        # This method clears the current text, and then inserts the most recent data retrieved by the subscriber.

        # Clears textbox text before inserting new data.
        self.display_textbox.delete('1.0', tkinter.END)
        # Insert all fields from the json data into the "display_textbox" all at once, separated by newlines. ("\n")
        self.display_textbox.insert(tkinter.INSERT, f"Listening to topic: {topic}\n"
                                    f"id: {id}\n"
                                    f"sea_level_pressure: {sea_level_pressure}\n"
                                    f"temperature: {temperature}\n"
                                    f"year: {year}\n"
                                    f"global_mean_sea_level: {global_mean_sea_level}\n"
                                    f"time_stamp: {time_stamp}\n")

    def pack_all(self):
        # Pack all the items to the bottom of the screen
        self.button_quit.pack(side=tkinter.BOTTOM)
        self.display_textbox.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=False)
        self.toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


# graph = DynamicGraph()
# # graph.update_plot(graph.x)
# graph.mainloop()
# graph.after(0, graph.update_())
# graph.mainloop()
# graph.root.mainloop()
# graph.update_text("test2")
# graph.update()
# graph.update_idletasks()
# graph.mainloop()
# graph.root.mainloop()
#
#
