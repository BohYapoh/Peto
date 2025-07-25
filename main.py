import math
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import time
import PIL
import pygame
from PIL import Image, ImageTk
print("Hello world")

v_0 = 0
y_0 = 500
g = 9.81
C = 0.0022
dt = 0.01

t = np.linspace(0, 20, 2001)
y = np.zeros((len(t)))
v = np.zeros((len(t)))
a = np.zeros((len(t)))
y[0] = 500
y_pos = 0

i=0
m=0

k_1 = 0
k_2 = 0
k_3 = 0
k_4 = 0

class Svin:
    def __init__(self):
        self.transp = False
        self.x_pos = 150
        self.y_pos = 700
        self.edet_right = False
        self.edet_left = False
        self.img = Image.open("Svin.png")
        self.small_Svin = self.img.resize((300, 200))
        self.Tk_small_Svin = ImageTk.PhotoImage(self.small_Svin)
        self.svin_obj = simulation.create_image(self.x_pos, self.y_pos, image=self.Tk_small_Svin)

    def rotate(self, a):
        if a == 0 and self.edet_right == True:
            self.img = Image.open("Svin.png")
            self.small_Svin = self.img.resize((300, 200))
            self.Tk_small_Svin = ImageTk.PhotoImage(self.small_Svin)
            self.svin_obj = simulation.create_image(self.x_pos, self.y_pos, image=self.Tk_small_Svin)
        if a == 1 and self.edet_left == True:
            self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
            self.small_Svin = self.img.resize((300, 200))
            self.Tk_small_Svin = ImageTk.PhotoImage(self.small_Svin)
            self.svin_obj = simulation.create_image(self.x_pos, self.y_pos, image=self.Tk_small_Svin)

    def start_move_right(self, event):
        if self.edet_right == False:
            print("начинаем")
            self.edet_right = True
            self.move_right()
            self.rotate(0)

    def end_move_right(self, event):
        print("кончаем")
        self.edet_right = False

    def move_right(self):

        if self.edet_right == True:
            self.x_pos += 10
            simulation.coords(self.svin_obj, self.x_pos, self.y_pos)
            root.after(20, lambda : self.move_right())

    def start_move_left(self, event):
        if self.edet_left == False:
            self.orient = 1
            self.edet_left = True
            self.rotate(1)
            self.move_left()

    def end_move_left(self, event):
        self.edet_left = False

    def move_left(self):
        if self.edet_left == True:
            self.x_pos -= 10
            simulation.coords(self.svin_obj, self.x_pos, self.y_pos)
            root.after(20, lambda : self.move_left())


def f(t, v):
    return -g-C*v*abs(v)

def move_circle( index ):
    global y_pos
    global i
    global m
    if index < len(t)-1:
        while i < index:
            k_1 = f(t[i], v[i])
            k_2 = f(t[i] + dt / 2, v[i] + k_1 * dt / 2)
            k_3 = f(t[i] + dt / 2, v[i] + k_2 * dt / 2)
            k_4 = f(t[i] + dt, v[i] + k_3 * dt)
            v[i + 1] = v[i] + (dt / 6) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
            y[i + 1] = y[i] + dt * v[i]
            i += 1
            #print (i)
        y_pos = -y[index] + 550
        if y_pos < 760:
            simulation.coords(gosling_obj, 50, y_pos)
        t_int = int(dt*1000)
        now = time.perf_counter()
        delta = now - start_time
        if delta > 5 and m == 0:
            m = 1
            print (delta, " ", index)
        index = int(100*delta)

        root.after(t_int, lambda : move_circle(index+1))


def key_check(event):
    print(f"Нажата: {event.char}")

print(t[500])
print(v[1])

root = tk.Tk()
root.title("Каки падают на асфальт")
root.geometry("1200x800")
simulation = tk.Canvas(bg = "white",width = 1200, height = 800)
simulation.pack(anchor= tk.CENTER, expand=1)
r = 20


gosling_landscape = Image.open("Landscape.png")
small_landscape = gosling_landscape.resize((1200,800))
Tk_small_landscape = ImageTk.PhotoImage(small_landscape)
landscape_obj = simulation.create_image(600, 400, image = Tk_small_landscape)
gosling_ball = Image.open("Gosling.png")
small_gosling_ball = gosling_ball.resize((80,80))
Tk_small_gosling_ball = ImageTk.PhotoImage(small_gosling_ball)
gosling_obj = simulation.create_image(100, 100, image = Tk_small_gosling_ball)

start_time = time.perf_counter()
move_circle(0)
Car1 = Svin()
root.bind("<Key>", key_check)
root.bind("<KeyPress-D>", Car1.start_move_right)
root.bind("<KeyRelease-D>", Car1.end_move_right)
root.bind("<KeyPress-d>", Car1.start_move_right)
root.bind("<KeyRelease-d>", Car1.end_move_right)
root.bind("<KeyPress-A>", Car1.start_move_left)
root.bind("<KeyRelease-A>", Car1.end_move_left)
root.bind("<KeyPress-a>", Car1.start_move_left)
root.bind("<KeyRelease-a>", Car1.end_move_left)

pygame.mixer.init()
pygame.mixer.music.load("Nightcall.mp3")
pygame.mixer.music.play(-1)
root.focus_set()
root.mainloop()
print("Hello world")
