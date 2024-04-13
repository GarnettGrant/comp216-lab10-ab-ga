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


class DynamicGraph:
    def __init__(self, initial_x=0.0, initial_y=0.0):
        self.root = tkinter.Tk()
        self.root.geometry('600x700+550+50')
        self.root.wm_title("Water Levels Figure")
        self.fig = Figure(figsize=(6, 5))
        self.plot = self.fig.add_subplot()

        self.x = []
        self.y = []
        self.x.append(initial_x)
        self.y.append(initial_y)

        self.plot_graph()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()

        self.display_textbox = tkinter.Text(master=self.root, height=7, width= 20)
        self.button_generate = tkinter.Button(master=self.root, text="Update", command=self.create_thread)
        self.button_quit = tkinter.Button(master=self.root, text="Quit", command=sys.exit)
        self.done = False
        self.pack_all()
        self.thread = None
        tkinter.mainloop()

    def plot_graph(self):
        self.plot.plot(self.x, self.y, "b")
        self.plot.fill_between(self.x, self.y)
        self.plot.set_xlabel('Time, in years')
        self.plot.set_ylabel('Rise in global sea levels, in millimeters')
        self.plot.set_title('Global rise in sea levels since 1880')
        if not hasattr(self, "canvas"):
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

    def update_plot(self, new_y=0.0, new_x=0.0):
        while not self.done:
            self.y.append(new_y)
            self.x.append(new_x)
            self.plot.clear()
            self.plot_graph()
            # redraw graph
            self.canvas.draw()
            time.sleep(0.1)

    def create_thread(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.update_plot, daemon=True)
            self.thread.start()

    def pack_all(self):
        self.button_quit.pack(side=tkinter.BOTTOM)
        self.button_generate.pack(side=tkinter.BOTTOM)
        self.display_textbox.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=False)
        self.toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


graph = DynamicGraph()
