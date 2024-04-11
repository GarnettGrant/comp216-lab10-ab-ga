import random
import tkinter
import group_9_data_generator
import threading
import time
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
root = tkinter.Tk()
root.wm_title("Water Levels Figure")
fig = Figure(figsize=(12, 4), dpi=100)
ax = fig.add_subplot()
sensor = group_9_data_generator.DataGenerator(0.0, 200.0, 200)
x, y = sensor.plot()

line = ax.plot(x, y, "b")
ax.fill_between(x, y)
ax.set_xlabel('Time, in years')
ax.set_ylabel('Rise in global sea levels, in millimeters')
ax.set_title('Global rise in sea levels since 1880')
#
# ax.xlim(1872 + num*6, 1880 + num*6.75 + 5*5)
# ax.ylim(y[0] - 1, y[-1])
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

done = False


def update_line():
    while not done:
        print(y)
        x.append(x[-1] + 0.5)
        y.append(y[-1] + (random.gauss(0, y[-1] * 0.035) + random.uniform(0.0, 5)))

        x.pop(0)
        y.pop(0)
        # line.set
        ax.clear()
        ax.plot(x, y, "b")
        ax.fill_between(x, y)
        # required to update canvas and attached toolbar!
        canvas.draw()
        print("drawn")
        time.sleep(0.1)


def create_thread():
    thread = threading.Thread(target=update_line, daemon=True)
    thread.start()


button_generate = tkinter.Button(master=root, text="Update", command=create_thread)
# slider_update = tkinter.Scale(root, from_=1, to=5, orient=tkinter.HORIZONTAL,
#                               command=update_frequency, label="Frequency [Hz]")

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
button_generate.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()
