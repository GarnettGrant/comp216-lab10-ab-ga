import random
import tkinter
import group_9_data_generator
import threading
import time
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


class DynamicGraph:
    def __init__(self, xmin=0.0, xmax=200.0, samples=200):
        self.xmin = xmin
        self.xmax = xmax
        self.samples = samples

        self.root = tkinter.Tk()
        self.root.wm_title("Water Levels Figure")
        self.fig = Figure(figsize=(6, 5))
        self.plot = self.fig.add_subplot()
        self.sensor = group_9_data_generator.DataGenerator(xmin, xmax, samples)
        self.x, self.y = self.sensor.plot()
        self.length = len(self.y)
        self.i = 1 / self.length
        self.plot_graph()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()

        self.button_generate = tkinter.Button(master=self.root, text="Update", command=self.create_thread)
        self.button_quit = tkinter.Button(master=self.root, text="Quit", command=self.root.destroy)
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

    def update_plot(self, new_y=0.0):
        while not self.done:
            # add the next x position, following the pattern from the data generator
            # because we start at 1880, we subtract 1880 from x
            self.x.append((len(self.x)+1) * (135.0/self.samples) + 1880)
            # add random noise to this new y position and then append to the list
            new_y = (200 / pow(135, 2)) * pow(self.x[-1] - 1880, 2)
            noise = abs(random.gauss(0, new_y * 0.035)) + random.uniform(0, 5)

            self.y.append(new_y + noise)
            # self.x.pop(0)
            # self.y.pop(0)
            # line.set
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
        self.toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


graph = DynamicGraph(0, 200, 200)
