import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from tkinter import *
import threading
import numpy as np
import re
import collections

c=0
temp = 0
ozwei= 0.0
xs = collections.deque(np.zeros(300))
ys = collections.deque(np.zeros(300))
y2s = collections.deque(np.zeros(300))
#xs = []
#ys = []
#y2s = []
def handle_data(data):
    global c
    global last
    global updated
    global temp
    global ozwei
    cc=data
    i=0
    c=c+1
    varlo.set(c)
    x = cc.split(" ")
 
    for xx in x:
        i=i+1
        xxx = re.sub("[^\d\.]", "", xx)
        if i == 6:
            ozwei=float(xxx)
            xxx=xxx.rjust(4)
            varo.set(xxx)
                 
        if i == 3:
            temp=int(xxx)
            xxx=xxx.rjust(4)
            vart.set(xxx)
 
        root.update_idletasks()


def read_from_port(ser):
    global connected 
    while not connected:
        connected = True

        while True:
           reading = ser.readline().decode()
           handle_data(reading)

last =0
countdata=0;

def animate(i, xs, ys, y2s):

    global updated
    global ozwei
    global temp

    ax1.cla()
    ax2.cla()
    ys.popleft();
    ys.append(temp)
    y2s.popleft();
    y2s.append(ozwei)

    line1 = ax1.plot( ys, label = 'AbgasTemperatur', color = 'red')
    line2 = ax2.plot( y2s, label = 'Abgas O2', color = 'blue')

    ax1.scatter(len(ys)-1,ys[-1])
    ax2.scatter(len(y2s)-1,y2s[-1])
    ax1.set_ylim(0, 400)
    ax2.set_ylim(0, 50)

connected=False
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h-200))
root.attributes('-fullscreen', True)
varo = StringVar()
varo.set('    ')
vart = StringVar()
vart.set('    ')
varlo = StringVar()
varlo.set('    ')
 
ol = Label(root, textvariable=varlo)
tl = Label(root, text="Abgastemp")
ol.config(font=("Courier", 44))
tl.config(font=("Courier", 44))
ol.pack()
o = Label(root, textvariable=varo,bg="lightblue")
t = Label(root, textvariable=vart,bg="orangered")
o.config(font=("Courier", int(round(h/4))))
t.config(font=("Courier", int(round(h/4))))
o.pack()
t.pack()
 
o.place(relx=0.5, rely=0.5, anchor="nw")
ol.place(x=0, y=0)
t.place(relx=0.5, rely=0.5, anchor="sw")
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig, ax1 = plt.subplots(figsize = (6, 4))
ax2 = ax1.twinx()

line1 = ax1.plot(xs, ys, label = 'Abgas Temperatur', color = 'red')
line2 = ax2.plot(xs, y2s, label = 'Abgas O2', color = 'blue')

lines = line1 + line2
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc = 'upper right')

ax1.set_ylim(0, 400)
ax2.set_ylim(0, 50)

ax1.tick_params(axis = 'x', which = 'both', top = False)
ax1.tick_params(axis = 'y', which = 'both', right = False, colors = 'red')
ax2.tick_params(axis = 'y', which = 'both', right = True, labelright = True, left = False, labelleft = False, colors = 'blue')

plt.setp(ax1.xaxis.get_majorticklabels(), rotation = 45)

ax1.set_xlabel('Date')
ax1.set_ylabel('Abgas Temperatur')
ax2.set_ylabel('Abgas O2')

ax1.yaxis.label.set_color('red')
ax2.yaxis.label.set_color('blue')

ax2.spines['left'].set_color('red')
ax2.spines['right'].set_color('blue')

plt.tight_layout()


line2 = FigureCanvasTkAgg(fig, root)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
try:
    ser = serial.Serial("COM9", 38400)
except: 
    try:
        ser = serial.Serial("/dev/ttyUSB0", 38400)
    except:ser = serial.Serial("/dev/ttyACM0", 38400)

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, y2s), interval=1000)
plt.draw()
root.mainloop()
