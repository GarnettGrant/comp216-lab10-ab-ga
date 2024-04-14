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
        self.wm_title("Water Levels Figure")
        self.fig = Figure(figsize=(6, 5))
        self.plot = self.fig.add_subplot()
        self.sensor = group_9_data_generator.DataGenerator(0, 200, 200)
        self.x = []
        self.y = []

        self.plot_graph()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.display_textbox = tkinter.Text(master=self, height=7, width=20)
        self.button_generate = tkinter.Button(master=self, text="Update", command=self.create_thread)
        self.button_quit = tkinter.Button(master=self, text="Quit", command=self.destroy)
        self.done = False
        self.pack_all()
        self.thread = None

    def plot_graph(self):
        self.plot.plot(self.x, self.y, "b")
        self.plot.fill_between(self.x, self.y)
        self.plot.set_xlabel('Time, in years')
        self.plot.set_ylabel('Rise in global sea levels, in millimeters')
        self.plot.set_title('Global rise in sea levels since 1880')
        if not hasattr(self, "canvas"):
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.update()
        self.update_idletasks()

    def update_plot(self, new_x=0.0, new_y=0.0):
        while not self.done:
            x, y = self.sensor.get_next_pair(self.x)
            print(x, y)
            self.y.append(y)
            self.x.append(x)
            self.plot.clear()
            self.plot_graph()
            # redraw graph
            self.canvas.draw()
            return
            # time.sleep(0.1)
            # else:
            #     x, y = self.sensor.get_next_pair(self.x)
            #     print(x, y)
            #     self.y.append(new_y)
            #     self.x.append(new_x)
            #     self.plot.clear()
            #     self.plot_graph()
            #     # redraw graph
            #     self.canvas.draw()
            #     time.sleep(0.1)


    def update_text(self, id="null", sea_level_pressure="null", temperature="null", year="null", global_mean_sea_level="null", time_stamp="null"):
        self.display_textbox.delete('1.0', tkinter.END)
        self.display_textbox.insert(tkinter.INSERT, f"id: {id}\n"
                                    f"sea_level_pressure: {sea_level_pressure}\n"
                                    f"temperature: {temperature}\n"
                                    f"year: {year}\n"
                                    f"global_mean_sea_level: {global_mean_sea_level}\n"
                                    f"time_stamp: {time_stamp}\n")
        # self.display_textbox.insert(0, "WEEEEWOOOWEEEWOO")

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
