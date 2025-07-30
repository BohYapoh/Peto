import math
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import time
import PIL
import pygame
import arcade
import random
import sys
import os
from PIL import Image, ImageTk
from pygame.transform import rotate

print("Hello world")

v_0 = 0
y_0 = 500
g = 19.81
C = 0.0022
dt = 0.01

t = np.linspace(0, 30, 1801)
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

gosling_time = 0

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GG (arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.background = arcade.Sprite(resource_path("assets/Landscape.png"), scale = 0.78125)
        self.background.center_x = 600
        self.background.center_y = 400
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.background)
        self.car = Svin()
        self.score = 0
        self.coin = Gosling(0)
        self.num = 1
        self.coin_list = []
        self.coin_list.append(self.coin)
        self.sprite_list.append(self.car)
        self.sprite_list.append(self.coin)

    def on_key_press(self, key, modifiers):
        self.car.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.car.on_key_release(key)

    def on_draw(self):
        #print(type(self.background))
        self.sprite_list.draw()
        arcade.draw_text(f"Score : {self.score}", x = 20, y =760, font_size = 25, color = arcade.color.PURPLE)

    def on_update(self, delta_time):
        global C
        global g
        global gosling_time
        gosling_time += 1
        self.car.update()
        #self.coin.update()
        for item in self.coin_list:
            item.move_coin()
            if arcade.check_for_collision(self.car, item):
                if item.Dead == False:
                    self.score += 10
                    item.Dead = True
                    print(item.Dead)
                item.remove_from_sprite_lists()
        if (gosling_time) > 60:
            gosling_time = 0
            self.coin1 = Gosling(self.num)
            g += 1
            self.coin_list.append(self.coin1)
            self.sprite_list.append(self.coin1)




class Svin(arcade.Sprite):
    change_x = 0
    def __init__(self):
        self.right1 = False
        self.left1 = False
        super().__init__(resource_path("assets/Svin.png"), scale=1)
        self.original_texture = self.texture
        self.flipped_texture = self.texture.flip_left_right()
        self.center_x = 150
        self.center_y = 100
        self.Power = 14700
        self.E_kin = 0
        self.mass = 300
        self.velocity = 0
        self.dir = 0
        self.g = 9.81
        self.desired_dir = 0

    def on_key_press(self,key):
        if key == arcade.key.D:
            #self.change_x = 5
            self.right1 = True
            self.desired_dir = 1
        elif key == arcade.key.A:
            #self.change_x = -5
            self.desired_dir = -1
            self.left1 = True
        else:
            self.right1 = False
            self.left1 = False


    def on_key_release(self, key):
        if key == arcade.key.D:
            self.change_x = 0
            self.right1 = False
        if key == arcade.key.A:
            self.change_x = 0
            self.left1 = False

    def update(self):
        global C
        if self.desired_dir == 1 and self.velocity == 0:
            self.dir = 1
            self.texture = self.original_texture
        if self.desired_dir == -1 and self.velocity == 0:
            self.dir = -1
            self.texture = self.flipped_texture
        if (self.right1 == True or self.left1 == True) and self.dir==self.desired_dir:
            self.E_kin += self.Power * (1 / 60)
        if (self.right1 == True or self.left1 == True) and self.dir!=self.desired_dir:
            if abs(self.E_kin) > abs(self.Power * (1 / 60)):
                self.E_kin -= self.Power * (1/60)
            else:
                self.E_kin = 0
        self.A_loss = (C * abs(self.velocity ** 3) + 0.3 * self.mass * self.g * abs(self.velocity)) * (1 / 60)
        if abs(self.E_kin) > abs(self.A_loss):
           self.E_kin -= self.A_loss
        else:
            self.E_kin = 0
        self.velocity = self.dir * math.sqrt(2 * self.E_kin / self.mass)
        #self.velocity = math.sqrt(2*self.E_kin/self.mass)
        self.center_x += self.velocity/0.6
        #print(self.E_kin, " ", self.velocity)


def f(t, v):
    return -g-C*v*abs(v)

class Gosling(arcade.Sprite):

    def __init__ (self, n):
        super().__init__(resource_path("assets/Gosling.png"), scale=1)
        self.start_time = time.perf_counter()
        self.center_x = random.randint(0, 1200)
        self.center_y = 800
        self.index = 0
        self.i = 0
        self.num = n
        self.Dead = False



    def move_coin(self):
        if self.index < len(t)-1:
            while self.i < self.index:
                k_1 = f(t[self.i], v[self.i])
                k_2 = f(t[self.i] + dt / 2, v[self.i] + k_1 * dt / 2)
                k_3 = f(t[self.i] + dt / 2, v[self.i] + k_2 * dt / 2)
                k_4 = f(t[self.i] + dt, v[self.i] + k_3 * dt)
                v[self.i + 1] = v[self.i] + (dt / 6) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
                y[self.i + 1] = y[self.i] + dt * v[self.i]
                self.i += 1
                #print (i)
            if self.center_y > 41:
                 self.center_y = y[self.index] + 250
            now = time.perf_counter()
            delta = now - self.start_time
            self.index = int(60*delta)
            #print(delta," ", self.index)

    def update(self):
        self.move_coin()


print(t[500])
print(v[1])


pygame.mixer.init()
pygame.mixer.music.load(resource_path("assets/Nightcall.mp3"))
pygame.mixer.music.play(-1)

game = GG(1200, 800)

arcade.run()
print("Hello world")
