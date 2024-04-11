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
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Water Levels Figure")
        self.fig = Figure(figsize=(12, 4), dpi=100)
        self.plot = self.fig.add_subplot()
        self.sensor = group_9_data_generator.DataGenerator(0.0, 200.0, 200)
        self.x, self.y = self.sensor.plot()
        self.length = len(self.y)
        self.i = 1 / self.length
        self.plot_graph()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()
        self.button_quit = tkinter.Button(master=self.root, text="Quit", command=self.root.destroy)
        self.done = False
        self.pack_all()
    def plot_graph(self):
        self.plot.plot(self.x, self.y, "b")
        self.plot.fill_between(self.x, self.y)
        self.plot.set_xlabel('Time, in years')
        self.plot.set_ylabel('Rise in global sea levels, in millimeters')
        self.plot.set_title('Global rise in sea levels since 1880')
        if (hasattr(self, "canvas")) == False:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
    def update_plot(self):
        while not self.done:
            print(self.y)
            # abs(self.__generator("gaussian", self.i * 0.035)) + self.__generator("uniform") * 5 + i

            # # m is the y-range of the graph
            # m = (self.xmax - self.xmin + 1 / self.n)
            # c = self.xmin
            # # list_x is the returned value (output of the method _generator() when using the parameter("constant"))
            # list_x = self.__generator("constant")  # returns a list of normalized values between 0 and 1
            # # print(f"x: {list_x}")
            # # y = mx + c, the required linear transformation
            # y = [(m * x) + c for x in list_x]
            #
            # # abs(self.__generator("gaussian", self.i * 0.035)) + self.__generator("uniform") * 5 + i

            self.x.append(self.x[-1] + 1)
            self.y.append(random.uniform(self.y[-1] -10, self.y[-1] + 10) + random.gauss(0, self.y[-1] * 0.035))

            self.x.pop(0)
            self.y.pop(0)
            # line.set
            self.plot.clear()
            self.plot_graph()
            # required to update canvas and attached toolbar!
            self.canvas.draw()
            print("drawn")
            time.sleep(0.1)

    def create_thread(self):
        thread = threading.Thread(target=self.update_plot, daemon=True)
        thread.start()

    def pack_all(self):
        self.button_generate = tkinter.Button(master=self.root, text="Update", command=self.create_thread)
        self.button_quit.pack(side=tkinter.BOTTOM)
        self.button_generate.pack(side=tkinter.BOTTOM)
        self.toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

graph = DynamicGraph()
tkinter.mainloop()
