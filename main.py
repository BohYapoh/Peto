import math
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import time
import PIL
from PIL import Image, ImageTk
print("Hello world")

v_0 = 0
y_0 = 500
g = 9.81
C = 0.0022
dt = 0.01

t = np.linspace(0, 5, 501)
y = np.zeros((len(t)))
v = np.zeros((len(t)))
a = np.zeros((len(t)))
y[0]=500

def f(t, v):
    return -g-C*v*abs(v)

def move_circle( index ):
    if index < len(t):
        y_pos = -y[index] + 530
        simulation.coords(gosling_obj, 50, y_pos)
        t_int = int(dt*1000)
        now = time.perf_counter()
        delta = now - start_time
        print (delta)
        print (y[index])
        print (index)
        root.after(t_int, lambda : move_circle(index+1))


for i in range(len(t) - 1):
    k_1 = f(t[i], v[i])
    k_2 = f(t[i] + dt/2, v[i] + k_1 * dt/2)
    k_3 = f(t[i] + dt/2, v[i] + k_2 * dt/2)
    k_4 = f(t[i] + dt, v[i] + k_3 * dt)
    v [i+1] = v[i] + (dt/6) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
    print(v[i])
for i in range (len(t)-1):
    y[i+1] = y[i] + dt * v[i]
    print(y[i])
#plt.plot(t, abs(v))
#plt.show()
print(t[500])
print(v[1])

root = tk.Tk()
root.title("Каки падают на асфальт")
root.geometry("1024x800")
simulation = tk.Canvas(bg = "white",width = 1024, height = 800)
simulation.pack(anchor= tk.CENTER, expand=1)
r = 20

gosling_ball = Image.open("Gosling.png")
small_gosling_ball = gosling_ball.resize((80,80))
Tk_small_gosling_ball = ImageTk.PhotoImage(small_gosling_ball)
gosling_obj = simulation.create_image(100, 100, image = Tk_small_gosling_ball)

start_time = time.perf_counter()
move_circle(0)
print("Hello world")
root.mainloop()
