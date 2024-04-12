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
        self.fig = Figure(figsize=(8, 4), dpi=100)
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
        self.thread = None
        tkinter.mainloop()

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
            self.x.append(self.x[-1] + 1)

            # the equation of our line is y = Ax^2 + Bx + C, but C and B are 0 so we only need y = ax^2.
            # we know that we want when X is 135, Y = 200
            # therefore:
            # 200 = A(pow(135,2))
            # 200/pow(135,2) = A
            # 200/pow(135,2) = 0.01097393689986282578875171467764
            # now that we have A, we can multiply it by any X value squared to get the accurate y position
            new_y = 0.01097393689986282578875171467764 * pow(self.x[-1] - 1880,
                                                             2)  # because we start at 1880, we subtract 1880 from x
            # add random noise to this new y position and then append to the list
            self.y.append(new_y + (random.gauss(0, new_y / (self.x[-1] - 1880) * 2)) + random.uniform(0, 5))
            # self.x.pop(0)
            # self.y.pop(0)
            # line.set
            self.plot.clear()
            self.plot_graph()
            # redraw graph
            self.canvas.draw()
            time.sleep(0.1)

    def create_thread(self):
        if self.thread == None:
            self.thread = threading.Thread(target=self.update_plot, daemon=True)
            self.thread.start()

    def pack_all(self):
        self.button_generate = tkinter.Button(master=self.root, text="Update", command=self.create_thread)
        self.button_quit.pack(side=tkinter.BOTTOM)
        self.button_generate.pack(side=tkinter.BOTTOM)
        self.toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


graph = DynamicGraph()
